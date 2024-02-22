import logging
from os import path
from logging import getLogger

from re import compile


log = getLogger('isatools')


def xml_config_contents(filename):
    """Gets the contents of a ISA Configuration XML file

    :param filename: ISA Configuration XML filename
    :return: String content of the configuration file
    """
    config_filepath = path.join(
        path.dirname(__file__),
        '..',
        'resources',
        'config',
        'xml',
        filename,
    )
    with open(config_filepath) as f:
        return f.read()


def pbar(x):
    return x


# column labels
_LABELS_MATERIAL_NODES = ['Source Name', 'Sample Name', 'Extract Name',
                          'Labeled Extract Name']
_LABELS_DATA_NODES = ['Raw Data File', 'Raw Spectral Data File',
                      'Derived Spectral Data File', 'Derived Array Data File',
                      'Array Data File', 'Protein Assignment File',
                      'Peptide Assignment File',
                      'Post Translational Modification Assignment File',
                      'Acquisition Parameter Data File',
                      'Free Induction Decay Data File',
                      'Derived Array Data Matrix File', 'Array Data Matrix File',
                      'Image File', 'Derived Data File', 'Metabolite Assignment File']
_LABELS_ASSAY_NODES = ['Assay Name', 'MS Assay Name', "NMR Assay Name",
                       'Hybridization Assay Name', 'Scan Name',
                       'Data Transformation Name', 'Normalization Name']

# REGEXES
_RX_I_FILE_NAME = compile(r'i_(.*?)\.txt')
_RX_DATA = compile(r'data\[(.*?)\]')
_RX_COMMENT = compile(r'Comment\[(.*?)\]')
_RX_DOI = compile(r'(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%"#? ])\\S)+)')
_RX_PMID = compile(r'[0-9]{8}')
_RX_PMCID = compile(r'PMC[0-9]{8}')
_RX_CHARACTERISTICS = compile(r'Characteristics\[(.*?)\]')
_RX_PARAMETER_VALUE = compile(r'Parameter Value\[(.*?)\]')
_RX_FACTOR_VALUE = compile(r'Factor Value\[(.*?)\]')
_RX_INDEXED_COL = compile(r'(.*?)\.\d+')

STUDY_SAMPLE_XML_CONFIG = xml_config_contents('studySample.xml')
NUMBER_OF_STUDY_GROUPS = 'Comment[Number of Study Groups]'

BASE_DIR = path.dirname(__file__)
default_config_dir = path.join(BASE_DIR, '..', 'resources', 'config', 'xml')


class _Defaults(object):
    """An internal object to hold defaults for ISA-Tab features"""

    def __init__(self):
        self._tab_options = {
            'readCellQuotes': False, # read cell quotes as part of cell values
            'writeCellQuotes': True, # write out cell values enclosed with quotes
            'forceFitColumns': True,
            'validateBeforeRead': False,
            'validateAfterWrite': False
        }
        self._show_progressbar = False
        self._log_level = logging.WARNING

    def set_tab_option(self, opt_name, opt_value):
        self._tab_options[opt_name] = opt_value

    def set_defaults(self, show_progressbar=None, log_level=None):
        if show_progressbar is not None:
            self._show_progressbar = show_progressbar
        if log_level is not None:
            self._log_level = log_level

    @property
    def tab_options(self):
        return self._tab_options

    @property
    def show_progressbar(self):
        return self._show_progressbar

    @property
    def log_level(self):
        return self._log_level


defaults = _Defaults()
