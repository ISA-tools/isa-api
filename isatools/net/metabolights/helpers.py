from os import path, makedirs

from isatools.net.metabolights.core import MTBLSInvestigation
from isatools.net.metabolights.utils import MTBLSDownloader
from isatools.model import Investigation


def get(mtbls_study_id: str, target_dir: str = None) -> str:
    investigation = MTBLSInvestigation(mtbls_study_id, target_dir)
    investigation.get_investigation()
    return investigation.output_dir


def getj(mtbls_study_id: str, target_dir: str = None) -> Investigation:
    investigation = MTBLSInvestigation(mtbls_study_id, target_dir, 'json')
    investigation.load_json()
    return investigation.investigation


def get_data_files(mtbls_study_id: str, factor_selection: dict = None) -> list:
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_data_files(factor_selection)


def get_factor_names(mtbls_study_id: str) -> set:
    """ This function gets the factor names of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A set of factor names associated with the study

    Example usage:
        factor_names = get_factor_names('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_factor_names()


def get_factor_values(mtbls_study_id: str, factor_name: str) -> set:
    """ This function gets the factor values of a factor in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :param factor_name: The factor name for which values are being queried
    :return: A set of factor values associated with the factor and study

    Example usage:
        factor_values = get_factor_values('MTBLS1', 'genotype')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_factor_values(factor_name)


def load(mtbls_study_id: str) -> Investigation:
    investigation = MTBLSInvestigation(mtbls_study_id)
    investigation.load_json()
    return investigation.investigation


def get_factors_summary(mtbls_study_id: str) -> list:
    """ This function gets a summary of the factors in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of factor names and their values

    Example usage:
        factors_summary = get_factors_summary('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_factors_summary()


def get_study_groups(mtbls_study_id: str) -> dict:
    """ This function gets the study groups of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A set of study groups associated with the study

    Example usage:
        study_groups = get_study_groups('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_groups()


def get_study_groups_samples_sizes(mtbls_study_id: str) -> list:
    """ This function gets the study groups and their sample sizes of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of study groups and their sample sizes

    Example usage:
        study_groups_samples_sizes = get_study_groups_samples_sizes('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_groups_samples_sizes()


def get_sources_for_sample(mtbls_study_id: str, sample_name: str) -> list:
    """ This function gets the sources for a sample in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :param sample_name: The sample name for which sources are being queried
    :return: A set of sources associated with the sample and study

    Example usage:
        sources = get_sources_for_sample('MTBLS1', 'sample1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_sources_for_sample(sample_name)


def get_data_for_sample(mtbls_study_id: str, sample_name: str) -> list:
    """ This function gets the data for a sample in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :param sample_name: The sample name for which data is being queried
    :return: A dictionary of data files and their associated data

    Example usage:
        data = get_data_for_sample('MTBLS1', 'sample1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_data_for_sample(sample_name)


def get_study_groups_data_sizes(mtbls_study_id: str) -> list:
    """ This function gets the study groups and their data sizes of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of study groups and their data sizes

    Example usage:
        study_groups_data_sizes = get_study_groups_data_sizes('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_groups_data_sizes()


def get_characteristics_summary(mtbls_study_id: str) -> list:
    """ This function gets a summary of the characteristics in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of characteristic names and their values

    Example usage:
        characteristics_summary = get_characteristics_summary('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_characteristics_summary()


def get_study_variable_summary(mtbls_study_id: str) -> list:
    """ This function gets a summary of the study variables in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of study variable names and their values

    Example usage:
        study_variable_summary = get_study_variable_summary('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_variable_summary()


def get_study_group_factors(mtbls_study_id: str) -> list:
    """ This function gets the factors of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of study groups and their factors

    Example usage:
        study_group_factors = get_study_group_factors('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_group_factors()


def get_filtered_df_on_factors_list(mtbls_study_id: str) -> None:
    raise NotImplementedError('Not implemented yet')


def get_mtbls_list() -> list:
    """
    This function gets a list of MTBLS studies from the FTP server

    :return: A list of MTBLS studies

    Example usage:
        mtbls_list = get_mtbls_list()
    """
    downloader = MTBLSDownloader()
    return downloader.get_mtbls_list()


def dl_all_mtbls_isatab(target_dir: str) -> int:
    download_count = 0
    for mtbls_id in get_mtbls_list():
        target_subdir = path.join(target_dir, mtbls_id)
        if not path.exists(target_subdir):
            makedirs(target_subdir)
        i = MTBLSInvestigation(mtbls_id, target_subdir)
        i.get_investigation()
        download_count += 1
    return download_count
