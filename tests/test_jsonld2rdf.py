import unittest
import os
from json import load, dumps, dump
from isatools.convert.jsonld2ttl import JSONLDToTTLConverter
from rdflib import Graph


class TestJsonLDtoTTLConverter(unittest.TestCase):

    def setUp(self):
        # the input json-ld for the converter:
        self.test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/json/BII-S-3/')

    def test_jsonld2ttl(self):
        # the input json-ld file:
        jsonld_filename = "BII-S-3-ld-isaterms-combined.jsonld"
        jsonld_path = os.path.join(self.test_path, jsonld_filename)

        # the name of the output file resulting from the conversion:
        turtle_filename = "BII-S-3-ld-isaterms-combined.ttl"
        turtle_path = os.path.join(self.test_path, turtle_filename)

        # the expected output, a known quantity:
        expected_turtle_path = os.path.join(self.test_path, "BII-S-3-ld-isaterms-combined-reference.ttl")
        expected_graph = Graph()
        expected_graph.parse(expected_turtle_path)
        # print(f"reference Graph g has {len(expected_graph)} statements.")

        # invoking the conversion:
        JSONLDToTTLConverter(jsonld_path, turtle_path)

        # reading the result of the conversion and testing
        with open(turtle_path, 'r') as rdf_file:
            converted_graph = Graph()
            converted_graph.parse(rdf_file)
            # print(f"converted Graph g has {len(converted_graph)} statements.")

        self.assertEqual(len(converted_graph), len(expected_graph))
        self.assertEqual(len(converted_graph), 2472)
        self.assertTrue(converted_graph, expected_graph)
