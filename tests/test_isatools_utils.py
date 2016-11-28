import unittest
from isatools import utils, isajson


class TestIsaGraph(unittest.TestCase):

    def test_detect_graph_process_pooling(self):
        ISA = isajson.load(open('/Users/dj/PycharmProjects/isa-api/tests/data/json/MTBLS1/MTBLS1.json'))
        for study in ISA.studies:
            print("Checking {}".format(study.filename))
            utils.detect_graph_process_pooling(study.graph)
            for assay in study.assays:
                print("Checking {}".format(assay.filename))
                utils.detect_graph_process_pooling(assay.graph)
