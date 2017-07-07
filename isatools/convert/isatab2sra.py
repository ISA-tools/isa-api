import os
from io import BytesIO
from zipfile import ZipFile
import logging
import json
from io import StringIO
from isatools.convert import isatab2json, json2sra
import isatools

logging.basicConfig(level=isatools.log_level)
LOG = logging.getLogger(__name__)


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
    LOG.info("Converting ISA-Tab to JSON for %s", source_path)
    isa_json = isatab2json.convert(source_path, validate_first=validate_first)
    LOG.debug("Writing JSON to memory file")
    isa_json_fp = StringIO(json.dumps(isa_json))
    isa_json_fp.name = "BII-S-3.json"
    LOG.info("Converting JSON to SRA, writing to %s", dest_path)
    LOG.info("Using SRA settings %s", sra_settings)
    json2sra.convert(isa_json_fp, dest_path, sra_settings=sra_settings, validate_first=False)
    LOG.info("Conversion from ISA-Tab to SRA complete")
    buffer = BytesIO()
    if os.path.isdir(dest_path):
        LOG.info("Zipping SRA files")
        with ZipFile(buffer, 'w') as zip_file:
            zipdir(dest_path, zip_file)
            LOG.debug("Zipped %s", zip_file.namelist())
        buffer.seek(0)
        LOG.info("Returning zipped files as memory file")
        return buffer
