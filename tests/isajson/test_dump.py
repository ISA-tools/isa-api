from unittest import TestCase
from json import dumps, loads

from isatools.isajson.dump import ISAJSONEncoder
from isatools.model import Investigation


class TestISAJsonDump(TestCase):

    def test_dump_empty_investigation(self):
        investigation = Investigation()
        investigation_dict = dumps(investigation, cls=ISAJSONEncoder)
        expected_dict = {
            "identifier": "", "title": "", "description": "", "publicReleaseDate": "", "submissionDate": "",
            "comments": [], "ontologySourceReferences": [], "people": [], "publications": [], "studies": []
        }
        self.assertEqual(loads(investigation_dict), expected_dict)

    def test_dump_with_error(self):

        class Test:
            pass

        with self.assertRaises(TypeError) as context:
            dumps(Test(), cls=ISAJSONEncoder)
        error = "Object of type Test is not JSON serializable"
        self.assertEqual(str(context.exception), error)
