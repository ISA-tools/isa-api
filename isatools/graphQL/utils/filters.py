def build_filter(targets, variable):
    """
    Test if the given filter name is in the operator field of the filters
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
        "treatmentGroup": filters['treatmentGroup'] if filters and 'treatmentGroup' in filters else None,
        "characteristics": filters['characteristics'] if filters and 'characteristics' in filters else None,
        "parameterValues": filters['parameterValues'] if filters and 'parameterValues' in filters else None
    }