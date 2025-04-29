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

    class TestInjectLDSplit(unittest.TestCase):

        @patch('isatools.convert.json2jsonld.open', new_callable=mock_open,
               read_data='{"properties": {"field": {"type": "string"}}}')
        def test_inject_ld_split_basic(self, mock_open):
            serializer = ISALDSerializer(json_instance={})
            serializer.schemas = {
                "test_schema.json": {
                    "properties": {
                        "field": {"type": "string"}
                    }
                }
            }
            instance = {"field": "value"}
            output = {}
            result = serializer._inject_ld_split("test_schema.json", output, instance)
            self.assertEqual(result["field"], "value")
            self.assertIn("@context", result)
            self.assertIn("@type", result)

        def test_inject_ld_split_with_array(self):
            serializer = ISALDSerializer(json_instance={})
            serializer.schemas = {
                "test_schema.json": {
                    "properties": {
                        "array_field": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
            instance = {"array_field": ["value1", "value2"]}
            output = {}
            result = serializer._inject_ld_split("test_schema.json", output, instance)
            self.assertEqual(result["array_field"], ["value1", "value2"])

        def test_inject_ld_split_with_object(self):
            serializer = ISALDSerializer(json_instance={})
            serializer.schemas = {
                "test_schema.json": {
                    "properties": {
                        "object_field": {"type": "object", "properties": {"subfield": {"type": "string"}}}
                    }
                }
            }
            instance = {"object_field": {"subfield": "subvalue"}}
            output = {}
            result = serializer._inject_ld_split("test_schema.json", output, instance)
            self.assertEqual(result["object_field"]["subfield"], "subvalue")

        def test_inject_ld_split_with_ref(self):
            serializer = ISALDSerializer(json_instance={})
            serializer.schemas = {
                "test_schema.json": {
                    "properties": {
                        "ref_field": {"$ref": "ref_schema.json"}
                    }
                },
                "ref_schema.json": {
                    "properties": {
                        "nested_field": {"type": "string"}
                    }
                }
            }
            instance = {"ref_field": {"nested_field": "nested_value"}}
            output = {}
            result = serializer._inject_ld_split("test_schema.json", output, instance)
            self.assertEqual(result["ref_field"]["nested_field"], "nested_value")

        def test_inject_ld_split_with_anyOf(self):
            serializer = ISALDSerializer(json_instance={})
            serializer.schemas = {
                "test_schema.json": {
                    "properties": {
                        "value": {
                            "anyOf": [
                                {"$ref": "ref_schema.json"}
                            ]
                        }
                    }
                },
                "ref_schema.json": {
                    "properties": {
                        "nested_field": {"type": "string"}
                    }
                }
            }
            instance = {"value": {"nested_field": "nested_value"}}
            output = {}
            result = serializer._inject_ld_split("test_schema.json", output, instance)
            self.assertEqual(result["value"]["nested_field"], "nested_value")

        def test_inject_ld_split_with_nested_array_of_objects(self):
            serializer = ISALDSerializer(json_instance={})
            serializer.schemas = {
                "test_schema.json": {
                    "properties": {
                        "array_field": {
                            "type": "array",
                            "items": {"$ref": "nested_schema.json"}
                        }
                    }
                },
                "nested_schema.json": {
                    "properties": {
                        "subfield": {"type": "string"}
                    }
                }
            }
            instance = {"array_field": [{"subfield": "value1"}, {"subfield": "value2"}]}
            output = {}
            result = serializer._inject_ld_split("test_schema.json", output, instance)
            self.assertEqual(result["array_field"][0]["subfield"], "value1")
            self.assertEqual(result["array_field"][1]["subfield"], "value2")

    # @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"@context": {}, "@type": "Test"}')
    # def test_inject_ld_split(self, mock_open_file):
    #     serializer = ISALDSerializer(json_instance={})
    #     serializer.schemas = {"test_schema.json": {"properties": {"field": {"type": "string"}}}}
    #     instance = {"field": "value"}
    #     output = serializer._inject_ld_split("test_schema.json", {}, instance)
    #     self.assertEqual(output["field"], "value")
    #     self.assertIn("@context", output)

    @patch('isatools.convert.json2jsonld.open', new_callable=MagicMock)
    def test_inject_ld_split(self, mock_open):
        # Mock schema and instance
        mock_open.return_value.__enter__.return_value.read.return_value = '{"properties": {"field": {"type": "string"}}}'
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "field": {"type": "string"},
                    "nested": {"type": "object", "properties": {"subfield": {"type": "string"}}}
                }
            }
        }
        instance = {"field": "value", "nested": {"subfield": "subvalue"}}
        output = {}

        # Call the method
        result = serializer._inject_ld_split("test_schema.json", output, instance)

        # Assertions
        self.assertIn("@context", result)
        self.assertIn("@type", result)
        self.assertEqual(result["field"], "value")
        self.assertIn("nested", result)
        self.assertEqual(result["nested"]["subfield"], "subvalue")

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
        ref = ISALDSerializer._get_any_of_ref("https://example.com/schema#field")
        self.assertEqual(ref, "field_schema.json")


class TestISALDSerializerAdditional(unittest.TestCase):

    # @patch('isatools.convert.json2jsonld.get')
    # def test_set_instance_with_invalid_url(self, mock_get):
    #     mock_get.side_effect = Exception("Network error")
    #     serializer = ISALDSerializer(json_instance="http://invalid-url.com")
    #     self.assertEqual(serializer.instance, {})

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"invalid": "schema"}')
    def test_resolve_network_with_invalid_schema(self, mock_open_file):
        serializer = ISALDSerializer(json_instance={})
        serializer._resolve_network()
        self.assertRaises(AssertionError)

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='[]')
    def test_set_format_with_invalid_format(self, mock_open_file):
        with self.assertRaises(AttributeError):
            serializer = ISALDSerializer(json_instance={})
            serializer.set_format(output_format="invalid_format")

    def test_get_context_url_with_edge_case(self):
        serializer = ISALDSerializer(json_instance={})
        url = serializer._get_context_url("https://raw.githubusercontent.com/ISA-tools/isa-api/develop/isatools/resources/json-context/obo/isa_isa_test_obo_context.jsonld")
        self.assertIn("https://raw.githubusercontent.com/ISA-tools/isa-api/develop/isatools/resources/json-context/obo/isa_isa_test_obo_context.jsonld", url)

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


class TestInjectLDSplit(unittest.TestCase):

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"properties": {"field": {"type": "string"}}}')
    def test_inject_ld_split_basic(self, mock_open):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "field": {"type": "string"}
                }
            }
        }
        instance = {"field": "value"}
        output = {}
        result = serializer._inject_ld_split("test_schema.json", output, instance)
        self.assertEqual(result["field"], "value")
        self.assertIn("@context", result)
        self.assertIn("@type", result)


    def test_inject_ld_split_with_object(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "object_field": {"type": "object", "properties": {"subfield": {"type": "string"}}}
                }
            }
        }
        instance = {"object_field": {"subfield": "subvalue"}}
        output = {}
        result = serializer._inject_ld_split("test_schema.json", output, instance)
        self.assertEqual(result["object_field"]["subfield"], "subvalue")

    def test_inject_ld_split_with_ref(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "ref_field": {"$ref": "ref_schema.json"}
                }
            },
            "ref_schema.json": {
                "properties": {
                    "nested_field": {"type": "string"}
                }
            }
        }
        instance = {"ref_field": {"nested_field": "nested_value"}}
        output = {}
        result = serializer._inject_ld_split("test_schema.json", output, instance)
        self.assertEqual(result["ref_field"]["nested_field"], "nested_value")

    def test_inject_ld_split_with_anyOf(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "value": {
                        "anyOf": [
                            {"$ref": "ref_schema.json"}
                        ]
                    }
                }
            },
            "ref_schema.json": {
                "properties": {
                    "nested_field": {"type": "string"}
                }
            }
        }
        instance = {"value": {"nested_field": "nested_value"}}
        output = {}
        result = serializer._inject_ld_split("test_schema.json", output, instance)
        self.assertEqual(result["value"]["nested_field"], "nested_value")

    def test_inject_ld_split_with_nested_array_of_objects(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "array_field": {
                        "type": "array",
                        "items": {"$ref": "nested_schema.json"}
                    }
                }
            },
            "nested_schema.json": {
                "properties": {
                    "subfield": {"type": "string"}
                }
            }
        }
        instance = {"array_field": [{"subfield": "value1"}, {"subfield": "value2"}]}
        output = {}
        result = serializer._inject_ld_split("test_schema.json", output, instance)
        self.assertEqual(result["array_field"][0]["subfield"], "value1")
        self.assertEqual(result["array_field"][1]["subfield"], "value2")


class TestInjectLDCollapsed(unittest.TestCase):

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"@context": {}, "@type": "Test"}')
    def test_inject_ld_collapsed_basic(self, mock_open_file):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "field": {"type": "string"}
                }
            }
        }
        instance = {"field": "value"}
        output = {}
        result = serializer._inject_ld_collapsed("test_schema.json", output, instance)
        self.assertEqual(result["field"], "value")
        self.assertIn("@type", result)


    def test_inject_ld_collapsed_with_object(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "object_field": {"type": "object", "properties": {"subfield": {"type": "string"}}}
                }
            }
        }
        instance = {"object_field": {"subfield": "subvalue"}}
        output = {}
        result = serializer._inject_ld_collapsed("test_schema.json", output, instance)
        self.assertEqual(result["object_field"]["subfield"], "subvalue")

    def test_inject_ld_collapsed_with_ref(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "ref_field": {"$ref": "ref_schema.json"}
                }
            },
            "ref_schema.json": {
                "properties": {
                    "nested_field": {"type": "string"}
                }
            }
        }
        instance = {"ref_field": {"nested_field": "nested_value"}}
        output = {}
        result = serializer._inject_ld_collapsed("test_schema.json", output, instance)
        self.assertEqual(result["ref_field"]["nested_field"], "nested_value")

    def test_inject_ld_collapsed_with_anyOf(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "value": {
                        "anyOf": [
                            {"$ref": "ref_schema.json"}
                        ]
                    }
                }
            },
            "ref_schema.json": {
                "properties": {
                    "nested_field": {"type": "string"}
                }
            }
        }
        instance = {"value": {"nested_field": "nested_value"}}
        output = {}
        result = serializer._inject_ld_collapsed("test_schema.json", output, instance)
        self.assertEqual(result["value"]["nested_field"], "nested_value")

    def test_inject_ld_collapsed_with_nested_array_of_objects(self):
        serializer = ISALDSerializer(json_instance={})
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "array_field": {
                        "type": "array",
                        "items": {"$ref": "nested_schema.json"}
                    }
                }
            },
            "nested_schema.json": {
                "properties": {
                    "subfield": {"type": "string"}
                }
            }
        }
        instance = {"array_field": [{"subfield": "value1"}, {"subfield": "value2"}]}
        output = {}
        result = serializer._inject_ld_collapsed("test_schema.json", output, instance)
        self.assertEqual(result["array_field"][0]["subfield"], "value1")
        self.assertEqual(result["array_field"][1]["subfield"], "value2")


class TestInjectLD(unittest.TestCase):

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"@context": {}, "@type": "Test"}')
    def test_inject_ld_combined(self, mock_open_file):
        # Test when combined is True
        serializer = ISALDSerializer(json_instance={})
        serializer.combined = True
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "field": {"type": "string"}
                }
            }
        }
        instance = {"field": "value"}
        output = serializer._inject_ld("test_schema.json", {}, instance)
        self.assertEqual(output["field"], "value")
        self.assertIn("@type", output)

    @patch('isatools.convert.json2jsonld.open', new_callable=mock_open, read_data='{"properties": {"field": {"type": "string"}}}')
    def test_inject_ld_split(self, mock_open_file):
        # Test when combined is False
        serializer = ISALDSerializer(json_instance={})
        serializer.combined = False
        serializer.schemas = {
            "test_schema.json": {
                "properties": {
                    "field": {"type": "string"}
                }
            }
        }
        instance = {"field": "value"}
        output = serializer._inject_ld("test_schema.json", {}, instance)
        self.assertEqual(output["field"], "value")
        self.assertIn("@context", output)
        self.assertIn("@type", output)


if __name__ == "__main__":
    unittest.main()
