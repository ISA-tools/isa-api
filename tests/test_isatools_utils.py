"""Tests on isatools.utils package"""
from __future__ import absolute_import

import logging
import os
import shutil
import tempfile
import unittest


from isatools import isajson
from isatools import utils

from isatools.tests import utils as test_utils


log = logging.getLogger(__name__)


def setUpModule():
    if not os.path.exists(test_utils.DATA_DIR):
        raise IOError('Could not fine test data directory in {0}. '
                                'Ensure you have cloned the ISAdatasets '
                                'repository using git clone -b tests '
                                '--single-branch git@github.com:ISA-tools/'
                                'ISAdatasets {0}'
                                .format(test_utils.DATA_DIR))


class TestIsaGraph(unittest.TestCase):

    def test_detect_graph_process_pooling(self):
        with open(os.path.join(
                test_utils.JSON_DATA_DIR, 'MTBLS1', 'MTBLS1.json')) as \
                isajson_fp:
            ISA = isajson.load(isajson_fp)
            for study in ISA.studies:
                utils.detect_graph_process_pooling(study.graph)
                for assay in study.assays:
                    pooling_list = utils.detect_graph_process_pooling(
                        assay.graph)
                    self.assertListEqual(
                        sorted(pooling_list),
                        sorted(['#process/Extraction1', '#process/NMR_assay1']))


class TestISArchiveExport(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_create_isatab_archive_missing_files(self):
        with open(os.path.join(
                test_utils.TAB_DATA_DIR, 'BII-I-1', 
                'i_investigation.txt')) as fp:
            result = utils.create_isatab_archive(inv_fp=fp)
            self.assertIsNone(result)  # returns None if can't create archive

    def test_create_isatab_archive(self):
        with open(os.path.join(
                test_utils.TAB_DATA_DIR, 'BII-S-3', 'i_gilbert.txt')) as fp:
            result = utils.create_isatab_archive(inv_fp=fp)
            self.assertIsInstance(result, list)
            self.assertListEqual(sorted(result),
                                 sorted(['i_gilbert.txt', 
                                         's_BII-S-3.txt', 
                                         'a_gilbert-assay-Gx.txt',
                                         'a_gilbert-assay-Tx.txt', 
                                         'EXHS9OF02.sff', 'EXHS9OF01.sff',
                                         'EWOEPZA01.sff', 'EWOEPZA02.sff', 
                                         'EX398L101.sff', 'EX398L102.sff',
                                         'EVHINN105.sff', 'EVNG8PH04.sff', 
                                         'EVUSNDQ01.sff', 'EVHINN102.sff',
                                         'EVHINN113.sff', 'EVUSNDQ02.sff', 
                                         'EVHINN101.sff', 'EVNG8PH01.sff',
                                         'EVHINN106.sff', 'EVHINN108.sff', 
                                         'EVHINN116.sff', 'EVHINN104.sff',
                                         'EVHINN110.sff', 'EVHINN107.sff', 
                                         'EVUSNDQ03.sff', 'EVHINN103.sff',
                                         'EVHINN112.sff', 'EVUSNDQ04.sff', 
                                         'EVHINN115.sff', 'EVNG8PH02.sff',
                                         'EVHINN114.sff', 'EVHINN111.sff', 
                                         'EVNG8PH03.sff', 'EVHINN109.sff']))

    def test_create_isatab_archive_filter_on_transcription_profiling(self):
        with open(os.path.join(
                test_utils.TAB_DATA_DIR, 'BII-S-3', 'i_gilbert.txt')) as fp:
            result = utils.create_isatab_archive(
                inv_fp=fp, filter_by_measurement='transcription profiling')
            self.assertIsInstance(result, list)
            self.assertListEqual(sorted(result),
                                 sorted(['i_gilbert.txt', 's_BII-S-3.txt', 
                                         'a_gilbert-assay-Tx.txt', 
                                         'EVHINN105.sff', 'EVNG8PH04.sff', 
                                         'EVUSNDQ01.sff', 'EVHINN102.sff', 
                                         'EVHINN113.sff', 'EVUSNDQ02.sff', 
                                         'EVHINN101.sff', 'EVNG8PH01.sff', 
                                         'EVHINN106.sff', 'EVHINN108.sff', 
                                         'EVHINN116.sff', 'EVHINN104.sff', 
                                         'EVHINN110.sff', 'EVHINN107.sff', 
                                         'EVUSNDQ03.sff', 'EVHINN103.sff', 
                                         'EVHINN112.sff', 'EVUSNDQ04.sff', 
                                         'EVHINN115.sff', 'EVNG8PH02.sff', 
                                         'EVHINN114.sff', 'EVHINN111.sff', 
                                         'EVNG8PH03.sff', 'EVHINN109.sff']))
