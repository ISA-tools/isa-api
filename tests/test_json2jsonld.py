import unittest
import os
from json import load, dump
from isatools.convert.json2jsonld import ISALDSerializer


class TestJson2JsonLD(unittest.TestCase):

    def setUp(self):
        self.test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/json/BII-S-3/')
        self.output_path = os.path.join(self.test_path, "BII-S-3-ld.json")
        with open(self.output_path, 'r') as output_file:
            self.expected_markup = load(output_file)

        combined_markup_path = os.path.join(self.test_path, "BII-S-3-ld-isaterms-combined-reference.jsonld")
        with open(combined_markup_path, 'r') as combined_file:
            self.combined_expected_markup = load(combined_file)

        not_combined_markup_path = os.path.join(self.test_path, "BII-S-3-ld-isaterms-remote-reference.jsonld")
        with open(not_combined_markup_path, 'r') as not_combined_file:
            self.not_combined_expected_markup = load(not_combined_file)

        instance_url = "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/tests/json/BII-S-3/BII-S-3-with@id.json"
        self.serializer = ISALDSerializer(instance_url, ontology="obo", combined=False)

    def test_BII_s_3_convert_remote(self):
        self.assertEqual(self.serializer.output, self.expected_markup)

    def test_BII_s_3_convert_local(self):
        instance_path = os.path.join(self.test_path, "BII-S-3-with@id.json")
        # with open(instance_path, 'r') as instance_file:
        #     instance = load(instance_file)
        #     instance_file.close()
        self.serializer.set_ontology("obo")
        self.serializer.set_contexts_method(False)
        self.serializer.set_instance(instance_path)
        self.assertEqual(self.serializer.output, self.expected_markup)

    def test_singleton(self):
        instance_url = "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/tests/json/BII-S-3/BII-S-3-with@id.json"
        serializer = ISALDSerializer(instance_url, ontology="obo", combined=True)
        self.assertTrue(self.serializer is serializer)
        self.assertTrue(id(self.serializer) == id(serializer))

    def test_inject_combined_contexts(self):
        self.serializer.set_ontology('isaterms')
        self.serializer.set_contexts_method(True)
        self.serializer.set_instance(
            "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/tests/json/BII-S-3/BII-S-3-with@id.json"
        )
        with open("./data/json/BII-S-3/BII-S-3-ld-isaterms-combined-test.jsonld", 'w') as out:
            dump(self.serializer.output,  out, ensure_ascii=False, indent=4)
        self.assertEqual(self.serializer.output, self.combined_expected_markup)

    def test_inject_remote_contexts(self):
        self.serializer.set_ontology('isaterms')
        self.serializer.set_contexts_method(False)
        self.serializer.set_instance(
            "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/tests/json/BII-S-3/BII-S-3-with@id.json"
        )
        with open("./data/json/BII-S-3/BII-S-3-ld-isaterms-remote-test.jsonld", 'w+') as out:
            dump(self.serializer.output,  out, ensure_ascii=False, indent=4)
        self.assertEqual(self.serializer.output, self.not_combined_expected_markup)
