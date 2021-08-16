import os
import unittest
from isatools.isatab import load


class TestGraphQLQueries(unittest.TestCase):

    def setUp(self):
        self.here_path = os.path.dirname(os.path.realpath(__file__))
        graph_filepath = os.path.join(self.here_path, "data/graphQL/example.graphql")
        investigation_filepath = os.path.join(self.here_path, "data/tab/BII-S-TEST/i_test.txt")
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
        print(response.data)

    def test_introspection(self):
        response = self.investigation.introspect()
        print(response.data)


