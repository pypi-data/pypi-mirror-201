import re
import traceback
import warnings

from importlib import import_module, resources

from importlib.metadata import version
__version__ = version(__name__)
__version_info__ = tuple(map(int, __version__.split('.')))


def _get_stacktrace(e):
    return ''.join(traceback.format_exception(None, e, e.__traceback__))


def _check(name, group):
    if group.endswith('*'):
        prefix = group.split('*')[0]
        return name.startswith(prefix)
    else:
        return name == group


def get_modules():
    modules = []
    for item in resources.files(__package__).iterdir():
        if item.stem == '__pycache__':
            continue

        module_name = f'{__package__}.{item.stem}'
        try:
            module = import_module(module_name)
        except Exception as e:  # pragma: no cover
            warnings.warn(f'Couldn\'t import {module_name!r}\n' + _get_stacktrace(e))
            continue

        modules.append(module)

    return sorted(modules, key=lambda m: m.__name__)


def get_functions_in_group(group):
    functions = []
    for module in get_modules():
        for func_name in dir(module):
            f = getattr(module, func_name)
            groups = getattr(f, '__katalytic_marks__', [])
            groups = [g for g in groups if _check(g, group)]
            if groups:
                functions.append((func_name, f, groups))

    return sorted(functions)


def mark(name):
    if not isinstance(name, str):
        raise TypeError(f'Only strings are allowed. Got {name!r}')

    if '\n' in name or '\t' in name or re.search(r'^\s*$', name):
        raise ValueError(f'Choose a meaningful name. Got {name!r}')

    def decorator(func):
        func.__katalytic_marks__ = getattr(func, '__katalytic_marks__', ())
        # prepend to maintain the intuitive order (top to bottom)
        func.__katalytic_marks__ = (name, *func.__katalytic_marks__)
        return func

    return decorator


@mark('__test_1')
@mark('__test_2')
@mark('__test_300')
def __test(): pass

@mark('__test_3::a')
@mark('__test_3::b')
@mark('__test_2')
def __test_2(): pass
