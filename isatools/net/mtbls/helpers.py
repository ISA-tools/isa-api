from os import path, makedirs
from tempfile import mkdtemp

import progressbar

from isatools.net.mtbls.core import MTBLSInvestigation
from isatools.net.mtbls.utils import MTBLSDownloader


def get(mtbls_study_id: str, target_dir: str = None) -> str:
    """
    This function downloads a Metabolights study as an ISA-Tab archive

    :param mtbls_study_id: Accession number of the Metabolights study
    :param target_dir: Optional directory to download the study to
    :return: The path to the downloaded study

    Example usage:
        get('MTBLS1', '/path/to/download/directory')
    """
    if target_dir is None:
        target_dir = mkdtemp()
    investigation = MTBLSInvestigation(mtbls_id=mtbls_study_id, output_directory=target_dir)
    investigation.get_investigation()
    return investigation.output_dir


def getj(mtbls_study_id: str) -> dict:
    """
    This function downloads a Metabolights study as an ISA-json

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: The ISA json dictionary

    Example usage:
        my_json = getj('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_id=mtbls_study_id, output_format='json')
    investigation.load_json()
    return investigation.investigation.to_dict()


def get_data_files(mtbls_study_id: str, factor_selection: dict = None) -> list:
    """
    This function gets the data files for a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :param factor_selection: A dictionary of factors and their values to filter the data files by
    :return: A list of data files associated with the study

    Example usage:
        data_files = get_data_files('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_data_files(factor_selection)


def get_factor_names(mtbls_study_id: str) -> set:
    """
    This function gets the factor names of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A set of factor names associated with the study

    Example usage:
        factor_names = get_factor_names('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_factor_names()


def get_factor_values(mtbls_study_id: str, factor_name: str) -> set:
    """
    This function gets the factor values of a factor in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :param factor_name: The factor name for which values are being queried
    :return: A set of factor values associated with the factor and study

    Example usage:
        factor_values = get_factor_values('MTBLS1', 'genotype')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_factor_values(factor_name)


def get_factors_summary(mtbls_study_id: str) -> list:
    """
    This function gets a summary of the factors in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of factor names and their values

    Example usage:
        factors_summary = get_factors_summary('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_factors_summary()


def get_study_groups(mtbls_study_id: str) -> dict:
    """
    This function gets the study groups of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A set of study groups associated with the study

    Example usage:
        study_groups = get_study_groups('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_groups()


def get_study_groups_samples_sizes(mtbls_study_id: str) -> list:
    """
    This function gets the study groups and their sample sizes of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of study groups and their sample sizes

    Example usage:
        study_groups_samples_sizes = get_study_groups_samples_sizes('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_groups_samples_sizes()


def get_sources_for_sample(mtbls_study_id: str, sample_name: str) -> list:
    """
    This function gets the sources for a sample in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :param sample_name: The sample name for which sources are being queried
    :return: A set of sources associated with the sample and study

    Example usage:
        sources = get_sources_for_sample('MTBLS1', 'my-sample-name')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_sources_for_sample(sample_name)


def get_data_for_sample(mtbls_study_id: str, sample_name: str) -> list:
    """
    This function gets the data for a sample in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :param sample_name: The sample name for which data is being queried
    :return: A dictionary of data files and their associated data

    Example usage:
        data = get_data_for_sample('MTBLS1', 'sample1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_data_for_sample(sample_name)


def get_study_groups_data_sizes(mtbls_study_id: str) -> list:
    """
    This function gets the study groups and their data sizes of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of study groups and their data sizes

    Example usage:
        study_groups_data_sizes = get_study_groups_data_sizes('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_groups_data_sizes()


def get_characteristics_summary(mtbls_study_id: str) -> list:
    """
    This function gets a summary of the characteristics in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of characteristic names and their values

    Example usage:
        characteristics_summary = get_characteristics_summary('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_characteristics_summary()


def get_study_variable_summary(mtbls_study_id: str) -> list:
    """
    This function gets a summary of the study variables in a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of study variable names and their values

    Example usage:
        study_variable_summary = get_study_variable_summary('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_variable_summary()


def get_study_group_factors(mtbls_study_id: str) -> list:
    """
    This function gets the factors of a Metabolights study

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: A dictionary of study groups and their factors

    Example usage:
        study_group_factors = get_study_group_factors('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_study_group_factors()


def get_filtered_df_on_factors_list(mtbls_study_id: str) -> list:
    """ Print the filtered dataframe on factors list and returns the applied queries

    :param mtbls_study_id: Accession number of the Metabolights study
    :return: a list of applied queries

    Example usage:
        queries = get_filtered_df_on_factors_list('MTBLS1')
    """
    investigation = MTBLSInvestigation(mtbls_study_id)
    return investigation.get_filtered_df_on_factors_list()


def get_mtbls_list() -> list:
    """
    This function gets a list of MTBLS studies from the FTP server

    :return: A list of MTBLS studies

    Example usage:
        mtbls_list = get_mtbls_list()
    """
    downloader = MTBLSDownloader()
    return downloader.get_mtbls_list()


def dl_all_mtbls_isatab(target_dir: str, mtbls_ids: list = None, limit: int = 0) -> tuple:
    """
    This function downloads all Metabolights studies as ISA-Tab

    :param target_dir: The directory to download the studies to
    :param mtbls_ids: A list of Metabolights study accession numbers to download. Downloads all studies if not specified
    :param limit: The maximum number of studies to download. Downloads all studies if not specified
    :return: The number of studies downloaded and a report for failing studies
    """
    download_count = 0
    download_errors = {}
    target_mtbls_ids = mtbls_ids if mtbls_ids else get_mtbls_list()
    total_size = len(target_mtbls_ids)
    for i in progressbar.progressbar(range(total_size)):
        mtbls_id = target_mtbls_ids[i]
        if 0 < limit == download_count:
            break
        target_subdir = path.join(target_dir, mtbls_id)
        if not path.exists(target_subdir):
            makedirs(target_subdir)

        try:
            i = MTBLSInvestigation(mtbls_id, target_subdir)
            i.get_investigation()
            download_count += 1
        except Exception as e:
            download_errors[mtbls_id] = e
    return download_count, download_errors


########################################################################################################################
# ISA commands for MTBLS
########################################################################################################################


def get_factors_command(study_id: str, output: str) -> list:
    """ TODO: write docstring """
    investigation = MTBLSInvestigation(study_id)
    with open(output, 'w+') as f:
        factors = investigation.get_factors_command(f)
    return factors


def get_factor_values_command(study_id: str, factor: str, output: str) -> list:
    """ TODO: write docstring """
    investigation = MTBLSInvestigation(study_id)
    with open(output, 'w+') as f:
        factors = investigation.get_factor_values_command(factor, f)
    return factors


def get_data_files_command(
        study_id: str,
        output: str,
        json_query: str = None,
        galaxy_parameters_file: str = None
) -> None:
    """ TODO: write docstring """
    investigation = MTBLSInvestigation(study_id)
    with open(output, 'w+') as f:
        investigation.get_data_files_command(f, json_query, galaxy_parameters_file)


def get_summary_command(study_id: str, json_output: str, html_output: str) -> list:
    """
    This function gets a json and html summary of the Metabolights study variables

    :param study_id: Accession number of the Metabolights study
    :param json_output: The path to the json output file
    :param html_output: The path to the html output file

    Example usage:
        html = get_summary_command('MTBLS1', '/path/to/summary/MTBLS1.json', '/path/to/summary/MTBLS1.html')
    """
    investigation = MTBLSInvestigation(study_id)
    with open(json_output, 'w+') as f:
        return investigation.get_summary_command(f, html_output)


def datatype_get_summary_command(study_id: str, output):
    """
        This function gets a json summary of the Metabolights study variables

        :param study_id: Accession number of the Metabolights study
        :param output: The path to the json output file

        Example usage:
            html = get_summary_command('MTBLS1', '/path/to/download/MTBLS1.json')
        """
    investigation = MTBLSInvestigation(study_id)
    with open(output, 'w+') as f:
        return investigation.datatype_get_summary_command(f)
