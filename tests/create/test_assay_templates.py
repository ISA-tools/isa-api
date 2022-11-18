import unittest

import isatools
from isatools.create import errors
from isatools.model import (
    OntologyAnnotation,
    OntologySource
)

from isatools.create.assay_templates import create_new_ontology_annotation


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.processed_ontology_annotation = {}
        self.ontosrc = OntologySource(name='toto')

    def test_create_new_ontology_annotation(self, term_name="something"):
        stuff = isatools.create.assay_templates.create_new_ontology_annotation(term_name),
        self.assertEqual(str(stuff), str((isatools.model.OntologyAnnotation(term='something', term_source=self.ontosrc,
                                                                            term_accession='', comments=[]),)))
