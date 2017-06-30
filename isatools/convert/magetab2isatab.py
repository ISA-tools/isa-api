from isatools import isatab
import os
import logging
from isatools.magetab import MageTabParser

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
LOG = logging.getLogger(__name__)


def convert(idf_file_path, output_path):
    """ Converter for MAGE-TAB to ISA-Tab
    :param idf_file_path: File descriptor of input IDF file
    :param output_path: Path to directory to write output ISA-Tab files to
    """
    parser = MageTabParser()
    parser.parse_idf(idf_file_path)
    print("Writing {0} to {1}".format("i_investigation.txt", output_path))
    isatab.dump(parser.ISA, output_path=output_path, skip_dump_tables=True)
    sdrf_files = [x.value for x in parser.ISA.studies[-1].comments if 'SDRF File' in x.name]
    if len(sdrf_files) == 1:
        table_files = parser.parse_sdrf_to_isa_table_files(os.path.join(os.path.dirname(idf_file_path), sdrf_files[0]))
        sfiles = [x for x in table_files if x.name.startswith('s_')]
        afiles = [x for x in table_files if x.name.startswith('a_')]

        study_filename = parser.ISA.studies[-1].filename
        LOG.info("Writing {0} to {1}".format(study_filename, output_path))
        if len(sfiles) == 1:
            pass
        assay_filename = parser.ISA.studies[-1].assays[-1].filename
        LOG.info("Writing {0} to {1}".format(assay_filename, output_path))
