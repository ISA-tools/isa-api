"""Tests for importing from SRA XML 1.5 to ISA-Tab"""

import os
import shutil
import tempfile
import unittest
import warnings
import zipfile
from io import BytesIO
from os import listdir, path, remove, walk
from pathlib import Path
from unittest.mock import MagicMock, patch

from isatools.net import sra2isatab
from isatools.tests import utils

SLOW_TESTS = int(os.getenv("SLOW_TESTS", "0"))

# TODO: If java is not present the slow test will fail. A check ought to be incorporated.


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError(
            f"Could not fine test data directory in {utils.DATA_DIR}. Ensure you have cloned "
            "the data repository using "
            "git clone -b tests --single-branch "
            f"git@github.com:ISA-tools/data {utils.DATA_DIR}"
        )


class TestZipDir(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file1 = os.path.join(self.test_dir.name, "file1.txt")
        self.test_file2 = os.path.join(self.test_dir.name, "file2.txt")

        # Create some dummy files
        with open(self.test_file1, "w") as f:
            f.write("Hello from file 1")
        with open(self.test_file2, "w") as f:
            f.write("Hello from file 2")

        # Temp file for zip
        self.zip_path = os.path.join(self.test_dir.name, "test.zip")
        self.zip_file = zipfile.ZipFile(self.zip_path, "w")

    def tearDown(self):
        self.zip_file.close()
        self.test_dir.cleanup()

    def test_zipdir_adds_all_files(self):
        sra2isatab.zipdir(self.test_dir.name, self.zip_file)
        self.zip_file.close()

        # Open the zip and verify contents
        with zipfile.ZipFile(self.zip_path, "r") as z:
            names = z.namelist()

            # Only the files should be in the zip, not the zip itself
            self.assertIn("file1.txt", [os.path.basename(n) for n in names])
            self.assertIn("file2.txt", [os.path.basename(n) for n in names])


class TestSraImport(unittest.TestCase):
    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    # https://www.ebi.ac.uk/ena/data/view/SRA108974&amp;display=xml

    @unittest.skipIf(not SLOW_TESTS, "slow")
    def test_sra_import(self):
        # TODO: Complete the offline fixtures and reconcile their XML structure with the XSLT.
        # Saxon exits with code 0, but the ZIP contains only
        # i_SRA108974.txt and s_SRA108974.txt; a_wgs-genomic.txt is missing.
        # Saxon reports FODC0002 warnings for missing local records:
        # SRP032345, SRS494979-SRS495064, SRS495322-SRS495494,
        # SRS495496-SRS495499 and SRS495504-SRS495640.
        # The current SRA108974.xml has a bare SUBMISSION root and experiment links,
        # whereas extract-studies.xsl selects /SUBMISSION_SET/SUBMISSION.
        # That mismatch prevents experiment discovery and assay generation. Restoring
        # the expected wrapper will also require fixtures for the linked experiments.
        # The previously inspected ROOT wrapper has the same XPath mismatch; the
        # newly retrieved SUBMISSION_SET response contained only file-report links,
        # without the study, sample and experiment links required for conversion.
        # Keep all linked XML and file-report lookups local when completing fixtures.
        # tests/data belongs to the separate ISAdatasets repository and is replaced
        # by get_test_data.sh, so preserve fixture changes before refreshing it.
        # Temporary ERROR-level diagnostics in sra2isatab.py capture Saxon's exit
        # code, stdout and stderr; remove them once diagnosis is complete. Exit code
        # 0 alone does not guarantee complete output or the absence of warnings.
        # To reproduce, enable SLOW_TESTS=1 and use # isa-api .venv,
        # running this test with -s --log-cli-level=INFO.
        fixture_dir = Path(utils.SRA_DATA_DIR) / "SRA108974"
        local_data_dir = Path(self._tmp_dir) / "ena"
        local_data_dir.mkdir()
        for fixture in fixture_dir.glob("*.xml"):
            # ENA URLs end with the accession rather than an XML file extension.
            shutil.copyfile(fixture, local_data_dir / fixture.stem)
        self.assertTrue((local_data_dir / "SRA108974").is_file())

        stylesheet_dir = Path(self._tmp_dir) / "stylesheets"
        shutil.copytree(sra2isatab.SRA_DIR, stylesheet_dir)
        local_data_uri = local_data_dir.as_uri() + "/"
        for stylesheet in stylesheet_dir.glob("*.xsl"):
            # Preserve the original stylesheet encoding and use local files for all ENA XML lookups.
            content = stylesheet.read_bytes().replace(
                b"https://www.ebi.ac.uk/ena/browser/api/xml/", local_data_uri.encode("ascii")
            )
            # File-report URLs embedded in XML must also resolve locally, without a network fallback.
            content = content.replace(
                b"unparsed-text($link)",
                f"unparsed-text(concat('{local_data_uri}', encode-for-uri($link), '.txt'))".encode("ascii"),
            )
            stylesheet.write_bytes(content)

        local_stylesheet = stylesheet_dir / Path(sra2isatab.STUDY_XSL_FILE).name
        with patch.object(sra2isatab, "STUDY_XSL_FILE", str(local_stylesheet)):
            zipped_bytes = sra2isatab.sra_to_isatab_batch_convert("SRA108974")
        with open(os.path.join(self._tmp_dir, "o.zip"), "wb") as zip_fp:
            shutil.copyfileobj(zipped_bytes, zip_fp, length=131072)

        with zipfile.ZipFile(os.path.join(self._tmp_dir, "o.zip"), "r") as zip_fp:
            self.assertListEqual(
                sorted([os.path.basename(x) for x in zip_fp.namelist()]),
                ["a_wgs-genomic.txt", "i_SRA108974.txt", "s_SRA108974.txt"],
            )

    @patch("subprocess.call")
    def test_sra_import_mocked(self, mock_call):
        with self.assertRaises(FileNotFoundError, msg="as subprocess.call is mocked files are nor generated"):
            sra2isatab.sra_to_isatab_batch_convert("SRA108974")
            mock_call.assert_called_with("java", "-jar")
