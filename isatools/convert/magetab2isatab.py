from isatools import isatab
import os
import logging
from isatools.magetab import MageTabParser

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


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
        study_df, assay_df = parser.parse_sdrf_to_dataframes(os.path.join(os.path.dirname(idf_file_path), sdrf_files[0]))

        columns = [x[:x.rindex('.')] if '.' in x else x for x in list(study_df.columns)]
        study_df.columns = columns
        columns = [x[:x.rindex('.')] if '.' in x else x for x in list(assay_df.columns)]
        assay_df.columns = columns

        study_filename = parser.ISA.studies[-1].filename
        assay_filename = parser.ISA.studies[-1].assays[-1].filename
        print("Writing {0} to {1}".format(study_filename, output_path))
        with open(os.path.join(output_path, study_filename), "w") as s_fp:
            study_df.to_csv(path_or_buf=s_fp, mode='a', sep='\t', encoding='utf-8', index=False)
        print("Writing {0} to {1}".format(assay_filename, output_path))
        with open(os.path.join(output_path, assay_filename), "w") as a_fp:
            assay_df.to_csv(path_or_buf=a_fp, mode='a', sep='\t', encoding='utf-8', index=False)

