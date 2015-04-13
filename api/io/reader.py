__author__ = 'Alfie Abdul-Rahman'

import os, glob, json

investigation_file_pattern = "i_*.json"

def read(isatabjson_ref):
    """Entry point to parse an ISA-Tab directory.

    isatab_ref can point to a directory of ISA-Tab data, in which case we
    search for the investigator file, or be a reference to the high level
    investigation file.
    """
    if os.path.isdir(isatabjson_ref):
        fnames = glob.glob(os.path.join(isatabjson_ref, investigation_file_pattern))
        assert len(fnames) == 1
        isatabjson_ref = fnames[0]
    assert os.path.exists(isatabjson_ref), "Did not find investigation file: %s" % isatabjson_ref
    isa_json_reader = IsatabJsonReader()
    with open(isatabjson_ref, "rU") as in_handle:
        rec = isa_json_reader.read(in_handle)
    return rec

class IsatabJsonReader():
    def read(self, in_handle):
        json_data = json.load(in_handle)
        return json_data