import unittest
import os
from isatools import utils, isajson
from tests import utils as test_utils


class TestIsaGraph(unittest.TestCase):

    def test_detect_graph_process_pooling(self):
        ISA = isajson.load(open(os.path.join(test_utils.JSON_DATA_DIR, 'MTBLS1', 'MTBLS1.json')))
        for study in ISA.studies:
            print("Checking {}".format(study.filename))
            utils.detect_graph_process_pooling(study.graph)
            for assay in study.assays:
                print("Checking {}".format(assay.filename))
                utils.detect_graph_process_pooling(assay.graph)
