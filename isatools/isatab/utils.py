from __future__ import annotations

from io import StringIO
from bisect import bisect_left, bisect_right
from itertools import tee
from math import isnan
from csv import reader as csv_reader
from json import loads
from pandas import DataFrame, Series

from isatools.constants import (
    SYNONYMS,
    ALL_LABELS,
    _LABELS_DATA_NODES,
    _LABELS_ASSAY_NODES,
    _LABELS_MATERIAL_NODES
)

from isatools.utils import utf8_text_file_open
from isatools.isatab.defaults import (
    log,
    _RX_CHARACTERISTICS,
    _RX_PARAMETER_VALUE,
    _RX_FACTOR_VALUE,
    _RX_COMMENT,
    defaults
)
from isatools.model import OntologyAnnotation


class IsaTabSeries(Series):
    """A wrapper for Pandas Series to use in IsaTabDataFrame"""

    @property
    def _constructor(self):
        return IsaTabSeries


class IsaTabDataFrame(DataFrame):
    """The IsaTabDataFrame is used to allow access to the cleaned-up ISA-Tab
    header as Pandas does not allow duplicate labels in the header but ISA-Tab
    needs them
    """

    def __init__(self, *args, **kw):
        super(IsaTabDataFrame, self).__init__(*args, **kw)

    @property
    def _constructor(self):
        return IsaTabDataFrame

    _constructor_sliced = IsaTabSeries

    @staticmethod
    def _clean_label(label):
        """Clean up a column header label

        :param label: A string corresponding to a column header
        :return: A cleaned up ISA-Tab header label
        """
        for clean_label in ALL_LABELS:
            if clean_label.lower() in label.strip().lower():
                return clean_label
            elif _RX_CHARACTERISTICS.match(label):
                return 'Characteristics[{val}]'.format(val=next(iter(_RX_CHARACTERISTICS.findall(label))))
            elif _RX_PARAMETER_VALUE.match(label):
                return 'Parameter Value[{val}]'.format(val=next(iter(_RX_PARAMETER_VALUE.findall(label))))
            elif _RX_FACTOR_VALUE.match(label):
                return 'Factor Value[{val}]'.format(val=next(iter(_RX_FACTOR_VALUE.findall(label))))
            elif _RX_COMMENT.match(label):
                return 'Comment[{val}]'.format(val=next(iter(_RX_COMMENT.findall(label))))

    @property
    def isatab_header(self):
        """Get the ISA-Tab header

        :return: A list of cleaned-up column headings
        """
        return list(map(lambda x: self._clean_label(x), self.columns))


class TransposedTabParser(object):
    """Parser for transposed tables, such as the ISA-Tab investigation table,
    or the MAGE-TAB IDF table. The headings are in column 0 with values,
    perhaps multiple, reading in columns towards the right. These tables do
    not necessarily have an even shape (row lengths may differ).

    This reads the transposed table into a dictionary where key is heading and
    value is a list of cell values for the heading. No relations between
    headings is assumed and the order of values is implied by the order of the
    cell value lists.

    Does not allow duplicate labels.
    """

    def __init__(self, tab_options=None, show_progressbar=None, log_level=None):
        if tab_options is None:
            self.tab_options = defaults.tab_options
        else:
            self.tab_options = tab_options
        if show_progressbar is None:
            self.show_progressbar = defaults.show_progressbar
        else:
            self.show_progressbar = show_progressbar
        if log_level is None:
            self.log_level = defaults.log_level
        else:
            if not isinstance(tab_options, dict):
                raise TypeError('tab_options must be dict, not {}'.format(type(tab_options)))
            self.log_level = log_level

        self._ttable_dict = dict(header=list(), table=dict())

    def parse(self, filename):
        """Parse a transposed table into a dictionary for further processing
        downstream

        :param filename: Path to a table file to parse
        :return: A dictionary with the table contents indexed with keys
        corresponding to the column headers
        """
        try:
            with utf8_text_file_open(filename) as unicode_file:
                ttable_reader = csv_reader(filter(lambda r: r[0] != '#', unicode_file), dialect='excel-tab')
                for row in ttable_reader:
                    if len(row) > 0:
                        key = get_squashed(key=row[0])
                        self._ttable_dict['header'].append(key)
                        self._ttable_dict['table'][key] = row[1:]
        except UnicodeDecodeError:
            with open(filename, encoding='ISO8859-2') as latin2_file:
                ttable_reader = csv_reader(filter(lambda r: r[0] != '#', latin2_file), dialect='excel-tab')
                for row in ttable_reader:
                    if len(row) > 0:
                        key = get_squashed(key=row[0])
                        self._ttable_dict['header'].append(key)
                        self._ttable_dict['table'][key] = row[1:]

        return self._ttable_dict


def strip_comments(in_fp):
    """Strip out comment lines indicated by a # at start of line from a given
    file

    :param in_fp: A file-like buffer object
    :return: A memory file buffer object with comments stripped out
    """
    out_fp = StringIO()
    if not isinstance(in_fp, StringIO):
        out_fp.name = in_fp.name
    for line in in_fp.readlines():
        log.debug('processing line: {}'.format(line))
        if line.lstrip().startswith('#'):
            log.debug('stripping line:'.format(line))
        elif len(line.strip()) > 0:
            out_fp.write(line)
    out_fp.seek(0)
    return out_fp


def process_keygen(protocol_ref, column_group, object_label_index, all_columns, series, series_index, DF):
    """Generate the process key.

    This works by trying to find the relevant Name column, if available, that
    the data indicates the disambiguation.

    If not available, we look at the Parameter Values and use their uniqueness
    to disambiguate the Processes.

    If PVs not available we look at the left-most inputs or right-most outputs
    to use as the disambiguation.

    :param protocol_ref: The Protocol REF value
    :param column_group: List of column headers for the object in context, e.g.
    [Sample Name, Characteristics[Material Type], Comment[My Comment]]
    :param object_label_index: Index of the main object label, e.g. Sample Name
    :param all_columns: List of all column headers
    :param series: A DataFrame Series object of the row we are processing
    :param series_index: Row index of the Series
    :param DF: The whole table's DataFrame
    :return: The process key to disambiguate Processes
    """
    name_column_hits = [n for n in column_group if n in _LABELS_ASSAY_NODES]
    if len(name_column_hits) == 1:
        return series[name_column_hits[0]]

    process_key = protocol_ref
    node_cols = [i for i, c in enumerate(all_columns) if c in _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES]
    input_node_value = ''
    output_node_value = ''
    output_node_index = find_gt(node_cols, object_label_index)
    if output_node_index > -1:
        output_node_label = all_columns[output_node_index]
        output_node_value = str(series[output_node_label])

    input_node_index = find_lt(node_cols, object_label_index)
    if input_node_index > -1:
        input_node_label = all_columns[input_node_index]
        input_node_value = str(series[input_node_label])

    input_nodes_with_prot_keys = DF[[all_columns[object_label_index], all_columns[input_node_index]]].drop_duplicates()
    output_nodes_with_prot_keys = DF[[all_columns[object_label_index],
                                      all_columns[output_node_index]]].drop_duplicates()

    if len(input_nodes_with_prot_keys) > len(output_nodes_with_prot_keys):
        node_key = output_node_value
    else:
        node_key = input_node_value

    if process_key == protocol_ref:
        process_key += '-' + str(series_index)

    pv_cols = [c for c in column_group if c.startswith('Parameter Value[')]
    if len(pv_cols) > 0:
        # 2. else try use protocol REF + Parameter Values as key
        if node_key is not None:
            process_key = node_key + ':' + protocol_ref + ':' + '/'.join([str(v) for v in series[pv_cols]])
        else:
            process_key = protocol_ref + ':' + '/'.join([str(v) for v in series[pv_cols]])
    else:
        # 3. else try use input + protocol REF as key
        # 4. else try use output + protocol REF as key
        if node_key is not None:
            process_key = node_key + '/' + protocol_ref

    date_col_hits = [c for c in column_group if c.startswith('Date')]
    if len(date_col_hits) == 1:
        process_key = ':'.join([process_key, series[date_col_hits[0]]])

    performer_col_hits = [c for c in column_group if c.startswith('Performer')]
    if len(performer_col_hits) == 1:
        process_key = ':'.join([process_key, series[performer_col_hits[0]]])

    return process_key


def find_gt(a, x):
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    return -1


def find_lt(a, x):
    i = bisect_left(a, x)
    if i:
        return a[i - 1]
    return -1


def pairwise(iterable):
    """A lovely pairwise iterator, e.g.

    [a, b, c, d] -> [(a, b), (b, c), (c, d)]

    :param iterable: A Python iterable
    :return: A pairwise generator
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def cell_has_value(cell):
    """Checks if a cell has any value. This is because Pandas DataFrames
    sometimes renders empty cells with default null values such as 'Unnamed: '
    or other strings

    :param cell: A value of a give cell
    :return: True if it has a value, False if it does not
    """
    if isinstance(cell, float):
        if isnan(cell):
            return True
        return False
    else:
        if cell.strip() == '':
            return False
        elif 'Unnamed: ' in cell:
            return False
        return True


def get_num_study_groups(study_sample_table, study_filename):
    """Gets the number of study groups based on Factor Value combinations
    found in the study-sample table

    :param study_sample_table: The study-sample table as a DataFrame
    :param study_filename: The filename of the file
    :return: The computed number of study groups
    """
    num_study_groups = -1
    factor_columns = [x for x in study_sample_table.columns if x.startswith('Factor Value')]
    if factor_columns:
        num_study_groups = len(study_sample_table[factor_columns].drop_duplicates())
    else:
        log.debug("No study factors found in {}".format(study_filename))
    return num_study_groups


def squashstr(string):
    """Squashes a string by removing the spaces and lowering it"""

    nospaces = "".join(string.split())
    return nospaces.lower()


def get_squashed(key):
    """Squashes an ISA-Tab header string for use as key elsewhere"""
    try:
        if '[' in key and ']' in key:
            return squashstr(key[0:key.index('[')]) + key[key.index('['):]
        else:
            return squashstr(key)
    except ValueError:
        return squashstr(key)


def set_defaults(show_progressbar=None, log_level=None):
    """Set the default ISA-Tab options

    :param show_progressbar: Boolean flag on whether to show progressbar in
    standard outputs
    :param log_level: Logging level (INFO, WARN, DEBUG) as standard Python
    logging levels.
    :return: None
    """
    defaults.set_defaults(show_progressbar, log_level)


def set_tab_option(optname, optvalue):
    """Set the default value for one of the options that gets passed into the
    IsaTabParser or IsaTabWriter constructor.

    :param optname: Option name as a string
    :param optvalue:  Option value
    :return: None
    """
    defaults.tab_options[optname] = optvalue


def get_characteristic_columns(label, c):
    """Generates Characteristics columns for a given material

    :param label: Header label needed for the material type,
    e.g. "Extract Name"
    :param c: The Characteristic object of interest
    :return: List of column labels
    """

    columns = []
    if not c or not c.category:
        return columns
    if isinstance(c.category.term, str):
        if c.category.term.startswith("{", ):
            c_as_json = loads(c.category.term)
            if "annotationValue" in c_as_json.keys():
                columns = ["{0}.Characteristics[{1}]".format(label, c_as_json["annotationValue"])]
                columns.extend(get_value_columns(columns[0], c))
    if isinstance(c.category.term, dict):
        columns = ["{0}.Characteristics[{1}]".format(label, c.category.term["annotationValue"])]
        columns.extend(get_value_columns(columns[0], c))
    else:
        columns = ["{0}.Characteristics[{1}]".format(label, c.category.term)]
        columns.extend(get_value_columns(columns[0], c))

    return columns


def get_comment_column(label, c):
    """Generates Comment columns for a given object

    :param label: Header label needed for the object
    :param c: The object of interest
    :return: List of column labels
    """
    columns = ["{0}.Comment[{1}]".format(label, c.name)]
    return columns


def get_pv_columns(label, pv):
    """Generates Parameter Value columns for a given process

    :param label: Header label needed for the process
    :param pv: The Parameter Value object of interest
    :return: List of column labels
    """
    columns = None
    try:
        if pv.category is not None:
            columns = ["{0}.Parameter Value[{1}]".format(label, pv.category.parameter_name.term)]
            # print(columns)
        else:
            raise ValueError
    except AttributeError:
        log.fatal(label, pv)
    if columns is not None:
        columns.extend(get_value_columns(columns[0], pv))
    return columns


def get_ontology_source_refs(i_df):
    """Gets the Term Source REFs of the declared Ontology Sources

    :param i_df: An investigation DataFrame
    :return: None
    """
    return i_df['ontology_sources']['Term Source Name'].tolist()


def convert_to_number(value: str) -> int | float | None:
    """Convert a value the type of which is a string to an integer or a flaot

    :param value:
    :return: an int or a float or None or an error
    """
    try:
        # Try converting to integer first
        return int(value)
    except ValueError:
        try:
            # If that fails, try converting to float
            return float(value)
        except ValueError:
            return


def get_value(object_column, column_group, object_series, ontology_source_map, unit_categories):
    """Gets the appropriate value for a give column group

    :param object_column: The object's column header name, e.g. Sample Name
    :param column_group: The column group that includes the object's qualifiers
    :param object_series: Pandas DataFrame Series for the row
    :param ontology_source_map: A mapping to the OntologySource objects
    created after parsing the investigation file
    :param unit_categories: A map of unit categories to reference
    :return: The appropriate value and unit according to the columns parsed,
    e.g. (str, None) (float, Unit), (OntologyAnnotation, None)
    """
    cell_value = object_series[object_column]

    if cell_value == '':
        return cell_value, None

    column_index = list(column_group).index(object_column)

    try:
        offset_1r_col = column_group[column_index + 1]
        offset_2r_col = column_group[column_index + 2]
    except IndexError:
        return cell_value, None

    if offset_1r_col.startswith('Term Source REF') and offset_2r_col.startswith('Term Accession Number'):
        value = OntologyAnnotation(term=str(cell_value))
        term_source_value = object_series[offset_1r_col]
        if term_source_value != '':
            try:
                value.term_source = ontology_source_map[term_source_value]
            except KeyError:
                log.debug('term source: ', term_source_value, ' not found')
        term_accession_value = object_series[offset_2r_col]
        if term_accession_value != '':
            value.term_accession = str(term_accession_value)
        return value, None

    try:
        offset_3r_col = column_group[column_index + 3]
    except IndexError:
        return cell_value, None

    if offset_1r_col.startswith('Unit') \
            and offset_2r_col.startswith('Term Source REF') \
            and offset_3r_col.startswith('Term Accession Number'):
        category_key = object_series[offset_1r_col]
        try:
            unit_term_value = unit_categories[category_key]
        except KeyError:
            unit_term_value = OntologyAnnotation(term=category_key)
            unit_categories[category_key] = unit_term_value
            unit_term_source_value = object_series[offset_2r_col]
            if unit_term_source_value != '':
                try:
                    unit_term_value.term_source = ontology_source_map[unit_term_source_value]
                except KeyError:
                    log.debug('term source: ', unit_term_source_value, ' not found')
            term_accession_value = object_series[offset_3r_col]
            if term_accession_value != '':
                unit_term_value.term_accession = term_accession_value
        return convert_to_number(cell_value), unit_term_value
    return cell_value, None


def get_object_column_map(isatab_header, df_columns):
    """Builds a mapping of headers to objects

    :param isatab_header: The list of ISA-Tab column names
    :param df_columns: The list of columns from the DataFrame
    :return: A list of column groups (also lists) splitting the header
    according to object type
    """
    labels = _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES
    if set(isatab_header) == set(df_columns):
        object_index = [i for i, x in enumerate(df_columns) if x in labels or 'Protocol REF' in x or ' File' in x]
    else:
        object_index = [i for i, x in enumerate(isatab_header) if x in labels + ['Protocol REF']]

    # group headers regarding objects delimited by object_index by slicing up the header list
    object_column_map = []
    prev_i = object_index[0]
    for curr_i in object_index:  # collect each object's columns
        if prev_i == curr_i:
            pass  # skip if there's no diff, i.e. first one
        else:
            object_column_map.append(df_columns[prev_i:curr_i])
        prev_i = curr_i

    # finally, collect last object's columns
    object_column_map.append(df_columns[prev_i:])
    return object_column_map


def get_value_columns(label, x):
    """ Generates the appropriate columns based on the value of the object.
    For example, if the object's .value value is an OntologyAnnotation,
    the ISA-Tab requires extra columns Term Source REF and
    Term Accession Number

    :param label: Header label needed for the object type, e.g. "Sample Name"
    :param x: The object of interest, e.g. a Sample() object
    :return: List of column labels, e.g. ["Sample Name.Term Source REF",
    "Sample Name.Term Accession Number"]
    """
    if isinstance(x.value, (int, float)) and x.unit:
        if isinstance(x.unit, OntologyAnnotation):
            labels = ["Unit", "Unit.Term Source REF", "Unit.Term Accession Number"]
            return map(lambda x: "{0}.{1}".format(label, x), labels)
        return ["{0}.Unit".format(label)]
    elif isinstance(x.value, OntologyAnnotation):
        return map(lambda y: "{0}.{1}".format(label, y), ["Term Source REF", "Term Accession Number"])
    return []


def get_fv_columns(label, fv):
    """Generates Factor Value columns for a given material

    :param fv: The Factor Value object of interest
    :param label: Header label needed for the material type,
    e.g. "Sample Name"
    :return: List of column labels
    """
    columns = ["{0}.Factor Value[{1}]".format(label, fv.factor_name.name)]
    columns.extend(get_value_columns(columns[0], fv))
    return columns
