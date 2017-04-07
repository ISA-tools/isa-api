import ftplib
import logging
import os
import tempfile
import shutil
import re
import glob
from isatools.convert import isatab2json
from isatools import isatab
from isatools.model.v1 import OntologyAnnotation, Process, ParameterValue
import networkx as nx
import pandas as pd

MTBLS_FTP_SERVER = 'ftp.ebi.ac.uk'
MTBLS_BASE_DIR = '/pub/databases/metabolights/studies/public'
INVESTIGATION_FILENAME = 'i_Investigation.txt'

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# REGEXES
_RX_FACTOR_VALUE = re.compile('Factor Value\[(.*?)\]')


def get(mtbls_study_id, target_dir=None):
    """
    This function downloads ISA content from the MetaboLights FTP site.

    :param mtbls_study_id: Study identifier for MetaboLights study to get, as a str (e.g. MTBLS1)
    :param target_dir: Path to write files to. If None, writes to temporary directory (generated on the fly)
    :return: Path where the files were written to

    Example usage:
        isa_json = MTBLS.get_study('MTBLS1', '/tmp/mtbls')
    """
    logging.info("Setting up ftp with {}".format(MTBLS_FTP_SERVER))
    ftp = ftplib.FTP(MTBLS_FTP_SERVER)
    logging.info("Logging in as anonymous user...")
    response = ftp.login()
    if '230' in response:  # 230 means Login successful
        logging.info("Log in successful!")
        try:
            logging.info("Looking for study '{}'".format(mtbls_study_id))
            ftp.cwd('{base_dir}/{study}'.format(base_dir=MTBLS_BASE_DIR, study=mtbls_study_id))
            if target_dir is None:
                target_dir = tempfile.mkdtemp()
            logging.info("Using directory '{}'".format(target_dir))
            out_file = open(os.path.join(target_dir, INVESTIGATION_FILENAME), 'wb')
            logging.info("Retrieving file '{}'".format(MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + INVESTIGATION_FILENAME))
            ftp.retrbinary('RETR ' + INVESTIGATION_FILENAME, out_file.write)
            with open(out_file.name, encoding='utf-8') as i_fp:
                i_bytes = i_fp.read()
                lines = i_bytes.splitlines()
                s_filenames = [l.split('\t')[1][1:-1] for l in lines if 'Study File Name' in l]
                for s_filename in s_filenames:
                    out_file = open(os.path.join(target_dir, s_filename), 'wb')
                    logging.info("Retrieving file '{}'".format(
                        MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + s_filename))
                    ftp.retrbinary('RETR ' + s_filename, out_file.write)
                a_filenames_lines = [l.split('\t') for l in lines if 'Study Assay File Name' in l]
                for a_filename_line in a_filenames_lines:
                    for a_filename in [f[1:-1] for f in a_filename_line[1:]]:
                        out_file = open(os.path.join(target_dir, a_filename), 'wb')
                        logging.info("Retrieving file '{}'".format(
                            MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + a_filename))
                        ftp.retrbinary('RETR ' + a_filename, out_file.write)
        except ftplib.error_perm as ftperr:
            logger.fatal("Could not retrieve MetaboLights study '{study}': {error}".format(study=mtbls_study_id, error=ftperr))
        finally:
            return target_dir
    else:
        raise ConnectionError("There was a problem connecting to MetaboLights: " + response)


def getj(mtbls_study_id):
    """
    This function downloads the specified MetaboLights study and returns an ISA JSON representation of it

    :param mtbls_study_id: Study identifier for MetaboLights study to get, as a str (e.g. MTBLS1)
    :return: ISA JSON representation of the MetaboLights study

    Example usage:
        isa_json = MTBLS.load('MTBLS1')
    """
    tmp_dir = get(mtbls_study_id)
    if tmp_dir is None:
        raise IOError("There was a problem retrieving the study ", mtbls_study_id)
    isa_json = isatab2json.convert(tmp_dir, identifier_type=isatab2json.IdentifierType.name,
                                   validate_first=False,
                                   use_new_parser=True)
    shutil.rmtree(tmp_dir)
    return isa_json


def get_data_files(mtbls_study_id, factor_selection=None):
    tmp_dir = get(mtbls_study_id)
    if tmp_dir is None:
        raise IOError("There was a problem retrieving study {}. Does it exist?".format(mtbls_study_id))
    else:
        result = slice_data_files(tmp_dir, factor_selection=factor_selection)
    shutil.rmtree(tmp_dir)
    return result


def slice_data_files(dir, factor_selection=None):
    """
    This function gets a list of samples and related data file URLs for a given MetaboLights study, optionally
    filtered by factor value (currently by matching on exactly 1 factor value)

    :param mtbls_study_id: Study identifier for MetaboLights study to get, as a str (e.g. MTBLS1)
    :param factor_selection: Selected factor values to filter on samples
    :return: A list of dicts {sample_name, list of data_files} containing sample names with associated data filenames

    Example usage:
        samples_and_data = mtbls.get_data_files('MTBLS1', {'Gender': 'Male'})

    TODO:  Need to work on more complex filters e.g.:
        {"gender": ["male", "female"]} selects samples matching "male" or "female" factor value
        {"age": {"equals": 60}} selects samples matching age 60
        {"age": {"less_than": 60}} selects samples matching age less than 60
        {"age": {"more_than": 60}} selects samples matching age more than 60

        To select samples matching "male" and age less than 60:
        {
            "gender": "male",
            "age": {
                "less_than": 60
            }
        }
    """
    results = list()
    # first collect matching samples
    for table_file in glob.iglob(os.path.join(dir, '[a|s]_*')):
        logger.info("Loading {}".format(table_file))
        with open(table_file, encoding='utf-8') as fp:
            df = isatab.load_table(fp)
            if factor_selection is None:
                matches = df['Sample Name'].items()
                for indx, match in matches:
                    sample_name = match
                    if len([r for r in results if r['sample'] == sample_name]) == 1:
                        continue
                    else:
                        results.append(
                            {
                                "sample": sample_name,
                                "data_files": []
                            }
                        )
            else:
                for factor_name, factor_value in factor_selection.items():
                    if 'Factor Value[{}]'.format(factor_name) in list(df.columns.values):
                        matches = df.loc[df['Factor Value[{}]'.format(factor_name)] == factor_value]['Sample Name'].items()
                        for indx, match in matches:
                            sample_name = match
                            if len([r for r in results if r['sample'] == sample_name]) == 1:
                                continue
                            else:
                                results.append(
                                    {
                                        "sample": sample_name,
                                        "data_files": [],
                                        "query_used": factor_selection
                                    }
                                )
    # now collect the data files relating to the samples
    for result in results:
        sample_name = result['sample']
        for table_file in glob.iglob(os.path.join(dir, 'a_*')):
            with open(table_file, encoding='utf-8') as fp:
                df = isatab.load_table(fp)
                data_files = list()
                table_headers = list(df.columns.values)
                sample_rows = df.loc[df['Sample Name'] == sample_name]
                if 'Raw Spectral Data File' in table_headers:
                    data_files = sample_rows['Raw Spectral Data File']
                elif 'Free Induction Decay Data File' in table_headers:
                    data_files = sample_rows['Free Induction Decay Data File']
                result['data_files'] = [i for i in list(data_files) if str(i) != 'nan']
    return results


def get_factor_names(mtbls_study_id):
    """
    This function gets the factor names used in a MetaboLights study

    :param mtbls_study_id: Accession number of the MetaboLights study
    :return: A set of factor names used in the study

    Example usage:
        factor_names = get_factor_names('MTBLS1')
    """
    tmp_dir = get(mtbls_study_id)
    from isatools import isatab
    factors = set()
    for table_file in glob.iglob(os.path.join(tmp_dir, '[a|s]_*')):
        with open(os.path.join(tmp_dir, table_file), encoding='utf-8') as fp:
            df = isatab.load_table(fp)
            factors_headers = [header for header in list(df.columns.values) if _RX_FACTOR_VALUE.match(header)]
            for header in factors_headers:
                factors.add(header[13:-1])
    return factors


def get_factor_values(mtbls_study_id, factor_name):
    """
    This function gets the factor values of a factor in a MetaboLights study

    :param mtbls_study_id: Accession number of the MetaboLights study
    :param factor_name: The factor name for which values are being queried
    :return: A set of factor values associated with the factor and study

    Example usage:
        factor_values = get_factor_values('MTBLS1', 'genotype')
    """
    tmp_dir = get(mtbls_study_id)
    from isatools import isatab
    fvs = set()
    for table_file in glob.iglob(os.path.join(tmp_dir, '[a|s]_*')):
        with open(os.path.join(tmp_dir, table_file), encoding='utf-8') as fp:
            df = isatab.load_table(fp)
            if 'Factor Value[{}]'.format(factor_name) in list(df.columns.values):
                for _, match in df['Factor Value[{}]'.format(factor_name)].iteritems():
                    try:
                        match = match.item()
                    except AttributeError:
                        pass
                    if isinstance(match, (str, int, float)):
                        if str(match) != 'nan':
                            fvs.add(match)
    shutil.rmtree(tmp_dir)
    return fvs


def load(mtbls_study_id):
    tmp_dir = get(mtbls_study_id)
    if tmp_dir is None:
        raise IOError("There was a problem retrieving the study ", mtbls_study_id)
    with open(glob.glob(os.path.join(tmp_dir, 'i_*.txt'))[0], encoding='utf-8') as f:
        ISA = isatab.load(f)
        shutil.rmtree(tmp_dir)
        return ISA


def get_factors_summary(mtbls_study_id):
    """
    This function generates a factors summary for a MetaboLights study

    :param mtbls_study_id: Accession number of the MetaboLights study
    :return: A list of dicts summarising the set of factor names and values associated with each sample

    Note: it only returns a summary of factors with variable values.

    Example usage:
        factor_summary = get_factors_summary('MTBLS1')
        [
            {
                "name": "ADG19007u_357", 
                "Metabolic syndrome": "Control Group", 
                "Gender": "Female"
            }, 
            {
                "name": "ADG10003u_162", 
                "Metabolic syndrome": "diabetes mellitus",
                "Gender": "Female"
            },
        ]


    """
    ISA = load(mtbls_study_id=mtbls_study_id)
    all_samples = []
    for study in ISA.studies:
        all_samples.extend(study.materials['samples'])
    samples_and_fvs = []
    for sample in all_samples:
        sample_and_fvs = {
                "name": sample.name
            }
        for fv in sample.factor_values:
            if isinstance(fv.value, (str, int, float)):
                fv_value = fv.value
            elif isinstance(fv.value, OntologyAnnotation):
                fv_value = fv.value.term
            sample_and_fvs[fv.factor_name.name] = fv_value
        samples_and_fvs.append(sample_and_fvs)
    df = pd.DataFrame(samples_and_fvs)
    nunique = df.apply(pd.Series.nunique)
    cols_to_drop = nunique[nunique == 1].index
    df = df.drop(cols_to_drop, axis=1)
    return df.to_dict(orient='records')


def get_characteristics_summary(mtbls_study_id):
    """
        This function generates a characteristics summary for a MetaboLights study

        :param mtbls_study_id: Accession number of the MetaboLights study
        :return: A list of dicts summarising the set of characteristic names and values associated with each sample

        Note: it only returns a summary of characteristics with variable values.

        Example usage:
            characteristics_summary = get_characteristics_summary('MTBLS5')
            [
                {
                    "name": "6089if_9",
                    "Variant": "Synechocystis sp. PCC 6803.sll0171.ko"
                },
                {
                    "name": "6089if_43",
                    "Variant": "Synechocystis sp. PCC 6803.WT.none"
                },
            ]


        """
    ISA = load(mtbls_study_id=mtbls_study_id)
    all_samples = []
    for study in ISA.studies:
        all_samples.extend(study.materials['samples'])
    samples_and_characs = []
    for sample in all_samples:
        sample_and_characs = {
                "name": sample.name
            }
        for source in sample.derives_from:
            for c in source.characteristics:
                if isinstance(c.value, (str, int, float)):
                    c_value = c.value
                elif isinstance(c.value, OntologyAnnotation):
                    c_value = c.value.term
                sample_and_characs[c.category.term] = c_value
        samples_and_characs.append(sample_and_characs)
    df = pd.DataFrame(samples_and_characs)
    nunique = df.apply(pd.Series.nunique)
    cols_to_drop = nunique[nunique == 1].index
    df = df.drop(cols_to_drop, axis=1)
    return df.to_dict(orient='records')


# PVs don't seem to vary in MTBLS, so maybe skip this function
# def get_parameter_value_summary(mtbls_study_id):
#     """
#         This function generates a parameter values summary for a MetaboLights study
#
#         :param mtbls_study_id: Accession number of the MetaboLights study
#         :return: A list of dicts summarising the set of parameters and values associated with each sample
#
#         Note: it only returns a summary of parameter values with variable values.
#
#         """
#     ISA = load(mtbls_study_id=mtbls_study_id)
#     all_samples = []
#     for study in ISA.studies:
#         all_samples.extend(study.materials['samples'])
#     samples_and_pvs = []
#     for sample in all_samples:
#         sample_and_pvs = {
#             "name": sample.name
#         }
#         for study in ISA.studies:
#             s_processes_linked_to_sample = [x for x in nx.algorithms.ancestors(study.graph, sample) if
#                                             isinstance(x, Process)]
#             for process in s_processes_linked_to_sample:
#                 for pv in process.parameter_values:
#                     if isinstance(pv, ParameterValue):
#                         if isinstance(pv.value, (str, int, float)):
#                             pv_value = pv.value
#                         elif isinstance(pv.value, OntologyAnnotation):
#                             pv_value = pv.value.term
#                         sample_and_pvs[pv.category.parameter_name.term] = pv_value
#             for assay in study.assays:
#                 for sample in assay.materials['samples']:
#                     a_processes_linked_to_sample = [x for x in nx.algorithms.descendants(assay.graph, sample) if
#                                                     isinstance(x, Process)]
#                     for process in a_processes_linked_to_sample:
#                         for pv in process.parameter_values:
#                             if isinstance(pv, ParameterValue):
#                                 if isinstance(pv.value, (str, int, float)):
#                                     pv_value = pv.value
#                                 elif isinstance(pv.value, OntologyAnnotation):
#                                     pv_value = pv.value.term
#                                 sample_and_pvs[pv.category.parameter_name.term] = pv_value
#         samples_and_pvs.append(sample_and_pvs)
#     df = pd.DataFrame(samples_and_pvs)
#     nunique = df.apply(pd.Series.nunique)
#     cols_to_drop = nunique[nunique == 1].index
#     df = df.drop(cols_to_drop, axis=1)
#     return df.to_dict(orient='records')


def get_study_variable_summary(mtbls_study_id):
    ISA = load(mtbls_study_id=mtbls_study_id)
    all_samples = []
    for study in ISA.studies:
        all_samples.extend(study.materials['samples'])
    samples_and_variables = []
    for sample in all_samples:
        sample_and_vars = {
            "name": sample.name
        }
        for fv in sample.factor_values:
            if isinstance(fv.value, (str, int, float)):
                fv_value = fv.value
            elif isinstance(fv.value, OntologyAnnotation):
                fv_value = fv.value.term
            sample_and_vars[fv.factor_name.name] = fv_value
        for source in sample.derives_from:
            for c in source.characteristics:
                if isinstance(c.value, (str, int, float)):
                    c_value = c.value
                elif isinstance(c.value, OntologyAnnotation):
                    c_value = c.value.term
                sample_and_vars[c.category.term] = c_value
        # Don't think pvs vary, so maybe skip this section
        # for study in ISA.studies:
        #     s_processes_linked_to_sample = [x for x in nx.algorithms.ancestors(study.graph, sample) if
        #                                     isinstance(x, Process)]
        #     for process in s_processes_linked_to_sample:
        #         for pv in process.parameter_values:
        #             if isinstance(pv, ParameterValue):
        #                 if isinstance(pv.value, (str, int, float)):
        #                     pv_value = pv.value
        #                 elif isinstance(pv.value, OntologyAnnotation):
        #                     pv_value = pv.value.term
        #                 sample_and_vars[pv.category.parameter_name.term] = pv_value
        #     for assay in study.assays:
        #         for sample in assay.materials['samples']:
        #             a_processes_linked_to_sample = [x for x in nx.algorithms.descendants(assay.graph, sample) if
        #                                             isinstance(x, Process)]
        #             for process in a_processes_linked_to_sample:
        #                 for pv in process.parameter_values:
        #                     if isinstance(pv, ParameterValue):
        #                         if isinstance(pv.value, (str, int, float)):
        #                             pv_value = pv.value
        #                         elif isinstance(pv.value, OntologyAnnotation):
        #                             pv_value = pv.value.term
        #                         sample_and_vars[pv.category.parameter_name.term] = pv_value
        samples_and_variables.append(sample_and_vars)
    df = pd.DataFrame(samples_and_variables)
    nunique = df.apply(pd.Series.nunique)
    cols_to_drop = nunique[nunique == 1].index
    df = df.drop(cols_to_drop, axis=1)
    return df.to_dict(orient='records')
