import os
from io import BytesIO
from zipfile import ZipFile
import logging
import json
from io import StringIO
from isatools.convert import isatab2json, json2sra


def zipdir(path, zip_file):
    """utility function to zip only SRA xmls from a whole directory"""
    # zip_file is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in [f for f in files if f in ['submission.xml', 'project_set.xml', 'run_set.xml',
                                               'experiment_set.xml', 'sample_set.xml']]:
            zip_file.write(os.path.join(root, file),
                           arcname=os.path.join(os.path.basename(root), file))

BASE_DIR = os.path.dirname(__file__)
default_config_dir = os.path.join(BASE_DIR, '..', 'config', 'xml')


def convert(source_path, dest_path, sra_settings=None, validate_first=True):
    isa_json = isatab2json.convert(source_path, validate_first=validate_first)
    isa_json_fp = StringIO(json.dumps(isa_json))
    isa_json_fp.name = "BII-S-3.json"
    json2sra.convert(isa_json_fp, dest_path, sra_settings=sra_settings, validate_first=False)
    logging.info("Conversion complete...")
    buffer = BytesIO()
    if os.path.isdir(dest_path):
        with ZipFile(buffer, 'w') as zip_file:
            # use relative dir_name to avoid absolute path on file names
            zipdir(dest_path, zip_file)
            print(zip_file.namelist())

            # clean up the target directory after the ZIP file has been closed
            # rmtree(sra_dir)

        buffer.seek(0)
        return buffer
