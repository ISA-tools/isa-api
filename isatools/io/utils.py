
import json
import sys
import os

def saveJsonDoc(file_name, json_doc):
    with open(file_name, "w") as outfile:
        json.dump(json_doc, outfile, indent=4, sort_keys=True)
    outfile.close()

if sys.version_info[0] == 3:
    makedirs = os.makedirs
else:
    def makedirs(dirpath, exist_ok=False):
        try:
            os.makedirs(dirpath)
        except OSError:
            if not exist_ok: raise
            else: pass

