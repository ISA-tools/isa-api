from unittest import TestCase

from isatools.model.investigation import Investigation
from isatools.model.ontology_source import OntologySource
from isatools.model.study import Study
from isatools.model.person import Person
from isatools.model.publication import Publication
from isatools.model.comments import Comment
from isatools.model.ontology_annotation import OntologyAnnotation


comments = [Comment(name='comment'), Comment(name='comment1', value='value1')]
expected_comments = [{'name': 'comment', 'value': ''}, {'name': 'comment1', 'value': 'value1'}]
contacts = [
    Person(first_name='first_name1', last_name='last_name1', email='email1',
           roles=[OntologyAnnotation(term='role1', id_='id1')]),
    Person(first_name='first_name2')
]
expected_contacts = [
    {
        'address': '',
        'affiliation': '',
        'comments': [], 'email':
        'email1', 'fax': '',
        'firstName': 'first_name1',
        'lastName': 'last_name1',
        'midInitials': '', 'phone': '',
        'roles': [
            {
                '@id': '#ontology_annotation/id1',
                'annotationValue': 'role1',
                'termSource': '',
                'termAccession': '',
                'comments': []
            }
        ]
    },
    {
        'address': '',
        'affiliation': '',
        'comments': [],
        'email': '',
        'fax': '',
        'firstName': 'first_name2',
        'lastName': '',
        'midInitials': '',
        'phone': '',
        'roles': []
    }
]
publications = [Publication(pubmed_id='pubmed_id', doi='doi', status='status', author_list='a, b, c')]
expected_publications = [
    {
        'authorList': 'a, b, c',
        'comments': [],
        'doi': 'doi',
        'pubMedID': 'pubmed_id',
        'status': 'status',
        'title': ''
    }
]


class TestSerialize(TestCase):

    def setUp(self):
        self.investigation = Investigation()

    def test_investigation_to_dict(self):
        expected_dict = {'identifier': '', 'title': '', 'publicReleaseDate': '', 'submissionDate': '', 'comments': [],
                         'ontologySourceReferences': [], 'people': [], 'publications': [], 'studies': []}
        self.assertEqual(self.investigation.to_dict(), expected_dict)

        # Test string fields
        expected_dict['identifier'] = 'id_1'
        expected_dict['title'] = 'Title'
        expected_dict['publicReleaseDate'] = 'why am I a string ?'
        expected_dict['submissionDate'] = 'why am I a string ?'
        self.investigation.title = 'Title'
        self.investigation.identifier = "id_1"
        self.investigation.public_release_date = "why am I a string ?"
        self.investigation.submission_date = "why am I a string ?"
        self.assertEqual(self.investigation.to_dict(), expected_dict)

        # Test comments
        self.investigation.comments = comments
        expected_dict['comments'] = expected_comments
        self.assertEqual(self.investigation.to_dict(), expected_dict)

        # Test ontology source references
        self.investigation.ontology_source_references = [
            OntologySource(name='name1', comments=[Comment(name='comment')]),
            OntologySource(name='name2', version='version2')
        ]
        expected_dict['ontologySourceReferences'] = [
            {
                'name': 'name1',
                'version': '',
                'comments': [{'name': 'comment', 'value': ''}],
                'file': '',
                'description': ''
            },
            {'name': 'name2', 'version': 'version2', 'comments': [], 'file': '', 'description': ''},
        ]
        self.assertEqual(self.investigation.to_dict(), expected_dict)

        # Test people/contacts
        self.investigation.contacts = contacts
        expected_dict['people'] = expected_contacts
        self.assertEqual(self.investigation.to_dict(), expected_dict)

        # Test publications
        self.assertEqual(self.investigation.publications, [])
        self.investigation.publications = publications
        expected_dict['publications'] = expected_publications
        self.assertEqual(expected_dict, self.investigation.to_dict())

    def test_study_to_dict(self):
        study = Study()
        expected_dict = {
            "filename": '', "identifier": '',  "title": '', "description": '',
            "submissionDate": '', "publicReleaseDate": '',
            "publications": [],
            "people": [],
            "studyDesignDescriptors": [],
            "protocols": [],
            "materials": {"sources": [], "samples": [], "otherMaterials": []},
            "processSequence": [],
            "factors": [],
            "characteristicCategories": [],
            "unitCategories": [],
            "comments": [],
            "assays": []
        }
        self.assertEqual(study.to_dict(), expected_dict)

        # Test string fields
        study.filename = 'filename'
        study.identifier = 'id_1'
        study.title = 'Title'
        study.description = 'Description'
        study.submission_date = 'submission_date'
        study.public_release_date = 'public_release_date'
        expected_dict['filename'] = 'filename'
        expected_dict['identifier'] = 'id_1'
        expected_dict['title'] = 'Title'
        expected_dict['description'] = 'Description'
        expected_dict['submissionDate'] = 'submission_date'
        expected_dict['publicReleaseDate'] = 'public_release_date'
        self.assertEqual(study.to_dict(), expected_dict)

        # Test comments
        study.comments = comments
        expected_dict['comments'] = expected_comments
        self.assertEqual(study.to_dict(), expected_dict)

        # Test contacts
        study.contacts = contacts
        expected_dict['people'] = expected_contacts
        self.assertEqual(study.to_dict(), expected_dict)

        # Test publications
        study.publications = publications
        expected_dict['publications'] = expected_publications
        self.assertEqual(study.to_dict(), expected_dict)

        # Test study design descriptors
        study.design_descriptors = [
            OntologyAnnotation(term_accession='accession1', term_source='source1', term='name1', id_='id1',
                               comments=comments)
        ]
        expected_dict['studyDesignDescriptors'] = [
            {
                '@id': '#ontology_annotation/id1',
                'annotationValue': 'name1',
                'termSource': 'source1',
                'termAccession': 'accession1',
                'comments': expected_comments
            }
        ]
        self.assertEqual(study.to_dict(), expected_dict)
