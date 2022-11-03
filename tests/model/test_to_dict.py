from unittest import TestCase

from isatools.model.investigation import Investigation
from isatools.model.ontology_source import OntologySource
from isatools.model.study import Study
from isatools.model.person import Person
from isatools.model.publication import Publication
from isatools.model.comments import Comment
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.protocol import Protocol
from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.source import Source
from isatools.model.sample import Sample
from isatools.model.material import LabeledExtract
from isatools.model.characteristic import Characteristic
from isatools.model.factor_value import FactorValue, StudyFactor
from isatools.model.process import Process
from isatools.model.assay import Assay
from isatools.model.context import set_context

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
                '@id': 'id1',
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
        expected_dict = {'identifier': '', 'title': '', 'publicReleaseDate': '', 'submissionDate': '',
                         'description': '',
                         'comments': [], 'ontologySourceReferences': [], 'people': [], 'publications': [], 'studies': []
                         }
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
            "filename": '', "identifier": '', "title": '', "description": '',
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
                '@id': 'id1',
                'annotationValue': 'name1',
                'termSource': 'source1',
                'termAccession': 'accession1',
                'comments': expected_comments
            }
        ]
        self.assertEqual(study.to_dict(), expected_dict)

        # Test protocols
        expected_dict['protocols'] = [
            {
                '@id': 'test_id',
                'name': 'test_name', 'version': '1.0', 'description': '', 'uri': '',
                'comments': [{'name': 'test_comment', 'value': ''}],
                'parameters': [
                    {
                        'parameterName': {
                            '@id': 'protocol_name_id',
                            'annotationValue': 'test_parameter', 'termSource': '', 'termAccession': '', 'comments': []
                        },
                        '@id': 'protocol_parameter_id'
                    }
                ],
                'protocolType': {
                    '@id': 'protocol_type_id',
                    'annotationValue': 'test_protocol_type',
                    'termSource': '',
                    'termAccession': '',
                    'comments': []},
                'components': []
            }
        ]
        protocol = Protocol(name='test_name', version='1.0',
                            id_='test_id',
                            comments=[Comment(name='test_comment')],
                            parameters=[
                                ProtocolParameter(
                                    parameter_name=OntologyAnnotation(term='test_parameter', id_='protocol_name_id'),
                                    id_='protocol_parameter_id'
                                ),
                            ],
                            protocol_type=OntologyAnnotation(term='test_protocol_type', id_='protocol_type_id'))
        study.protocols = [protocol]
        self.assertEqual(study.to_dict(), expected_dict)

        # Test materials
        source = Source(name='source', id_='source_id')
        sample = Sample(name='sample', id_='sample_id')
        other_material = LabeledExtract(name='extract', id_='extract_id')
        study.sources = [source]
        study.samples = [sample]
        study.other_material = [other_material]
        expected_dict['materials'] = {
            'sources': [{'@id': 'source_id', 'name': 'source', 'characteristics': [], 'comments': []}],
            'samples': [
                {
                    '@id': 'sample_id', 'name': 'sample',
                    'characteristics': [], 'factorValues': [], 'derivesFrom': [], 'comments': []
                }
            ],
            'otherMaterials': [
                {
                    '@id': 'extract_id', 'name': 'extract', 'type': 'Labeled Extract Name',
                    'characteristics': [], 'comments': []
                }
            ]
        }

        self.assertEqual(study.to_dict(), expected_dict)


class LDTest(TestCase):

    def setUp(self):
        self.investigation = Investigation()

    def test_to_ld(self):
        from isatools.model import Comment, OntologySource
        import json

        self.maxDiff = None

        comment_1 = Comment(name='comment_1', value='value_1')
        comment_2 = Comment(name='comment_2', value='value_2')
        comment_3 = Comment(name='comment_3', value='value_3')
        osr_1 = OntologySource(name='osr_1', file='file_1', version='version_1', description='description_1',
                               comments=[comment_3])
        role = OntologyAnnotation(term='term_1', id_='oa1', comments=[comment_2])
        person = Person(first_name='first_name', last_name='last_name', mid_initials='mid_initials', roles=[role])
        publication = Publication(title='title', status=OntologyAnnotation(term='status', id_='status_id'), doi='doi')
        design_descriptor = OntologyAnnotation(term='term_2', id_='oa2')
        protocol = Protocol(name='name', version='version', id_='protocol_id',
                            parameters=[ProtocolParameter(parameter_name=OntologyAnnotation(term='term_3'))],
                            protocol_type=OntologyAnnotation(term='protocolType', id_='oa4'))
        category = OntologyAnnotation(term='term_4', id_='#characteristic_category/1234')
        characteristic = Characteristic(category=category,
                                        value=OntologyAnnotation(term='my characteristic value', id_='char_val_id'))
        source = Source(name='source1', id_='source_id', comments=[comment_1], characteristics=[characteristic])
        study_factor = StudyFactor(name='factor_name', factor_type=OntologyAnnotation(term='type'))
        factor_value = FactorValue(factor_name=study_factor,
                                   value=OntologyAnnotation(term='value'))
        sample = Sample(name='sample1', id_='sample_id',
                        comments=[comment_1], characteristics=[characteristic],
                        factor_values=[factor_value], derives_from=[source])
        process = Process(name='p1', id_='process_id_1',
                          executes_protocol=protocol, inputs=[source], outputs=[sample])
        next_process = Process(name='p3', id_='process_id_3', executes_protocol=protocol, inputs=[sample])

        assay = Assay()

        study = Study(filename='filename', identifier='identifier', title='title', description='description',
                      contacts=[person],
                      publications=[publication],
                      comments=[comment_1],
                      design_descriptors=[design_descriptor],
                      protocols=[protocol],
                      sources=[source],
                      samples=[sample],
                      factors=[study_factor],
                      process_sequence=[process, next_process],
                      characteristic_categories=[category],
                      units=[OntologyAnnotation(term='unit', id_='unit_id')],
                      assays=[assay])

        self.investigation.comments = [comment_1]
        self.investigation.ontology_source_references = [osr_1]
        self.investigation.contacts = [person]
        self.investigation.publications = [publication]
        self.investigation.studies = [study]

        set_context('wdt', False, False)
        inv_ld = self.investigation.to_ld()
        print(json.dumps(inv_ld))
        investigation = Investigation()
        investigation.from_dict(inv_ld)
        self.assertEqual(investigation.to_dict(), self.investigation.to_dict())
