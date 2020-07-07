import os
import yaml
# import logging
import csv
from collections import OrderedDict

# log = logging.getLogger('isatools')

__author__ = 'proccaserra@gmail.com'

INPUT = "./resources/config/ISA-json-config-assay-headers-by-technology.csv"
RESOURCE_DIR = "./resources/config/yaml/"


def csv2yaml():
    """
    :return: to_yaml_success

    """
    try:
        to_yaml_success = True
        with open(os.path.join(INPUT)) as file_in:
            data_reader = csv.reader(file_in, delimiter=",", quotechar='"')
            # result = OrderedDict()
            result = {}
            data_headings = OrderedDict()
            for row_index, row in enumerate(data_reader):

                if row_index == 0:
                    for heading_index, heading in enumerate(row):
                        fixed_heading = heading.lower().replace(" ", "_")
                        data_headings[heading_index] = fixed_heading
                elif row_index > 0:
                    record = []
                    for cell_index, cell in enumerate(row):
                        kv_pair = {data_headings[cell_index]: cell}
                        record.append(kv_pair)
                    # result[row_index] = record
                    result[row_index]=record
        with open(os.path.join(RESOURCE_DIR, 'isa_assay_config_json_options.yml'), "w+") as out:
            yaml.dump(result, out, default_flow_style=False, indent=3)

    except IOError as ioe:
            # log.info("conversion to yaml failed: " + ioe)
            print("Error: ", ioe)
            to_yaml_success = False

    return to_yaml_success


if __name__ == "__main__":
    success = csv2yaml()
    print(success)
