from os import path

from isatools.isatab.defaults import log
from isatools.isatab.validate.store import validator
from isatools.utils import utf8_text_file_open


def check_table_files_read(i_df_dict, dir_context):
    """Used for rules 0006 and 0008

    :param i_df_dict: A dictionary of DataFrames and lists of DataFrames representing the investigation file
    :param dir_context: Path to where the investigation file is found
    :return: None
    """
    for i, study_df in enumerate(i_df_dict["studies"]):
        study_filename = study_df.iloc[0]["Study File Name"]
        if study_filename != "":
            try:
                with utf8_text_file_open(path.join(dir_context, study_filename)):
                    pass
            except FileNotFoundError:
                spl = f"Study File {study_filename} does not appear to exist"
                validator.add_error(message="Missing study tab file(s)", supplemental=spl, code=6)
                log.error(f"(E) Study File {study_filename} does not appear to exist")
        for j, assay_filename in enumerate(i_df_dict["s_assays"][i]["Study Assay File Name"].tolist()):
            if assay_filename != "":
                try:
                    with utf8_text_file_open(path.join(dir_context, assay_filename)):
                        pass
                except FileNotFoundError:
                    spl = f"Assay File {assay_filename} does not appear to exist"
                    validator.add_error(message="Missing assay tab file(s)", supplemental=spl, code=8)
                    log.error(f"(E) Assay File {assay_filename} does not appear to exist")


def check_sample_names(study_sample_table, assay_tables=None):
    """Checks that samples in the assay tables also appear in the study-sample table

    :param study_sample_table: Study table DataFrame
    :param assay_tables: A list of Assay table DataFrames
    :return: None
    """
    if assay_tables is None:
        assay_tables = []
    if len(assay_tables) > 0:
        study_samples = set(study_sample_table["Sample Name"])
        for assay_table in assay_tables:
            assay_samples = set(assay_table["Sample Name"])
            for assay_sample in assay_samples:
                spl = "{} is a Sample Name in {}, but it is not defined in the Study Sample File {}."
                spl = spl.format(assay_sample, assay_table.filename, study_sample_table.filename)
                if assay_sample not in study_samples:
                    validator.add_warning(message="Missing Sample", supplemental=spl, code=1003)
                    log.warning(f"(W) {spl}")
