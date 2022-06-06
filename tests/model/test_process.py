from unittest import TestCase
from unittest.mock import patch

from isatools.model.process import Process
from isatools.model.protocol import Protocol
from isatools.model.parameter_value import ParameterValue
from isatools.model.datafile import DataFile
from isatools.model.material import Material
from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.ontology_annotation import OntologyAnnotation


class TestProcess(TestCase):

    def setUp(self):
        self.process = Process(id_='test')

    def test_init(self):
        self.assertIsInstance(self.process, Process)
        self.assertTrue(self.process.id == 'test')

        protocol = Protocol()
        parameter_value = ParameterValue()
        input_file = DataFile(filename='input.txt')
        output_file = DataFile(filename='output.txt')
        process = Process(
            name='test',
            executes_protocol=protocol,
            parameter_values=[parameter_value],
            inputs=[input_file],
            outputs=[output_file]
        )
        self.assertIsInstance(process, Process)
        self.assertTrue(process.name == 'test')
        self.assertTrue(process.executes_protocol == protocol)
        self.assertTrue(process.parameter_values == [parameter_value])
        self.assertTrue(process.inputs == [input_file])
        self.assertTrue(process.outputs == [output_file])

    def test_name(self):
        self.assertIsNone(self.process.name)
        self.process.name = 'test'
        self.assertTrue(self.process.name == 'test')

        with self.assertRaises(AttributeError) as context:
            self.process.name = 1
        self.assertTrue('Process.name must be a string' in str(context.exception))

    def test_executes_protocol(self):
        self.assertIsInstance(self.process.executes_protocol, Protocol)
        self.process.executes_protocol = Protocol()
        self.assertIsInstance(self.process.executes_protocol, Protocol)

        with self.assertRaises(AttributeError) as context:
            self.process.executes_protocol = 1
        self.assertTrue('Process.executes_protocol must be a Protocol or None; '
                        'got 1:<class \'int\'>' in str(context.exception))

    def test_date(self):
        self.assertIsNone(self.process.date)
        self.process.date = '2017-01-01'
        self.assertTrue(self.process.date == '2017-01-01')

        with self.assertRaises(AttributeError) as context:
            self.process.date = 1
        self.assertTrue('Process.date must be a string' in str(context.exception))

    def test_performer(self):
        self.assertIsNone(self.process.performer)
        self.process.performer = 'test'
        self.assertTrue(self.process.performer == 'test')

        with self.assertRaises(AttributeError) as context:
            self.process.performer = 1
        self.assertTrue('Process.performer must be a string' in str(context.exception))

    def test_parameter_values(self):
        self.assertTrue(self.process.parameter_values == [])
        self.process.parameter_values = [ParameterValue()]
        self.assertTrue(self.process.parameter_values == [ParameterValue()])

        with self.assertRaises(AttributeError) as context:
            self.process.parameter_values = 1
        self.assertTrue('Process.parameter_values must be iterable containing ParameterValues'
                        in str(context.exception))

    def test_inputs(self):
        self.assertTrue(self.process.inputs == [])
        self.process.inputs = [DataFile()]
        self.assertTrue(self.process.inputs == [DataFile()])

        expected_error = ('Process.inputs must be iterable containing objects of types '
                          '(Material, Source, Sample, DataFile)')
        with self.assertRaises(AttributeError) as context:
            self.process.inputs = 1
        self.assertTrue(expected_error in str(context.exception))

    def test_outputs(self):
        self.assertTrue(self.process.outputs == [])
        self.process.outputs = [DataFile()]
        self.assertTrue(self.process.outputs == [DataFile()])

        expected_error = ('Process.outputs must be iterable containing objects of types '
                          '(Material, Source, Sample, DataFile)')
        with self.assertRaises(AttributeError) as context:
            self.process.outputs = 1
        self.assertTrue(expected_error in str(context.exception))

    def test_previous_process(self):
        self.assertIsNone(self.process.prev_process)
        self.process.prev_process = Process()
        self.assertIsInstance(self.process.prev_process, Process)

        with self.assertRaises(AttributeError) as context:
            self.process.prev_process = 1
        self.assertTrue('Process.prev_process must be a Process or None; got 1:<class \'int\'>'
                        in str(context.exception))

    def test_next_process(self):
        self.assertIsNone(self.process.next_process)
        self.process.next_process = Process()
        self.assertIsInstance(self.process.next_process, Process)

        with self.assertRaises(AttributeError) as context:
            self.process.next_process = 1
        self.assertTrue('Process.next_process must be a Process or None; got 1:<class \'int\'>'
                        in str(context.exception))

    def test_repr(self):
        expected_protocol_str = ("Protocol(\n\t"
                                 "name=\n\t"
                                 "protocol_type=\n\t"
                                 "uri=\n\t"
                                 "version=\n\t"
                                 "parameters=0 ProtocolParameter objects\n\t"
                                 "components=0 OntologyAnnotation objects\n\t"
                                 "comments=0 Comment objects\n)")
        expected_str = ('isatools.model.process.Process(id="test". name="None", executes_protocol={0}, '
                        'date="None", performer="None", inputs=[], outputs=[])').format(expected_protocol_str)
        self.assertEqual(expected_str, repr(self.process))
        self.assertEqual(hash(self.process), hash(repr(self.process)))

    def test_str(self):
        self.assertTrue(str(self.process) == 'Process(name=None)')

    def test_equalities(self):
        self.assertEqual(Process(id_="1"), Process(id_="1"))
        self.assertNotEqual(self.process, Process())
        self.assertNotEqual(self.process, 1)

    @patch('isatools.model.identifiable.uuid4', return_value='uuid')
    def test_to_dict(self, mocked_uuid4):
        process = Process(name='', id_='process_id')
        expected_dict = {
            '@id': 'process_id',
            'name': '',
            'executes_protocol': {"@id": '#protocol/' + mocked_uuid4.return_value},
            'date': '',
            'performer': '',
            'parameterValues': [],
            'inputs': [],
            'outputs': [],
            'comments': []
        }
        self.assertEqual(process.to_dict(), expected_dict)

        # Test strings
        process.name = 'test_process'
        expected_dict['name'] = 'test_process'
        process.performer = 'test_performer'
        expected_dict['performer'] = 'test_performer'
        process.date = '2017-01-01'
        expected_dict['date'] = '2017-01-01'
        self.assertEqual(process.to_dict(), expected_dict)

        # Test inputs and outputs
        process.inputs = [Material(id_='material_id')]
        expected_dict['inputs'] = [{'@id': 'material_id'}]
        process.outputs = [Material(id_='material_id2')]
        expected_dict['outputs'] = [{'@id': 'material_id2'}]
        self.assertEqual(process.to_dict(), expected_dict)

        # Test previous and next process
        process.prev_process = Process(id_='process_id2')
        expected_dict['previousProcess'] = {'@id': 'process_id2'}
        process.next_process = Process(id_='process_id3')
        expected_dict['nextProcess'] = {'@id': 'process_id3'}
        self.assertEqual(process.to_dict(), expected_dict)

        # Test parameters values
        category = ProtocolParameter(id_='category_id')
        value = OntologyAnnotation(term='test_value', id_='value_id')
        process.parameter_values = [ParameterValue(value="abc", category=category)]
        expected_dict['parameterValues'] = [{'category': {'@id': 'category_id'}, 'value': 'abc', 'unit': ''}]
        self.assertEqual(process.to_dict(), expected_dict)
        process.parameter_values = [ParameterValue(value=value, category=category)]
        expected_dict['parameterValues'] = [
            {
                'category': {'@id': 'category_id'},
                'value': {
                    '@id': 'value_id', 'annotationValue': 'test_value',
                    'termSource': '', 'termAccession': '', 'comments': []
                },
                'unit': ''
            }
        ]
        self.assertEqual(process.to_dict(), expected_dict)
        unit = OntologyAnnotation(term='mg', id_='unit_id')
        process.parameter_values = [ParameterValue(value=1, category=category, unit=unit)]
        expected_dict['parameterValues'] = [
            {'category': {'@id': 'category_id'}, 'value': 1, 'unit': {'@id': 'unit_id'}}
        ]
        self.assertEqual(process.to_dict(), expected_dict)
