from isatools.graphQL.utils.find import (
    find_exposure_value,
    find_characteristics,
    find_protocol,
    find_measurement,
    find_technology_type,
    find_exposure,
    find_parameter_value,
    compare_values
)
from isatools.graphQL.utils.filters import build_assays_filters


def search_assays(assays, filters, operator):
    """
    Search the assays and returns the ones that match the given filters
    :param assays: the assays to search into
    :param filters: the filters to apply
    :param operator: the operator for combining the filters. Should be AND or OR
    :return: a list of assays or an empty list
    """
    if operator not in ['AND', 'OR']:
        raise Exception("Operator should be AND or OR")
    target = filters['target'] or None
    filters = build_assays_filters(filters)
    measurement_value, measurement_operator = filters['measurementType']
    technology_value, technology_operator = filters['technologyType']
    protocol_value, protocol_operator = filters['executesProtocol']
    exposition_factors = filters['treatmentGroup']
    parameter_values = filters['parameterValues']
    output = []
    for assay_type in assays:
        found = [find_protocol(assay_type.process_sequence, protocol_value, protocol_operator),
                 find_measurement(assay_type.measurement_type, measurement_value, measurement_operator),
                 find_technology_type(assay_type.technology_type, technology_value, technology_operator),
                 find_exposure(assay_type.process_sequence, exposition_factors)]

        if filters['characteristics']:
            found_sample = False
            for process in assay_type.process_sequence:
                for input_value in process.inputs:
                    input_classname = type(input_value).__name__
                    if input_classname == target:
                        local_found = []
                        for characteristic in filters['characteristics']:
                            local_found.append(find_characteristics(input_value, characteristic))
                        if False not in list(set(local_found)) or local_found == []:
                            found_sample = True
                        if found_sample:
                            break
                if found_sample:
                    break
            found.append(found_sample)

        if parameter_values:
            found_assay = False
            for process in assay_type.process_sequence:
                found_process = []
                for target in process.parameter_values:
                    found_process.append(False not in find_parameter_value(target, parameter_values))
                found_process = list(set(found_process))
                found_assay = True in found_process if len(found_process) > 0 else False
                if found_assay:
                    found.append(True)
                    break
            if not found_assay:
                found.append(False)

        if operator == 'AND' and False not in list(set(found)):
            output.append(assay_type)
        elif operator == 'OR' and True in found:
            output.append(assay_type)
    return output


def search_process_sequence(process_sequence, filters, operator):
    """
    Search the process sequence and returns the processes that match the given filters
    :param process_sequence: the sequence of processes to apply the filter to
    :param filters: the filters to apply
    :param operator: the operator for combining the filters. Should be AND or OR
    :return: a list of processes or an empty list
    """
    if operator not in ['AND', 'OR']:
        raise Exception("Operator should be AND or OR")

    if not filters:
        return process_sequence

    exposition_factors = filters['treatmentGroup'] if 'treatmentGroup' in filters else None
    protocol = filters['executesProtocol'] if 'executesProtocol' in filters else None
    characteristics = filters['characteristics'] if 'characteristics' in filters else None
    parameter_values = filters['parameterValues'] if 'parameterValues' in filters else None

    if not protocol and not exposition_factors and not characteristics and not parameter_values:
        return process_sequence

    processes = []
    for process in process_sequence:
        append_process = []
        match_exposure = []
        if not exposition_factors:
            match_exposure = [True]
        else:
            for input_data in process.inputs:
                if type(input_data).__name__ == "Sample":
                    for factor in exposition_factors:
                        match_exposure.append(find_exposure_value(input_data, factor, factor['name']))
        if list(set(match_exposure)) == [True]:
            append_process.append(True)

        if not protocol:
            append_process.append(True)
        else:
            comparator = list(protocol.keys())[0]
            append_process.append(compare_values(process.executes_protocol.protocol_type.term,
                                                 protocol[comparator],
                                                 comparator))

        if not characteristics:
            append_process.append(True)
        else:
            found_sample = False
            for sample in process.inputs:
                input_classname = type(sample).__name__
                if input_classname == filters['target']:
                    local_found = []
                    for characteristic in characteristics:
                        local_found.append(find_characteristics(sample, characteristic))
                    if False not in list(set(local_found)) or local_found == []:
                        found_sample = True
                    if found_sample:
                        break
            append_process.append(found_sample)

        if parameter_values:
            found = []
            for target in process.parameter_values:
                found.append(False not in find_parameter_value(target, parameter_values))
            found = list(set(found))
            append_process.append(True in found if len(found) > 0 else False)

        append_process = list(set(append_process))
        if operator == 'AND' and False not in append_process:
            processes.append(process)
        elif operator == 'OR' and True in append_process:
            processes.append(process)

    return processes


def search_inputs(process_inputs, filters, operator):
    """
    Search in the process inputs to find the one that match the given filters
    :param process_inputs: the inputs to search for
    :param filters: a valid filters object
    :param operator: should be 'AND' or 'OR'
    :return:
    """
    if not filters:
        return process_inputs
    outputs = []
    if filters.is_valid:
        for input_data in process_inputs:
            found = []
            input_classname = type(input_data).__name__
            if input_classname == filters['target'] == "Sample" and 'treatmentGroup' in filters:
                local_found = []
                for factor in filters['treatmentGroup']:
                    local_found.append(find_exposure_value(input_data, factor, factor['name']))
                if False not in list(set(local_found)) or local_found == []:
                    found.append(True)
                else:
                    found.append(False)
            if input_classname == filters['target'] and 'characteristics' in filters:
                local_found = []
                for characteristic in filters['characteristics']:
                    local_found.append(find_characteristics(input_data, characteristic))
                if False not in list(set(local_found)) or local_found == []:
                    found.append(True)
                else:
                    found.append(False)
            if operator == "AND" and False not in found:
                outputs.append(input_data)
            elif operator == "OR" and True in found:
                outputs.append(input_data)
        return outputs


def search_outputs(process_outputs, filters):
    """
    Search in the process outputs to find the one that match the given filters
    :param process_outputs: the outputs to search for
    :param filters: should be 'AND' or 'OR'
    :return:
    """
    if not filters:
        return process_outputs

    if filters.is_valid:
        outputs = []
        for output_data in process_outputs:
            if type(output_data).__name__ == filters['target'] == "DataFile":
                operator = list(filters['label'].keys())[0]
                if compare_values(output_data.label, filters['label'][operator], operator):
                    outputs.append(output_data)
            elif filters['target'] == type(output_data).__name__ == "Material":
                operator = list(filters['label'].keys())[0]
                if compare_values(output_data.type, filters['label'][operator], operator):
                    outputs.append(output_data)
            elif filters['target'] == type(output_data).__name__ == "Sample":
                # TODO: Filter samples on exposure FV, needs a valid input (no samples in current assays outputs)
                print("SAMPLE HERE, NOT DONE YET")
        return outputs


def search_data_files(data_files, label):
    """
    Search the data files for object with the given label
    :param data_files: the data files list to search into
    :param label: the label to search for
    :return: a list of filtered data files
    """
    if label:
        operator = list(label.keys())[0]
        return [x for x in data_files if compare_values(x.label, label[operator], operator)]
    return data_files


def search_parameter_values(process, filters):
    """
    Search the processes for parameter values that match the given filters
    :param process: the process to search
    :param filters: the filters to apply
    :return: a list a processes that match
    """
    output = []
    parameter_filter = filters['parameterValues'] if filters and 'parameterValues' in filters else None
    for parameter_value in process.parameter_values:
        found = list(set(find_parameter_value(parameter_value, parameter_filter)))
        if False not in found:
            output.append(parameter_value)
    return output
