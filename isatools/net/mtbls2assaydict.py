from __future__ import absolute_import
import os
import shutil
import sys
import csv
from collections import OrderedDict
import json
import logging
import hashlib
import rdflib
import datetime
import requests
from rdflib import URIRef, Graph, RDFS
from rdflib.resource import Resource


__author__ = ['philippe.rocca-serra@oerc.ox.ac.uk']

MTBLS_DIR = os.path.join(os.path.dirname(__file__), 'resources', 'mtbls/current')
MTBLS_TMPDIR = os.path.join(os.path.dirname(__file__), 'resources', 'mtbls/tmp')

MTBLS_ASSAY_DEF_FILE = os.path.join(MTBLS_DIR, 'MetaboLightsAssayMaster.tsv')

MTBLS_CV_OWL = os.path.join(MTBLS_DIR, 'Metabolights.owl')

RESOURCES_MTBLS_DIR = os.path.join('../resources/config/json', 'datascriptor')

logging.basicConfig()
logger = logging.getLogger('logger')
logger.warning('warning-message')

logger.debug(MTBLS_ASSAY_DEF_FILE)


def update_current_file(input_file):
    try:

        new_folder_name = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        dst = os.path.join('resources/mtbls', new_folder_name)

        if os.path.exists(os.path.join('resources/mtbls', new_folder_name)):
            if ".tsv" in input_file:
                shutil.move(MTBLS_ASSAY_DEF_FILE, os.path.join(dst, "MetaboLightsAssayMaster.tsv.previous"))
                shutil.move(input_file, os.path.join('resources/mtbls/current', "MetaboLightsAssayMaster.tsv"))
                latest_version =  os.path.join('resources/mtbls/current', "MetaboLightsAssayMaster.tsv")
            elif ".owl" in input_file:
                shutil.move(MTBLS_CV_OWL, os.path.join(dst, "Metabolights.owl.previous"))
                shutil.move(input_file, os.path.join('resources/mtbls/current', "Metabolights.owl"))
                latest_version = os.path.join('resources/mtbls/current', "Metabolights.owl")

        else:
            os.makedirs(os.path.join('resources/mtbls', new_folder_name))
            if ".tsv" in input_file:
                shutil.move(MTBLS_ASSAY_DEF_FILE, os.path.join(dst, "MetaboLightsAssayMaster.tsv.previous"))
                shutil.move(input_file, os.path.join('resources/mtbls/current', "MetaboLightsAssayMaster.tsv"))
                latest_version = os.path.join('resources/mtbls/current', "MetaboLightsAssayMaster.tsv")
            elif ".owl" in input_file:
                shutil.move(MTBLS_CV_OWL, os.path.join(dst, "Metabolights.owl.previous"))
                shutil.move(input_file, os.path.join('resources/mtbls/current', "Metabolights.owl"))
                latest_version = os.path.join('resources/mtbls/current', "Metabolights.owl")

    except IOError as ioe:
        logger.error(ioe)

    return latest_version

def check_file_for_updates(old_file, resource_url):

    try:
        if ".tsv" in resource_url:
            MTBLS_MASTER_LATEST = os.path.join(MTBLS_TMPDIR, 'MetaboLightsAssayMaster-latest.tsv')
            MTBLS_MASTER_URL = requests.get(resource_url)
            MTBLS_MASTER_DL = open(MTBLS_MASTER_LATEST, 'wb').write(MTBLS_MASTER_URL.content)

            new_master_file_sha256 = sha256_checksum(MTBLS_MASTER_LATEST)
            old_master_file_sha256 = sha256_checksum(old_file)

            if old_master_file_sha256 == new_master_file_sha256:
                mtbls_master_file = old_file

            else:
                mtbls_master_file = MTBLS_MASTER_LATEST
                mtbls_master_file = update_current_file(mtbls_master_file)

        elif ".owl" in resource_url:
            MTBLS_MASTER_LATEST = os.path.join(MTBLS_TMPDIR, 'Metabolights-Ontology-latest.owl')
            MTBLS_MASTER_URL = requests.get(resource_url)
            MTBLS_MASTER_DL = open(MTBLS_MASTER_LATEST, 'wb').write(MTBLS_MASTER_URL.content)
            new_master_file_sha256 = sha256_checksum(MTBLS_MASTER_LATEST)
            old_master_file_sha256 = sha256_checksum(old_file)

            if old_master_file_sha256 == new_master_file_sha256:
                mtbls_master_file = old_file

            else:
                mtbls_master_file = MTBLS_MASTER_LATEST
                mtbls_master_file = update_current_file(mtbls_master_file)

        else:
            exit()

    except ConnectionError as con_err:
        logger.error(con_err)

    return mtbls_master_file


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def load_terms_from_mtblds_owl(ontology_file):
    """
    a method to load all subclasses of Instruments from Metabolights.owl ontology file.
    :return:
    """
    vocab_graph = rdflib.Graph()
    try:
        ontofile_sha256 = sha256_checksum(ontology_file)
        vocab_graph.parse(owl_file, format='xml')
        class_labels = []
        mtbls_class = Resource(vocab_graph, URIRef("http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000283"))
        subclasses = list(mtbls_class.transitive_subjects(RDFS.subClassOf))

        for class_item in subclasses:
            if str(class_item.label()) not in class_labels:
                class_labels.append(str(class_item.label()))
    except IOError as g_ioe:
        logger.error(g_ioe)

    return class_labels, subclasses, ontofile_sha256


def build_params_slim(protocol_row_record, assay_dictionary, param_prefix, tech, mtbls_class_names,
                      mtbls_associated_subclasses, mtbls_owl_sha256):
    """
    a method too build an isa-create-mode assay dictionary
    :protocol_param protocol_row_record: a row corresponding to a protocol workflow definition
    as found MTBLSAssayMaster.tsv
    :protocol_param assay_dictionary: an isa-create-mode assay dictionary stub
    :return: assay_dictionary
    """
    # getting all subclasses of Instruments from Metabolights.owl

    def make_param_values(protocol_params, mtbls_associated_subclasses):

        for protocol_param in protocol_params:
            search_protocol_param = None
            if param_prefix in ["Mass Spectrometry Imaging"]:
                search_protocol_param = protocol_param
            elif param_prefix == "NMR Spectroscopy Imaging":
                search_protocol_param = protocol_param
            elif param_prefix == "Liquid Chromatography" and protocol_param == "Chromatography Instrument":
                search_protocol_param = "Liquid Chromatography Instrument Model"
            elif param_prefix == "Liquid Chromatography" and protocol_type == "chromatography":
                search_protocol_param = "Liquid Chromatography " + protocol_param
            elif param_prefix == "Liquid Chromatography" and protocol_type == "mass spectrometry":
                search_protocol_param = "Mass Spectrometry " + protocol_param
            elif param_prefix == "Gas Chromatography" and protocol_param == "Chromatography Instrument":
                search_protocol_param = "Gas" + " " + "Chromatography" + " " + "Instrument" + " " + "Model"
            elif param_prefix == "Gas Chromatography" and protocol_type == "chromatography" \
                    and protocol_param != "Chromatography Instrument":
                search_protocol_param = "Gas Chromatography " + protocol_param
            elif param_prefix == "Gas Chromatography" and protocol_type == "mass spectrometry":
                search_protocol_param = "Mass Spectrometry " + protocol_param
            elif param_prefix == "MALDI" and protocol_type == "mass spectrometry":
                search_protocol_param = "Mass Spectrometry " + protocol_param
            elif param_prefix == "SPE-IMS" and "mass spectrometry" in protocol_type:
                search_protocol_param = "Mass Spectrometry " + protocol_param
            elif tech == "GC-FID":
                search_protocol_param = "Gas Chromatography " + protocol_param
            elif tech == "LC-DAD":
                search_protocol_param = "Liquid Chromatography " + protocol_param
            elif param_prefix == "NMR":
                protocol_param = protocol_param.replace("NMR ", "")
                search_protocol_param = "NMR " + protocol_param
            elif param_prefix == "Capillary electrophoresis" and "instrument" in protocol_param:
                protocol_param = protocol_param.replace("CE Instrument", "Capillary electrophoresis")
                search_protocol_param = protocol_param
            elif param_prefix == "Capillary electrophoresis" and protocol_type == "mass spectrometry":
                search_protocol_param = "Mass Spectrometry " + protocol_param
            elif param_prefix == "Direct injection" and protocol_type == "mass spectrometry":
                search_protocol_param = "Mass Spectrometry " + protocol_param
            else:
                search_protocol_param = protocol_param

            param_setup[search_protocol_param] = { "description": "", "options": [], "values": [] }

            for this_element in mtbls_associated_subclasses:
                if str(this_element.label()).lower() == search_protocol_param.lower():
                    # getting all the subclasses for that matched parameter
                    param_values = list(this_element.transitive_subjects(RDFS.subClassOf))

                    # this is to skip the parent class
                    iter_param_values = iter(param_values)
                    next(iter_param_values)

                    # adding the found parameter uri to the list of context in the assay dictionary definition
                    iri = str(this_element.identifier)
                    assay_dictionary["@context"][search_protocol_param] = iri

                    for this_value in iter_param_values:
                        option = dict()
                        option.update({
                            'term': "",
                            'iri': None,
                            'source': None
                        })
                        option["iri"] = str(this_value.identifier)
                        option["term"] = str(this_value.label())
                        option["source"] = "Metabolights.owl"
                        param_setup[search_protocol_param]["options"].append(option)
        return param_setup

    for element in protocol_row_record:

        workflow_segment = []
        node_type = None

        # This is to create the protocol application segment of the workflow:
        if element != "" and "|" in element:

            (protocol_type, parameters) = element.split("|")

            protocol_type = protocol_type.lower()

            if protocol_type not in ["sample collection",
                                     "data transformation",
                                     "histology",
                                     "metabolite identification",
                                     "nmr assay"]:
                workflow_segment.append({"term": protocol_type, "iri": None, "source": None})
            if "sample collection" in protocol_type:
                node_type = None
                # node_type = ["sample",
                #              {
                #                  "node_type": "sample",
                #                  "characteristics_category": "sample type",
                #                  "characteristics_value": {
                #                      "options": ["aliquot", "other"],
                #                      "values": []
                #                  },
                #                  "is_input_to_next_protocols": {
                #                      "value": True
                #                  }
                #              }]
            if "preparation" in protocol_type:
                node_type = None
            if protocol_type == "histology":
                node_type = None
            if protocol_type == "data transformation":
                node_type = None
            if "extraction" in protocol_type and "solid" not in protocol_type:
                node_type = ["extract", {
                        "node_type": "extract",
                        "characteristics_category": "extract type",
                        "characteristics_value": {
                            "options": ["polar fraction", "non-polar fraction"],
                            "values": []
                        },
                        "is_input_to_next_protocols": {
                            "value": True
                        }
                    }]
            if "labeling" in protocol_type or "labelling" in protocol_type:
                node_type = ["labeled extract", {
                        "node_type": "labeled extract",
                        "characteristics_category": "labeled extract type",
                        "characteristics_value": {
                            "options": [
                                "label_0", "label_1"
                            ],
                            "values": []
                        },
                        "is_input_to_next_protocols": {
                            "value": True
                        }
                    }
                ]
            if "nmr spectroscopy" in protocol_type:
                node_type = [
                            {
                                "term": "raw spectral data file",
                                "iri": "http://nmrML.org/nmrCV#NMR:1400119",
                                "source": None
                            },
                            {
                                "node_type": "data file",
                                "is_input_to_next_protocols": {
                                    "value": True
                                }
                            }
                        ]
            if "mass spectrometry" in protocol_type:
                node_type = [
                            {
                                "term": "raw spectral data file",
                                "iri": "http://purl.obolibrary.org/obo/MS_1003083",
                                "source": None
                            },
                            {
                                "node_type": "data file",
                                "is_input_to_next_protocols": {
                                    "value": True
                                }
                            }
                        ]
            if tech == "LC-DAD" and "chromatography" in protocol_type:
                node_type = [
                            {
                                "term": "raw data file",
                                "iri": "",
                                "source": None
                            },
                            {
                                "node_type": "data file",
                                "is_input_to_next_protocols": {
                                    "value": True
                                }
                            }
                        ]
            if "Gas Chromatography" in param_prefix and tech == "GC-FID" and "chromatography" in protocol_type:
                node_type = [
                            {
                                "term": "raw data file",
                                "iri": "",
                                "source": None
                            },
                            {
                                "node_type": "data file",
                                "is_input_to_next_protocols": {
                                    "value": True
                                }
                            }
                        ]
            if "in vivo magnetic resonance assay" in protocol_type:
                node_type = [
                    {
                        "term": "raw spectral data file",
                        "iri": "http://purl.obolibrary.org/obo/MS_1003083",
                        "source": None
                    },
                    {
                        "node_type": "data file",
                        "is_input_to_next_protocols": {
                            "value": True
                        }
                    }
                ]

            param_setup = {}
            protocol_params = parameters.split(";")

            if len(protocol_params) > 0 and protocol_params[0] != "" and \
                    protocol_type not in ["data transformation", "histology"]:
                param_setup["#replicates"] = {
                        "value": 1
                }

                # build the list of allowed parameter values from the MTBLS ontology
                param_setup = make_param_values(protocol_params, mtbls_associated_subclasses)

                # add to the assay protocol workflow section being built
                workflow_segment.append(param_setup)

            if workflow_segment:
                assay_dictionary["workflow"].append(workflow_segment)

        # This is to add the output Node of the protocol:
        if node_type is not None:
                assay_dictionary["workflow"].append(node_type)

    return assay_dictionary


def parse_mtbls_assay_def(file, mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256 ):
    """
    parsing the MetabolightsAssayMaster.tsv definition,
    making a lookup on the StudyTerms4Curators-template.xlsx file with one sheet per assay type,
    to obtain parameter values
    """
    all_assays = []
    try:
        mtbls_assaymaster_sha256 = sha256_checksum(MTBLS_ASSAY_DEF_FILE)

        with open(file) as tsvfile:
            assay_master = csv.reader(tsvfile, delimiter='\t')
            counter = 0
            for row in assay_master:
                if "-protocol" in row[0]:
                    protocol_row = row
                    tech_type = row[0].partition("-protocol  ")[0]
                    assay_dict = OrderedDict()

                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if "NMR" in tech_type:
                            assay_dict["id"] = counter
                            assay_dict["name"] = "metabolite profiling by NMR"
                            assay_dict["icon"] = "fas fa-atom"
                            assay_dict["color"] = "orange"
                            assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                            assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                            assay_dict["creation_date"] = now
                            assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                              "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                              "source": "OBI"}
                            assay_dict["technology_type"] = {"term": "NMR spectroscopy",
                                                             "uri": "http://purl.obolibrary.org/obo/OBI_0000623",
                                                             "source": "OBI"}
                            assay_dict["workflow"] = []
                            assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                      "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                            assay_param_prefix = "NMR"
                            assay_dict = build_params_slim(protocol_row, assay_dict, assay_param_prefix,
                                                           tech_type, mtbls_class_names, mtbls_associated_subclasses,
                                                           mtbls_owl_sha256)
                            all_assays.append(assay_dict)

                            counter += 1

                    elif "MRImaging" in tech_type:
                            assay_dict["id"] = counter
                            assay_dict["name"] = "metabolite spatial distribution imaging using NMR spectroscopy"
                            assay_dict["icon"] = "fas fa-atom"
                            assay_dict["color"] = "orange"
                            assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                            assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                            assay_dict["creation_date"] = now
                            assay_dict["measurement_type"] = {"term": "metabolite spatial distribution imaging",
                                                              "uri": "http://purl.obolibrary.org/obo/OBI_0000185",
                                                              "source": "OBI"}
                            assay_dict["technology_type"] = {"term": "NMR spectroscopy",
                                                             "uri": "http://purl.obolibrary.org/obo/OBI_0000623",
                                                             "source": "OBI"}
                            assay_dict["workflow"] = []
                            assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                      "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                            # assay_param_prefix = "NMRImaging"
                            param_prefix = "NMR Spectroscopy Imaging"
                            assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                           mtbls_class_names, mtbls_associated_subclasses,
                                                           mtbls_owl_sha256)
                            all_assays.append(assay_dict)

                            counter += 1

                    elif "LC-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by LC-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "blue"

                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "liquid chromatography mass spectrometry",
                                                         "uri": "http://purl.obolibrary.org/obo/OBI_0000051",
                                                         "source": "OBI"}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        assay_param_prefix = "Liquid Chromatography"
                        assay_dict = build_params_slim(protocol_row, assay_dict, assay_param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "MSImaging" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "imaging by MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "imaging",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000185",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "mass spectrometry",
                                                         "uri": "http://purl.obolibrary.org/obo/OBI_0000470",
                                                         "source": "OBI"}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "Mass Spectrometry Imaging"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "GC-MS" in tech_type and "GCxGC" not in tech_type and "TD-GC" not in tech_type:
                            assay_dict["id"] = counter
                            assay_dict["name"] = "metabolite profiling by GC-MS"
                            assay_dict["icon"] = "fas fa-chart-bar"
                            assay_dict["color"] = "light-blue"
                            assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                            assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                            assay_dict["creation_date"] = now
                            assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                              "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                              "source": "OBI"}
                            assay_dict["technology_type"] = {"term": "gas chromatography mass spectrometry",
                                                             "uri": "http://purl.obolibrary.org/obo/OBI_0200199",
                                                             "source": "OBI"}
                            assay_dict["workflow"] = []
                            assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                      "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                            param_prefix = "Gas Chromatography"
                            assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                           mtbls_class_names, mtbls_associated_subclasses,
                                                           mtbls_owl_sha256)
                            all_assays.append(assay_dict)
                            counter += 1

                    elif "DI-MS" in tech_type and "MALDI" not in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by DI-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "direct infusion mass spectrometry",
                                                         "uri": "",
                                                         "source": ""}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "Direct injection"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "FIA-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by FIA-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "flow injection mass spectrometry",
                                                         "uri": "",
                                                         "source": ""}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "Direct injection"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "CE-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by CE-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "capillary electrophoresis mass spectrometry",
                                                         "uri": "",
                                                         "source": ""}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "Capillary electrophoresis"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "MALDI-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by MALDI-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "maldi mass spectrometry",
                                                         "uri": "http://purl.obolibrary.org/obo/CHMO_0000519",
                                                         "source": "CHMO"}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "MALDI"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "SPE-IMS-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by SPE-IMS-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "solid-phase extraction ion mobility mass spectrometry"
                                                       , "uri": "http://purl.obolibrary.org/obo/CHMO_0000499",
                                                         "source": "CHMO"}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "SPE-IMS"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "GCxGC-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by GCxGC-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "tandem gas chromatography mass spectrometry",
                                                         "uri": "http://purl.obolibrary.org/obo/CHMO_0002862",
                                                         "source": "CHMO"}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "Gas Chromatography"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "LC-DAD" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by LC-DAD"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "liquid chromatography diode-array-detector",
                                                         "uri": "http://purl.obolibrary.org/obo/CHMO_0001738",
                                                         "source": "CHMO"}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "Liquid Chromatography"
                        tech_type = "LC-DAD"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "GC-FID" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by GC-FID"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "gas chromatography flame-ionization-detector",
                                                         "uri": "http://purl.obolibrary.org/obo/CHMO_0001736",
                                                         "source": "CHMO"}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "Gas Chromatography"
                        tech_type = "GC-FID"
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

                    elif "TD-GC-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by tandem gas chromatography mass-spectrometry"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["mtbls_owl_sha256"] = str(mtbls_owl_sha256)
                        assay_dict["mtbls_assaymaster_sha256"] = mtbls_assaymaster_sha256
                        assay_dict["creation_date"] = now
                        assay_dict["measurement_type"] = {"term": "metabolite profiling",
                                                          "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
                                                          "source": "OBI"}
                        assay_dict["technology_type"] = {"term": "gas chromatography-tandem mass spectrometry",
                                                         "uri": "http://purl.obolibrary.org/obo/CHMO_0002862",
                                                         "source": "CHMO"}
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        param_prefix = "Gas Chromatography"
                        tech_type = ""
                        assay_dict = build_params_slim(protocol_row, assay_dict, param_prefix, tech_type,
                                                       mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256)
                        all_assays.append(assay_dict)
                        counter += 1

        return all_assays

    except IOError as ioe:
        logger.error(ioe)


if __name__ == "__main__":

    assay_file = check_file_for_updates(MTBLS_ASSAY_DEF_FILE, "https://raw.githubusercontent.com/EBI-Metabolights/MtblsWS-Py/master/resources/MetaboLightsAssayMaster.tsv")

    owl_file = check_file_for_updates(MTBLS_CV_OWL, "https://raw.githubusercontent.com/EBI-Metabolights/Ontology/master/Metabolights.owl")

    mtbls_class_names, mtbls_associated_subclasses, mtbls_owl_sha256 = load_terms_from_mtblds_owl(owl_file)
    output = os.path.join(RESOURCES_MTBLS_DIR, "mtbls_isa_assay_ds_config.json")

    with open(output, 'w') as config_file:
        json.dump(parse_mtbls_assay_def(assay_file, mtbls_class_names,
                                        mtbls_associated_subclasses,
                                        mtbls_owl_sha256),  config_file, indent=4)
