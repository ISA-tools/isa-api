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
            new_result = []
            data_headings = OrderedDict()

            for row_index, row in enumerate(data_reader):
                if row_index == 0:
                    seen_heading = {}
                    for heading_index, heading in enumerate(row):
                        fixed_heading = heading.lower().replace(" ", "_")
                        # print(fixed_heading)
                        if fixed_heading not in seen_heading.keys():
                            # print("first time:", fixed_heading)
                            seen_heading[fixed_heading] = [heading_index]
                        else:
                            # print("deja vu:", fixed_heading)
                            seen_heading[fixed_heading].append(heading_index)
                        data_headings[heading_index] = fixed_heading
                elif row_index > 0:
                    record = []
                    new_record = {}
                    # new_record = OrderedDict()
                    for cell_index, cell in enumerate(row):
                        if cell_index == 0:
                            new_record["measurement_type"] = {"term": cell}
                        if cell_index == 1:
                            new_record["measurement_type"]["url"] = cell
                        if cell_index == 2:
                            new_record["technology_type"] = {"term": cell}
                        if cell_index == 3:
                            new_record["technology_type"]["url"] = cell
                        if cell_index == 4:
                            new_record["protocol_type"] = {"term": cell}
                        if cell_index == 5:
                            new_record["protocol_type"]["url"] = cell
                        if cell_index == 6:
                            new_record["parameter-like_file"] ={"value": cell}
                        if cell_index == 7:
                            new_record["node_name"] = cell
                        if cell_index == 8:
                            new_record["key_file_prefix"] = cell
                        if cell_index == 9:
                            new_record["raw_data_file"] = cell
                        if cell_index == 10:
                            new_record["derived_data_file"] = [cell]
                        if cell_index in [11, 12, 13]:
                            if cell is not "":
                                new_record["derived_data_file"].append(cell)

                        kv_pair = {data_headings[cell_index]: cell}
                        record.append(kv_pair)
                    # result[row_index] = record
                    # result[row_index] = record
                    new_result.append(new_record)

            for key in seen_heading.keys():
                print("Key:", key, seen_heading[key])
        # with open(os.path.join(RESOURCE_DIR, 'isa_assay_config_json_options.yml'), "w+") as out:
        #     yaml.dump(result, out, default_flow_style=False, indent=3)
        with open(os.path.join(RESOURCE_DIR, 'isa_assay_config_json_options.yml'), "w+") as new_out:
            yaml.dump(new_result, new_out, default_flow_style=False, indent=3)

    except IOError as ioe:
            # log.info("conversion to yaml failed: " + ioe)
            print("Error: ", ioe)
            to_yaml_success = False

    return to_yaml_success


if __name__ == "__main__":
    success = csv2yaml()
    print(success)
