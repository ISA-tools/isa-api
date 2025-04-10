# -*- coding: utf-8 -*
""" ISA-specific exceptions """


class AttributeError(AttributeError):
    """
    If attempting to set a ISA Python object attribute to an invalid value.
    """


class ISAModelTypeError(TypeError):
    """
    If attempting to use a ISA Python object of a wrong type.
    """


class ISAModelValueError(ValueError):
    """
    If passing a parameter of the right type but the wrong value to an ISA model method.
    """


class ISAModelIndexError(IndexError):
    """
    If an index is out of bounds
    """


