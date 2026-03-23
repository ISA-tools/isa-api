from json import dumps, loads
from unittest import TestCase
from unittest.mock import patch

from isatools.isajson.dump import ISAJSONEncoder
from isatools.model import Investigation


class TestISAJsonDump(TestCase):
    @patch("isatools.model.identifiable.uuid4", return_value="mocked_UUID")
    def test_dump_empty_investigation(self, mock_uuid4):
        expected_dict = {
            "@id": "#investigation/" + mock_uuid4.return_value,
            "identifier": "",
            "title": "",
            "description": "",
            "publicReleaseDate": "",
            "submissionDate": "",
            "comments": [],
            "ontologySourceReferences": [],
            "people": [],
            "publications": [],
            "studies": [],
        }
        investigation = Investigation()
        investigation_dict = dumps(investigation, cls=ISAJSONEncoder)
        self.assertEqual(loads(investigation_dict), expected_dict)

    def test_dump_with_error(self):
        class Test:
            pass

        with self.assertRaises(TypeError) as context:
            dumps(Test(), cls=ISAJSONEncoder)
        error = "Object of type Test is not JSON serializable"
        self.assertEqual(str(context.exception), error)
