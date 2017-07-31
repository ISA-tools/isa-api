"""Various utility functions."""
import csv
import json
import logging
import os
import pandas as pd
import uuid
from zipfile import ZipFile

from isatools import config
from isatools import isatab

logging.basicConfig(level=config.log_level)
log = logging.getLogger(__name__)


def format_report_csv(report):
    """Format JSON validation report as CSV string

    :param report: JSON report output from validator
    :return: string representing csv formatted report
    """
    output = str()
    if report["validation_finished"]:
        output = "Validation=success\n"
    for warning in report["warnings"]:
        output += str("{},{},{}\n").format(warning["code"], warning["message"], warning["supplemental"])
    for error in report["errors"]:
        output += str("{},{},{}\n").format(error["code"], error["message"], error["supplemental"])
    return output


def detect_graph_process_pooling(G):
    from isatools.model import Process
    report = list()
    for process in [n for n in G.nodes() if isinstance(n, Process)]:
        if len(G.in_edges(process)) > 1:
            log.info("Possible process pooling detected on: {}"
                     .format(' '.join([process.id, process.executes_protocol.name])))
            report.append(process.id)
    return report


def detect_isatab_process_pooling(fp):
    from isatools import isatab
    report = []
    ISA = isatab.load(fp)
    for study in ISA.studies:
        log.info("Checking {}".format(study.filename))
        pooling_list = detect_graph_process_pooling(study.graph)
        if len(pooling_list) > 0:
            report.append({
                study.filename: pooling_list
            })
        for assay in study.assays:
            log.info("Checking {}".format(assay.filename))
            pooling_list = detect_graph_process_pooling(assay.graph)
            if len(pooling_list) > 0:
                report.append({
                    assay.filename: pooling_list
                })
    return report


def insert_distinct_parameter(table_fp, protocol_ref_to_unpool):
    reader = csv.reader(table_fp, dialect="excel-tab")
    headers = next(reader)  # get column headings
    table_fp.seek(0)
    df = isatab.load_table(table_fp)
    protocol_ref_indices = [x for x, y in enumerate(df.columns) if df[y][0] == protocol_ref_to_unpool]  # find protocol ref column by index
    if len(protocol_ref_indices) != 1:
        raise IndexError("Could not find Protocol REF with provided value {}".format(protocol_ref_to_unpool))
    distindex = list()
    for i in range(0, len(df.index)):
        distindex.append(str(uuid.uuid4())[:8])
    protocol_ref_index = protocol_ref_indices[0]
    name_header = None
    head_from_prot = headers[protocol_ref_index:]
    for x, y in enumerate(head_from_prot):
        if y.endswith(" Name"):
            name_header = y
            break
    if name_header is not None:
        print("Are you sure you want to add a column of hash values in {}? Y/(N)".format(name_header))
        confirm = input()
        if confirm == "Y":
            df[name_header] = distindex
            table_fp.seek(0)
            df.to_csv(table_fp, index=None, header=headers, sep="\t")
    else:
        print("Could not find appropriate column to fill with hashes")
    # return df


def contains(small_list, big_list):
    if len(small_list) == 0:
        return False
    for i in iter(range(len(big_list) - len(small_list) + 1)):
        for j in iter(range(len(small_list))):
            if big_list[i + j] != small_list[j]:
                break
        else:
            return i, i + len(small_list)
    return False


def create_isatab_archive(inv_fp, target_filename=None, filter_by_measurement=None):
    """Function to create an ISArchive; option to select by assay measurement type

    Example usage:

        >>> create_isatab_archive(open('/path/to/i_investigation.txt', target_filename='isatab.zip')
        >>> create_isatab_archive(open('/path/to/i.txt', filter_by_measurement='transcription profiling')
    """
    if target_filename is None:
        target_filename = os.path.join(os.path.dirname(inv_fp.name), "isatab.zip")
    ISA = isatab.load(inv_fp)
    all_files_in_isatab = []
    found_files = []
    for s in ISA.studies:
        if filter_by_measurement is not None:
            log.debug("Selecting ", filter_by_measurement)
            selected_assays = [a for a in s.assays if a.measurement_type.term == filter_by_measurement]
        else:
            selected_assays = s.assays
        for a in selected_assays:
            all_files_in_isatab += [d.filename for d in a.data_files]
    dirname = os.path.dirname(inv_fp.name)
    for fname in all_files_in_isatab:
        if os.path.isfile(os.path.join(dirname, fname)):
            found_files.append(fname)
    missing_files = [f for f in all_files_in_isatab if f not in found_files]
    if len(missing_files) == 0:
        log.debug("Do zip")
        with ZipFile(target_filename, mode='w') as zip_file:
            # use relative dir_name to avoid absolute path on file names
            zip_file.write(inv_fp.name, arcname=os.path.basename(inv_fp.name))
            for s in ISA.studies:
                zip_file.write(os.path.join(dirname, s.filename), arcname=s.filename)
                for a in selected_assays:
                    zip_file.write(os.path.join(dirname, a.filename), arcname=a.filename)
            for file in all_files_in_isatab:
                zip_file.write(os.path.join(dirname, file), arcname=file)
            log.debug(zip_file.namelist())
            return zip_file.namelist()
    else:
        log.debug("Not zipping")
        log.debug("Missing: ", missing_files)
        return None


def squashstr(string):
    nospaces = "".join(string.split())
    return nospaces.lower()


def pyvar(string):
    for ch in string:
        if ch.isalpha() or ch.isdigit():
            pass
        else:
            string = string.replace(ch, '_')
    return string


def recast_columns(columns):
    casting_map = {
        'Material Type': 'Characteristics[Material Type]',
        'Date': 'Parameter Value[Date]',
        'Performer': 'Parameter Value[Performer]'
    }
    for k, v in casting_map.items():
        columns = list(map(lambda x: v if x == k else x, columns))
    return columns


def pyisatabify(dataframe):
    columns = dataframe.columns
    pycolumns = []
    nodecontext = None
    attrcontext = None
    col2pymap = {}
    columns = recast_columns(columns=columns)
    for column in columns:
        squashedcol = squashstr(column)
        if squashedcol.endswith(('name', 'file')) or squashedcol == 'protocolref':
            nodecontext = squashedcol
            pycolumns.append(squashedcol)
        elif squashedcol.startswith(('characteristics', 'parametervalue', 'comment', 'factorvalue')) and nodecontext is not None:
            attrcontext = squashedcol
            if attrcontext == 'factorvalue':  # factor values are not in node context
                pycolumns.append(pyvar(attrcontext))
            else:
                pycolumns.append('{0}__{1}'.format(nodecontext, pyvar(attrcontext)))
        elif squashedcol.startswith(('term', 'unit')) and nodecontext is not None and attrcontext is not None:
            pycolumns.append('{0}__{1}_{2}'.format(nodecontext, pyvar(attrcontext), pyvar(squashedcol)))
        col2pymap[column] = pycolumns[-1]
    return col2pymap


def factor_query_isatab(df, q):
    """
    :param df: A Pandas DataFrame
    :param q: Query, like "rate is 0.2 and limiting nutrient is sulphur"
    :return: DataFrame sliced on the query
    """
    columns = df.columns
    columns = recast_columns(columns=columns)
    for i, column in enumerate(columns):
        columns[i] = pyvar(column) if column.startswith('Factor Value[') else column
    df.columns = columns

    qlist = q.split(' and ')
    fmt_query = []
    for factor_query in qlist:
        factor_value = factor_query.split(' == ')
        fmt_query_part = "Factor_Value_{0}_ == '{1}'".format(pyvar(factor_value[0]), factor_value[1])
        fmt_query.append(fmt_query_part)
    fmt_query = ' and '.join(fmt_query)
    log.debug('running query: {}'.format(fmt_query))
    return df.query(fmt_query)


def compute_factor_values_summary(df):
    # get all factors combinations
    factor_columns = [x for x in df.columns if x.startswith("Factor Value")]
    if len(factor_columns) > 0:  # add branch to get all if no FVs
        study_group_factors_df = df[factor_columns].drop_duplicates()
        factors_list = [x[13:-1] for x in study_group_factors_df.columns]
        queries = []
        factors_and_levels = {}
        for i, row in study_group_factors_df.iterrows():
            fvs = []
            for x, y in zip(factors_list, row):
                fvs.append(' == '.join([x, str(y)]))
                try:
                    factor_and_levels = factors_and_levels[x]
                except KeyError:
                    factors_and_levels[x] = set()
                    factor_and_levels = factors_and_levels[x]
                factor_and_levels.add(str(y))
            queries.append(' and '.join(fvs))
        groups_and_samples = []
        print("Calculated {} study groups".format(len(queries)))
        for k, v in factors_and_levels.items():
            print("factor: {0} | levels={1} | {2}".format(k, len(v), tuple(v)))
        for query in queries:
            try:
                df2 = factor_query_isatab(df, query)
                data_column = [x for x in df.columns if x.startswith(('Raw', 'Array', 'Free Induction Decay'))
                               and x.endswith('Data File')][0]
                groups_and_samples.append(
                    (query,
                     'sources = {}'.format(len(list(df2['Source Name'].drop_duplicates()))),
                     'samples = {}'.format(len(list(df2['Sample Name'].drop_duplicates()))),
                     'raw files = {}'.format(len(list(df2[data_column].drop_duplicates()))))
                    )
            except Exception as e:
                print("error in query, {}".format(e))
        for gs in groups_and_samples:
            print(gs)


def check_loadable(tab_dir_root):
    for mtbls_dir in [x for x in os.listdir(tab_dir_root) if x.startswith("MTBLS")]:
        try:
            isatab.load(os.path.join(tab_dir_root, mtbls_dir))
            print("{} load OK".format(mtbls_dir))
        except Exception as e:
            print("{0} load FAIL, reason: {1}".format(mtbls_dir, e))


def compute_study_factors_on_mtbls(tab_dir_root):
    """
    Produces study factors report like:

    [
        {
            "assays": [
                {
                    "assay_key": "a_mtbls1_metabolite_profiling_NMR_spectroscopy.txt/metabolite profiling/NMR spectroscopy/Bruker",
                    "factors_and_levels": [
                        {
                            "factor": "Metabolic syndrome",
                            "num_levels": 2
                        },
                        {
                            "factor": "Gender",
                            "num_levels": 2
                        }
                    ],
                    "group_summary": [
                        {
                            "raw_files": 22,
                            "samples": 22,
                            "sources": 1,
                            "study_group": "Gender == Male and Metabolic syndrome == diabetes mellitus"
                        },
                        {
                            "raw_files": 26,
                            "samples": 26,
                            "sources": 1,
                            "study_group": "Gender == Female and Metabolic syndrome == diabetes mellitus"
                        },
                        {
                            "raw_files": 56,
                            "samples": 56,
                            "sources": 1,
                            "study_group": "Gender == Male and Metabolic syndrome == Control Group"
                        },
                        {
                            "raw_files": 28,
                            "samples": 28,
                            "sources": 1,
                            "study_group": "Gender == Female and Metabolic syndrome == Control Group"
                        }
                    ],
                    "num_samples": 132,
                    "num_sources": 132,
                    "total_study_groups": 4
                }
            ],
            "study_key": "MTBLS1",
            "total_samples": 132,
            "total_sources": 1
        }
    ]

    :param tab_dir_root: Directory containing MTBLS prefixed ISA-Tab directories
    :return: None, output writes to stdout

    Usage:
        >>> compute_study_factors_on_mtbls('tests/data')
        # if tests/data contains tests/data/MTBLS1, tests/data/MTBLS2 etc.

        To write to an output file:
        >>> import sys
        >>> stdout_console = sys.stdout  # save normal stdout
        >>> sys.stdout = open('out.txt')  # set to file
        >>> compute_study_factors_on_mtbls('tests/data')
        >>> sys.stdout = stdout_console  # reset stdout
    """
    for mtbls_dir in [x for x in os.listdir(tab_dir_root) if x.startswith("MTBLS")]:
        study_dir = os.path.join(tab_dir_root, mtbls_dir)
        analyzer = IsaTabAnalyzer(study_dir)
        try:
            analyzer.pprint_study_design_report()
        except ValueError:
            pass


class IsaTabAnalyzer(object):

    def __init__(self, path):
        self.path = path

    def generate_study_design_report(self, get_num_study_groups=True, get_factors=True, get_num_levels=True,
                                     get_levels=True, get_study_groups=True):
        isa = isatab.load(self.path, skip_load_tables=False)
        study_design_report = []
        raw_data_file_prefix = ('Raw', 'Array', 'Free Induction Decay')
        for study in isa.studies:
            study_key = study.identifier if study.identifier != '' else study.filename
            study_design_report.append({
                'study_key': study_key,
                'total_sources': len(study.materials['sources']),
                'total_samples': len(study.materials['samples']),
                'assays': []
            })
            with open(os.path.join(self.path, study.filename)) as s_fp:
                s_df = isatab.load_table(s_fp)
                for assay in study.assays:
                    assay_key = '/'.join([assay.filename, assay.measurement_type.term, assay.technology_type.term,
                                           assay.technology_platform])
                    assay_report = {
                        'assay_key': assay_key,
                        'num_sources': len(assay.materials['samples']),
                        'num_samples': len([x for x in assay.data_files
                                              if x.label.startswith(raw_data_file_prefix)])
                    }
                    with open(os.path.join(self.path, assay.filename)) as a_fp:
                        a_df = isatab.load_table(a_fp)
                        merged_df = pd.merge(s_df, a_df, on='Sample Name')
                        factor_cols = [x for x in merged_df.columns if x.startswith("Factor Value")]
                        if len(factor_cols) > 0:  # add branch to get all if no FVs
                            study_group_factors_df = merged_df[factor_cols].drop_duplicates()
                            factors_list = [x[13:-1] for x in study_group_factors_df.columns]
                            queries = []
                            factors_and_levels = {}
                            for i, row in study_group_factors_df.iterrows():
                                fvs = []
                                for x, y in zip(factors_list, row):
                                    fvs.append(' == '.join([x, str(y)]))
                                    try:
                                        factor_and_levels = factors_and_levels[x]
                                    except KeyError:
                                        factors_and_levels[x] = set()
                                        factor_and_levels = factors_and_levels[x]
                                    factor_and_levels.add(str(y))
                                queries.append(' and '.join(fvs))
                            assay_report['total_study_groups'] = len(queries)
                            assay_report['factors_and_levels'] = []
                            assay_report['group_summary'] = []
                            for k, v in factors_and_levels.items():
                                assay_report['factors_and_levels'].append({
                                    'factor': k,
                                    'num_levels': len(v),
                                })
                            for query in queries:
                                try:
                                    columns = merged_df.columns
                                    columns = recast_columns(columns=columns)
                                    for i, column in enumerate(columns):
                                        columns[i] = pyvar(column) if column.startswith('Factor Value[') else column
                                    merged_df.columns = columns
                                    qlist = query.split(' and ')
                                    fmt_query = []
                                    for factor_query in qlist:
                                        factor_value = factor_query.split(' == ')
                                        fmt_query_part = "Factor_Value_{0}_ == '{1}'".format(pyvar(factor_value[0]),
                                                                                             factor_value[1])
                                        fmt_query.append(fmt_query_part)
                                    fmt_query = ' and '.join(fmt_query)
                                    log.debug('running query: {}'.format(fmt_query))
                                    df2 = merged_df.query(fmt_query)
                                    data_column = [x for x in merged_df.columns if x.startswith(raw_data_file_prefix)
                                                   and x.endswith('Data File')][0]
                                    assay_report['group_summary'].append(
                                        dict(study_group=query,
                                             sources=len(list(df2['Source Name'].drop_duplicates())),
                                             samples=len(list(df2['Sample Name'].drop_duplicates())),
                                             raw_files=len(list(df2[data_column].drop_duplicates()))
                                        ))
                                except Exception as e:
                                    print("error in query, {}".format(e))
                    study_design_report[-1]['assays'].append(assay_report)
        return study_design_report

    def pprint_study_design_report(self):
        print(json.dumps(self.generate_study_design_report(), indent=4, sort_keys=True))
