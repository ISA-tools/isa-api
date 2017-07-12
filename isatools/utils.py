from isatools.model.v1 import Publication, Comment, OntologySource, OntologyAnnotation
from Bio import Entrez, Medline
from isatools.isatab import load_table, load
import uuid
import csv
import json
from urllib.request import urlopen
from urllib.parse import urlencode
import os
from zipfile import ZipFile
import logging
import isatools
from isatools import isatab
import pandas as pd

logging.basicConfig(level=isatools.log_level)
LOG = logging.getLogger(__name__)


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
    from isatools.model.v1 import Process
    report = list()
    for process in [n for n in G.nodes() if isinstance(n, Process)]:
        if len(G.in_edges(process)) > 1:
            LOG.info("Possible process pooling detected on: {}"
                     .format(' '.join([process.id, process.executes_protocol.name])))
            report.append(process.id)
    return report


def detect_isatab_process_pooling(fp):
    from isatools import isatab
    report = []
    ISA = isatab.load(fp)
    for study in ISA.studies:
        LOG.info("Checking {}".format(study.filename))
        pooling_list = detect_graph_process_pooling(study.graph)
        if len(pooling_list) > 0:
            report.append({
                study.filename: pooling_list
            })
        for assay in study.assays:
            LOG.info("Checking {}".format(assay.filename))
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
    df = load_table(table_fp)
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


def get_pubmed_article(pubmed_id):
    # http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc126
    response = {}
    Entrez.email = "isatools@googlegroups.com"
    handle = Entrez.efetch(db="pubmed", id=pubmed_id.strip(), rettype="medline", retmode="text")
    records = Medline.parse(handle)
    for record in records:
        response["pubmedid"] = pubmed_id
        response["title"] = record.get("TI", "")
        response["authors"] = record.get("AU", "")
        response["journal"] = record.get("TA", "")
        response["year"] = record.get("EDAT", "").split("/")[0]
        lidstring = record.get("LID", "")
        if "[doi]" in lidstring:
            response["doi"] = record.get("LID", "").split(" ")[0]
        else:
            response["doi"] = ""
        if not response["doi"]:
            aids = record.get("AID", "")
            for aid in aids:
                LOG.debug("AID:" + aid)
                if "[doi]" in aid:
                    response["doi"] = aid.split(" ")[0]
                    break
                else:
                    response["doi"] = ""

        break
    return response


def set_pubmed_article(publication):
    """
        Given a Publication object with pubmed_id set to some value, set the rest of the values from information
        collected via Entrez webservice from PubMed
    """
    if isinstance(publication, Publication):
        response = get_pubmed_article(publication.pubmed_id)
        publication.doi = response["doi"]
        publication.author_list = ", ".join(response["authors"])
        publication.title = response["title"]
        publication.comments = [Comment(name="Journal", value=response["journal"])]
    else:
        raise TypeError("Can only set PubMed details on a Publication object")


OLS_API_BASE_URI = "http://www.ebi.ac.uk/ols/api"
OLS_PAGINATION_SIZE = 500


def get_ols_ontologies():
    """Returns a list of OntologySource objects according to what's in OLS"""
    ontologiesUri = OLS_API_BASE_URI + "/ontologies?size=" + str(OLS_PAGINATION_SIZE)
    LOG.debug(ontologiesUri)
    J = json.loads(urlopen(ontologiesUri).read().decode("utf-8"))
    ontology_sources = []
    for ontology_source_json in J["_embedded"]["ontologies"]:
        ontology_sources.append(OntologySource(
            name=ontology_source_json["ontologyId"],
            version=ontology_source_json["config"]["version"],
            description=ontology_source_json["config"]["title"],

            file=ontology_source_json["config"]["versionIri"]
        ))
    return ontology_sources


def get_ols_ontology(ontology_name):
    """Returns a single OntologySource objects according to what's in OLS"""
    ontologiesUri = OLS_API_BASE_URI + "/ontologies?size=" + str(OLS_PAGINATION_SIZE)
    LOG.debug(ontologiesUri)
    J = json.loads(urlopen(ontologiesUri).read().decode("utf-8"))
    ontology_sources = []
    for ontology_source_json in J["_embedded"]["ontologies"]:
        ontology_sources.append(OntologySource(
            name=ontology_source_json["ontologyId"],
            version=ontology_source_json["config"]["version"],
            description=ontology_source_json["config"]["title"],

            file=ontology_source_json["config"]["versionIri"]
        ))
    hits = [o for o in ontology_sources if o.name == ontology_name]
    if len(hits) == 1:
        return hits[0]
    else:
        return None


def search_ols(term, ontology_source):
    """Returns a list of OntologyAnnotation objects according to what's returned by OLS search"""
    url = OLS_API_BASE_URI + "/search"
    queryObj = {
        "q": term,
        "rows": OLS_PAGINATION_SIZE,
        "start": 0,
        "ontology": ontology_source.name if isinstance(ontology_source, OntologySource) else ontology_source
    }
    query_string = urlencode(queryObj)
    url += '?q=' + query_string
    LOG.debug(url)
    J = json.loads(urlopen(url).read().decode("utf-8"))
    ontology_annotations = []
    for search_result_json in J["response"]["docs"]:
        ontology_annotations.append(
            OntologyAnnotation(
                term=search_result_json["label"],
                term_accession=search_result_json["iri"],
                term_source=ontology_source if isinstance(ontology_source, OntologySource) else None
            ))
    return ontology_annotations


def create_isatab_archive(inv_fp, target_filename=None, filter_by_measurement=None):
    """Function to create an ISArchive; option to select by assay measurement type

    Example usage:

        >>> create_isatab_archive(open('/path/to/i_investigation.txt', target_filename='isatab.zip')
        >>> create_isatab_archive(open('/path/to/i.txt', filter_by_measurement='transcription profiling')
    """
    if target_filename is None:
        target_filename = os.path.join(os.path.dirname(inv_fp.name), "isatab.zip")
    ISA = load(inv_fp)
    all_files_in_isatab = []
    found_files = []
    for s in ISA.studies:
        if filter_by_measurement is not None:
            LOG.debug("Selecting ", filter_by_measurement)
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
        LOG.debug("Do zip")
        with ZipFile(target_filename, mode='w') as zip_file:
            # use relative dir_name to avoid absolute path on file names
            zip_file.write(inv_fp.name, arcname=os.path.basename(inv_fp.name))
            for s in ISA.studies:
                zip_file.write(os.path.join(dirname, s.filename), arcname=s.filename)
                for a in selected_assays:
                    zip_file.write(os.path.join(dirname, a.filename), arcname=a.filename)
            for file in all_files_in_isatab:
                zip_file.write(os.path.join(dirname, file), arcname=file)
            LOG.debug(zip_file.namelist())
            return zip_file.namelist()
    else:
        LOG.debug("Not zipping")
        LOG.debug("Missing: ", missing_files)
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
    LOG.debug('running query: {}'.format(fmt_query))
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

    MTBLS1 load OK
    Study sample level: total sources = 1, total samples = 132
    Assay level: total samples = 132, total raw data = 132
    Calculated 4 study groups
    factor: Gender | levels=2 | ('Female', 'Male')
    factor: Metabolic syndrome | levels=2 | ('diabetes mellitus', 'Control Group')
    ('Gender == Male and Metabolic syndrome == diabetes mellitus', 'sources = 1', 'samples = 22', 'raw files = 22')
    ('Gender == Female and Metabolic syndrome == diabetes mellitus', 'sources = 1', 'samples = 26', 'raw files = 26')
    ('Gender == Male and Metabolic syndrome == Control Group', 'sources = 1', 'samples = 56', 'raw files = 56')
    ('Gender == Female and Metabolic syndrome == Control Group', 'sources = 1', 'samples = 28', 'raw files = 28')

    :param tab_dir_root: Directory containing MTBLS ISA-Tab directories
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
        ISA = None
        study_dir = os.path.join(tab_dir_root, mtbls_dir)
        try:
            ISA = isatab.load(study_dir, skip_load_tables=False)
            print("{} load OK".format(mtbls_dir))
        except Exception as e:
            print("{0} load FAIL, reason: {1}".format(mtbls_dir, e))
        if ISA is None:
            continue
        for S in ISA.studies:
            print('Study sample level: total sources = {0}, total samples = {1}'.format(
                len(S.materials['sources']), len(S.materials['samples'])))
            with open(os.path.join(study_dir, S.filename)) as s_fp:
                s_df = isatab.load_table(s_fp)
                for A in S.assays:
                    print('Assay level: total samples = {0}, total raw data = {1}'.format(
                        len(A.materials['samples']),
                        len([x for x in A.data_files if x.label.startswith(('Raw', 'Array', 'Free Induction Decay'))])))
                    with open(os.path.join(study_dir, A.filename)) as a_fp:
                        a_df = isatab.load_table(a_fp)
                        sa_df = pd.merge(s_df, a_df, on='Sample Name')
                        compute_factor_values_summary(sa_df)
