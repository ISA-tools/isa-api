import unittest
from isatools import isajson2
from isatools.model.v1 import *


class UnitTestIsaJson(unittest.TestCase):

    def test_read_list_json(self):

        J = [
            {
                "test": "test 1"
            },
            {
                "test": "test 2"
            }
        ]

        def read_test(test_json):
            return test_json["test"]

        o = isajson2.read_list(J, read_test)

        self.assertIsInstance(o, list)
        self.assertEqual(o[0], J[0]["test"])
        self.assertEqual(o[1], J[1]["test"])

    def test_isajson_read_investigation(self):

        J = {
            "ontology_source_references": [],
            "comments": [],
            "publications": [],
            "filename": "investigation filename",
            "title": "investigation title",
            "publicReleaseDate": "investigation public release date",
            "submissionDate": "investigation submission date",
            "contacts": [],
            "identifier": "investigation identifier",
            "studies": [],
            "description": "investigation description"
        }

        o = isajson2.read_investigation(J)

        self.assertIsInstance(o, Investigation)
        self.assertEqual(o.ontology_source_references, [])
        self.assertEqual(o.comments, [])
        self.assertEqual(o.ontology_source_references, [])
        self.assertEqual(o.filename, J["filename"])
        self.assertEqual(o.title, J["title"])
        self.assertEqual(o.public_release_date, J["publicReleaseDate"])
        self.assertEqual(o.submission_date, J["submissionDate"])
        self.assertEqual(o.contacts, [])
        self.assertEqual(o.identifier, J["identifier"])
        self.assertEqual(o.studies, [])
        self.assertEqual(o.description, J["description"])

    def test_isajson_read_comment_json(self):

        J = {
            "name": "comment name",
            "value": "comment value"
        }

        o = isajson2.read_comment(J)

        self.assertIsInstance(o, Comment)
        self.assertEqual(o.name, J["name"])
        self.assertEqual(o.value, J["value"])

    def test_read_ontology_source_json(self):

        J = {
            "name": "ontology source name",
            "version": "ontology source version",
            "description": "ontology source description",
            "file": "ontology source file",
            "comments": []
        }

        o = isajson2.read_ontology_source(J)

        self.assertIsInstance(o, OntologySource)
        self.assertEqual(o.name, J["name"])
        self.assertEqual(o.version, J["version"])
        self.assertEqual(o.description, J["description"])
        self.assertEqual(o.file, J["file"])
        self.assertEqual(o.comments, [])

    def test_read_publication_json(self):

        J = {
            "pubMedID": "publication pubMedID",
            "doi": "publication DOI",
            "title": "publication title",
            "authorList": "publication author list",
            "status": {
                "name": "status value"
            },
            "comments": []
        }

        o = isajson2.read_publication(J)

        self.assertIsInstance(o, Publication)
        self.assertEqual(o.pubmed_id, J["pubMedID"])
        self.assertEqual(o.doi, J["doi"])
        self.assertEqual(o.title, J["title"])
        self.assertEqual(o.author_list, J["authorList"])
        self.assertEqual(o.status, J["status"])
        self.assertEqual(o.comments, [])

    def test_read_person_json(self):

        J = {
            "affiliation": "person affiliation",
            "comments": [],
            "email": "person email",
            "phone": "person phone",
            "lastName": "person last name",
            "midInitials": "person mid initials",
            "firstName": "person first name",
            "roles": [],
            "address": "person address",
            "fax": "person fax"
        }

        o = isajson2.read_person(J)

        self.assertIsInstance(o, Person)
        self.assertEqual(o.affiliation, J["affiliation"])
        self.assertEqual(o.comments, [])
        self.assertEqual(o.email, J["email"])
        self.assertEqual(o.last_name, J["lastName"])
        self.assertEqual(o.mid_initials, J["midInitials"])
        self.assertEqual(o.first_name, J["firstName"])
        self.assertEqual(o.roles, [])
        self.assertEqual(o.fax, J["fax"])

    def test_read_annotation_json(self):

        J = {
            "termSource": "O",
            "annotationValue": "a term",
            "termAccession": "term accession",
            "comments": []
        }

        o = isajson2.read_annotation(J)

        self.assertIsInstance(o, OntologyAnnotation)
        self.assertEqual(o.term_source, J["termSource"])
        self.assertEqual(o.term, J["annotationValue"])
        self.assertEqual(o.term_accession, J["termAccession"])
        self.assertEqual(o.comments, [])

    def test_read_annotation_json_with_ontology_sources_dict(self):

        J = {
            "termSource": "O",
            "annotationValue": "a term",
            "termAccession": "term accession",
            "comments": []
        }

        #  ontology_sources_dict should be generated after read_ontology_source() has been run
        ontology_sources_dict = {
            "O": OntologySource(name="O")
        }

        o = isajson2.read_annotation(J, ontology_sources_dict)

        self.assertIsInstance(o, OntologyAnnotation)
        self.assertIsInstance(o.term_source, OntologySource)
        self.assertEqual(o.term_source.name, J["termSource"])
        self.assertEqual(o.term, J["annotationValue"])
        self.assertEqual(o.term, J["annotationValue"])
        self.assertEqual(o.term_accession, J["termAccession"])
        self.assertEqual(o.comments, [])

    def test_read_study_factor_json(self):

        J = {
            "factorType": {
                "termSource": "O",
                "annotationValue": "a term",
                "termAccession": "term accession",
                "comments": []
            },
            "comments": [],
            "factorName": "factor name"
        }

        #  ontology_sources_dict should be generated after read_ontology_source() has been run
        ontology_sources_dict = {
            "O": OntologySource(name="O")
        }

        o = isajson2.read_study_factor(J, ontology_sources_dict)

        self.assertIsInstance(o, StudyFactor)
        self.assertIsInstance(o.factor_type, OntologyAnnotation)
        self.assertEqual(o.name, J["factorName"])
        self.assertEqual(o.comments, [])

    def test_read_protocol_parameter_json(self):

        J = {
            "parameterName": {
                "termSource": "O",
                "annotationValue": "a term",
                "termAccession": "term accession",
                "comments": []
            },
            "comments": []
        }

        #  ontology_sources_dict should be generated after read_ontology_source() has been run
        ontology_sources_dict = {
            "O": OntologySource(name="O")
        }

        o = isajson2.read_protocol_parameter(J, ontology_sources_dict)

        self.assertIsInstance(o, ProtocolParameter)
        self.assertIsInstance(o.parameter_name, OntologyAnnotation)
        self.assertEqual(o.parameter_name.term, J["parameterName"]["annotationValue"])
        self.assertEqual(o.comments, [])

    def test_read_protocol_json(self):

        J = {
            "parameters": [],
            "comments": [],
            "version": "protocol version",
            "name": "protocol name",
            "description": "protocol description",
            "protocolType": {
                "termSource": "O",
                "annotationValue": "a term",
                "termAccession": "term accession",
                "comments": []
            },
            "components": [],
            "uri": "protocol uri"
        }

        #  ontology_sources_dict should be generated after read_ontology_source() has been run
        ontology_sources_dict = {
            "O": OntologySource(name="O")
        }

        o = isajson2.read_protocol(J, ontology_sources_dict)

        self.assertIsInstance(o, Protocol)
        self.assertIsInstance(o.protocol_type, OntologyAnnotation)
        self.assertEqual(o.parameters, [])
        self.assertEqual(o.comments, [])
        self.assertEqual(o.version, J["version"])
        self.assertEqual(o.name, J["name"])
        self.assertEqual(o.description, J["description"])
        self.assertEqual(o.protocol_type.term, J["protocolType"]["annotationValue"])
        self.assertEqual(o.components, []),
        self.assertEqual(o.uri, J["uri"])
