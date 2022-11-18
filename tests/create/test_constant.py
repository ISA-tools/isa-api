import unittest

from isatools.create.constants import DEFAULT_SOURCE_TYPE, set_defaulttype_value, default_ontology_source_reference


class TestConstant(unittest.TestCase):
    def test_set_defaulttype_value(self):
        set_defaulttype_value()
        self.assertEqual( DEFAULT_SOURCE_TYPE.value.term, "Human")
        self.assertEqual( DEFAULT_SOURCE_TYPE.value.term_accession, "http://purl.obolibrary.org/obo/NCIT_C14225")
        self.assertEqual( DEFAULT_SOURCE_TYPE.value.term_source, default_ontology_source_reference)



