from __future__ import absolute_import
import json
import os
import shutil
import tempfile

from isatools import isatab
from isatools.convert import magetab2isatab
from isatools.isajson import ISAJSONEncoder


def convert(idf_file_path):
    tmp = tempfile.mkdtemp()
    ISA = None
    try:
        magetab2isatab.convert(idf_file_path, output_path=tmp)
        with open(os.path.join(
                tmp, 'i_investigation.txt'), encoding='utf-8') as isa_inv_fp:
            ISA = isatab.load(isa_inv_fp)
    finally:
        shutil.rmtree(tmp)
        if ISA is not None:
            return json.loads(json.dumps(ISA, cls=ISAJSONEncoder))
