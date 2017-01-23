import unittest
import os
import json
from isatools import isajson
from isatools.io import mtbls as MTBLS
from io import StringIO
from jsonschema.exceptions import ValidationError
from tests import utils as test_utils
from isatools import utils


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
