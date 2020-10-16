from __future__ import absolute_import
import os
import csv
from collections import OrderedDict
import pandas as pd
import json
import rdflib

from rdflib import *
import logging

from rdflib.resource import Resource

__author__ = ['philippe.rocca-serra@oerc.ox.ac.uk']

MTBLS_DIR = os.path.join(os.path.dirname(__file__), 'resources', 'mtbls')
MTBLS_FILE = 'MetaboLightsAssayMaster.tsv'
MTBLS_CV_FILE = os.path.join(MTBLS_DIR, 'StudyTerms4Curators-template.xlsx')
MTLBS_CV_OWL = os.path.join(MTBLS_DIR, 'Metabolights.owl')

MTBLS_ASSAY_DEF_FILE = os.path.join(MTBLS_DIR, MTBLS_FILE)

print(MTBLS_ASSAY_DEF_FILE)

XLS_LOOKUP = pd.ExcelFile(MTBLS_CV_FILE)

logging.basicConfig()
logger = logging.getLogger('logger')
logger.warning('warning-message')


def load_terms_from_mtblds_owl():
    """
    a method to load all subclasses of Instruments from Metabolights.owl ontology file.
    :return:
    """
    vocab_graph = rdflib.Graph()
    try:
        vocab_graph.parse(MTLBS_CV_OWL, format='xml')
        class_labels = []
        mtbls_class = Resource(vocab_graph, URIRef("http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000283"))
        subclasses = list(mtbls_class.transitive_subjects(RDFS.subClassOf))

        for c in subclasses:
            # l = list(c.objects(RDFS.label))
            # print("class name:", c.label(), "| uri: ", c)
            if str(c.label()) not in class_labels:
                class_labels.append(str(c.label()))

    except IOError as g_ioe:
        print("error reading graph:", g_ioe)

    return class_labels, subclasses


def build_params(protocol_row_record, assay_dictionary, datafr):
    """
    a method too build an isa-create-mode assay dictionary
    :protocol_param protocol_row_record: a row corresponding to a protocol workflow definition
    as found MTBLSAssayMaster.tsv
    :protocol_param assay_dictionary: an isa-create-mode assay dictionary stub
    :protocol_param datafr: a pandas dataframe obtained from looking up sheet in StudyTerms4Curators-template.xlsx
    :return:
    """
    # getting all subclasses of Instruments from Metabolights.owl
    class_names, associated_subclasses = load_terms_from_mtblds_owl()
    # print("from ontology:", class_names)

    for element in protocol_row_record:
        workflow_segment = []
        if element is not "" and "|" in element:
            (protocol_type, parameters) = element.split("|")
            protocol_type = protocol_type.lower()
            workflow_segment.append({"term": protocol_type, "iri": None, "source": None})

            if "sample collection" in protocol_type:
                node_type = ["sample",
                             {
                                 "node_type": "sample",
                                 "characteristics_category": "sample type",
                                 "characteristics_value": {
                                     "options": ["aliquot", "other"],
                                     "values": []
                                 },
                                 "is_input_to_next_protocols": {
                                     "value": True
                                 }
                             }]
            elif "extraction" in protocol_type:
                node_type = ["extract",
                    {
                        "node_type": "extract",
                        "characteristics_category": "extract type",
                        "characteristics_value": {
                            "options": ["polar fraction", "nonpolar fraction"],
                            "values": []
                        },
                        "is_input_to_next_protocols": {
                            "value": True
                        }
                    }]
            elif "labeling" in protocol_type or "labelling" in protocol_type:
                node_type = [
                "labeled extract",
                    {
                        "node_type": "labeled extract",
                        "characteristics_category": "labelled extract type",
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
            elif "nmr spectroscopy" in protocol_type:
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
            elif "mass spectrometry" in protocol_type:
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
            else:
                node_type = None

            protocol_params = parameters.split(";")
            param_setup = {}

            if len(protocol_params) > 0 and protocol_params[0] is not "":

                param_setup["replicates"] = {
                        "value": 1
                    }

                for protocol_param in protocol_params:
                    # print("This particular protocol parameter:", protocol_param)
                    param_setup[protocol_param] = {"options": [], "values": []}
                    # checking if protocol parameter name is also present in the ontology
                    # if protocol_param in class_names:
                    #     print("protocol_param: ", protocol_param, "|", class_names)
                    #     # print("index", class_labels.index(protocol_param), class_labels[class_labels.index(protocol_param)])
                    #     this_param_class = associated_subclasses[class_names.index(protocol_param)]
                    #     print("THIS class:", this_param_class)
                    #     param_values = list(this_param_class.transitive_subjects(RDFS.subClassOf))
                    #     for this_value in param_values:
                    #         print("element v2:", this_value.label(), this_value)
                    # else:
                    #     print("no class found:  ", protocol_param)
                    #     next()

                    # param_values = ()

                    # obtaining the list of protocol parameters and if any, getting values
                    # from the relevant assay spreadsheet
                    for field in datafr.columns:

                        if protocol_param in field:

                            for c in associated_subclasses:
                                if c.label() in field:
                                    iri = str(c.identifier)
                                    assay_dictionary["@context"][protocol_param] = iri

                            for value in datafr[field].unique():
                                option = {"term": "", "iri": None, "source": None}
                                if pd.isna(value) is False:
                                    if isinstance(value, int) is False or isinstance(value, float) is False:
                                        option["term"] = str(value)
                                        for c in associated_subclasses:
                                            if c.label() in field:
                                                option["iri"] = str(c.identifier)
                                        param_setup[protocol_param]["options"].append(option)

                                    else:
                                        option["term"] = value
                                        param_setup[protocol_param]["options"].append(option)
                else:
                    param_setup["replicates"] = {
                        "value": 1
                    }

                workflow_segment.append(param_setup)

            assay_dictionary["workflow"].append(workflow_segment)
            if node_type is not None:
                    assay_dictionary["workflow"].append(node_type)

    return assay_dictionary


def parse_mtbls_assay_def(file):
    """
    parsing the MetabolightsAssayMaster.tsv definition,
    making a lookup on the StudyTerms4Curators-template.xlsx file with one sheet per assay type,
    to obtain parameter values
    """
    all_assays = []
    try:
        with open(file) as tsvfile:
            assay_master = csv.reader(tsvfile, delimiter='\t')
            counter = 0
            for row in assay_master:
                if "-protocol" in row[0]:
                    protocol_row = row
                    tech_type = row[0].partition("-protocol  ")[0]
                    assay_dict = OrderedDict()

                    if "NMR" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by NMR"
                        assay_dict["icon"] = "fas fa-atom"
                        assay_dict["color"] = "orange"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "NMR spectroscopy"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, 'NMR Study')

                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)

                        counter += 1

                    if "LC-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by LC-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "liquid chromatography mass spectrometry"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, 'LC-MS Study')
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

                    if "GC-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by GC-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "gas chromatography mass spectrometry"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, "GC-MS Study")
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

                    if "DI-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by DI-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "direct infusion mass spectrometry"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, "DI-MS Study")
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

                    if "FIA-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by FIA-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "flow injection mass spectrometry"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, "FIA-MS Study")
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

                    if "CE-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by FIA-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "capillary electrophoresis mass spectrometry"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, "CE-MS Study")
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

                    if "MALDI-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by FIA-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "maldi mass spectrometry"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, "MALDI-MS Study")
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

                    if "SPE-IMS-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by FIA-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "solid-phase extraction ion mobility mass spectrometry"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, "SPE-IMS-MS Study")
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

                    if "GCxGC-MS" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by FIA-MS"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "tandem gas chromatography mass spectrometry"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, "GCxGC-MS Study")
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

                    if "LC-DAD" in tech_type:
                        assay_dict["id"] = counter
                        assay_dict["name"] = "metabolite profiling by LC-DAD"
                        assay_dict["icon"] = "fas fa-chart-bar"
                        assay_dict["color"] = "light-blue"
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "liquid chromatography diode-array-detector"
                        assay_dict["workflow"] = []
                        assay_dict["@context"] = {"measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                                                  "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521"}
                        # obtain the list of parameter values by doing the lookup
                        param_df = pd.read_excel(XLS_LOOKUP, "LC-DAD Study")
                        assay_dict = build_params(protocol_row, assay_dict, param_df)
                        all_assays.append(assay_dict)
                        counter += 1

        return all_assays

    except IOError as ioe:
        print("error reading assay definition file:", ioe)


if __name__ == "__main__":
    # assays = parse_mtbls_assay_def(MTBLS_ASSAY_DEF_FILE)
    # print(json.dumps(assay_dict, indent=4))
    print(json.dumps(parse_mtbls_assay_def(MTBLS_ASSAY_DEF_FILE), indent=4))
