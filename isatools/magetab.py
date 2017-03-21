from isatools import isatab
import os
import tempfile


def write_sdrf_table_file(inv_obj, output_dir):
    tmp = tempfile.mkdtemp()
    isatab.write_study_table_files(inv_obj=inv_obj, output_dir=tmp)
    isatab.write_assay_table_files(inv_obj=inv_obj, output_dir=tmp)
    isatab.merge_study_with_assay_tables(os.path.join(tmp, inv_obj.studies[0].filename),
                                         os.path.join(tmp, inv_obj.studies[0].assays[0].filename),
                                         os.path.join(output_dir, "sdrf.txt"))

