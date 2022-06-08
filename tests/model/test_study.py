from unittest import TestCase
import datetime
from copy import deepcopy

from isatools.model.study import Study
from isatools.model.assay import Assay
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.protocol import Protocol
from isatools.model.sample import Sample
from isatools.model.factor_value import StudyFactor


class StudyTest(TestCase):

    def setUp(self):
        self.study = Study()

    def test_init(self):
        mock_date = datetime.datetime(day=1, month=1, year=2017)
        study = Study(
            filename='file',
            identifier='0',
            title='T',
            description='D',
            submission_date=mock_date,
            public_release_date=mock_date,
            design_descriptors=[OntologyAnnotation(term='term')],
            protocols=[Protocol(name='p1')],
            assays=[Assay(filename='file')],
            factors=[StudyFactor(name='f1', factor_type='nucleic acid hybridization')]
        )
        self.assertEqual('file', study.filename)
        self.assertEqual('0', study.identifier)
        self.assertEqual('T', study.title)
        self.assertEqual('D', study.description)
        self.assertEqual(mock_date, study.submission_date)
        self.assertEqual(mock_date, study.public_release_date)
        self.assertEqual([OntologyAnnotation(term='term')], study.design_descriptors)
        self.assertEqual([Protocol(name='p1')], study.protocols)
        self.assertEqual([Assay(filename='file')], study.assays)
        self.assertEqual([StudyFactor(name='f1', factor_type='nucleic acid hybridization')], study.factors)

    def test_design_descriptors(self):
        self.assertEqual([], self.study.design_descriptors)
        ontology_annotation = OntologyAnnotation(term='term')
        self.study.design_descriptors = [ontology_annotation]
        self.assertEqual([ontology_annotation], self.study.design_descriptors)
        self.study.design_descriptors = [456]
        self.assertEqual([ontology_annotation], self.study.design_descriptors)

        with self.assertRaises(AttributeError) as context:
            self.study.design_descriptors = 456
        self.assertEqual("Study.design_descriptors must be iterable containing OntologyAnnotations",
                         str(context.exception))

    def test_protocols(self):
        self.assertEqual([], self.study.protocols)
        protocol = Protocol(name='p1')
        self.study.protocols = [protocol]
        self.assertEqual([protocol], self.study.protocols)

        with self.assertRaises(AttributeError) as context:
            self.study.protocols = 1
        self.assertEqual("The object supplied is not an iterable of Protocol objects", str(context.exception))

    def test_add_protocol(self):
        protocol = Protocol(name='p1')
        self.study.add_protocol(protocol)
        self.assertEqual([protocol], self.study.protocols)

        with self.assertRaises(TypeError) as context:
            self.study.add_protocol(1)
        self.assertEqual('The object supplied is not an instance of Protocol', str(context.exception))

    def test__get_default_protocol(self):
        parameter_list_index = {
            'mass spectrometry': [
                'instrument',
                'ion source',
                'detector',
                'analyzer',
                'chromatography instrument',
                'chromatography column'],
            'nmr spectroscopy': [
                'instrument',
                'NMR probe',
                'number of acquisition',
                'magnetic field strength',
                'pulse sequence'],
            'nucleic acid hybridization': [
                'Array Design REF'],
            'nucleic acid sequencing': [
                'sequencing instrument',
                'quality scorer',
                'base caller']
        }
        default_protocol = self.study._Study__get_default_protocol('None')
        self.assertIsInstance(default_protocol, Protocol)
        self.assertEqual([], default_protocol.parameters)

        for protocol in parameter_list_index.keys():
            default_protocol = self.study._Study__get_default_protocol(protocol)
            self.assertIsInstance(default_protocol, Protocol)
            for parameter in default_protocol.parameters:
                self.assertIn(parameter.parameter_name.term, parameter_list_index[protocol])

    def test_add_prot(self):
        self.study.add_prot(protocol_name='p1', protocol_type='mass spectrometry')
        default_protocol = self.study._Study__get_default_protocol('mass spectrometry')
        default_protocol.name = 'p1'
        self.assertEqual(1, len(self.study.protocols))
        self.assertEqual('p1', self.study.protocols[0].name)
        self.assertIsInstance(self.study.protocols[0], Protocol)
        self.assertIsInstance(self.study.protocols[0].parameters[0].parameter_name, OntologyAnnotation)
        self.assertEqual(self.study.protocols[0], default_protocol)

        self.study.add_prot(protocol_name='p2', protocol_type='mass spectrometry', use_default_params=False)
        protocol = Protocol(name='p2', protocol_type=OntologyAnnotation(term='mass spectrometry'))
        self.assertEqual(2, len(self.study.protocols))
        self.assertEqual(self.study.protocols[1], protocol)

        self.study.add_prot(protocol_name='p1', protocol_type='mass spectrometry')
        self.assertEqual(2, len(self.study.protocols))

    def test_add_factor(self):
        self.study.add_factor(name='f1', factor_type='factor type')
        self.assertEqual(1, len(self.study.factors))
        self.assertIsInstance(self.study.factors[0], StudyFactor)
        self.assertEqual('f1', self.study.factors[0].name)
        self.study.add_factor(name='f1', factor_type='factor type')
        self.assertEqual(1, len(self.study.factors))

        self.study.del_factor(name='abc')
        self.assertEqual(1, len(self.study.factors))
        self.study.del_factor(name='f1')
        self.assertEqual(1, len(self.study.factors))
        self.study.del_factor(name='f1', are_you_sure=True)
        self.assertEqual(0, len(self.study.factors))

    def test_assays(self):
        self.assertEqual([], self.study.assays)
        assay = Assay(filename='file')
        self.study.assays = [assay]
        self.assertEqual([assay], self.study.assays)

        with self.assertRaises(AttributeError) as context:
            self.study.assays = 1
        self.assertEqual("Study.assays must be iterable containing Assays", str(context.exception))

    def test_factors(self):
        self.assertEqual([], self.study.factors)
        factor = StudyFactor(name='f1')
        self.study.factors = [factor]
        self.assertEqual([factor], self.study.factors)

        with self.assertRaises(AttributeError) as context:
            self.study.factors = 1
        self.assertEqual("Study.factors must be iterable containing StudyFactors", str(context.exception))

    def test_repr(self):
        expected_str = ("isatools.model.Study(filename='', "
                        "identifier='', title='', description='', "
                        "submission_date='', public_release_date='', "
                        "contacts=[], design_descriptors=[], publications=[], "
                        "factors=[], protocols=[], assays=[], sources=[], "
                        "samples=[], process_sequence=[], other_material=[], "
                        "characteristic_categories=[], comments=[], units=[])")
        self.assertEqual(expected_str, repr(self.study))
        self.assertEqual(hash(expected_str), hash(self.study))

    def test_str(self):
        self.assertEqual("""Study(
    identifier=
    filename=
    title=
    description=
    submission_date=
    public_release_date=
    contacts=0 Person objects
    design_descriptors=0 OntologyAnnotation objects
    publications=0 Publication objects
    factors=0 StudyFactor objects
    protocols=0 Protocol objects
    assays=0 Assay objects
    sources=0 Source objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.study))

    def test_equalities(self):
        first_study = Study(filename='file1')
        second_study = Study(filename='file1')
        self.assertEqual(first_study, second_study)
        self.assertNotEqual(first_study, 1)
        self.assertNotEqual(first_study, self.study)
        self.assertNotEqual(first_study, None)

    def test_shuffle_assays(self):
        assay = Assay(filename='file1')
        samples = [
            Sample(name="Sample1"),
            Sample(name="Sample2"),
            Sample(name="Sample3"),
            Sample(name="Sample4"),
            Sample(name="Sample5"),
            Sample(name="Sample6"),
            Sample(name="Sample7")
        ]
        copied_sample_names = deepcopy(samples)
        assay.samples = copied_sample_names
        self.study.assays = [assay]
        self.study.shuffle_assays(["samples"])
        self.assertNotEqual(assay.samples, samples)

    def test_dict(self):
        expected_dict = {
            "filename": "",
            "identifier": "",
            "title": "",
            "description": "",
            "submissionDate": "",
            "publicReleaseDate": "",
            "publications": [],
            "people": [],
            "studyDesignDescriptors": [],
            "protocols": [],
            "materials": {
                "sources": [],
                "samples": [],
                "otherMaterials": []
            },
            "processSequence": [],
            "factors": [],
            "characteristicCategories": [],
            "unitCategories": [],
            "comments": [],
            "assays": []
        }
        self.assertEqual(self.study.to_dict(), expected_dict)

        # Test characteristics categories
        expected_dict['characteristicCategories'] = [
            {
                '@id': '#characteristic_category/first_id',
                'characteristicType': {
                    '@id': 'first_id',
                    'annotationValue': 'first_category',
                    'termSource': '',
                    'termAccession': '',
                    'comments': []
                }
            },
            {
                '@id': '#characteristic_category/second_id',
                'characteristicType': {
                    '@id': '#ontology_annotation/second_id',
                    'annotationValue': 'second_category',
                    'termSource': '',
                    'termAccession': '',
                    'comments': []
                }
            }
        ]
        first_category = OntologyAnnotation(term='first_category', id_='first_id')
        second_category = OntologyAnnotation(term='second_category', id_='#ontology_annotation/second_id')
        self.study.characteristic_categories = [first_category, second_category]
        self.assertTrue(self.study.to_dict(), expected_dict)

        expected_dict = {
            'filename': '', 'identifier': '', 'title': '', 'description': '',
            'submissionDate': '', 'publicReleaseDate': '',
            'publications': [
                {
                    "authorList": '',
                    "doi": '',
                    "pubMedID": '',
                    "status": {
                        '@id': '123',
                        'annotationValue': 'OA',
                        'termSource': '',
                        'termAccession': '',
                        'comments': []
                    },
                    "title": 'self.title',
                    "comments": []
                }
            ],
            'people': [
                {
                    'address': 'address',
                    'affiliation': 'affiliation',
                    'comments': [],
                    'email': 'email@test.com',
                    'fax': 'fax',
                    'firstName': 'first_name',
                    'lastName': 'last_name',
                    'midInitials': 'mid_initials',
                    'phone': 'test_phone',
                    'roles': [
                        {
                            '@id': '#ontology_annotation/mocked_UUID',
                            'annotationValue': 'test_term',
                            'termSource': '',
                            'termAccession': 'test_term_accession',
                            'comments': []
                        }
                    ]
                }
            ],
            'studyDesignDescriptors': [
                {
                    "@id": "design_descriptor_1",
                    "annotationValue": "value5",
                    "termAccession": "1111",
                    'termSource': '',
                    "comments": []
                }
            ],
            'protocols': [
                {
                    '@id': 'test_id',
                    'name': 'test_name', 'version': '', 'description': '', 'uri': '',
                    'comments': [],
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
            ],
            'materials': {'sources': [], 'samples': [], 'otherMaterials': []},
            'processSequence': [], 'factors': [],
            'characteristicCategories': [
                {
                    "@id": "my_cat3",
                    "annotationValue": "value3",
                    "termAccession": "1010",
                    "comments": []
                }
            ],
            'unitCategories': [
                {
                    "@id": "my_unit1",
                    "annotationValue": "dosage",
                    "termAccession": "1011",
                    'termSource': '',
                    "comments": []
                }
            ],
            'comments': [],
            'assays': [
                {
                    "characteristicCategories": [
                        {
                            "@id": "my_cat",
                            "annotationValue": "value",
                            "termAccession": "123",
                            "comments": []
                        }
                    ]
                },
                {
                    "characteristicCategories": [
                        {
                            "@id": "my_cat2",
                            "annotationValue": "value2",
                            "termAccession": "456",
                            "comments": []
                        }
                    ]
                }
            ]
        }
        study = Study()
        study.from_dict(expected_dict)
        study_dict = study.to_dict()
        self.assertEqual(study_dict['unitCategories'], expected_dict['unitCategories'])
        self.assertEqual(study_dict['publications'], expected_dict['publications'])
        self.assertEqual(study_dict['people'], expected_dict['people'])
        self.assertEqual(study_dict['studyDesignDescriptors'], expected_dict['studyDesignDescriptors'])

