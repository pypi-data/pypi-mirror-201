import asyncio
import enum
import glob
import locale
import os
import traceback
from abc import ABC, abstractmethod
from pathlib import Path, PurePath
from collections.abc import Callable
import orjson
from navconfig import config
from navconfig.logging import logging
from asyncdb import AsyncDB
from asyncdb.drivers.abstract import BaseDriver
from navigator.conf import default_dsn
from flowtask.exceptions import FileNotFound
from flowtask.utils import SafeDict, fnExecutor, cPrint
from flowtask.utils.constants import (get_constant, get_func_value,
                                             is_constant, is_function)
from .functions import FuncSupport

class SkipErrors(enum.Enum):
    SKIP: str = 'skip'
    LOG: str = 'log_only'
    ENFORCE: str = None


class DtComponent(FuncSupport, ABC):
    """Abstract

    Overview:

            Helper for building components that consume REST APIs

        .. table:: Properties
       :widths: auto
    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  method      |   Yes    | Component for Data Integrator                                     |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  attributes  |   Yes    | Attribute: barcode                                                |
    +--------------+----------+-----------+-------------------------------------------------------+


    Return the list of arbitrary days

    """
    _memory: BaseDriver = None
    skipError: SkipErrors = SkipErrors.ENFORCE
    use_coro: bool = False
    TaskName: str = None
    encoding: str = 'UTF-8'

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        if loop:
            self._loop = loop
            asyncio.set_event_loop(self._loop)
        else:
            self._loop = asyncio.get_event_loop()
        # stats object:
        self.stat = stat
        # Future Logic: trigger logic:
        self.runIf: list = []
        self.triggers: list = []
        # vars
        self._TaskPile = None
        self._environment = None
        self.locale: str = None
        self._attrs: dict = {} # attributes
        self._variables = {} # variables
        self._vars = {} # other vars
        self._mask = {} # masks for function replacing
        self._params = {} # other parameters
        self._args: dict = {}
        # previous Component
        self._component = None
        # collection of results:
        self._result = None
        self.data = None
        # Object Name:
        self.__name__: str = self.__class__.__name__
        # logging object
        self._logger = logging.getLogger(__name__)
        # Debugging
        try:
            self._debug = bool(kwargs['debug'])
            del kwargs['debug']
        except KeyError:
            self._debug = False
        if self._debug:
            self._logger.setLevel(logging.DEBUG)
        # memcache connector
        try:
            self._memory = kwargs['memory']
            del kwargs['memory']
        except KeyError:
            pass
        # program
        try:
            self._program = kwargs['program']
            del kwargs['program']
        except KeyError:
            self._program = 'navigator'
        # getting the argument parser:
        try:
            self._argparser = kwargs['argparser']
            del kwargs['argparser']
        except KeyError:
            self._argparser = None
        # can pass a previous data as Argument:
        try:
            self._input_result = kwargs['input_result']
            del kwargs['input_result']
        except KeyError:
            self._input_result = None
        # getting the Task Pile (components pile)
        try:
            self._TaskPile = kwargs['TaskPile']
            del kwargs['TaskPile']
            setattr(self, 'TaskPile', self._TaskPile)
        except KeyError:
            pass
        # Config Environment
        try:
            self._environment = kwargs['ENV']
            del kwargs['ENV']
        except (KeyError, AttributeError):
            self._environment = config
        # Template Parser
        try:
            self._templateparser = kwargs['template']
            del kwargs['template']
        except KeyError:
            self._templateparser = None
        # for changing vars (in components with "vars" feature):
        try:
            self._vars = kwargs['_vars']
            del kwargs['_vars']
        except KeyError:
            pass
        # attributes (root-level of component arguments):
        try:
            self._attributes = kwargs['attributes']
            del kwargs['attributes']
        except KeyError:
            self._attributes = {}
        try:
            self._args = kwargs['_args']
            del kwargs['_args']
        except KeyError:
            self._args = {}
        # conditions:

        try:
            self.conditions: dict = kwargs['conditions']
            del kwargs['conditions']
        except KeyError:
            pass
        # params:
        try:
            self._params = kwargs['params']
            del kwargs['params']
        except KeyError:
            self._params = {}
        # parameters
        try:
            self._parameters = kwargs['parameters']
            del kwargs['parameters']
        except KeyError:
            self._parameters = []
        # arguments list
        try:
            self._arguments = kwargs['arguments']
            del kwargs['arguments']
        except KeyError:
            self._arguments = []
        # processing variables
        try:
            variables = kwargs['variables']
            del kwargs['variables']
            if isinstance(variables, str):
                try:
                    variables = orjson.loads(variables)
                except ValueError:
                    try:
                        variables = dict(x.split(':')
                                         for x in variables.split(','))
                    except (TypeError, ValueError, IndexError):
                        variables = {}
            if variables:
                for arg, val in variables.items():
                    self._variables[arg] = val
        except KeyError:
            pass
        # previous Job has variables, need to update from existing
        if job:
            self._component = job
            if isinstance(job, list):
                self._multi = True
                variables = {}
                for j in job:
                    variables = {**variables , **j.variables}
                try:
                    self._variables = {**self._variables, **variables}
                except Exception as err:
                    print(err)
            else:
                self._multi = False
                try:
                    self._variables = {**self._variables, **job.variables}
                except Exception as err:
                    print(err)
        # mask processing:
        try:
            masks = kwargs['_masks']
            del kwargs['_masks']
        except KeyError:
            masks = {}
        # filling Masks:
        if 'masks' in kwargs:
            self._mask = kwargs['masks']
            del kwargs['masks']
            object.__setattr__(self, 'masks', self._mask)
        for mask, replace in masks.items():
            self._mask[mask] = replace # override component's masks
        try:
            for mask, replace in self._mask.items():
                # first: making replacement of masks based on vars:
                try:
                    if mask in self._variables:
                        value = self._variables[mask]
                    else:
                        value = replace.format(**self._variables)
                except Exception as err:
                    value = replace
                value = fnExecutor(value, env=self._environment)
                self._mask[mask] = value
        except Exception as err:
            logging.debug(f'Mask Error: {err}')
        # existing parameters:
        try:
            self._params = {**kwargs, **self._params }
        except (TypeError, ValueError):
            pass
        for arg, val in self._params.items():
            try:
                if arg == 'no-worker':
                    continue
                elif arg == self.TaskName:
                    values = dict(x.split(':')
                                  for x in self._params[arg].split(','))
                    for key, value in values.items():
                        self._params[key] = value
                        object.__setattr__(self, key, value)
                else:
                    if arg not in ['program', 'TaskPile', 'TaskName']:
                        self._attrs[arg] = val
                        if arg in self._attributes:
                            val = self._attributes[arg]
                        try:
                            # logging.debug(f'SET Attribute: {arg}={val}, {type(arg)}, {type(val)}')
                            setattr(self, arg, val)
                        except Exception as err:
                            logging.warning(f'Wrong Attribute: {arg}={val}')
                            logging.exception(err)
            except (AttributeError, KeyError) as err:
                self._logger.error(err)
        # attributes: component-based parameters (only for that component):
        for key, val in self._attributes.items():
            if key in self._attributes:
                # i need to override attibute
                current_val = self._attributes[key]
                if isinstance(current_val, dict):
                    val = {**current_val, **val}
                elif isinstance(current_val, list):
                    val = current_val.append(val)
                try:
                    object.__setattr__(self, key, val)
                    self._attrs[key] = val
                except (ValueError, AttributeError) as err:
                    self._logger.error(err)
        # Localization
        if self.locale is None:
            newloc = (locale.getlocale())[0]
            self.locale = f'{newloc}.{self.encoding}'
        else:
            self.locale = f'{self.locale}.{self.encoding}'
        try:
            #avoid errors on unsupported locales
            locale.setlocale(locale.LC_TIME, self.locale)
        except (RuntimeError, NameError, locale.Error) as err:
            print(err)
            newloc = (locale.getlocale())[0]
            self.locale = f'{newloc}.UTF-8'
            locale.setlocale(locale.LC_TIME, self.locale)
        # processing the variables:
        if hasattr(self, 'vars'):
            for key, val in self._vars.items():
                if key in self.vars:
                    self.vars[key] = val
        # SkipError:
        if self.skipError == 'skip':
            self.skipError = SkipErrors.SKIP
        elif self.skipError == 'log':
            self.skipError = SkipErrors.LOG
        else:
            self.skipError = SkipErrors.ENFORCE

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"<{type(self).__name__}>"

    @abstractmethod
    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """

    @abstractmethod
    async def run(self):
        """
        run.

        Run operations declared inside Component.
        """

    @abstractmethod
    async def close(self):
        """
        close.

        Close (if needed) component requirements.
        """

    def ComponentName(self):
        return self.__name__

    def output(self):
        return self._result

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    def user_params(self):
        return self._params

    @property
    def input(self):
        if isinstance(self._component, list):
            # TODO: get an array the results from different components
            result = []
            for component in self._component:
                if component:
                    result.append(component.output())
            if len(result) == 1:
                return result[0]
            else:
                return result
        elif self._component:
            return self._component.output()
        else:
            return self._input_result

    @property
    def previous(self):
        if self._component is not None:
            return self._component
        elif self._input_result is not None:
            return self ## result data is already on component
        else:
            return None

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    def setVar(self, name, value):
        logging.debug(f'Setting VAR ON: {name} = {value}')
        self._variables[name] = value

    def setTaskVar(self, name, value):
        name = f"{self.TaskName}_{name}"
        self._variables[name] = value

    def set_attributes(self, name: str = 'pattern'):
        if hasattr(self, name):
            obj = getattr(self, name)
            for field, val in obj.items():
                if field in self._params:
                    # already calculated:
                    self._attrs[field] = self._params[field]
                    setattr(self, field, self._params[field])
                elif field in self._attributes:
                    self._attrs[field] = self._attributes[field]
                    setattr(self, field, self._attributes[field])
                elif field in self._parameters:
                    self._attrs[field] = self._parameters[field]
                    setattr(self, field, self._parameters[field])
                elif field in self._variables:
                    self._attrs[field] = self._variables[field]
                    setattr(self, field, self._variables[field])
                else:
                    value = self.getFunc(val)
                    self._attrs[field] = value
                    setattr(self, field, value)
            del self._attrs['pattern']
        else:
            return False

    def process_pattern(self, name: str = 'file', parent = None):
        if not parent:
            try:
                obj = getattr(self, name)
            except AttributeError:
                return False
        else:
            try:
                obj = parent[name]
            except AttributeError:
                return False
        if obj:
            # pattern has the form {file, value}:
            if not isinstance(obj, dict):
                return obj
            else:
            # first, I need the pattern object:
                try:
                    pattern = obj['pattern']
                    # del obj['pattern']
                except Exception:
                    return obj
            # processing the rest of variables:
            if self._vars and f'{name}.pattern' in self._vars:
                pattern = self._vars[f'{name}.pattern']
            elif self._variables and 'pattern' in self._variables:
                pattern = self._variables['pattern']
            elif 'value' in self._variables:
                pattern = pattern.format_map(SafeDict(value=self._variables['value']))
            if self._vars and f'{name}.value' in self._vars:
                result = self._vars[f'{name}.value']
                return pattern.format_map(SafeDict(value=result))
            elif 'value' in obj:
                # simple replacement:
                result = self.getFunc(obj['value'])
                # print('RESULT IS ', result)
                return pattern.format_map(SafeDict(value=result))
            elif 'values' in obj:
                variables = {}
                result = obj['values']
                for key, val in result.items():
                    variables[key] = self.getFunc(val)
                return pattern.format_map(SafeDict(**variables))
            else:
                # multi-value replacement
                variables = {}
                if self._variables:
                    pattern = pattern.format_map(SafeDict(**self._variables))
                for key, val in obj.items():
                    if key in self._variables:
                        variables[key] = self._variables[key]
                    else:
                        variables[key] = self.getFunc(val)
                return pattern.format_map(SafeDict(**variables))
        else:
            return False

    def process_mask(self, name):
        if hasattr(self, name):
            obj = getattr(self, name)
            for key, value in obj.items():
                if key in self._vars:
                    obj[key] = self._vars[key]
                elif self._vars and f'{name}.{key}' in self._vars:
                    obj[key] = self._vars[f'{name}.{key}']
                elif key in self._variables:
                    obj[key] = self._variables[key]
                else:
                    # processing mask
                    for mask, replace in self._mask.items():
                        obj[key] = value.replace(mask, str(replace))
            return obj
        else:
            return {}

    def mask_replacement(self, obj):
        for mask, replace in self._mask.items():
            if mask in self._variables:
                value = self._variables[mask]
            else:
                value = str(obj).replace(mask, str(replace))
            if isinstance(obj, PurePath):
                obj = Path(value).resolve()
            else:
                obj = value
        return obj

    def set_conditions(self, name: str = 'conditions'):
        if hasattr(self, name):
            obj = getattr(self, name)
            for condition, val in obj.items():
                if hasattr(self, condition):
                    obj[condition] = getattr(self, condition)
                elif is_constant(val):
                    obj[condition] = get_constant(val)
                elif is_function(val):
                    obj[condition] = get_func_value(val)
                if condition in self._variables:
                    obj[condition] = self._variables[condition]
                elif condition in self._mask:
                    obj[condition] = self._mask[condition]
                else:
                    if condition in self.conditions:
                        obj[condition] = val
            if 'pattern' in obj:
                pattern = obj['pattern']
                del obj['pattern']
                # getting conditions as patterns
                for field in pattern:
                    if field in obj:
                        # already settled
                        continue
                    if field in self._params:
                        obj[field] = self._params[field]
                    else:
                        result = None
                        val = pattern[field]
                        if is_constant(val):
                            result = get_constant(val)
                        else:
                            result = self.getFunc(val)
                        obj[field] = result

    def get_filename(self):
        """
        get_filename.

        Detect if File exists.
        """
        if not self.filename: # pylint: disable=E0203
            if hasattr(self, "file") and self.file:
                file = self.get_filepattern()
                filelist = glob.glob(os.path.join(self.directory, file))
                if filelist:
                    self.filename = filelist[0]
                    self._variables['__FILEPATH__'] = self.filename
                    self._variables['__FILENAME__'] = os.path.basename(
                        self.filename)
                else:
                    raise FileNotFound("File is empty or doesn't exists")
            elif self.previous:
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = filenames[0]
                        self._variables['__FILEPATH__'] = self.filename
                        self._variables['__FILENAME__'] = os.path.basename(
                            self.filename)
                    except IndexError as e:
                        raise FileNotFound(
                            f"({__name__}): File is empty or doesn't exists"
                        ) from e
            else:
                raise FileNotFound(
                    f"({__name__}): File is empty or doesn't exists"
                )
        else:
            return self.filename

    def get_env_value(self, key, default: str = None):
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            return key

    def save_traceback(self):
        try:
            self.stat.stacktrace(
                traceback.format_exc()
            )
        finally:
            pass

    def add_metric(self, name, value):
        try:
            self.stat.add_metric(name, value)
        except AttributeError:
            pass

    def debug(self, message):
        self._logger.debug(message)
        if self._debug is True:
            cPrint(message, level='DEBUG')

    def warning(self, message):
        self._logger.warning(message)
        if self._debug is True:
            cPrint(message, level='WARN')

    def exception(self, message):
        self._logger.exception(message, stack_info=True)
        if self._debug is True:
            cPrint(message, level='CRITICAL')

    def get_connection(self, event_loop: asyncio.AbstractEventLoop = None, driver: str = 'pg', params: dict = None, **kwargs):
        # TODO: datasources and credentials
        if not kwargs:
            kwargs = {
                "server_settings": {
                    'client_min_messages': 'notice',
                    'max_parallel_workers': '24',
                    'jit': 'off',
                    'statement_timeout': '3600000'
                }
            }
        if not event_loop:
            event_loop = self._loop
        return AsyncDB(driver, dsn=default_dsn, loop=event_loop, timeout=360000, params=params, **kwargs)
