from io import StringIO

from pandas import read_csv
from numpy import nan

from isatools.utils import utf8_text_file_open
from isatools.isatab.defaults import log
from isatools.isatab.utils import strip_comments, IsaTabDataFrame


def read_investigation_file(fp):
    """Reads an investigation file into a dictionary of DataFrames, each
    DataFrame being each section of the investigation file. e.g. One DataFrame
    for the INVESTIGATION PUBLICATIONS section

    :param fp: A file-like buffer object of the investigation file
    :return: A dictionary holding a set of DataFrames for each section of the
    investigation file. See below implementation for detail
    """

    def _peek(f):
        """Peek at the next line without moving to the next line. This function
        get the position of the next line, reads the next line, then resets the
        file pointer to the original position

        :param f: A file-like buffer object
        :return: The next line past the current line
        """
        position = f.tell()
        line = f.readline()
        f.seek(position)
        return line

    def _read_tab_section(f, sec_key, next_sec_key=None):
        """Slices a file by section delimited by section keys

        :param f: A file-like buffer object
        :param sec_key: Delimiter key of beginning of section
        :param next_sec_key: Delimiter key of end of section
        :return: A memory file of the section slice, as a string buffer object
        """
        line = f.readline()
        normed_line = line.rstrip()
        if normed_line[0] == '"':
            normed_line = normed_line[1:]
        if normed_line[len(normed_line) - 1] == '"':
            normed_line = normed_line[:len(normed_line) - 1]
        if not normed_line == sec_key:
            raise IOError("Expected: " + sec_key + " section, but got: "
                          + normed_line)
        memf = StringIO()
        while not _peek(f=f).rstrip() == next_sec_key:
            line = f.readline()
            if not line:
                break
            memf.write(line.rstrip() + '\n')
        memf.seek(0)
        return memf

    def _build_section_df(f: StringIO):
        """Reads a file section into a DataFrame

        :param f: A file-like buffer object
        :return: A DataFrame corresponding to the file section
        """
        df = read_csv(f, names=range(0, 128), sep='\t', engine='python',
                      encoding='utf-8').dropna(axis=1, how='all')
        df = df.T
        df.replace(nan, '', regex=True, inplace=True)
        #  Strip out the nan entries
        df.reset_index(inplace=True)
        #  Reset index so it is accessible as column
        df.columns = df.iloc[0]
        #  If all was OK, promote this row to the column headers
        df = df.reindex(df.index.drop(0))
        #  Reindex the DataFrame
        return df

    memory_file = StringIO()
    line = True
    while line:
        line = fp.readline()
        if not line.lstrip().startswith('#'):
            memory_file.write(line)
    memory_file.seek(0)

    df_dict = dict()

    # Read in investigation file into DataFrames first
    df_dict['ontology_sources'] = _build_section_df(_read_tab_section(
        f=memory_file,
        sec_key='ONTOLOGY SOURCE REFERENCE',
        next_sec_key='INVESTIGATION'
    ))
    df_dict['investigation'] = _build_section_df(_read_tab_section(
        f=memory_file,
        sec_key='INVESTIGATION',
        next_sec_key='INVESTIGATION PUBLICATIONS'
    ))
    df_dict['i_publications'] = _build_section_df(_read_tab_section(
        f=memory_file,
        sec_key='INVESTIGATION PUBLICATIONS',
        next_sec_key='INVESTIGATION CONTACTS'
    ))
    df_dict['i_contacts'] = _build_section_df(_read_tab_section(
        f=memory_file,
        sec_key='INVESTIGATION CONTACTS',
        next_sec_key='STUDY'
    ))
    df_dict['studies'] = list()
    df_dict['s_design_descriptors'] = list()
    df_dict['s_publications'] = list()
    df_dict['s_factors'] = list()
    df_dict['s_assays'] = list()
    df_dict['s_protocols'] = list()
    df_dict['s_contacts'] = list()
    while _peek(memory_file):  # Iterate through STUDY blocks until end of file
        df_dict['studies'].append(_build_section_df(_read_tab_section(
            f=memory_file,
            sec_key='STUDY',
            next_sec_key='STUDY DESIGN DESCRIPTORS'
        )))
        df_dict['s_design_descriptors'].append(
            _build_section_df(_read_tab_section(
                f=memory_file,
                sec_key='STUDY DESIGN DESCRIPTORS',
                next_sec_key='STUDY PUBLICATIONS'
            )))
        df_dict['s_publications'].append(_build_section_df(_read_tab_section(
            f=memory_file,
            sec_key='STUDY PUBLICATIONS',
            next_sec_key='STUDY FACTORS'
        )))
        df_dict['s_factors'].append(_build_section_df(_read_tab_section(
            f=memory_file,
            sec_key='STUDY FACTORS',
            next_sec_key='STUDY ASSAYS'
        )))
        df_dict['s_assays'].append(_build_section_df(_read_tab_section(
            f=memory_file,
            sec_key='STUDY ASSAYS',
            next_sec_key='STUDY PROTOCOLS'
        )))
        df_dict['s_protocols'].append(_build_section_df(_read_tab_section(
            f=memory_file,
            sec_key='STUDY PROTOCOLS',
            next_sec_key='STUDY CONTACTS'
        )))
        df_dict['s_contacts'].append(_build_section_df(_read_tab_section(
            f=memory_file,
            sec_key='STUDY CONTACTS',
            next_sec_key='STUDY'
        )))
    return df_dict


def read_tfile(tfile_path, index_col=None, factor_filter=None) -> IsaTabDataFrame:
    """Read a table file into a DataFrame

    :param tfile_path: Path to a table file to load
    :param index_col: The column to use as index
    :param factor_filter: Factor filter tuple, e.g. ('Gender', 'Male') will
    filter on FactorValue[Gender] == Male
    :return: A table file DataFrame
    """
    log.debug("Opening %s", tfile_path)
    with utf8_text_file_open(tfile_path) as tfile_fp:
        log.debug("Reading file header")
        tfile_fp.seek(0)
        log.debug("Reading file into DataFrame")
        tfile_fp = strip_comments(tfile_fp)
        tfile_df = IsaTabDataFrame(
            read_csv(tfile_fp, dtype=str, sep='\t', index_col=index_col,
                     memory_map=True, encoding='utf-8').fillna(''))
    if factor_filter:
        log.debug(
            "Filtering DataFrame contents on Factor Value %s",
            factor_filter)
        return tfile_df[tfile_df['Factor Value[{}]'.format(
            factor_filter[0])] == factor_filter[1]]
    else:
        return tfile_df