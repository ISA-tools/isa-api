from __future__ import absolute_import
import os
import json
import logging
import rdflib
from rdflib import URIRef, Graph, RDFS
from rdflib.resource import Resource


__author__ = ['philippe.rocca-serra@oerc.ox.ac.uk']

MTBLS_DIR = os.path.join(os.path.dirname(__file__), 'resources', 'mtbls')
MTBLS_FILE = 'MetaboLightsAssayMaster.tsv'
# MTBLS_CV_FILE = os.path.join(MTBLS_DIR, 'StudyTerms4Curators-template.xlsx')
MTLBS_CV_OWL = os.path.join(MTBLS_DIR, 'Metabolights.owl')

MTBLS_ASSAY_DEF_FILE = os.path.join(MTBLS_DIR, MTBLS_FILE)

# XLS_LOOKUP = pd.ExcelFile(MTBLS_CV_FILE)

logging.basicConfig()
logger = logging.getLogger('logger')
logger.warning('warning-message')

logger.debug(MTBLS_ASSAY_DEF_FILE)


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

        for class_item in subclasses:
            if str(class_item.label()) not in class_labels:
                # print(str(class_item.label()))
                class_labels.append(str(class_item.label()))

    except IOError as g_ioe:
        logger.error(g_ioe)

    return class_labels, subclasses


def test_graphnav(params):

    class_names, associated_subclasses = load_terms_from_mtblds_owl()
    assay_dictionary = {"@context": {}}
    param_setup = {}
    count_param = 0
    for param in params:
        count_param = count_param + 1

        # initilization of the object to include an override option
        param_setup[param] = {"options": [{"term": "user defined",
                                           "iri": None,
                                           "source": None}],
                              "values": []
                              }
        # looking for a match:
        for element in associated_subclasses:
            if str(element.label()) == param:

                # getting all the subclasses for that matched parameter
                param_values = list(element.transitive_subjects(RDFS.subClassOf))

                # this is to skip the parent class
                iter_param_values = iter(param_values)
                next(iter_param_values)

                # now forming the list of options for that parameter
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
                    param_setup[param]["options"].append(option)

                # adding the found parameter uri to the list of context in the assay dictionary definition
                iri = str(element.identifier)
                assay_dictionary["@context"][param] = iri

    return param_setup


if __name__ == "__main__":
    # assays = parse_mtbls_assay_def(MTBLS_ASSAY_DEF_FILE)

    parameterlist = ["NMR solvent", "NMR Instrument", "NMR tube type", "NMR Magnetic field strength", "NMR probe",  "NMR Pulse Sequence Name"]
    setup = test_graphnav(parameterlist)

    print(json.dumps(setup, indent=4))
