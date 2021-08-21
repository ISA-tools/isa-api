import unittest
import os
import json
from json import load
from isatools.convert.json2jsonld import ISALDSerializer


class TestJson2JsonLD(unittest.TestCase):

    def setUp(self):
        output_path = os.path.join("./data/json/BII-S-3/", "BII-S-3-ld-v0.json")
        with open(output_path, 'r') as output_file:
            self.expected_markup = load(output_file)
            output_file.close()

        instance_url = "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/master/json/BII-S-3/BII-S-3.json"
        self.serializer = ISALDSerializer(instance_url)
        self.serializer.set_ontology("obo")

    # def test_BII_s_3_convert_remote(self):
        # self.assertEqual(self.serializer.output, self.expected_markup)

    def test_BII_s_3_convert_local(self):
        # ontologies = ['obo', 'wdt', 'sdo']
        instance_path = os.path.join("./data/json/BII-S-3/", "BII-S-3.json")

        with open(instance_path, 'r') as instance_file:
            instance = load(instance_file)
            instance_file.close()
        # for ontology in ontologies:
            ontology = "obo"
            self.serializer.set_ontology(ontology)
            self.serializer.set_instance(instance)
            # self.maxDiff = None
            # self.assertEqual(self.serializer.output, self.expected_markup)
            jsonldcontent = self.serializer.output
        try:
            with open(os.path.join("./data/json/BII-S-3/", "BII-S-3-ld-new-v1.json"), 'w') as outfile:
                # outfile.write(str(jsonldcontent))
                json.dump(jsonldcontent,  outfile, ensure_ascii=False, indent=4)
        except IOError as ioe:
            print(ioe)

    def test_singleton(self):
        instance_url = "https://raw.githubusercontent.com/ISA-tools/ISAdatasets/master/json/BII-S-3/BII-S-3.json"
        serializer = ISALDSerializer(instance_url)
        self.assertTrue(self.serializer is serializer)
        self.assertTrue(id(self.serializer) == id(serializer))
