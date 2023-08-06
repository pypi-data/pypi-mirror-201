import sys
import importlib
import logging
from navconfig.conf import TASK_PATH
from flowtask.exceptions import NotSupported, ComponentError
from .abstract import SkipErrors, DtComponent
from .user import UserComponent
from .group import GroupComponent


__all__ = ('SkipErrors', 'DtComponent', 'UserComponent', 'GroupComponent' )

_COMPONENTS = {}


def loadComponent(component, program: str = None):
    try:
        # try to using importlib
        classpath = f"flowtask.components.{component}"
        module = importlib.import_module(classpath, package='components')
        obj = getattr(module, component)
        return obj
    except ImportError:
        try:
            # another, check if task is an User-Defined Component
            sys.path.insert(0, str(TASK_PATH))
            classpath = f"{program}.functions.{component}"
            module = importlib.import_module(classpath, package='functions')
            obj = getattr(module, component)
            return obj
        except ImportError as e:
            raise NotSupported(
                f"Error: No Component {component!r} was Found: {e}"
            ) from e


def getComponent(component, program: str = None):
    try:
        if component in _COMPONENTS:
            return _COMPONENTS[component]
        else:
            cls = loadComponent(component, program=program)
            _COMPONENTS[component] = cls
            return cls
    except KeyError as err:
        logging.exception(
            f'Error loading component {component}: {err}',
            stack_info=True
        )
        raise ComponentError(
            f'Error loading component {component}: {err}'
        ) from err
