import unittest
import tempfile
import shutil
import os
import logging
import time

from isatools import isatab
from isatools.net.biocrates2isa import DEFAULT_SAXON_EXECUTABLE
from isatools.net.biocrates2isa import DESTINATION_DIR
from isatools.net.biocrates2isa import biocrates_to_isatab_convert
from isatools.net.biocrates2isa import generate_maf_stub
from isatools.net.biocrates2isa import add_sample_metadata
from isatools.tests import utils


log = logging.getLogger('isatools')

__author__ = 'proccaserra@gmail.com'


class biocrates2ISATest(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        self._biocrates_data_dir = utils.BIOCRATES_DATA_DIR

    # def tearDown(self):
    #     shutil.rmtree(self._tmp_dir)

    def test_conversion2isa(self):

        success, biocrates_out_dir, validate = biocrates_to_isatab_convert(
            biocrates_filename='biocrates-merged-output.xml',
            saxon_jar_path=DEFAULT_SAXON_EXECUTABLE,
            outputdir=self._tmp_dir + "/" + DESTINATION_DIR,
            validate_option=True)

        # print("conversion status:", success)
        # print("\noutput directory:", biocrates_out_dir)
        # print("\nvalidation option:", validate)

        # exit_code = sys.exit()

        if success and validate:
            log.info("conversion successful, invoking the validator for " + biocrates_out_dir)
            with open(os.path.join(biocrates_out_dir, 'i_inv_biocrates.txt')) as fp:
                report = isatab.validate(fp)
                # print(report)
                if len(report['errors']) > 0:
                    self.fail("conversion successful but validation failed")
        elif success:
            log.info("conversion successful but not validated yet " + biocrates_out_dir)
        else:
            self.fail("conversion failed, validation was not invoked")

    def test_maf_file_creation(self):
        # with open(os.path.join(self._biocrates_data_dir, 'xml', 'biocrates-merged-output.xml')) as biocrates_xml:
        generate_maf_stub(biocrates_filename='biocrates-merged-output.xml',
                          inputdir=os.path.join(self._biocrates_data_dir, 'xml'),
                          outputdir=os.path.join(self._tmp_dir, 'maf_file'))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'maf_file',
                                                                'm_MTBLSXXX_KIT2-0-8015_1024503073_positive_maf.txt')))

    # def test_add_sample_metadata(self):
    #     with open(os.path.join(self._biocrates_data_dir, 'isa', 's_study_biocrates.txt')) as biocrates_isa_study:
    #         with open(os.path.join(self._biocrates_data_dir, 'metadata', 'EX0003_sample_metadata.csv')) as biocrates_meta:
    #                 add_sample_metadata(biocrates_meta, biocrates_isa_study)
    #                 # self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir,
    #                 #                                             's_study_biocrates_augmented.txt')))
