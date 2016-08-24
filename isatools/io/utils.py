
import json


def saveJsonDoc(file_name, json_doc):
    with open(file_name, "w") as outfile:
        json.dump(json_doc, outfile, indent=4, sort_keys=True)
    outfile.close()