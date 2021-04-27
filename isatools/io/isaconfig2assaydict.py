from isatools import *
from isatools.io import isatab_configurator as configurator

import uuid
import re
import os
import logging
from collections import OrderedDict
import datetime
import logging
from isatools.utils import utf8_text_file_open
import json

__author__ = ['philippe.rocca-serra@oerc.ox.ac.uk']

logging.basicConfig()
logger = logging.getLogger('logger')
logger.warning('warning-message')


BASE_DIR = os.path.dirname('../')
default_config_dir = os.path.join(BASE_DIR, 'resources', 'config', 'xml')
print(default_config_dir)

log = logging.getLogger('isatools')


RESOURCES_DSCONFIG_DIR = os.path.join('../resources/config/json', 'datascriptor')
outputdirname = os.path.join(RESOURCES_DSCONFIG_DIR, str(datetime.datetime.now().strftime("%Y-%m-%d")))

output = os.path.join(outputdirname, "isaconfig2assay_ds_config.json")



# def convert_xml_config(config):
# """
# config_orderedDict:
# """
#     config_orderedDict = OrderedDict()
#
#     config_orderedDict = {}
#
# return config_orderedDict

ASSAY_ONTO_MAPPINGS = {
    "transcription profiling": "http://purl.obolibrary.org/obo/OBI_0000424",
    "transcription factor binding site identification": "http://purl.obolibrary.org/obo/OBI_0000291",
    "metabolite profiling": "http://purl.obolibrary.org/obo/OBI_0000366",
    "copy number variation profiling": "http://purl.obolibrary.org/obo/OBI_0000537",
    "dna methylation profiling": "http://purl.obolibrary.org/obo/OBI_0000634",
    "protein-protein interaction detection": "http://purl.obolibrary.org/obo/OBI_0000288",
    "protein expression profiling": "http://purl.obolibrary.org/obo/OBI_0000615",
    "protein-dna binding site identification": "",
    "protein identification": "",
    "cell counting": "",
    "cell sorting": "",
    "clinical chemistry analysis": "http://purl.obolibrary.org/obo/OBI_0000520",
    "hematology": "http://purl.obolibrary.org/obo/OBI_0000630",
    "histology": "http://purl.obolibrary.org/obo/OBI_0000630",
    "environmental gene survey": "",
    "genome sequencing": "",
    "metagenome sequencing": "",
    "loss of heterozygosity profiling": "",
    "snp analysis": "",
    "histone modification profiling": "",
    "nucleotide sequencing": "http://purl.obolibrary.org/obo/OBI_0000626",
    "mass spectrometry": "http://purl.obolibrary.org/obo/OBI_0000470",
    "nmr spectroscopy": "http://purl.obolibrary.org/obo/OBI_0000623",
    "dna microarray": "http://purl.obolibrary.org/obo/OBI_0400148",
    "protein microarray": "http://purl.obolibrary.org/obo/OBI_0400149",
    "flow cytometry": "http://purl.obolibrary.org/obo/OBI_0000916",
    "real time pcr": "http://purl.obolibrary.org/obo/OBI_0000893",
    "gel electrophoresis": "http://purl.obolibrary.org/obo/OBI_0600053",
}


try:
    configs = configurator.load(default_config_dir)
    if configs is None:
        raise SystemError(
            "No configuration to load so cannot proceed with validation!")
        # log.info("Using configurations found in {}".format(config_dir))
    else:
        counter = 0
        assay_defs = []

        for config in configs:
            print(config[0], config[1])
            parsed_config = configurator.get_config(configs, measurement_type=config[0], technology_type=config[1])
            print("PARSED:", parsed_config)

            counter += 1
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # building the header
            assay_dict = OrderedDict()
            assay_dict["id"] = str(uuid.uuid4())
            assay_dict["name"] = config[0] + " by " + config[1]
            assay_dict["icon"] = "fas fa-atom"
            assay_dict["color"] = "orange"
            assay_dict["creation_date"] = now
            if "[sample]" not in config[0] and "[investigation]" not in config[0] and config[1] :
                    assay_dict["measurement_type"] = {"term": config[0],
                                                      "uri": ASSAY_ONTO_MAPPINGS[config[0]],
                                                      "source": "OBI"}

                    print("config key:", config[1])
                    assay_dict["technology_type"] = {"term": config[1],
                                                     "uri": ASSAY_ONTO_MAPPINGS[config[1]],
                                                     "source": "OBI"}
            assay_dict["workflow"] = []
            assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                      "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}

            # initializing sub
            workflow_segment = {} # a dictionary holding the assay workflow
            protocol_param_setup = {} # an array of parameters associated to the current  protocol_type
            material_chars = {} # an dictionary of characteristics associated to the current material node
            protocol_counter = 0
            protocol_chain = 0
            protocol_node_type = []
            all_protocols = []
            # for element in sorted_config_object:
            for element in parsed_config:
                if isinstance(element, configurator.FieldType):
                    if element.get_header() == "Sample Name":

                        MoD_node_type = ["sample", {
                            "node_type": "sample",
                            "is_input_to_next_protocols": {
                                "value": True
                            }
                        }]

                        protocol_chain = 0

                    if element.get_header() == "Extract Name":
                        # creation of a new node
                        MoD_node_type = ["extract", {
                            "node_type": "extract",
                            "characteristics_category": "extract type",
                            "characteristics_value": {
                                "options": [],
                                "values": []
                            },
                            "is_input_to_next_protocols": {
                                "value": True
                            }
                        }]

                        # updating the assay_dict workflow with a new protocol element
                        # assay_dict["workflow"].append(protocol_param_setup)
                        assay_dict["workflow"].append(protocol_node_type)

                        # we meet a node, we reset the counter for protocol chain size
                        protocol_chain = 0
                        protocol_node_type = []

                        # adding the new node to the assay_dict workflow
                        assay_dict["workflow"].append(MoD_node_type)
                        # protocol_param_setup = {}

                    if element.get_header() == "Labeled Extract Name":
                        MoD_node_type = ["labeled extract", {
                            "node_type": "labeled extract",
                            "characteristics_category": "labeled extract type",
                            "characteristics_value": {
                                "options": [],
                                "values": []
                            },
                            "is_input_to_next_protocols": {
                                "value": True
                            }
                        }]

                        # assay_dict["workflow"].append(protocol_param_setup)
                        assay_dict["workflow"].append(protocol_node_type)

                        # resetting the protocol chain counter and protocol_node_type
                        protocol_chain = 0

                        protocol_node_type = []
                        assay_dict["workflow"].append(MoD_node_type)

                    if "Parameter Value[" in element.get_header():
                        # Getting Parameter Name by removing ISA prefix and brackets:
                        new_param = element.get_header()[:-1]
                        new_param = new_param.split("[", 1)[1]

                        all_keys = current_protocol_type.keys()

                        # Getting the Param description and cleaning it
                        pattern = re.compile(r'\n\s+')
                        cleaned_desc = re.sub(pattern, ' ', element.get_description())
                        protocol_param_options = {"newValues": True,
                                                  "isQuantitative": False,
                                                  "description": cleaned_desc,
                                                  "options": [],
                                                  "values": []}

                        # Getting the list of allowed values for that parameter
                        if element.get_list_values() is not None:
                            param_values = element.get_list_values().split(",")
                            pattern = re.compile(r'\n\s+')
                            cleaned_values = [re.sub(pattern, ' ', x) for x in param_values]
                            protocol_param_options["options"] = cleaned_values

                        protocol_param_setup = current_protocol_type
                        # print("currently using:", protocol_param_setup[latest_protocol])
                        current_protocol_type[latest_protocol][new_param] = protocol_param_options

                    # TODO: deal with more than one Characteristics (not currently supported)
                    # elif "Characteristics[" in element.get_header():
                    #     print("current Material:", node_type)
                    #     charax = element.get_header()[:-1]
                    #     charax = charax.split("[", 1)[1]
                    #     pattern = re.compile(r'\n\s+')
                    #     cleaned_desc = re.sub(pattern, ' ', element.get_description())
                    #
                    #     material_chars["characteristics_category"] = charax
                    #     if element.get_list_values() is not None:
                    #         charax_values = element.get_list_values().split(",")
                    #         pattern = re.compile(r'\n\s+')
                    #         cleaned_charax_values = [re.sub(pattern, ' ', x) for x in charax_values]
                    #         material_chars["characteristics_values"] = cleaned_charax_values

                    if element.get_header() == "Raw Data File" and config[1] == "nucleotide sequencing":
                        MoD_node_type = [
                            {
                                "term": "raw data file",
                                "iri": "",
                                "source": None
                            },
                            {
                                "node_type": "data file",
                                "is_input_to_next_protocols": {
                                    "value": True
                                },
                                "extension": {
                                    "options": ["fastq"],
                                    "value": "fastq",
                                    "newValues": True
                                }
                            }
                        ]

                        # adding the Protocol Node to the workflow
                        assay_dict["workflow"].append(protocol_node_type)
                        # Resetting the protocol chain counter
                        protocol_chain = 0
                        protocol_node_type = []

                        # adding the Data Node to the workflow
                        assay_dict["workflow"].append(MoD_node_type)

                        # we exit because we've reach the Raw Data File Element and we don't need more elments to build
                        # the OrderedDict required from ISA-API create mode.
                        break

                    if "Raw Spectral Data File" in element.get_header():
                        MoD_node_type = [
                            {
                                "term": "raw data file",
                                "iri": "",
                                "source": None
                            },
                            {
                                "node_type": "data file",
                                "is_input_to_next_protocols": {
                                    "value": True
                                },
                                "extension": {
                                    "options": ["mzml", "RAW", "wiff"],
                                    "value": "mzml",
                                    "newValues": True
                                }
                            }
                        ]

                        # adding the Protocol Node to the workflow
                        assay_dict["workflow"].append(protocol_node_type)
                        # Resetting the protocol chain counter
                        protocol_chain = 0
                        protocol_node_type = []

                        # adding the Data Node to the workflow
                        assay_dict["workflow"].append(MoD_node_type)

                        # we exit because we've reach the Raw Data File Element and we don't need more elments to build
                        # the OrderedDict required from ISA-API create mode.
                        break

                    if "Free Induction Decay Data File" in element.get_header():
                        MoD_node_type = [
                            {
                                "term": "raw data file",
                                "iri": "",
                                "source": None
                            },
                            {
                                "node_type": "data file",
                                "is_input_to_next_protocols": {
                                    "value": True
                                },
                                "extension": {
                                    "options": ["mzml", "RAW", "wiff"],
                                    "value": "mzml",
                                    "newValues": True
                                }
                            }
                        ]

                        # adding the Protocol Node to the workflow
                        assay_dict["workflow"].append(protocol_node_type)
                        # Resetting the protocol chain counter
                        protocol_chain = 0
                        protocol_node_type = []

                        # adding the Data Node to the workflow
                        assay_dict["workflow"].append(MoD_node_type)

                        # we exit because we've reach the Raw Data File Element and we don't need more elments to build
                        # the OrderedDict required from ISA-API create mode.
                        break

                    if "Array Data File" in element.get_header():
                        MoD_node_type = [
                            {
                                "term": "raw data file",
                                "iri": "",
                                "source": None
                            },
                            {
                                "node_type": "data file",
                                "is_input_to_next_protocols": {
                                    "value": True
                                },
                                "extension": {
                                    "options": ["CEL", "raw", "txt"],
                                    "value": "CEL",
                                    "newValues": True
                                }
                            }
                        ]

                        # adding the Protocol Node to the workflow
                        assay_dict["workflow"].append(protocol_node_type)
                        # Resetting the protocol chain counter
                        protocol_chain = 0
                        protocol_node_type = []

                        # adding the Data Node to the workflow
                        assay_dict["workflow"].append(MoD_node_type)

                        # we exit because we've reach the Raw Data File Element and we don't need more elments to build
                        # the OrderedDict required from ISA-API create mode.
                        break

                elif isinstance(element, configurator.ProtocolFieldType):
                    latest_protocol = element.protocol_type
                    current_protocol_type = {}
                    current_protocol_type[latest_protocol] = {"#replicates": {
                            "value": 1
                        }}
                    protocol_counter = protocol_counter+1
                    protocol_chain = protocol_chain+1

                    if len(protocol_node_type) > 0:
                        print(len(protocol_node_type), "starting from non-empty")
                        # daisy chain of protocols, adding the new one to the list
                        protocol_node_type.append(current_protocol_type)

                    else:
                        # fresh new protocol
                        print(len(protocol_node_type), "starting fresh")
                        protocol_node_type = []
                        protocol_param_setup[latest_protocol] = {"#replicates": {
                            "value": 1
                        }}
                        # protocol_chain_array = []
                        protocol_node_type.append(current_protocol_type)
            assay_defs.append(assay_dict)



        try:
            if os.path.exists(outputdirname):
                with open(output, 'w+') as config_file:
                    # for assay in assay_defs:
                         json.dump(assay_defs, config_file, indent=4)
            else:
                os.makedirs(outputdirname)
                with open(output, 'w+') as config_file:
                    # for assay in assay_defs:
                        json.dump(assay_defs, config_file, indent=4)

        except IOError as another_ioe:
            logger.error(another_ioe)

except IOError as ioe:
    log.error(ioe)

