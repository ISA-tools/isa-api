from . import magetab2isatab
import json
from isatools import isatab
from isatools.isajson import ISAJSONEncoder
import tempfile
import os
import shutil


def convert(source_path, technology_type=None, measurement_type=None):
    tmp = tempfile.mkdtemp()
    ISA = None
    try:
        magetab2isatab.convert(source_path, output_path=tmp, technology_type=technology_type,
                               measurement_type=measurement_type)
        with open(os.path.join(tmp, "i_investigation.txt")) as isa_inv_fp:
            ISA = isatab.load(isa_inv_fp)
    finally:
        shutil.rmtree(tmp)
        if ISA is not None:
            return json.loads(json.dumps(ISA, cls=ISAJSONEncoder))
