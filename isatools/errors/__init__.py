""" ISA-specific exceptions """


class ISAModelAttributeError(AttributeError):
    """
    If attempting to set a ISA Python object attribute to an invalid value.
    """


class IsaValueTypeError(TypeError):
    """
    If attempting to use a ISA Python object of a wrong type value.
    """
