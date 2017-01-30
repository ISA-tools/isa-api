import unittest
import os
import json
from isatools import isajson
from isatools.io import mtbls as MTBLS
from io import StringIO
from jsonschema.exceptions import ValidationError
from tests import utils as test_utils
from isatools import utils
from isatools.model.v1 import OntologySource, OntologyAnnotation


def setUpModule():
    if not os.path.exists(test_utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(test_utils.DATA_DIR))


class TestIsaGraph(unittest.TestCase):

    def test_detect_graph_process_pooling(self):
        ISA = isajson.load(open(os.path.join(test_utils.JSON_DATA_DIR, 'MTBLS1', 'MTBLS1.json')))
        for study in ISA.studies:
            print("Checking {}".format(study.filename))
            utils.detect_graph_process_pooling(study.graph)
            for assay in study.assays:
                print("Checking {}".format(assay.filename))
                pooling_list = utils.detect_graph_process_pooling(assay.graph)
                self.assertListEqual(sorted(pooling_list),
                                     sorted(['#process/Extraction1', '#process/ADG_normalized_data.xlsx']))

    def test_detect_graph_process_pooling_batch_on_mtbls(self):
        for i in range(1, 1):
            try:
                print("Loading MTBLS{}".format(i))
                J = MTBLS.getj("MTBLS{}".format(i))
                ISA = isajson.load(StringIO(json.dumps(J)))
                for study in ISA.studies:
                    print("Checking {}".format(study.filename))
                    utils.detect_graph_process_pooling(study.graph)
                    for assay in study.assays:
                        print("Checking {}".format(assay.filename))
                        utils.detect_graph_process_pooling(assay.graph)
            except IOError:
                print("IO Error, skipping...")
            except KeyError:
                print("KeyError, skipping...")
            except AttributeError:
                print("AttributeError, skipping...")
            except ValidationError:
                print("jsonschema ValidationError, skipping...")


class TestOlsSearch(unittest.TestCase):

    def test_get_ontologies(self):
        ontology_sources = utils.get_ols_ontologies()
        self.assertGreater(len(ontology_sources), 0)
        self.assertIsInstance(ontology_sources, list)
        self.assertIsInstance(ontology_sources[0], OntologySource)

    def test_get_ontology(self):
        ontology_source = utils.get_ols_ontology("efo")
        self.assertIsInstance(ontology_source, OntologySource)
        self.assertEqual(ontology_source.name, "efo")
        self.assertEqual(ontology_source.file, None)
        self.assertEqual(ontology_source.version, "2.80")
        self.assertEqual(ontology_source.description, "Experimental Factor Ontology")

    def test_search_for_term(self):
        ontology_source = utils.get_ols_ontology("efo")
        ontology_annotations = utils.search_ols("cell type", ontology_source)
        self.assertIsInstance(ontology_annotations, list)
        self.assertGreater(len(ontology_annotations), 0)
        ontology_anotation = [oa for oa in ontology_annotations if oa.term == "cell type"][0]  # always do a search, as order is not immutable
        self.assertIsInstance(ontology_anotation, OntologyAnnotation)
        self.assertEqual(ontology_anotation.term, "cell type")
        self.assertEqual(ontology_anotation.term_accession, "http://www.ebi.ac.uk/efo/EFO_0000324")
        self.assertEqual(ontology_anotation.term_source, ontology_source)
