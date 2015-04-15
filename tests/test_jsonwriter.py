import api
from io.reader import read

__author__ = 'Alfie Abdul-Rahman'

"""Tests for writing and parsing ISA-Tab JSON format.
"""
import os, unittest


class IsatabJsonTest(unittest.TestCase):
    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), "isatab-json")

    # currently just reading
    def test_basic_writing(self):
        """Test general parsing of an example ISA-Tab JSON directory.
        """
        work_dir = os.path.join(self._dir, "BII-I-1_json")
        json_data = read(work_dir)
        assert json_data["investigation"]["investigationIdentifier"] == "BII-I-1"
        assert len(json_data["ontologySourceReference"]) == 6
        assert json_data["ontologySourceReference"][2]["termSourceName"] == "UO"
        assert len(json_data["investigationPublications"]) == 1
        assert json_data["investigationPublications"][0]["investigationPublicationDOI"] == "doi:10.1186/jbiol54"

        assert len(json_data["studies"]) == 2
        study = json_data["studies"][0]
        assert study["studyFileName"] == "s_BII-S-1.txt"
        assert len(study["studyAssays"]) == 3
        assert study["studyAssays"][0]["studyAssayFileName"] == "a_metabolome.txt"