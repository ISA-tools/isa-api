def find_technology_type(technology_type, expected_value, operator):
    """
    Test if the technology type matches the given input
    :param technology_type: the type to test
    :param expected_value: the value to check against
    :param operator: must be eq, inc, sup, supEq, inf, infEq
    :return: {Boolean}
    """
    if not expected_value or compare_values(technology_type.term, expected_value, operator):
        return True
    return False


def find_measurement(measurement_type, expected_value, operator):
    """
    Test if the measurement type matches the given input
    :param measurement_type: the type to test
    :param expected_value: the value to check against
    :param operator: must be eq, inc, sup, supEq, inf, infEq
    :return: {Boolean}
    """
    if not expected_value or compare_values(measurement_type.term, expected_value, operator):
        return True
    return False


def find_exposure_value(sample, expected_value, target):
    """
    Tests if a given sample contains the given factor value
    :param sample: the sample too look at
    :param expected_value: the value to look for
    :param target: the target of sample to look into
    :return: {Boolean}
    """
    if not expected_value or not expected_value['value']:
        return True
    for factor in sample.factor_values:
        value_operator = list(expected_value['value'].keys())[0]
        name_operator = list(target.keys())[0]
        val = expected_value['value'][value_operator]
        name = target[name_operator]
        if compare_values(factor.factor_name.name, name, name_operator) \
                and compare_values(factor.value.term, val, value_operator):
            return True
    return False


def find_characteristics(sample, expected_value):
    """
    Tests if a given sample contains the given characteristics
    :param sample: the sample too look at
    :param expected_value: the value to look for
    :return: {Boolean}
    """
    if not expected_value or not expected_value['value']:
        return True
    target = expected_value['name']
    target_operator = list(target.keys())[0]
    target_value = target[target_operator]
    value = expected_value['value']
    value_operator = list(value.keys())[0]
    value_value = value[value_operator]
    for characteristic in sample.characteristics:
        if hasattr(characteristic, target_value):
            field = getattr(characteristic, target_value)
            field_value = field.term
            if compare_values(field_value, value_value, value_operator):
                return True
        return False
    return False


def find_exposure(process_sequence, exposure):
    """
    Tests if the process in the process sequence have an input sample with the given exposure factorValue
    :param process_sequence: the process sequence to filter
    :param exposure: the exposure variables to sort on
    :return: if the factorValues were found or not
    """
    if not exposure:
        return True
    for process in process_sequence:
        for input_data in process.inputs:
            if type(input_data).__name__ == "Sample":
                is_found = []
                for factor in exposure:
                    found = find_exposure_value(input_data, factor, factor['name'])
                    is_found.append(found)
                if list(set(is_found)) == [True]:
                    return True
    return False


def find_protocol(process_sequence, expected_value, operator):
    """
    Test if the process in the process sequence relies on the given protocol
    :param process_sequence: the process sequence to look at
    :param expected_value: the protocol value to look for
    :param operator: must be eq, inc, sup, supEq, inf, infEq
    :return: {Boolean}
    """
    if not expected_value:
        return True
    for process in process_sequence:
        if compare_values(process.executes_protocol.protocol_type.term, expected_value, operator):
            return True
    return False


def find_parameter_value(parameter, filters):
    """
    Test if the given parameter value matches with the given filters
    :param parameter: the parameter value of a process
    :param filters: the filters to match with
    :return: list of booleans representing each filter matching value
    """
    if not filters:
        return [True]
    found = []
    for filter_name, filter_content in filters.items():
        operator = list(filter_content.keys())[0]
        filter_value = filter_content[operator]
        target = getattr(parameter, filter_name)
        if filter_name == "category":
            target = target.parameter_name.term
        if not isinstance(target, str):
            target = target.term
        found.append(compare_values(target, filter_value, operator))
    return found


def compare_values(reference, target, operator):
    """
    Compares two string or integers given an operator
    :param reference: the reference value
    :param target: the target value
    :param operator: must be eq, includes, gt, gte, lt, lte
    :return:
    """
    if operator == 'eq':
        return reference == target
    elif operator == 'includes':
        return target in reference
    else:
        try:
            target = int(target)
            if type(reference).__name__ == 'str':
                return False
            reference = int(reference)
            if operator == 'gt':
                return target > reference
            elif operator == 'gte':
                return target >= reference
            elif operator == 'le':
                return target < reference
            elif operator == 'lte':
                return target <= reference
        except Exception:
            message = "Both value and target should be integers when using lt, gt, lte or gte got" \
                      " value: '%s' and target: '%s'" % (reference, target)
            raise Exception(message)
