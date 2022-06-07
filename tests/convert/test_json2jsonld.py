import unittest
import os
from json import load, dumps, dump
from isatools.convert.json2jsonld import ISALDSerializer


@unittest.skip("Not working yet")
class TestJson2JsonLD(unittest.TestCase):

    def setUp(self):
        self.test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/json/BII-S-3/')
        output_path = os.path.join(self.test_path, "BII-S-3-ld.json")
        with open(output_path, 'r') as output_file:
            self.expected_markup = load(output_file)

        alternative_markup_path = os.path.join(self.test_path, "BII-S-3-ld-isaterms-combined-test.jsonld")
        with open(alternative_markup_path, 'r') as alternative_file:
            self.alternative_expected_markup = load(alternative_file)

        instance_url = "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/tests/json/BII-S-3/BII-S-3-with@id.json"
        self.serializer = ISALDSerializer(instance_url)

    def test_BII_s_3_convert_remote(self):
        self.assertEqual(self.serializer.output, self.expected_markup)

    def test_BII_s_3_convert_local(self):
        instance_path = os.path.join(self.test_path, "BII-S-3-with@id.json")
        with open(instance_path, 'r') as instance_file:
            instance = load(instance_file)
            instance_file.close()
        self.serializer.set_ontology("obo")
        self.serializer.set_instance(instance)
        self.assertEqual(self.serializer.output, self.expected_markup)

    def test_singleton(self):
        instance_url = "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/tests/json/BII-S-3/BII-S-3-with@id.json"
        serializer = ISALDSerializer(instance_url)
        self.assertTrue(self.serializer is serializer)
        self.assertTrue(id(self.serializer) == id(serializer))

    def test_inject_combined_contexts(self):
        self.serializer.set_ontology('isaterms')
        self.serializer.set_contexts_method(True)
        self.serializer.set_instance(
            "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/tests/json/BII-S-3/BII-S-3-with@id.json"
        )
        # with open("./data/json/BII-S-3/BII-S-3-ld-isaterms-combined.jsonld", 'w') as out:
        #     dump(self.serializer.output,  out, ensure_ascii=False, indent=4)
        self.assertEqual(self.serializer.output, self.alternative_expected_markup)
