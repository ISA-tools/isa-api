import unittest
from unittest.mock import patch, mock_open, MagicMock
from isatools.convert.json2jsonld import ISALDSerializer


class TestISALDSerializer(unittest.TestCase):

    @patch('isatools.convert.json2jsonld.get')
    def test_set_instance_with_url(self, mock_get):
        mock_get.return_value.text = '{"key": "value"}'
        serializer = ISALDSerializer(json_instance="https://example.com/instance.json")
        self.assertEqual(serializer.instance, {"key": "value"})

    # @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"properties": {}}')
    # @patch('os.listdir', return_value=['schema1.json', 'schema2.json'])
    # def test_resolve_network(self, mock_listdir, mock_open_file):
    #     serializer = ISALDSerializer(json_instance={})
    #     self.assertIn('schema1.json', serializer.schemas)
    #     self.assertIn('schema2.json', serializer.schemas)

    def test_set_contexts_method(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.set_contexts_method(combined=True)
        self.assertTrue(serializer.combined)

    def test_set_format(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.set_format(output_format="jsonld")
        self.assertEqual(serializer.format, "jsonld")

    def test_set_ontology(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.set_ontology("sdo")
        self.assertEqual(serializer.ontology, "sdo")

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"@context": {}, "@type": "Test"}')
    def test_inject_ld_split(self, mock_open_file):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {"test_schema.json": {"properties": {"field": {"type": "string"}}}}
        instance = {"field": "value"}
        output = serializer._inject_ld_split("test_schema.json", {}, instance)
        self.assertEqual(output["field"], "value")
        self.assertIn("@context", output)

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"@context": {}, "@type": "Test"}')
    def test_inject_ld_collapsed(self, mock_open_file):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {"test_schema.json": {"properties": {"field": {"type": "string"}}}}
        instance = {"field": "value"}
        output = serializer._inject_ld_collapsed("test_schema.json", {}, instance)
        self.assertEqual(output["field"], "value")
        self.assertIn("@type", output)

    def test_get_context_key(self):
        key = ISALDSerializer._get_context_key("test_schema.json")
        self.assertEqual(key, "Test")

    def test_get_any_of_ref(self):
        ref = ISALDSerializer._get_any_of_ref("http://example.com/schema#field")
        self.assertEqual(ref, "field_schema.json")




class TestISALDSerializerAdditional(unittest.TestCase):

    @patch('isatools.convert.json2jsonld.get')
    def test_set_instance_with_invalid_url(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        serializer = ISALDSerializer(json_instance="http://invalid-url.com")
        self.assertEqual(serializer.instance, {})

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"invalid": "schema"}')
    def test_resolve_network_with_invalid_schema(self, mock_open_file):
        with self.assertRaises(KeyError):
            serializer = ISALDSerializer(json_instance={})
            serializer._resolve_network()

    def test_set_format_with_invalid_format(self):
        serializer = ISALDSerializer(json_instance={})
        with self.assertRaises(AttributeError):
            serializer.set_format(output_format="invalid_format")

    def test_get_context_url_with_edge_case(self):
        serializer = ISALDSerializer(json_instance={})
        url = serializer._get_context_url("test_schema.json")
        self.assertIn("test_schema", url)

    def test_get_any_of_ref_with_invalid_input(self):
        ref = ISALDSerializer._get_any_of_ref("invalid#input")
        self.assertEqual(ref, "input_schema.json")

    def test_get_context_key_with_edge_case(self):
        key = ISALDSerializer._get_context_key("test_schema.json")
        self.assertEqual(key, "Test")

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"@context": {}, "@type": "Test"}')
    def test_inject_ld_split_with_nested_json(self, mock_open_file):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "nested": {"type": "object", "properties": {"field": {"type": "string"}}}
                }
            }
        }
        instance = {"nested": {"field": "value"}}
        output = serializer._inject_ld_split("test_schema.json", {}, instance)
        self.assertEqual(output["nested"]["field"], "value")
        self.assertIn("@context", output)

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"@context": {}, "@type": "Test"}')
    def test_inject_ld_collapsed_with_nested_json(self, mock_open_file):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "nested": {"type": "object", "properties": {"field": {"type": "string"}}}
                }
            }
        }
        instance = {"nested": {"field": "value"}}
        output = serializer._inject_ld_collapsed("test_schema.json", {}, instance)
        self.assertEqual(output["nested"]["field"], "value")
        self.assertIn("@type", output)


if __name__ == "__main__":
    unittest.main()
