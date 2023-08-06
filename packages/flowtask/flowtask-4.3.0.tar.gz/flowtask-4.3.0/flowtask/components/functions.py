import builtins
from abc import ABC
from navconfig.logging import logging
from flowtask.exceptions import ComponentError
from flowtask.types import SafeDict

## functions
from flowtask.utils.functions import * #pylint: disable=W0614,W0401
from querysource.utils.functions import * #pylint: disable=W0401,C0411


class FuncSupport(ABC):
    """
    Interface for adding Add Support for Function Replacement.
    """
    def getFunc(self, val):
        result = None
        try:
            if isinstance(val, list):
                fname = val[0]
                args = {}
                try:
                    args = val[1]
                except IndexError:
                    args = {}
                try:
                    fn = getattr(builtins, fname)
                except (TypeError, AttributeError):
                    fn = globals()[fname]
                if args:
                    result = fn(**args)
                else:
                    result = fn()
            elif val in self._variables:
                result = self._variables[val]
            elif val in self._mask:
                result = self._mask[val]
            else:
                result = val
        except Exception as err:
            raise ComponentError(
                f"{__name__}: Error parsing Pattern Function: {err}"
            ) from err
        finally:
            return result

    def get_filepattern(self):
        fname = self.file['pattern']
        result = None
        try:
            try:
                val = self.file['value']
            except KeyError:
                val = fname
            if isinstance(val, str):
                if val in self._variables:
                    # get from internal variables
                    result = self._variables[val]
            elif isinstance(val, list):
                func = val[0]
                try:
                    kwargs = val[1]
                except IndexError:
                    kwargs = None
                try:
                    f = getattr(builtins, func)
                    if kwargs:
                        result = f(**kwargs)
                    else:
                        result = f()
                except (TypeError, AttributeError):
                    try:
                        if kwargs:
                            result = globals()[func](**kwargs)
                        else:
                            result = globals()[func]()
                    except (TypeError, ValueError) as e:
                        logging.error(e)
            else:
                result = val
        except (NameError, KeyError) as err:
            print(str(err))
        return fname.format_map(SafeDict(value=result))
