import os
import time
import asyncio
import uuid
import random
import locale
import traceback
from collections.abc import Callable, Awaitable
from abc import ABC, abstractmethod
import jsonschema
# asyncdb
from asyncdb import AsyncDB
from asyncdb.drivers.abstract import BaseDriver
from asyncdb.meta import Record
# and navconfig
from navconfig import config, DEBUG
from navconfig.conf import (
    asyncpg_url,
    TASK_PATH,
    SYSTEM_LOCALE,
    MEMCACHE_HOST,
    MEMCACHE_PORT
)
from navconfig.logging import logging
# DI
from flowtask.utils.stats import TaskMonitor
from flowtask.models import (
    TaskState,
    setTaskState
)
from flowtask.events import (
    TaskEvent,
    logEvent,
    notifyOnSuccess,
    notifyEvent,
    notifyFailure,
    notifyWarning,
    saveExecution,
    startedTask
)
from flowtask.exceptions import (
    TaskError,
    TaskParseError,
    TaskDefinition,
    TaskNotFound
)
from flowtask.parsers import (
    JSONParser,
    TOMLParser,
    YAMLParser
)
from .template import getTemplateHandler

class AbstractTask(ABC):
    """
    AbstractTask.

        Base class for all Dataintegration tasks.
    """
    _logger: logging.Logger = None
    # memory object
    _memory: BaseDriver = None
    # pre-init and post-end functions
    pre_init: Awaitable[asyncio.Task] = None
    post_end: Awaitable[asyncio.Task] = None

    def __init__(
        self,
        task_id: str = None,
        task: str = None,
        program: str = None,
        loop: asyncio.AbstractEventLoop = None,
        parser: Callable = None,
        **kwargs
    ):
        self._state = TaskState.PENDING
        self.stat = None
        self.enable_stat: bool = True
        self._task = task
        self._taskname = f"{self._task!s}"
        self._taskdef = None
        self._env = config
        self._attrs = {}
        # program definition
        self._program = program
        if not self._program:
            self._program = 'navigator'
        self._schema = program
        self._kwargs = {}
        self._args = {}
        self._conditions = {}
        self._argparser = None
        self._options = None
        self._parameters: list = []
        self._arguments: list = []
        # re-use task Stat object from parent (subtasks)
        try:
            self.stat = kwargs['stat']
            del kwargs['stat']
        except KeyError:
            pass
        if parser:
            self._argparser = parser
            self._options = parser.options
        self._taskdef: Record = None
        # define if results are returned or not (when run on scheduler)
        try:
            self._ignore_results: bool = bool(kwargs['ignore_results'])
            del kwargs['ignore_results']
        except KeyError:
            self._ignore_results: bool = False
            if parser:
                if 'ignore-results' in parser.attributes:
                    self._ignore_results: bool = bool(parser.attributes['ignore-results'])
        if loop:
            self._loop = loop
        else:
            self._loop = asyncio.new_event_loop()
        # Task ID:
        if not task_id:
            self.task_id = uuid.uuid1(node=random.getrandbits(48) | 0x010000000000)
        else:
            self.task_id = task_id
        # defining Locale
        try:
            locale.setlocale(locale.LC_ALL, SYSTEM_LOCALE)
        except locale.Error as e:
            logging.exception(e, exc_info=True)
        # DEBUG
        try:
            self._debug = kwargs['debug']
            del kwargs['debug']
        except KeyError:
            self._debug = DEBUG
        # configure logging
        self._logger = logging.getLogger('DataIntegration')
        if self._debug:
            self._logger.setLevel(logging.DEBUG)
        logging.info(f'::: TASK DEBUG IS {self._debug} :::')
        if 'memory' in kwargs:
            self._memory = kwargs['memory']
            del kwargs['memory']
        # initialize the event system
        self._events = TaskEvent()
        self._events.addEvent(
            onTaskInit=[logEvent],
            onTaskStart=[logEvent, setTaskState, startedTask],
            onTaskRunning=[logEvent, setTaskState],
            onTaskDone=[logEvent, setTaskState, saveExecution, notifyOnSuccess],
            onTaskFailure=[logEvent, setTaskState, saveExecution, notifyFailure ],
            onTaskError=[logEvent, setTaskState, saveExecution, notifyEvent],
            onDataNotFound=[logEvent, setTaskState, saveExecution, notifyWarning],
            onTaskFileError=[logEvent, setTaskState, saveExecution, notifyWarning ],
            onFileNotFound=[logEvent, setTaskState, saveExecution, notifyWarning ]
        )
        # for file-based tasks
        self.taskpath = TASK_PATH.joinpath(self._program, 'tasks')
        # we have Task Path, calculate the environment and ini per-program
        self.program_init()
        # template system
        self._template = getTemplateHandler()
        # params
        self._params = {}
        if 'params' in kwargs:
            self._params = {**kwargs['params']}
            del kwargs['params']
        # also, work with arguments
        # command-line arguments
        self._arguments = []
        if parser:
            self._arguments = self._options.arguments
        try:
            args = kwargs['arguments']
            del kwargs['arguments']
            if isinstance(args, list):
                self._arguments = self._arguments + args
        except KeyError:
            pass
        if parser:
            try:
                self._args = self._options.args
            except (KeyError, ValueError, TypeError):
                pass
        elif 'args' in kwargs:
            self._args = kwargs['args']
        # processed parameters
        try:
            self._parameters = self._options.parameters
        except AttributeError:
            pass
        if kwargs:
            # remain args go to kwargs:
            self._kwargs = {**kwargs}

    # Context Methods:
    async def __aenter__(self) -> "AbstractTask":
        """ Magic Context Methods """
        if callable(self.pre_init):
            # this is a function called before start.
            await self.pre_init() # pylint: disable=E1102
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # clean up anything you need to clean up
        try:
            await self.close()
        finally:
            # this is a function called when Task Ends.
            if callable(self.post_end):
                await self.post_end() # pylint: disable=E1102

    def program_init(self):
        """
        Program Init.

          Initialization of Task based on Program logic, load INI, etc.
        """
        # getting per-program ini
        try:
            program_ini = self.taskpath.joinpath(self._program)
            l = list(program_ini.glob('*.ini'))
            if l:
                self._env.addFiles(l)
        except Exception as err:
            logging.debug(
                f'Task: {self._taskname} Error on Program init: {err!s}'
            )

    def set_timezone(self, timezone:str = 'UTC') -> None:
        os.environ['TZ'] = timezone
        time.tzset()

    async def setup_memcached(self):
        # create a Memcache connection
        params = {
            "host": MEMCACHE_HOST,
            "port": MEMCACHE_PORT
        }
        try:
            self._memory = AsyncDB('memcache', params=params)
            await self._memory.connection()
            connected = self._memory.is_connected()
            logging.debug(f'Connection Status to memcached: {connected}')
        except Exception as err:
            self._memory = None
            logging.exception(err)

    async def start(self) -> bool:
        self._state = TaskState.STARTED
        self._events.onTaskInit(
            message=f":: Starting Task {self._taskname} for program: {self._program}"
        )
        if not self.stat:
            if self.enable_stat is True:
                # create the stat component:
                try:
                    self.stat = TaskMonitor(
                        name=self._taskname,
                        program=self._program,
                        task_id=self.task_id
                    )
                    await self.stat.start()
                except Exception as err:
                    raise TaskError(
                        f"Task: Error on TaskMonitor: {err}"
                    ) from err
        if not self._memory:
            await self.setup_memcached()
        try:
            # getting Task information
            await self.get_task()
        except Exception as err:
            logging.exception(err)
            self._state = TaskState.FAILED
            self._events.onTaskFailure(
                message=f'Task Error: {self._taskname}: {err!r}',
                task=self
            )
        # check for different types of Tasks
        if self._taskdef:
            self._events.onTaskStart(
                message=f'Database-based Task {self._taskname!s}',
                task=self
            )
        else:
            self._events.onTaskStart(
                message=f':: File-based Task {self._taskname!s}',
                task=self
            )

    @abstractmethod
    async def run(self) -> bool:
        pass

    async def close(self):
        self.set_timezone('UTC') # forcing UTC at Task End.
        # TODO: closing Memcached-related connections
        try:
            await self._memory.close()
        except Exception as err:
            logging.exception(err)

    @property
    def taskname(self):
        return self._taskname

    def getState(self):
        return self._state

    def getProgram(self):
        return self._program

    def schema(self):
        return self._schema

    @property
    def stats(self) -> TaskMonitor:
        """stats.
        Return a TaskMonitor object with all collected stats.
        Returns:
            TaskMonitor: stat object.
        """
        return self.stat

    def setStat(self, stat):
        self.stat = stat

    async def get_taskrow(self, table: str, conn: BaseDriver) -> Record:
        definition = None
        t = """
         SELECT task_id, url, url_response, task_function, task_path,
         task_definition, attributes, params, is_coroutine, executor,
         program_slug FROM {table} WHERE enabled = true AND task='{task}';
        """
        task = t.format(table=table, task=self._taskname)
        logging.debug(f':: Task SQL: {task}')
        try:
            result, error = await conn.queryrow(task)
            if error:
                return None
            if result:
                definition = Record.from_dict(dict(result))
                return definition
        except Exception as err:
            print(err)
            logging.exception(err, stack_info=True)

    async def get_task(self):
        try:
            # db = postgres(dsn=asyncpg_url)
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)
            db = AsyncDB('pg', dsn=asyncpg_url, loop=loop)
            async with await db.connection() as conn:
                # first, check if a Tasks table exists on tenant:
                sql = f"""SELECT EXISTS (
                       SELECT FROM pg_catalog.pg_class c
                       JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                       WHERE  n.nspname = '{self._program}'
                       AND    c.relname = 'tasks'
                       AND    c.relkind = 'r');"""
                try:
                    row, error = await conn.queryrow(sql)
                    if error:
                        logging.error(f'Task Error: {error}')
                    if row and row['exists']:
                        # its a database-defined task
                        table = f"{self._program}.tasks"
                        self._schema = self._program
                        taskdef = await self.get_taskrow(table, conn)
                        if not taskdef:
                            # fallback to troc.tasks:
                            table = "troc.tasks"
                            self._schema = 'troc'
                        else:
                            self._taskdef = taskdef
                            return True
                    else:
                        # fallback to troc.tasks:
                        table = "troc.tasks"
                        self._schema = 'troc'
                    # getting task definition
                    taskdef = await self.get_taskrow(table, conn)
                    if taskdef is not None:
                        self._taskdef = taskdef
                        return True
                    else:
                        self._schema = None
                        logging.info(
                            f'Task \'{self._taskname}\' not found in database.'
                        )
                        return False
                except Exception as err:
                    print(err)
                    return False
        except Exception as err:
            print(err)
            dump = traceback.format_exc()
            self._state = TaskState.EXCEPTION
            self._events.onTaskFailure(
                message=f'Task cannot connect to Postgres Database, error {err!s}',
                cls=err,
                trace=dump,
                task=self
            )
            return False

    def checkSyntax(self, task):
        """
        checkSyntax.

        Check syntax of JSON task (if is json-based)
        """
        schema = {
           "$schema": "http://json-schema.org/draft-07/schema#",
           "type": "object",
           "properties": {
              "name": {"type": "string"},
              "description": {"type": "string"},
              "timezone": {"type": "string"},
              "comments": {"type": "string"},
              "steps": {
                  "type": "array",
                  "items": {
                    "anyOf": [
                    	{"type": "object"}
                    ]
                  }
              }
            },
           "required": [
             "name", "steps"
           ]
        }
        try:
            jsonschema.validate(instance=task, schema=schema)
            return True
        except jsonschema.ValidationError as err:
            raise TaskParseError(
                f'Task: Error parsing {self._taskname}: {err!s}'
            ) from err
        except Exception as err:
            raise TaskParseError(
                f'Task: Unknown parsing Error on {self._taskname}: {err!s}'
            ) from err


    async def open_task(
            self,
            taskname: str,
            filepath: str = None
        ):
        """
        openTask.

        Open a Task from file, support json, yaml and toml formats.
        """
        formats = ('json', 'yaml', 'toml', )
        for f in formats:
            filename = filepath.joinpath(f'{taskname}.{f}')
            if filename.exists():
                # is a JSON File
                try:
                    if f == 'json':
                        parse = JSONParser(str(filename))
                    elif f == 'yaml':
                        parse = YAMLParser(str(filename))
                    elif f == 'toml':
                        parse = TOMLParser(str(filename))
                    return await parse.run()
                except TaskParseError as err:
                    raise TaskParseError(
                        f"Task Parse Error: {err}"
                    ) from err
                except Exception as err:
                    raise TaskDefinition(
                        f'DI: Error Parsing {f} Task in {taskname}: {err}'
                    ) from err
            else:
                continue
        raise TaskNotFound(
            f'DI: Task {taskname} Not Found'
        )
