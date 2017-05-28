from . import magetab2isatab
import json
from isatools import isatab
from isatools.isajson import ISAJSONEncoder
import tempfile
import os
import shutil


def convert(source_idf_fp):
    tmp = tempfile.mkdtemp()
    magetab2isatab.convert(source_idf_fp=source_idf_fp, output_path=tmp)
    with open(os.path.join(tmp, "i_investigation.txt")) as isa_inv_fp:
        ISA = isatab.load(isa_inv_fp)
        shutil.rmtree(tmp)
        return json.loads(json.dumps(ISA, cls=ISAJSONEncoder))
