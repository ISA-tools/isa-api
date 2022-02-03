import os
import unittest
import logging
from isatools.isatab import load
from isatools.graphQL.utils.validate import validate_input, validate_outputs
from isatools.graphQL.utils.search import (
    search_assays,
    search_process_sequence,
    search_inputs,
    search_outputs,
    search_data_files,
    search_parameter_values
)
from isatools.graphQL.utils.find import (
    find_technology_type,
    find_measurement,
    find_exposure_value,
    find_characteristics,
    find_protocol,
    compare_values
)

here_path = os.path.dirname(os.path.realpath(__file__))
investigation_filepath = os.path.join(here_path, "data/tab/BII-S-TEST/i_test.txt")
with open(investigation_filepath, 'r') as investigation_file:
    investigation = load(investigation_file)
    investigation_file.close()

log = logging.getLogger('isatools')


class I0Data:
    def __init__(self, target, treatment_group, characteristics):
        self.target = target
        self.treatmentGroup = treatment_group
        self.characteristics = characteristics


class TestGraphQLQueries(unittest.TestCase):

    def setUp(self):
        graph_filepath = os.path.join(here_path, "data/graphQL/example.gql")
        with open(graph_filepath, 'r') as graph_file:
            self.query = graph_file.read()
            graph_file.close()

    def test_full_query(self):
        variables = {
            "technologyType": "nucleotide sequencing",
            "measurementType": "transcription profiling",
            "fileType": "Raw Data F",
            "protocol": "nucleic acid ext",
            "compound": "carbon diox",
            "dose": "high"
        }
        response = investigation.execute_query(self.query, variables)
        log.warning('graphQL')
        log.warning(response)
        self.assertTrue(not response.errors)

    def test_introspection(self):
        response = investigation.introspect()
        self.assertTrue(not response.errors)


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.input_data = I0Data("Sample", "group", "characteristics")

    def test_validate_inputs(self):
        valid = validate_input({})
        self.assertTrue(valid)
        valid = validate_input(self.input_data)
        self.assertTrue(valid)

    def test_validate_outputs(self):
        valid = validate_outputs({})
        self.assertTrue(valid)
        valid = validate_outputs(self.input_data)
        self.assertTrue(valid)

    def test_validation_exceptions(self):
        self.input_data = I0Data("TEST", "group", "characteristics")
        with self.assertRaises(Exception) as context:
            validate_input(self.input_data)
        self.assertTrue("Inputs 'on' argument should be Material, DataFile, Sample or Source" == str(context.exception))
        with self.assertRaises(Exception) as context:
            validate_outputs(self.input_data)
        self.assertTrue("Outputs 'on' argument should be Material, DataFile or Sample" == str(context.exception))

        self.input_data = I0Data("Material", "group", "characteristics")
        with self.assertRaises(Exception) as context:
            validate_input(self.input_data)
        self.assertTrue("Inputs 'treatmentGroup' argument can only be applied to Sample" == str(context.exception))
        self.input_data = I0Data("DataFile", None, "characteristics")
        with self.assertRaises(Exception) as context:
            validate_input(self.input_data)
        self.assertTrue("Inputs 'characteristics' argument can only be applied to Sample, Material or Source"
                        == str(context.exception))


class TestSearch(unittest.TestCase):

    def test_search_assays(self):
        assays = search_assays(investigation.studies[0].assays, {}, "AND")
        self.assertTrue(len(assays) == 2)

        filters = {
            "target": "Sample",
            "technologyType": {"eq": "nucleotide sequencing"},
            "measurementType": {"eq": "transcription profiling"},
            "executesProtocol": {"includes": "nucleic acid ext"},
            "characteristics": [
                {
                    "name": {"eq": "category"},
                    "value": {"eq": "anatomical part"}
                },
                {
                    "name": {"eq": "value"},
                    "value": {"eq": "liver"}
                }
            ],
            "treatmentGroup": [
                {
                    "name": {"eq": "compound"},
                    "value": {"includes": "carb"}
                }
            ]
        }
        assays = search_assays(investigation.studies[0].assays, filters, "AND")
        self.assertTrue(len(assays) == 1)
        self.assertTrue(assays[0].filename == "a_test-assay-Tx.txt")

        assays = search_assays(investigation.studies[0].assays, filters, "OR")
        self.assertTrue(len(assays) == 2)

        filters = {
            "parameterValues": {
                "category": {"eq": "library strategy"},
                "value": {"eq": "WGS"}
            }
        }
        assays = search_assays(investigation.studies[0].assays, filters, "AND")
        self.assertTrue(len(assays) == 1)

        with self.assertRaises(Exception) as context:
            search_assays(investigation.studies[0].assays, filters, "TEST")
        self.assertTrue("Operator should be AND or OR" == str(context.exception))

    def test_search_process_sequence(self):
        process_sequence = search_process_sequence(investigation.studies[0].assays[0].process_sequence, {}, 'AND')
        self.assertTrue(len(process_sequence) == 18)

        process_sequence = search_process_sequence(investigation.studies[0].assays[0].process_sequence, {
            "target": "Sample"
        }, 'AND')
        self.assertTrue(len(process_sequence) == 18)

        filters = {
            "executesProtocol": {"includes": "nucleic acid ext"},
            "treatmentGroup": [
                {
                    "name": {"eq": "compound"},
                    "value": {"includes": "carb"}
                }
            ]
        }
        process_sequence = search_process_sequence(investigation.studies[0].assays[0].process_sequence, filters, 'AND')
        self.assertTrue(len(process_sequence) == 8)
        filters['target'] = "Sample"
        filters['characteristics'] = [
            {
                "name": {"eq": "category"},
                "value": {"eq": "anatomical part"}
            },
            {
                "name": {"eq": "value"},
                "value": {"eq": "liver"}
            }
        ]
        process_sequence = search_process_sequence(investigation.studies[0].assays[0].process_sequence, filters, 'AND')
        self.assertTrue(len(process_sequence) == 3)
        process_sequence = search_process_sequence(investigation.studies[0].assays[0].process_sequence, filters, 'OR')
        self.assertTrue(len(process_sequence) == 8)

        filters = {"parameterValues": {
            "category": {"eq": "library strategy"},
            "value": {"includes": "WG"}
        }}
        process_sequence = search_process_sequence(investigation.studies[0].assays[0].process_sequence, filters, 'AND')
        self.assertTrue(len(process_sequence) == 4)

        with self.assertRaises(Exception) as context:
            search_process_sequence(investigation.studies[0].assays[0].process_sequence, filters, 'TEST')
        self.assertTrue("Operator should be AND or OR" == str(context.exception))

    def test_search_inputs(self):
        filters = {}
        inputs = search_inputs(investigation.studies[0].assays[0].process_sequence[0].inputs, filters, "AND")
        self.assertTrue(inputs[0].name == "GSM255770")

        filters = {
            "treatmentGroup": [
                {
                    "name": {"eq": "compound"},
                    "value": {"includes": "carb"}
                }
            ],
            "target": "Sample"
        }
        found = 0
        for process in investigation.studies[0].assays[0].process_sequence:
            inputs = search_inputs(process.inputs, filters, "AND")
            if len(inputs) > 0:
                found += 1
                self.assertTrue(type(inputs[0]).__name__ == "Sample")
        self.assertTrue(found == 4)

        found = 0
        filters['treatmentGroup'][0]['value'] = {"eq": "test"}
        for process in investigation.studies[0].assays[0].process_sequence:
            inputs = search_inputs(process.inputs, filters, "AND")
            if len(inputs) > 0:
                found += 1
        self.assertTrue(found == 0)

        filters['treatmentGroup'][0]['value'] = {"includes": "carb"}
        filters['characteristics'] = [
            {
                "name": {"eq": "category"},
                "value": {"eq": "anatomical part"}
            },
            {
                "name": {"eq": "value"},
                "value": {"eq": "liver"}
            }
        ]
        for process in investigation.studies[0].assays[0].process_sequence:
            inputs = search_inputs(process.inputs, filters, "AND")
            if len(inputs) > 0:
                found += 1
                self.assertTrue(type(inputs[0]).__name__ == "Sample")
        self.assertTrue(found == 3)
        found = 0

        for process in investigation.studies[0].assays[0].process_sequence:
            inputs = search_inputs(process.inputs, filters, "OR")
            if len(inputs) > 0:
                found += 1
                self.assertTrue(type(inputs[0]).__name__ == "Sample")
        self.assertTrue(found == 4)

    def test_search_outputs(self):
        filters = {}
        found = 0
        for process in investigation.studies[0].assays[0].process_sequence:
            outputs = search_outputs(process.outputs, filters)
            if len(outputs) > 0:
                found += 1
                self.assertTrue(type(outputs[0]).__name__ in ["Material", "DataFile"])
        self.assertTrue(found == 14)

        found = 0
        filters = {
            "target": "DataFile",
            "label": {"eq": "Raw Data File"}
        }
        for process in investigation.studies[0].assays[0].process_sequence:
            outputs = search_outputs(process.outputs, filters)
            if len(outputs) > 0:
                found += 1
                self.assertTrue(type(outputs[0]).__name__ == "DataFile")
        self.assertTrue(found == 6)

        found = 0
        filters = {
            "target": "Material",
            "label": {"includes": "Extract Name"}
        }
        for process in investigation.studies[0].assays[0].process_sequence:
            outputs = search_outputs(process.outputs, filters)
            if len(outputs) > 0:
                found += 1
                self.assertTrue(type(outputs[0]).__name__ == "Material")
                self.assertTrue(outputs[0].type in ["Extract Name", "Labeled Extract Name"])
        self.assertTrue(found == 8)

        found = 0
        filters = {
            "target": "Sample",
            "label": {"includes": "123"}
        }
        for process in investigation.studies[0].assays[0].process_sequence:
            outputs = search_outputs(process.outputs, filters)
            if len(outputs) > 0:
                found += 1
        self.assertTrue(found == 0)

    def test_search_data_files(self):
        files = search_data_files(investigation.studies[0].assays[0].data_files, {"eq": "Raw Data File"})
        self.assertTrue(len(files) == 6)

    def test_search_parameter_values(self):
        found = 0
        for process in investigation.studies[0].assays[0].process_sequence:
            if len(process.parameter_values) > 0:
                parameter_values = search_parameter_values(process, {})
                if len(parameter_values) > 0:
                    found += 1
        self.assertTrue(found == 10)

        found = 0
        filters = {
            "parameterValues": {
                "category": {"eq": "library strategy"},
                "value": {"includes": "WG"}
            }
        }
        for process in investigation.studies[0].assays[0].process_sequence:
            if len(process.parameter_values) > 0:
                parameter_values = search_parameter_values(process, filters)
                if len(parameter_values) > 0:
                    found += 1
        self.assertTrue(found == 4)


class TestFind(unittest.TestCase):

    def setUp(self):
        class FindObject:
            def __init__(self, term):
                self.term = term
        self.template = FindObject("test")
        self.sample = investigation.studies[0].assays[0].process_sequence[0].inputs[0]

    def test_find_technology_type(self):
        found = find_technology_type(self.template, "test", "eq")
        self.assertTrue(found)
        found = find_technology_type(self.template, "anotherTest", "eq")
        self.assertFalse(found)

    def test_find_measurement(self):
        found = find_measurement(self.template, "test", "eq")
        self.assertTrue(found)
        found = find_measurement(self.template, "anotherTest", "eq")
        self.assertFalse(found)

    def test_find_exposure_value(self):
        found = find_exposure_value(self.sample, None, None)
        self.assertTrue(found)
        found = find_exposure_value(self.sample, {"value": {"includes": "carb"}}, {"eq": "compound"})
        self.assertTrue(found)
        found = find_exposure_value(self.sample, {"value": {"eq": "carb"}}, {"eq": "compound"})
        self.assertFalse(found)

    def test_find_characteristics(self):
        found = find_characteristics(self.sample, None)
        self.assertTrue(found)
        found = find_characteristics(self.sample, {
            "value": {"eq": "anatomical part"},
            "name": {"eq": "category"}
        })
        self.assertTrue(found)
        found = find_characteristics(self.sample, {
            "value": {"eq": "anatomical part"},
            "name": {"eq": "cat"}
        })
        self.assertFalse(found)

        from copy import copy
        another_sample = copy(self.sample)
        another_sample.characteristics = []
        found = find_characteristics(another_sample, {
            "value": {"eq": "anatomical part"},
            "name": {"eq": "category"}
        })
        self.assertFalse(found)

    def test_find_protocol(self):
        found = find_protocol(None, None, None)
        self.assertTrue(found)
        found = find_protocol(investigation.studies[0].assays[0].process_sequence, "nucleic acid extraction", "eq")
        self.assertTrue(found)
        found = find_protocol(investigation.studies[0].assays[0].process_sequence, "nucleic acid", "eq")
        self.assertFalse(found)

    def test_compare_values(self):
        self.assertTrue(compare_values("test", "test", "eq"))
        self.assertFalse(compare_values("test1", "test", "eq"))
        self.assertTrue(compare_values("test", "te", "includes"))
        self.assertFalse(compare_values("test", "123", "includes"))

        self.assertTrue(compare_values(100, 90, "lt"))
        self.assertTrue(compare_values(100, 90, "lte"))
        self.assertFalse(compare_values(90, 100, "lt"))
        self.assertFalse(compare_values(90, 100, "lte"))

        self.assertTrue(compare_values(90, 100, "gt"))
        self.assertTrue(compare_values(90, 100, "gte"))
        self.assertFalse(compare_values(100, 90, "gt"))
        self.assertFalse(compare_values(100, 90, "gte"))

        with self.assertRaises(Exception) as context:
            compare_values(100, "test", "gte")
        error = "Both value and target should be integers when using lt, gt, lte or gte got value: '100' " \
                "and target: 'test'"
        self.assertTrue(error == str(context.exception))
        self.assertFalse(compare_values("100", 90, "gte"))
