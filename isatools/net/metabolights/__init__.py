from isatools.net.metabolights.core import MTBLSInvestigation


def get(mtbls_study_id, target_dir=None):
    investigation = MTBLSInvestigation(mtbls_study_id, target_dir)
    investigation.get()
    return investigation.output_dir


def getj(mtbls_study_id, target_dir=None):
    investigation = MTBLSInvestigation(mtbls_study_id, target_dir, 'json')
    investigation.get()
    return investigation.investigation


def get_factor_values(mtbls_study_id, factor_name):
    """
    This function gets the factor values of a factor in a MetaboLights study

    :param mtbls_study_id: Accession number of the MetaboLights study
    :param factor_name: The factor name for which values are being queried
    :return: A set of factor values associated with the factor and study

    Example usage:
        factor_values = get_factor_values('MTBLS1', 'genotype')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_factor_values(factor_name)
