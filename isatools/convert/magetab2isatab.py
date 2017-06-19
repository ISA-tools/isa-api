import pandas as pd
from isatools import isatab
import os
import logging
from isatools import magetab

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(source_idf_fp, output_path, technology_type, measurement_type):
    """ Converter for MAGE-TAB to ISA-Tab
    :param source_idf_fp: File descriptor of input IDF file
    :param output_dir: Path to directory to write output ISA-Tab files to
    """
    df = pd.read_csv(source_idf_fp, names=range(0, 128), sep='\t', engine='python', encoding='utf-8', comment='#').dropna(axis=1, how='all')
    df = df.T  # transpose
    df.reset_index(inplace=True)  # Reset index so it is accessible as column
    df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
    df = df.reindex(df.index.drop(0))
    # second set output s_ and a_ files
    for _, row in df.iterrows():
        sdrf_file = row["SDRF File"]
        if isinstance(sdrf_file, str):
            study_df, assay_df = split_tables(sdrf_path=os.path.join(os.path.dirname(source_idf_fp.name), sdrf_file))
            study_df.columns = study_df.isatab_header
            assay_df.columns = assay_df.isatab_header
            # write out ISA table files
            print("Writing s_{0} to {1}".format(os.path.basename(sdrf_file), output_path))
            with open(os.path.join(output_path, "s_" + os.path.basename(sdrf_file)), "w") as s_fp:
                study_df.to_csv(path_or_buf=s_fp, mode='a', sep='\t', encoding='utf-8', index=False)
            print("Writing a_{0} to {1}".format(os.path.basename(sdrf_file), output_path))
            with open(os.path.join(output_path, "a_" + os.path.basename(sdrf_file)), "w") as a_fp:
                assay_df.to_csv(path_or_buf=a_fp, mode='a', sep='\t', encoding='utf-8', index=False)
    print("Writing {0} to {1}".format("i_investigation.txt", output_path))
    source_idf_fp.seek(0)
    ISA = magetab.parse_idf(source_idf_fp.name, technology_type=technology_type, measurement_type=measurement_type)
    isatab.dump(ISA, output_path=output_path, skip_dump_tables=True)


def get_investigation_title(line, ISA):
    split_line = [x for x in line.split('\t') if x != '']
    if len(split_line) > 1:
        value = split_line[1]
        ISA.title = value


def split_tables(sdrf_path):
    sdrf_df = isatab.read_tfile(sdrf_path)
    sdrf_df_isatab_header = sdrf_df.isatab_header
    if "Sample Name" in sdrf_df.columns:
        sample_name_index = list(sdrf_df.columns).index("Sample Name")
    elif "Extract Name" in sdrf_df.columns:
        sample_name_index = list(sdrf_df.columns).index("Extract Name")
    elif "Labeled Extract Name" in sdrf_df.columns:
        sample_name_index = list(sdrf_df.columns).index("Labeled Extract Name")
    else:
        raise magetab.MageTabParserException("Could not split SDRF table as could not find suitable column to split on")
    study_df = sdrf_df[sdrf_df.columns[0:sample_name_index+1]].drop_duplicates()
    study_df.isatab_header = sdrf_df_isatab_header[0:sample_name_index+1]
    assay_df = sdrf_df[sdrf_df.columns[sample_name_index:]]
    assay_df.isatab_header = sdrf_df_isatab_header[sample_name_index:]
    return study_df, assay_df