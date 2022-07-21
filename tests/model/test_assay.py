from unittest import TestCase
from unittest.mock import patch

from isatools.model.assay import Assay
from isatools.model.datafile import DataFile
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.ontology_source import OntologySource
from isatools.model.sample import Sample
from isatools.model.protocol import Protocol
from isatools.model.material import Material
from isatools.model.parameter_value import ProtocolParameter
from isatools.model.process import Process
from isatools.model.study import Study
from isatools.model.loader_indexes import loader_states as indexes


class TestAssay(TestCase):

    def setUp(self):
        self.assay = Assay()

    def test_init(self):
        assay = Assay(measurement_type=OntologyAnnotation(term='MT'),
                      technology_type=OntologyAnnotation(term='TT'),
                      technology_platform='TP',
                      filename='file',
                      data_files=[DataFile(filename='file1')])
        self.assertEqual(OntologyAnnotation(term='MT'), assay.measurement_type)
        self.assertEqual(OntologyAnnotation(term='TT'), assay.technology_type)
        self.assertEqual('TP', assay.technology_platform)
        self.assertEqual('file', assay.filename)
        self.assertEqual(1, len(assay.data_files))
        self.assertEqual('file1', assay.data_files[0].filename)

    def test_measurement_type(self):
        self.assertIsInstance(self.assay.measurement_type, OntologyAnnotation)
        self.assertEqual(self.assay.measurement_type.term, '')
        self.assay.measurement_type = OntologyAnnotation(term='MT')
        self.assertEqual(OntologyAnnotation(term='MT'), self.assay.measurement_type)

        with self.assertRaises(AttributeError) as context:
            self.assay.measurement_type = 1
        self.assertTrue("Assay.measurement_type must be a OntologyAnnotation or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_technology_type(self):
        self.assertIsInstance(self.assay.technology_type, OntologyAnnotation)
        self.assertEqual(self.assay.technology_type.term, '')
        self.assay.technology_type = OntologyAnnotation(term='TT')
        self.assertEqual(OntologyAnnotation(term='TT'), self.assay.technology_type)

        with self.assertRaises(AttributeError) as context:
            self.assay.technology_type = 1
        self.assertTrue("Assay.technology_type must be a OntologyAnnotation or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_technology_platform(self):
        self.assertEqual('', self.assay.technology_platform)
        self.assay.technology_platform = 'TP'
        self.assertEqual('TP', self.assay.technology_platform)

        with self.assertRaises(AttributeError) as context:
            self.assay.technology_platform = 1
        self.assertTrue("Assay.technology_platform must be a str or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_data_files(self):
        self.assertEqual(0, len(self.assay.data_files))
        datafile = DataFile()
        self.assay.data_files = [datafile]
        self.assertEqual(self.assay.data_files, [datafile])
        self.assay.data_files = [123]
        self.assertEqual(self.assay.data_files, [datafile])

        with self.assertRaises(AttributeError) as context:
            self.assay.data_files = 1
        self.assertTrue("Assay.data_files must be iterable containing DataFiles"
                        in str(context.exception))

    def test_repr(self):
        expected_str = ("isatools.model.Assay(measurement_type="
                        "isatools.model.OntologyAnnotation(term='', "
                        "term_source=None, term_accession='', comments=[]), "
                        "technology_type=isatools.model.OntologyAnnotation("
                        "term='', term_source=None, term_accession='', "
                        "comments=[]), technology_platform='', filename='', "
                        "data_files=[], samples=[], process_sequence=[], "
                        "other_material=[], characteristic_categories=[], "
                        "comments=[], units=[])")
        self.assertEqual(expected_str, repr(self.assay))
        self.assertEqual(hash(expected_str), hash(self.assay))

    def test_str(self):
        self.assertEqual("""Assay(
    measurement_type=
    technology_type=
    technology_platform=
    filename=
    data_files=0 DataFile objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.assay))

    def test_equalities(self):
        first_assay = Assay(measurement_type=OntologyAnnotation(term='MT1'))
        second_assay = Assay(measurement_type=OntologyAnnotation(term='MT1'))
        third_assay = Assay(measurement_type=OntologyAnnotation(term='MT2'))
        self.assertTrue(first_assay == second_assay)
        self.assertFalse(first_assay == third_assay)
        self.assertFalse(first_assay != second_assay)
        self.assertTrue(first_assay != third_assay)

    @patch('isatools.model.identifiable.uuid4', return_value='test_uuid')
    def test_to_dict(self, mock_uuid4):
        study = Study()
        assay = Assay(
            filename='file',
            measurement_type=OntologyAnnotation(term='MT', id_='MT_ID'),
            technology_type=OntologyAnnotation(term='TT', id_='TT_ID')
        )
        expected_dict = {
            'measurementType': {
                '@id': 'MT_ID',
                'annotationValue': 'MT',
                'termSource': '',
                'termAccession': '',
                'comments': []},
            'technologyType': {
                '@id': 'TT_ID',
                'annotationValue': 'TT',
                'termSource': '',
                'termAccession': '',
                'comments': []
            },
            'technologyPlatform': '',
            'filename': 'file',
            'characteristicCategories': [],
            'unitCategories': [],
            'comments': [],
            'materials': {
                'samples': [],
                'otherMaterials': []
            },
            'dataFiles': [],
            'processSequence': []
        }
        self.assertEqual(expected_dict, assay.to_dict())

        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        expected_dict['unitCategories'] = [{
            '@id': 'unit_ID',
            'annotationValue': 'my_unit',
            'termSource': '',
            'termAccession': '',
            'comments': []
        }]
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        expected_dict['materials']['samples'] = [{"@id": 'my_sample'}]
        indexes.samples = {'my_sample': Sample(id_='my_sample')}
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        # Data Files
        expected_dict['dataFiles'] = [
            {
                "@id": 'my_data_file',
                "name": "filename",
                "type": "RawDataFile",
                "comments": []
            }
        ]
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)
        indexes.term_sources = {'term_source1': OntologySource(name='term_source1')}
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        # Other Materials
        expected_dict['materials']['otherMaterials'] = [
            {
                '@id': 'my_other_material_id',
                'name': 'extract-my_other_material_name',  # add extract- for string replace test
                'type': 'Extract Name',
                'comments': [],
                'characteristics': [
                    {
                        'category': {'@id': 'my_other_material_characteristic_id'},
                        'value': {
                            '@id': 'my_other_material_characteristic_value',
                            'annotationValue': 'my_other_material_characteristic_value2_term',
                            'termAccession': 'term_accession_val',
                            'comments': [],
                            'termSource': ''
                        },
                        'comments': []
                    },
                    {
                        'category': {'@id': 'my_other_material_characteristic_id2'},
                        'value': {
                            '@id': 'my_other_material_characteristic_value2_id',
                            'annotationValue': 'my_other_material_characteristic_value2_term',
                            'termAccession': 'term_accession_val',
                            'comments': [],
                            'termSource': ''
                        },
                        'comments': []
                    }
                ]
            }
        ]
        indexes.add_characteristic_category(OntologyAnnotation(id_='my_other_material_characteristic_id'))
        indexes.add_characteristic_category(OntologyAnnotation(id_='my_other_material_characteristic_id2'))
        assay = Assay()
        assay.from_dict(expected_dict, study)
        # Make sur the string 'extract-' is removed from the expected_dict material name before assertion
        # And set the characteristic value as an ontology annotation output
        expected_value = {
            '@id': 'my_other_material_characteristic_value',
            'annotationValue': 'my_other_material_characteristic_value2_term',
            'comments': [],
            'termAccession': 'term_accession_val',
            'termSource': ''
        }
        expected_dict['materials']['otherMaterials'][0]['name'] = 'my_other_material_name'
        expected_dict['materials']['otherMaterials'][0]['characteristics'][0]['value'] = expected_value
        self.assertEqual(assay.to_dict(), expected_dict)

        # Process Sequence
        expected_dict['processSequence'] = [
            {
                "@id": "my_process_sequence_id",
                "executesProtocol": {"@id": "my_protocol_id"},
                "name": "my process",
                "comments": [],
                "date": "",
                'inputs': [],
                'outputs': [],
                'parameterValues': [],
                'performer': ''
            }
        ]
        protocol = Protocol(
            id_="my_protocol_id",
            protocol_type=OntologyAnnotation(term="nucleic acid sequencing")
        )
        indexes.add_protocol(protocol)
        protocol = Protocol(
            id_="my_protocol_id2",
            protocol_type=OntologyAnnotation(term="data collection")
        )
        indexes.add_protocol(protocol)
        expected_dict['technologyType']['annotationValue'] = 'DNA microarray'
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        # Process Inputs and outputs
        expected_dict['processSequence'][0]['inputs'] = [{"@id": "sample_id"}]
        assay = Assay()
        indexes.add_sample(Sample(id_='sample_id'))
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)
        expected_dict['processSequence'][0]['inputs'] = [{"@id": "assay_other_material_id"}]
        assay = Assay()
        indexes.add_sample(Material(id_='assay_other_material_id'))
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)
        expected_dict['processSequence'][0]['inputs'] = [{"@id": "assay_data_file_id"}]
        assay = Assay()
        indexes.add_sample(DataFile(id_='assay_data_file_id'))
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)
        expected_dict['processSequence'][0]['outputs'] = [
            {"@id": "sample_id"},
            {"@id": "assay_other_material_id"},
            {"@id": "assay_data_file_id"}
        ]
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        # Parameter Values
        expected_dict['processSequence'][0]['parameterValues'] = [
            {
                "category": {"@id": "#parameter/Array_Design_REF"},
                "value": "a value"
            }
        ]
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.process_sequence[0].array_design_ref, "a value")

        expected_dict['processSequence'][0]['parameterValues'][0] = {
            "category": {"@id": "parameter_id"},
            "value": 123,
        }
        indexes.add_parameter(ProtocolParameter(id_='parameter_id', comments=[]))
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        expected_dict['processSequence'][0]['parameterValues'][0]['unit'] = {"@id": "unit_id"}
        indexes.add_unit(OntologyAnnotation(id_='unit_id'))
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        expected_dict['processSequence'][0]['parameterValues'] = [
            {
                'category': {'@id': 'parameter_id'},
                'value': {
                    '@id': 'parameter_id',
                    'annotationValue': '',
                    'comments': [],
                    'termAccession': '',
                    'termSource': ''
                }
            }
        ]
        indexes.add_characteristic_category(ProtocolParameter(id_='parameter_id'))
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict(), expected_dict)

        expected_dict['processSequence'][0]['parameterValues'] = [{"value": 123}]
        assay = Assay()
        assay.from_dict(expected_dict, study)

        expected_dict['processSequence'][0] = {
            "executesProtocol": {"@id": "my_protocol_id"},
            "name": "my process",
            "comments": [],
            "date": "",
            'inputs': [],
            'outputs': [],
            'parameterValues': [],
            'performer': '',
            "@id": "my_process_sequence_id",
            'previousProcess': {'@id': 'previous_process_id'},
            'nextProcess': {'@id': 'next_process_id'}
        }
        indexes.add_process(Process(id_='previous_process_id'))
        indexes.add_process(Process(id_='next_process_id'))
        assay = Assay()
        assay.from_dict(expected_dict, study)
        self.assertEqual(assay.to_dict()['processSequence'][0], expected_dict['processSequence'][0])

    def test_io_errors_in_load(self):
        error_msg = "Could not find input node in samples or materials or data dicts: error_id"
        expected_dict = {
            'measurementType': {},
            'technologyType': {},
            'technologyPlatform': '',
            'filename': 'file',
            'characteristicCategories': [],
            'unitCategories': [],
            'comments': [],
            'materials': {
                'samples': [],
                'otherMaterials': []
            },
            'dataFiles': [],
            'processSequence': [
                {"executesProtocol": {"@id": "123"}, "inputs": [{"@id": "error_id"}]}
            ]
        }
        indexes.add_protocol(Protocol(id_='123'))
        assay = Assay()
        study = Study()
        with self.assertRaises(IOError) as context:
            assay.from_dict(expected_dict, study)
        self.assertEqual(str(context.exception), error_msg)

        error_msg = "Could not find output node in samples or materials or data dicts: another_error_id"
        expected_dict['processSequence'][0]['outputs'] = [{"@id": "another_error_id"}]
        indexes.add_sample(Sample(id_='error_id'))
        assay = Assay()
        with self.assertRaises(IOError) as context:
            assay.from_dict(expected_dict, study)
        self.assertEqual(str(context.exception), error_msg)
