import csv
import pandas as pd
import numpy as np
from isatools.utils import contains

_IFILE_BASE_INDEX_LABELS = (
    'ONTOLOGY SOURCE REFERENCE',
    'Term Source Name',
    'Term Source File',
    'Term Source Version',
    'Term Source Description',
    'INVESTIGATION',
    'Investigation Identifier',
    'Investigation Title',
    'Investigation Description',
    'Investigation Submission Date',
    'Investigation Public Release Date'
)
_IFILE_PUBLICATIONS_SECTION_LABELS = (
    '{} PUBLICATIONS',
    '{} PubMed ID',
    '{} Publication DOI',
    '{} Publication Author List',
    '{} Publication Title',
    '{} Publication Status',
    '{} Publication Status Term Accession Number',
    '{} Publication Status Term Source REF',
)

_IFILE_CONTACTS_SECTION_LABELS = (
    '{} CONTACTS',
    '{} Person Last Name',
    '{} Person First Name',
    '{} Person Mid Initials',
    '{} Person Email',
    '{} Person Phone',
    '{} Person Fax',
    '{} Person Address',
    '{} Person Affiliation',
    '{} Person Roles',
    '{} Person Roles Term Accession Number',
    '{} Person Roles Term Source REF',
)

_TFILE_BASE_HEADER_LABELS = ()


class Investigation(object):

    def __init__(self, df=None):
        if df is None:
            if not isinstance(df, pd.DataFrame):
                raise TypeError("df must be of type pandas.DataFrame")
            if df.empty:
                raise ValueError("df can not be empty")
            self._ifile_df = pd.DataFrame(index=_IFILE_BASE_INDEX_LABELS, columns=range(0, 1)).fillna('')
            print(self._ifile_df)
        else:
            # run some checks on load, e.g. all labels in index, at least 1 column wide etc,
            # and if valid ISA-Tab i_ file
            # https: // github.com / JosPolfliet / pandas - profiling / blob / master / pandas_profiling / base.py
            self._ifile_df = df

    @property
    def identifier(self):
        return self._ifile_df.loc['Investigation Identifier'][0]

    @identifier.setter
    def identifier(self, new_id):
        self._ifile_df.loc['Investigation Identifier'][0] = new_id

    @property
    def title(self):
        return self._ifile_df.loc['Investigation Title'][0]

    @title.setter
    def title(self, new_title):
        self._ifile_df.loc['Investigation Title'][0] = new_title

    @property
    def description(self):
        return self._ifile_df.loc['Investigation Title'][0]

    @description.setter
    def description(self, new_description):
        self._ifile_df.loc['Investigation Description'][0] = new_description

    @property
    def submission_date(self):
        return self._ifile_df.loc['Investigation Submission Date'][0]

    @submission_date.setter
    def submission_date(self, new_submission_date):
        self._ifile_df.loc['Investigation Submission Date'][0] = new_submission_date

    @property
    def public_release_date(self):
        return self._ifile_df.loc['Investigation Submission Date'][0]

    @public_release_date.setter
    def public_release_date(self, new_public_release_date):
        self._ifile_df.loc['Investigation Public Release Date'][0] = new_public_release_date

    @property
    def publications(self):
        pass


class ProcessSequence(object):

    def __init__(self, df=None):
        if df is None:
            self._df = pd.DataFrame(columns=_TFILE_BASE_HEADER_LABELS)
        else:
            # run some checks on load, e.g. all labels in index, at least 1 column wide etc,
            # and if valid ISA-Tab i_ file
            self._df = df

    @property
    def samples(self):
        sample_indexed_df = self._df.set_index('Sample Name')
        sample_list = list(map(lambda x: Sample(name=x, sample_indexed_df=sample_indexed_df),
                          sample_indexed_df.index.drop_duplicates()))
        return sample_list


class Material(object):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_):
        if isinstance(name_, str):
            self._name = name_
        else:
            raise TypeError


class Source(Material):

    def __init__(self, name):
        super().__init__(name)


class Sample(Material):

    def __init__(self, name):
        super().__init__(name)


class ProcessSequenceFactory(object):

    def __init__(self, xml_configuration):
        self._xml_configuration = xml_configuration

    def create_from_df(self, DF):
        sources = {}
        samples = {}
        for i in DF.index:
            source_name = DF.loc[DF.index[i]]['Source Name']
            if source_name not in sources.keys():
                sources[source_name] = Source(name=source_name)
            sample_name = DF.loc[DF.index[i]]['Sample Name']
            if sample_name not in samples.keys():
                samples[sample_name] = Sample(name=sample_name)
        return None

    def create_from_json(self, J):
        pass


def read_ifile(ifile_path):
    with open(ifile_path) as ifile_fp:
        reader = csv.reader(ifile_fp, delimiter='\t')
        maxwidth = len(max(reader, key=len))
        ifile_fp.seek(0)
        ifile_df = pd.read_csv(ifile_fp, sep='\t', header=None, names=list(range(0, maxwidth)), index_col=0, encoding='utf-8', comment='#')
    return ifile_df


def read_tfile(tfile_path, index_col):
    with open(tfile_path) as tfile_fp:
        reader = csv.reader(tfile_fp, delimiter='\t')
        header = list(next(reader))
        tfile_fp.seek(0)
        tfile_df = pd.read_csv(tfile_fp, sep='\t', index_col=index_col, encoding='utf-8', comment='#')
        tfile_df.isatab_header = header
    return tfile_df


def check_ontology_source_reference_section(ifile_df):
    ifile_index = list(ifile_df.index)
    section_index = ifile_df.index[ifile_index.index('ONTOLOGY SOURCE REFERENCE'):ifile_index.index('INVESTIGATION')]
    expected_index = ['Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description']
    if contains(expected_index, section_index):
        print("OK")
    else:
        print("Not OK")


# def get_ontology_sources(ifile_df):
#     ifile_index = list(ifile_df.index)
#     for i, v in ifile_df[ifile_index.index('ONTOLOGY SOURCE REFERENCE'):ifile_index.index('INVESTIGATION')].items():
#         try:
#             yield OntologySource(
#                 name=v.loc['Term Source Name'] if isinstance(v.loc['Term Source Name'], str) else '',
#                 file=v.loc['Term Source File'] if isinstance(v.loc['Term Source File'], str) else '',
#                 version=v.loc['Term Source Version'] if isinstance(v.loc['Term Source Version'], str) else '',
#                 description=v.loc['Term Source Description'] if isinstance(v.loc['Term Source Description'], str) else ''
#             )
#         except AttributeError:
#             pass


def get_multiple_index(file_index, key):
    return np.where(np.array(file_index) == key)[0]
