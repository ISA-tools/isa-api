import os
import unittest
from isatools.isatab import load
from isatools.graphQL.utils.validate import validate_input, validate_outputs


class I0Data:
    def __init__(self, target, treatment_group, characteristics):
        self.target = target
        self.treatmentGroup = treatment_group
        self.characteristics = characteristics


class TestGraphQLQueries(unittest.TestCase):

    def setUp(self):
        self.here_path = os.path.dirname(os.path.realpath(__file__))
        graph_filepath = os.path.join(self.here_path, "../data/graphQL/example.graphql")
        investigation_filepath = os.path.join(self.here_path, "../data/tab/BII-S-TEST/i_test.txt")
        with open(graph_filepath, 'r') as graph_file:
            self.query = graph_file.read()
            graph_file.close()
        with open(investigation_filepath, 'r') as investigation_file:
            self.investigation = load(investigation_file)
            investigation_file.close()

    def test_full_query(self):
        variables = {
            "measurement": "metagenome sequencing",
            "executes": "nucleic acid extraction",
            "fileType": "Raw Data File",
            "compound": "carbon dioxide",
            "dose1": "normal",
            "technologyType": "nucleotide sequencing",
            "dose2": "high",
            "material": "Extract Name"
        }
        response = self.investigation.execute_query(self.query, variables)
        self.assertTrue(response.errors)

    def test_introspection(self):
        response = self.investigation.introspect()
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
