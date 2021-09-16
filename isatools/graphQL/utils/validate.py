def validate_input(inputs):
    """
    Validate the 'inputs" arguments of the queries
    :param inputs: the inputs to validate
    :return: True or raise Exception
    """
    validate_target(inputs, "input")
    validate_treatment_group(inputs)
    validate_characteristics(inputs)
    return True


def validate_outputs(outputs):
    """
    Validate the 'outputs" arguments of the queries
    :param outputs: the inputs to validate
    :return: True or raise Exception
    """
    validate_target(outputs, "outputs")
    validate_treatment_group(outputs)
    validate_characteristics(outputs)
    return True


def validate_target(inputs, input_type):
    """
    Validate the target depending of the input_type.
    :param inputs: the value to validate
    :param input_type: 'input' or 'output'
    :return: True or raise Exception
    """
    if not hasattr(inputs, 'target') or not inputs.target:
        return True
    if input_type == "input" and inputs.target not in ["Material", "DataFile", "Sample", "Source"]:
        raise Exception("Inputs 'on' argument should be Material, DataFile, Sample or Source")
    if input_type == "outputs" and inputs.target not in ["Material", "DataFile", "Sample"]:
        raise Exception("Outputs 'on' argument should be Material, DataFile or Sample")
    return True


def validate_treatment_group(inputs):
    """
    Validate the treatment group input
    :param inputs: the value to validate
    :return: True or raise Exception
    """
    if not hasattr(inputs, 'treatmentGroup') or not inputs.treatmentGroup:
        return True
    if inputs.treatmentGroup and inputs.target != "Sample":
        raise Exception("Inputs 'treatmentGroup' argument can only be applied to Sample")
    return True


def validate_characteristics(inputs):
    """
    Validate the characteristics input
    :param inputs: the value to validate
    :return: True or raise Exception
    """
    if not hasattr(inputs, 'characteristics') or not inputs.characteristics:
        return True
    if inputs.characteristics and inputs.target not in ["Sample", "Material", "Source"]:
        raise Exception("Inputs 'characteristics' argument can only be applied to Sample, Material or Source")
    return True
