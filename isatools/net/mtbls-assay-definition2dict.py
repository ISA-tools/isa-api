import os
import csv
from collections import OrderedDict
import pandas as pd
import modin.pandas as pd_modin
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

xls = pd.ExcelFile(MTBLS_CV_FILE)

logging.basicConfig()
logger = logging.getLogger('logger')
logger.warning('warning: something went sideways')


def load_terms_from_owl():
    vocab_graph = rdflib.Graph()
    try:
        vocab_graph.parse(MTLBS_CV_OWL, format='xml')
        print(vocab_graph)
        class_labels = []
        mtbls_class = Resource(vocab_graph, URIRef("http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000283"))
        subclasses = list(mtbls_class.transitive_subjects(RDFS.subClassOf))

        for c in subclasses:
            # print("class name:", c.label())
            # l = list(c.objects(RDFS.label))
            class_labels.append(str(c.label()))

    except IOError as g_ioe:
        print("error reading graph:", g_ioe)

    return class_labels, subclasses

def build_params(record, assay_dictionary, datafr):

    # vocab_graph = rdflib.Graph()
    # try:
    #     vocab_graph.parse(MTLBS_CV_OWL, format='xml')
    #     print(vocab_graph)
    #     class_labels = []
    #     mtbls_class = Resource(vocab_graph, URIRef("http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000283"))
    #     subclasses = list(mtbls_class.transitive_subjects(RDFS.subClassOf))
    #
    #     for c in subclasses:
    #         print("class name:", c.label())
    #         # l = list(c.objects(RDFS.label))
    #         class_labels.append(str(c.label()))
    #
    #
    # except IOError as g_ioe:
    #     print("error reading graph:", g_ioe)
    class_names, these_subclasses = load_terms_from_owl()

    for element in record:
        if element is not "" and "|" in element:
            (protocol_type, parameters) = element.split("|")
            params = parameters.split(";")
            # param_settings = '{}'
            # param_settings_dict = {}
            param_value = {}
            if len(params) > 0 and params[0] is not "":
                protocol_type = protocol_type.lower()

                for param in params:
                    # print("class names: ", class_labels)
                    if param in class_names:
                        print("param: ", param, class_names)
                        # print("index", class_labels.index(param), class_labels[class_labels.index(param)])
                        this_param_class = these_subclasses[class_names.index(param)]
                        print("THIS class:", this_param_class)
                        param_values = list(this_param_class.transitive_subjects(RDFS.subClassOf))
                        for element in param_values:
                            # print("element v1:", element)
                            print("element v2:", element.label())
                    else:
                        print("no class found:  ", param)
                    param_values = ()
                    for field in datafr.columns:
                        # [expression for item in list if conditional]
                        [print("TOTO:", c.value(RDF.type).qname()) for c in these_subclasses if field==c.label()]

                        if param in field:
                            param_values = []
                            param_value[param] = []
                            param_settings = []
                            for value in datafr[field]:
                                if pd.isna(value) is False:
                                    # print("parameter value:", value) value.isdigit()
                                    if isinstance(value, int) is False or isinstance(value, float) is False:
                                        # param_values.append("OntologyAnnotation(term='" + str(value) + "')")
                                        param_values.append(str(value))
                                    else:
                                        param_values.append(value)

                            # param_value["OntologyAnnotation(TERM='" + param + "')"] = param_values
                            param_value[param] = param_values

            # print(protocol_type, param_settings)
            assay_dictionary[protocol_type] = param_value

    return assay_dictionary


def parse_mtbls_assay_def(file):
    # assay_defs = {}
    try:
        with open(file) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')

            for row in reader:
                techtype = ""

                if "-protocol" in row[0]:

                    techtype = row[0].partition("-protocol  ")[0]
                    #print("TECHTYPE:", techtype)

                    assay_dict = OrderedDict()
                    if "NMR" in techtype:
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "NMR spectroscopy"
                        param_df = pd.read_excel(xls, 'NMR Study')
                        assay_dict = build_params(row, assay_dict, param_df)

                        # print(assay_dict)
                        # print(json.dumps(assay_dict, indent=4))

                    if "LC-MS" in techtype:
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "gas chromatography mass spectrometry"
                        param_df = pd.read_excel(xls, 'LC-MS Study')
                        assay_dict = build_params(row, assay_dict, param_df)

                        # print(assay_dict)

                    if "GC-MS" in techtype:
                        assay_dict["measurement_type"] = "metabolite profiling"
                        assay_dict["technology_type"] = "liquid chromatography mass spectrometry"
                        param_df = pd.read_excel(xls, "GC-MS Study")
                        assay_dict = build_params(row, assay_dict, param_df)
                        assay_dict["raw_spectral_data_file"] = "[{'node_type': 'DATA_FILE','size': 1," \
                                                               "'technical_replicates': 1," \
                                                               "'is_input_to_next_protocols': False}]"
                        # print(assay_dict)

    except IOError as ioe:
        print("error reading assay definition file:", ioe)


if __name__ == "__main__":
    parse_mtbls_assay_def(MTBLS_ASSAY_DEF_FILE)
