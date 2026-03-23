import json
import logging
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from isatools import isatab
from isatools.net.mw2isa import mw2isa_convert

log = logging.getLogger("isatools")

__author__ = "proccaserra@gmail.com"


class mw2ISATest(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def _load_fixture(self, name):
        data_path = Path(__file__).parent / "fixtures" / name
        return data_path.read_bytes()

    def _make_requests_response(self, body_bytes, status=200, headers=None):
        m = Mock()
        m.status_code = status
        m.content = body_bytes
        m.text = body_bytes.decode("utf-8")

        # Provide .json() for convenience if used by code
        def _json():
            return json.loads(m.text)

        m.json = _json
        m.headers = headers or {}
        return m

    @patch("isatools.net.mw2isa.mw2isa_convert")
    def test_conversion_ms(self, mock_get):
        def _side_effect():
            return self._make_requests_response(self._load_fixture("ST000367.json"))

        mock_get.side_effect = _side_effect

        success, study_id, validate = mw2isa_convert(
            studyid="ST000367", outputdir=self._tmp_dir, dl_option="no", validate_option=True
        )
        if success and validate:
            log.info("conversion successful, invoking the validator for " + study_id)
            with open(os.path.join(self._tmp_dir, study_id, "i_investigation.txt")) as fp:
                report = isatab.validate(fp)
                print(report)
                for error in report["errors"]:
                    # print("ERROR:", error)
                    # self.assertEqual(error['code'], 4014)
                    # self.assertTrue(len(report['errors']) > 0)
                    self.assertIn(error["code"], [4003, 4014])

        else:
            self.fail("conversion failed, validation was not invoked")

    @patch("isatools.net.mw2isa.mw2isa_convert")
    def test_conversion_nmr(self, mock_get):
        def _side_effect():
            return self._make_requests_response(self._load_fixture("ST000102.json"))

        mock_get.side_effect = _side_effect

        success, study_id, validate = mw2isa_convert(
            studyid="ST000102", outputdir=self._tmp_dir, dl_option="no", validate_option=True
        )
        if success and validate:
            log.info("conversion successful, invoking the validator for " + study_id)
            with open(os.path.join(self._tmp_dir, study_id, "i_investigation.txt")) as fp:
                report = isatab.validate(fp)
                self.assertEqual(report["errors"][0]["code"], 1007)
        else:
            self.assertFalse(success)

    @patch("isatools.net.mw2isa.mw2isa_convert")
    def test_conversion_invalid_id(self, mock_get):
        def _side_effect():
            return self._make_requests_response(self._load_fixture("TOTO.json"))

        mock_get.side_effect = _side_effect

        success, study_id, validate = mw2isa_convert(
            studyid="TOTO", outputdir=self._tmp_dir, dl_option="no", validate_option=True
        )
        self.assertFalse(success)

    @patch("isatools.net.mw2isa.mw2isa_convert")
    def test_conversion_invalid_dloption(self, mock_get):
        def _side_effect():
            return self._make_requests_response(self._load_fixture("ST000102.json"))

        mock_get.side_effect = _side_effect

        with self.assertRaises(Exception) as context:
            success, study_id, validate = mw2isa_convert(
                studyid="ST000102", outputdir=self._tmp_dir, dl_option="TOTO", validate_option=False
            )
            self.assertFalse(success)
            self.assertTrue("invalid input, option not recognized" in context.exception)
