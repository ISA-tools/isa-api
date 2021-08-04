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
    Identifies if a given sample contains the given factor value
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


def find_exposure(process_sequence, exposure):
    """
    Finds if the process in the process sequence have an input sample with the given exposure factorValue
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
    Find the process in the process sequence that relies on the given protocol
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


def build_filter(targets, variable):
    """
    Checks if the given filter name is in the operator field of the filters
    :param targets: the filters to look into
    :param variable: the filter name to look for
    :return: None or the filter value
    """
    if not targets:
        return None, None
    else:
        if variable in targets:
            sub_operator = list(targets[variable].keys())[0]
            return targets[variable][sub_operator], sub_operator
        else:
            return None, None


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


def build_assays_filters(filters):
    """
    Given some filters, build the filters input for search_assays
    :param filters: the user filters
    :return: an object to pass as an input to search_assays()
    """
    return {
        "measurementType": build_filter(filters, 'measurementType'),
        "technologyType": build_filter(filters, 'technologyType'),
        "executesProtocol": build_filter(filters, 'executesProtocol'),
        "treatmentGroup": filters['treatmentGroup'] if filters and 'treatmentGroup' in filters else None
    }


def search_assays(assays, filters, operator):
    """
    Search the assays and returns the ones that match the given filters
    :param assays: the assays to search into
    :param filters: the filters to apply
    :param operator: the operator for combining the filters. Should be AND or OR
    :return: a list of assays or an empty list
    """
    measurement_value, measurement_operator = filters['measurementType']
    technology_value, technology_operator = filters['technologyType']
    protocol_value, protocol_operator = filters['executesProtocol']
    exposition_factors = filters['treatmentGroup']
    output = []
    for assay_type in assays:
        found = [find_protocol(assay_type.process_sequence, protocol_value, protocol_operator),
                 find_measurement(assay_type.measurement_type, measurement_value, measurement_operator),
                 find_technology_type(assay_type.technology_type, technology_value, technology_operator),
                 find_exposure(assay_type.process_sequence, exposition_factors)]
        if operator == 'AND' and False not in list(set(found)):
            output.append(assay_type)
        elif operator == 'OR' and True in found:
            output.append(assay_type)
    return output
