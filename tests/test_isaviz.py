from __future__ import absolute_import
import io
import os
import shutil
import tempfile
import unittest

from isatools import isatab
from isatools import isaviz


class TestIsaVizualization(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self._tab_data_dir = os.path.join(os.path.dirname(__file__), 'data',
                                          'tab')
        self.parser = isatab.Parser()
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
            self.parser.parse(fp)

        self.study = next(iter(self.parser.isa.studies))
        self.assay = next(iter(self.study.assays))

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_make_study_summary(self):
        isaviz.make_study_summary(self.study, self.tmp_dir)
        self.assertTrue(
            os.path.isfile(os.path.join(self.tmp_dir,
                                        '{}.png'.format(next(iter(
                                            os.path.splitext(
                                                self.study.filename)))))))

    def test_make_assay_summary(self):
        isaviz.make_assay_summary(self.assay, self.tmp_dir)
        self.assertTrue(
            os.path.isfile(os.path.join(self.tmp_dir,
                                        '{}.png'.format(next(iter(
                                            os.path.splitext(
                                                self.assay.filename)))))))