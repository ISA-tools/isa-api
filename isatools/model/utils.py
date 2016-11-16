# coding: utf-8
__author__ = 'althonos'

import functools
import itertools
import six

def accepts(*types, **kw):
    """Method decorator enforcing particular types for a setter.

    Loosely based on the PythonDecoratorLibrary type enforcement decorator
    (https://wiki.python.org/moin/PythonDecoratorLibrary)
    """

    if not kw:
        allow_empty = True
    else:
        allow_empty = kw['allow_empty']

    if None in types: allow_None = True
    types = tuple(t for t in types if t is not None)
    assert all(isinstance(t, type) for t in types)

    try:
        def decorator(setter):
            @functools.wraps(setter)
            def new_setter(self, other):

                # Handle str to unicode if Python2
                if six.PY2 and isinstance(other, str):
                    other = other.decode('utf-8')

                # checks for type
                if not isinstance(other, types) and not(allow_None and other is None):
                    msg = _type_info(self, setter, types, other, allow_None)
                    raise AttributeError(msg)

                # Checks that the argument is not empty
                if not allow_empty and not other.strip():
                    msg = _empty_info(self, setter)
                    raise AttributeError(msg)

                return setter(self, other)
            return new_setter
    except AttributeError:
        raise
    return decorator




def _type_info(obj, method, types, other, allow_None):
    '''Convenience function returns nicely formatted error/warning msg.'''
    #"OntologySource.file must be a str or None"

    return "{classname}.{methname} must be a {ok_types}, not {wrong_type} ({other})".format(
                classname = type(obj).__name__,
                methname = method.__name__,
                ok_types = ' or '.join([t.__name__ for t in types] + (['None'] if allow_None else [])),
                wrong_type = type(other).__name__,
                other=other,
            )


def _empty_info(obj, method):
    return "{classname}.{methname} must not be empty".format(
                classname = type(obj).__name__,
                methname = method.__name__
            )


