from unittest import TestCase
from unittest.mock import patch
from isatools.model.context import ContextPath


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    mocked = MockResponse({'@context': 'test'}, 200)
    return mocked


class TestContextPath(TestCase):

    def setUp(self) -> None:
        self.context = ContextPath()

    def test_attributes(self):
        self.assertEqual(self.context.context, 'obo')
        self.context.context = 'sdo'
        self.assertEqual(self.context.context, 'sdo')

        with self.assertRaises(ValueError) as context:
            self.context.context = 'test'
        self.assertEqual(str(context.exception),
                         "Context name must be one in ['obo', 'sdo', 'wdt', 'wd', 'sio'] but got test")

    def test_repr(self):
        self.context.context = 'sdo'
        self.assertEqual(repr(self.context), "sdo")
        self.assertEqual(str(self.context), "sdo")

    def test_get_context(self):
        self.context.local = False
        url = ("https://raw.githubusercontent.com/ISA-tools/isa-api/master/isatools/resources/json-context/obo/"
               "isa_allinone_obo_context.jsonld")
        self.assertEqual(self.context.get_context("Investigation"), url)

    def test_load_context_local(self):
        self.context.local = True
        self.context.all_in_one = False
        context_path = self.context.get_context("Investigation")
        context = self.context.load_context(context_path)
        self.assertIn('@context', context)
        self.assertEqual(type(context), dict)

    @patch('isatools.model.context.requests.get', side_effect=mocked_requests_get)
    def test_load_context_remote(self, mock_get):
        self.context.local = False
        self.context.all_in_one = False
        context_path = self.context.get_context("Investigation")
        context = self.context.load_context(context_path)
        self.assertEqual(context, {"@context": "test"})

        url = ("https://raw.githubusercontent.com/ISA-tools/isa-api/master/isatools/resources/json-context/obo/"
               "isa_test_obo_context.jsonld")
        self.context.contexts[url] = {"@context": 'test'}
        self.assertEqual(self.context.get_context('test'), url)

        self.context.include_contexts = True
        self.assertEqual(self.context.get_context('test'), {'@context': 'test'})
