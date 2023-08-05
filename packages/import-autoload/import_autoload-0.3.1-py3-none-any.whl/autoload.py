####
##
#   autoloader
#

__version__ = "0.3.1"

import os, sys, importlib, importlib.util
from fnmatch import fnmatch

# почему не __main__ != "__main__" ?
if not hasattr(sys.modules["__main__"], "__file__"):
    raise RuntimeWarning("`autoload` not works by direct call or interactive mode")

modules = sys.modules
ROOT = os.path.dirname(sys.modules["__main__"].__file__)
PATTERN = "*.py"


def autoload(module_name=None, pattern=None):
    _all_ = set()

    if "__name__" in sys._getframe(1).f_locals:
        #   вызов из модуля
        _current_ = sys._getframe(1).f_locals["__name__"]
    else:
        _current_ = ROOT
        _current_ = ""

    # print('вызов из модуля >>>>> ', _current_)

    # pattern = pattern or PATTERN
    # module_name = module_name or '.'

    #   нельзя просто так узнать количество аргументов функции
    if module_name is None and pattern is None:
        # print(111)
        pattern = PATTERN
        # module_name = '.'
        # module_name = _current_

    elif module_name is not None and pattern is None:
        # print(222)
        pattern = PATTERN
        # module_name = '.'
        # module_name = _current_

    elif module_name is None and pattern is not None:
        # print(333)
        # module_name = '.'
        # module_name = _current_
        pass

    elif module_name is not None and pattern is not None:
        # print(444)
        # module_name = _current_ + "." + module_name
        pass

    else:
        # print(555)
        pass

    # print('_current_, module_name, pattern :', _current_, module_name, pattern)

    if _current_:
        if module_name:
            module_name = _current_ + "." + module_name
            spec = importlib.util.find_spec(module_name)
        else:
            spec = importlib.util.find_spec(_current_)
    elif module_name:
        spec = importlib.util.find_spec(module_name)
    else:
        spec = None

    # print(spec)

    if spec:
        if "submodule_search_locations" in dir(spec):
            if spec.submodule_search_locations is not None:
                path = spec.submodule_search_locations[0]
            else:
                path = spec.origin
                # _mod_ = importlib.util.module_for_loader(path)
                # надеемся, что модуль загружается
                _mod_ = importlib.util.module_from_spec(spec)

                #######
                return tuple(_mod_.__name__)

        else:
            # var_dump(spec)
            pass
    else:
        path = ROOT

    if ".py" != pattern[-3:].lower():
        pattern = pattern + ".py"

    # print('path', path, pattern)

    # (root, dirs, files) = list(os.walk(os.path.dirname(_file_)))[0]
    (root, dirs, files) = list(os.walk(path))[0]

    for fn in files:
        if not fn == "__init__.py" and fnmatch(fn, PATTERN) and fnmatch(fn, pattern):
            _subname_ = os.path.splitext(fn)[0]

            # print("file:>>>", fn)
            # print('from `', module_name, '` import', _subname_)

            # importlib.import_module(
            #    _name_ + "." + _subname_ if _name_ != "__main__" else _subname_
            # )

            if module_name:
                _mod_ = importlib.import_module(module_name + "." + _subname_)
                # _mod_ = importlib.import_module(_current_, _subname_)
                # _mod_ = importlib.import_module(module_name, _subname_)
            else:
                _mod_ = importlib.import_module(_subname_)

            # print(_mod_)

            # importlib.__import__(module_name, globals(), locals(), [_subname_], 0)
            """different scopes (module's visibility)"""

            _all_.add(_subname_)

    return tuple(_all_)


__all__ = ("autoload", "modules", "PATTERN", "ROOT")
