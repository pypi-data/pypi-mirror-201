import asyncio
import logging
import importlib
from collections.abc import Callable
from flowtask.exceptions import ComponentError
from settings.settings import TASK_PATH
from .abstract import DtComponent

def getFunction(program, function):
    """getFunction."""
    try:
        fn_path = TASK_PATH.joinpath(program, 'functions', f'{function}.py')
        spec = importlib.util.spec_from_file_location(function, fn_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        obj = getattr(module, function)
        return obj
    except ImportError as e:
        logging.error(
            f"UserFunc: No Function {function} was Found"
        )
        raise ComponentError(
            f"UserFunc: No Function {function} was Found on {TASK_PATH}"
        ) from e


class UserFunc(DtComponent):
    """
    UserFunc.

       Overview

       Run a arbitrary user function and return result

     .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  function    |   Yes    | Name function                                                     |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  params      |   Yes    | Allows you to set parameters                                      |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  foo         |   Yes    | Variable name                                                     |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  api_keys    |   Yes    | Api password to query                                             |
    +--------------+----------+-----------+-------------------------------------------------------+

    Return the list of arbitrary days




    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self._fn = None
        self.data = None
        self.params = None
        self.function: Callable = None
        super(UserFunc, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        """Obtain Previous data."""
        if self.previous:
            self.data = self.input
        try:
            self._fn = getFunction(self._program, self.function)
        except ComponentError as err:
            raise ComponentError(
                f"UserFunc: Error getting Function from {self.function}"
            ) from err

    async def close(self):
        """Close Method."""

    async def run(self):
        """Run Method."""
        self._result = None
        params = {
            "data": self.data,
            "variables": self._variables
        }
        if self.params:
            params = {**params, **self.params}
        try:
            if asyncio.iscoroutinefunction(self._fn):
                result = await self._fn(
                    self,
                    loop=self._loop,
                    env=self._environment,
                    **params
                )
            else:
                result = self._fn(
                    self,
                    loop=self._loop,
                    env=self._environment,
                    **params
                )
            self._result = result
            self.add_metric('UDF', f"{self._fn!r}")
            return self._result
        except ComponentError as err:
            raise ComponentError(
                f"UserFunc: Error calling {self._fn}: {err}"
            ) from err
