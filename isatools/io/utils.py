
import json
import six
import os

def saveJsonDoc(file_name, json_doc):
    with open(file_name, "w") as outfile:
        json.dump(json_doc, outfile, indent=4, sort_keys=True)
    outfile.close()

if six.PY3:
    makedirs = os.makedirs
else:
    def makedirs(dirpath, exist_ok=False):
        splitted_path = dirpath.split(os.path.sep)
        for i in range(len(splitted_path)):
            try:
                os.makedirs(dirpath[:i])
            except OSError:
                if not exist_ok: raise
                else: pass

