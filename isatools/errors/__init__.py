""" ISA-specific exceptions """


class ISAModelAttributeError(AttributeError):
    """
    If attempting to set a ISA Python object attribute to an invalid value.
    """