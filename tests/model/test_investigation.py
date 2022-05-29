from datetime import datetime
from unittest import TestCase

from isatools.model.investigation import Investigation
from isatools.model.ontology_source import OntologySource
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.study import Study
from isatools.model.person import Person
from isatools.model.publication import Publication
from isatools.model.comments import Comment


class InvestigationTest(TestCase):

    def setUp(self):
        self.investigation = Investigation()

    def test_init(self):
        mocked_date = datetime(day=1, month=1, year=2017)
        ontology_source = OntologySource(name='name', file='file')
        study = Study(filename='file')
        investigation = Investigation(
            identifier='id', filename='file', title='T',
            submission_date=mocked_date,
            public_release_date=mocked_date,
            ontology_source_references=[ontology_source],
            studies=[study])
        self.assertEqual('id', investigation.identifier)
        self.assertEqual('file', investigation.filename)
        self.assertEqual('T', investigation.title)
        self.assertEqual(mocked_date, investigation.submission_date)
        self.assertEqual(mocked_date, investigation.public_release_date)
        self.assertEqual(1, len(investigation.ontology_source_references))
        self.assertEqual(ontology_source, investigation.ontology_source_references[0])
        self.assertEqual(1, len(investigation.studies))
        self.assertEqual(study, investigation.studies[0])

    def test_ontology_source_references(self):
        self.assertEqual([], self.investigation.ontology_source_references)
        ontology_source = OntologySource(name='name')
        self.investigation.ontology_source_references = [ontology_source]
        self.assertEqual(1, len(self.investigation.ontology_source_references))
        self.assertEqual(ontology_source, self.investigation.ontology_source_references[0])

        self.investigation.add_ontology_source_reference(name='name')
        self.assertEqual(2, len(self.investigation.ontology_source_references))
        self.assertEqual(ontology_source, self.investigation.ontology_source_references[1])
        self.assertEqual(self.investigation.ontology_source_references, [ontology_source, ontology_source])
        self.assertEqual(self.investigation.get_ontology_source_references(), [ontology_source, ontology_source])

        self.assertTrue(['name', 'name'], self.investigation.get_ontology_source_reference_names())

        with self.assertRaises(AttributeError) as context:
            self.investigation.ontology_source_references = 1
        self.assertEqual('Investigation.ontology_source_references must be iterable containing OntologySource objects',
                         str(context.exception))

    def test_yield_ontology_source_references(self):
        ontology_source = OntologySource(name='name')
        self.investigation.ontology_source_references = [ontology_source]
        self.assertEqual(1, len(list(self.investigation.yield_ontology_source_references())))
        self.assertEqual(ontology_source, list(self.investigation.yield_ontology_source_references())[0])
        self.assertEqual(0, len(list(self.investigation.yield_ontology_source_references('another name'))))

    def test_get_ontology_source_reference(self):
        ontology_source = OntologySource(name='name')
        self.investigation.ontology_source_references = [ontology_source, ontology_source]
        self.assertEqual(ontology_source, self.investigation.get_ontology_source_reference(name='name'))
        self.assertEqual(None, self.investigation.get_ontology_source_reference(name='another name'))

    def test_studies(self):
        study = Study()
        self.investigation.studies = [study]
        self.assertEqual([study], self.investigation.studies)
        self.investigation.studies = [1]
        self.assertEqual([study], self.investigation.studies)

        with self.assertRaises(AttributeError) as context:
            self.investigation.studies = 1
        self.assertEqual('Investigation.studies must be iterable containing Study objects', str(context.exception))

    def test_execute_query(self):
        self.investigation.title = 'Title'
        query = "{investigation { title }}"
        data = self.investigation.execute_query(query)
        data = data.data
        self.assertEqual(data, {'investigation': {'title': 'Title'}})

    def test_introspection(self):
        introspection = self.investigation.introspect()
        self.assertTrue(len(introspection.data['schemas']['types']) == 46)
        self.assertEqual(introspection.data['schemas']['types'][0]['name'], "IsaQuery")

    def test_repr(self):
        self.assertEqual("isatools.model.Investigation(identifier='', "
                         "filename='', title='', submission_date='', "
                         "public_release_date='', "
                         "ontology_source_references=[], publications=[], "
                         "contacts=[], studies=[], comments=[])",
                         repr(self.investigation))

    def test_str(self):
        self.assertEqual("""Investigation(
    identifier=
    filename=
    title=
    submission_date=
    public_release_date=
    ontology_source_references=0 OntologySources
    publications=0 Publication objects
    contacts=0 Person objects
    studies=0 Study objects
    comments=0 Comment objects
)""", str(self.investigation))

    def test_eq(self):
        expected_investigation = Investigation()
        self.assertEqual(expected_investigation, self.investigation)
        self.assertEqual(hash(expected_investigation), hash(self.investigation))

    def test_ne(self):
        expected_other_investigation = Investigation(
            identifier='id2', filename='file2', title='T2',
            submission_date=datetime(day=2, month=1, year=2017),
            public_release_date=datetime(day=2, month=1, year=2017))
        self.assertNotEqual(expected_other_investigation, self.investigation)
        self.assertNotEqual(
            hash(expected_other_investigation), hash(self.investigation))

    def test_to_dict(self):
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
        self.investigation.comments = [Comment(name='comment'), Comment(name='comment1', value='value1')]
        expected_dict['comments'] = [{'name': 'comment', 'value': ''}, {'name': 'comment1', 'value': 'value1'}]
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
        self.investigation.contacts = [
            Person(first_name='first_name1', last_name='last_name1', email='email1',
                   roles=[OntologyAnnotation(term='role1', id_='id1')]),
            Person(first_name='first_name2')
        ]
        expected_dict['people'] = [
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
            }]
        self.assertEqual(self.investigation.to_dict(), expected_dict)

        # Test publications
        self.assertEqual(self.investigation.publications, [])
        self.investigation.publications = [
            Publication(pubmed_id='pubmed_id', doi='doi', status='status', author_list='a, b, c')
        ]
        expected_dict['publications'] = [
            {
                'authorList': 'a, b, c',
                'comments': [],
                'doi': 'doi',
                'pubMedID': 'pubmed_id',
                'status': 'status',
                'title': ''
            }
        ]
        self.assertEqual(expected_dict, self.investigation.to_dict())
