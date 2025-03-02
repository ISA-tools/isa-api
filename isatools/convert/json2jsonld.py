import os
import json
from requests import get


class ISALDSerializer:

    # TODO : use kwargs instead of default values;

    _instance = None

    def __init__(self, json_instance, ontology="obo", combined=False):
        """
        Given an instance url, serializes it into a JSON-LD. You can find the output of the serializer in self.output.
        This is a soft singleton.
        :param {String|Object} json_instance: An ISA JSON instance or the URL of the instance.
        :param {String} ontology: name of the ontology used to build the context names
        :param {Boolean} combined: a boolean to indicate whether to inject context as a single all-in-one file or not.
        Defaults to False.
        """
        self.main_schema = "investigation_schema.json"
        self.instance = {}
        self.output = {}
        self.schemas = {}
        self.contexts = {}
        self.combined = combined
        self.ontology = ontology
        self._resolve_network()
        self.set_instance(json_instance)

    def __new__(cls, json_instance, ontology="obo"):
        if cls._instance is None:
            cls._instance = super(ISALDSerializer, cls).__new__(cls)
        return cls._instance

    def set_contexts_method(self, combined):
        """
        Set the method to inject the LD context: single or multiple contexts.
        :param {Boolean} combined: should the contexts be combined or not.
        :return:
        """
        self.combined = combined

    def set_format(self, output_format):
        """
        Sets the format of the output. Must be jsonld or ttl.
        :param {String} output_format: the name of the output format.
        """
        self.format = output_format

    def _resolve_network(self):
        """
        Resolves the network into self.schemas and self.contexts
        """
        schemas_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "../resources/schemas/v1.0.1/")
        path = os.path.join('./', schemas_path)
        schemas_path = os.listdir(path)
        for schema_name in schemas_path:
            schema_path = os.path.join(path, schema_name)
            with open(schema_path, 'r') as schema:
                self.schemas[schema_name] = json.load(schema)
                self.contexts[schema_name] = self._get_context_url(schema_name)
                schema.close()

    def set_instance(self, instance):
        """
        Changes the instance without reloading the schemas and restart the injection process
        :param instance: ISA JSON instance or url of the instance to load
        Defaults to False.
        """
        self.instance = instance
        if isinstance(instance, str) and (instance.startswith('http://') or instance.startswith('https://')):
            self.instance = json.loads(get(instance).text)
        self.output = self._inject_ld(self.main_schema, {}, self.instance)

    def set_ontology(self, ontology):
        """
        Setter to change the ontology source used to build the context URLs
        :param {String} ontology: an ontology name (e.g.: "sdo")
        """
        self.ontology = ontology

    def _inject_ld(self, schema_name, output, instance):
        """
        :param schema_name: name of the schema
        :param output: the output to inject the ld attributes into
        :param instance: the json instance to get the fields
        :return:
        """
        if not self.combined:
            return self._inject_ld_split(schema_name, output, instance)
        else:
            filename = '../resources/json-context/%s/isa_%s_allinone_context.jsonld' % (self.ontology, self.ontology)
            context_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
            with open(context_path) as f:
                output = json.load(f)
            return self._inject_ld_collapsed(schema_name, output, instance)

    def _inject_ld_split(self, schema_name, output, instance, reference=False):
        """
        Inject the LD properties at for the given instance or sub-instance using separate context files
        :param schema_name: the name of the schema to get the properties from
        :param output: the output to add the properties to
        :param instance: the instance to get the values from
        :param reference: string indicating a fake reference for building the context url
        :return: the output of the LD injection
        """
        props = self.schemas[schema_name]
        if 'properties' in self.schemas[schema_name].keys():
            props = self.schemas[schema_name]['properties']
        context_key = self._get_context_key(schema_name)
        output["@context"] = self._get_context_url(schema_name)
        if isinstance(reference, str):
            context_key = schema_name.replace("_schema.json", "").replace("#", "")
            output["@context"] = self._get_context_url(reference)
        output["@type"] = context_key
        for field in instance:
            if field in props:
                field_props = props[field]
                if 'type' in field_props.keys() and field_props['type'] == 'array':
                    if 'items' in field_props.keys() and '$ref' in field_props['items']:
                        ref = field_props['items']['$ref'].replace("#", "")
                        for value in instance[field]:
                            value = self._inject_ld_split(ref, value, value)
                    else:
                        if field == 'inputs':
                            for input_val in instance['inputs']:
                                ref = self._get_any_of_ref(input_val["@id"])
                                if ref:
                                    input_val = self._inject_ld_split(ref, input_val, input_val)
                        elif field == 'outputs':
                            for output_val in instance['outputs']:
                                ref = self._get_any_of_ref(output_val["@id"])
                                if ref:
                                    output_val = self._inject_ld_split(ref, output_val, output_val)
                        else:
                            ref = field + '_schema.json'
                            self.schemas[ref] = field_props
                            for value in instance[field]:
                                value = self._inject_ld_split(ref, value, value, schema_name)
                elif 'type' in field_props.keys() and field_props['type'] == 'object':
                    ref = field + '_schema.json'
                    self.schemas[ref] = field_props
                    instance[field] = self._inject_ld_split(ref, instance[field], instance[field], schema_name)
                elif '$ref' in field_props.keys():
                    ref = field_props['$ref'].replace("#", "")
                    instance[field] = self._inject_ld_split(ref, instance[field], instance[field])
                elif 'anyOf' in field_props.keys() and field == 'value' and isinstance(instance[field], dict):
                    ref = [n for n in field_props['anyOf'] if '$ref' in n.keys()][0]['$ref'].replace("#", "")
                    instance[field] = self._inject_ld_split(ref, instance[field], instance[field])
            output[field] = instance[field]
        return output

    def _inject_ld_collapsed(self, schema_name, output, instance):
        """
        Inject the LD properties at for the given instance or subinstance using a single context file
        :param schema_name: the name of the schema to get the properties from
        :param output: the output to add the properties to
        :param instance: the instance to get the values from
        :return: the output of the LD injection
        """
        output["@type"] = self._get_context_key(schema_name)
        props = self.schemas[schema_name]['properties'] if 'properties' in self.schemas[schema_name].keys() \
            else self.schemas[schema_name]
        for field in instance:
            if field in props:
                field_props = props[field]
                if 'type' in field_props.keys() and field_props['type'] == 'array':
                    if 'items' in field_props.keys() and '$ref' in field_props['items']:
                        ref = field_props['items']['$ref'].replace("#", "")
                        for value in instance[field]:
                            value = self._inject_ld_collapsed(ref, value, value)
                    else:
                        if field == 'inputs':
                            for input_val in instance['inputs']:
                                ref = self._get_any_of_ref(input_val["@id"])
                                if ref:
                                    input_val = self._inject_ld_collapsed(ref, input_val, input_val)
                        elif field == 'outputs':
                            for output_val in instance['outputs']:
                                ref = self._get_any_of_ref(output_val["@id"])
                                if ref:
                                    output_val = self._inject_ld_collapsed(ref, output_val, output_val)
                        else:
                            ref = field + '_schema.json'
                            self.schemas[ref] = field_props
                            for value in instance[field]:
                                value = self._inject_ld_collapsed(ref, value, value)
                elif 'type' in field_props.keys() and field_props['type'] == 'object':
                    ref = field + '_schema.json'
                    self.schemas[ref] = field_props
                    instance[field] = self._inject_ld_collapsed(ref, instance[field], instance[field])
                elif '$ref' in field_props.keys():
                    ref = field_props['$ref'].replace("#", "")
                    instance[field] = self._inject_ld_collapsed(ref, instance[field], instance[field])
                elif 'anyOf' in field_props.keys() and field == 'value' and isinstance(instance[field], dict):
                    ref = [n for n in field_props['anyOf'] if '$ref' in n.keys()][0]['$ref'].replace("#", "")
                    instance[field] = self._inject_ld_collapsed(ref, instance[field], instance[field])
            output[field] = instance[field]
        return output

    def _get_context_url(self, raw_name):
        """
        Build the url of the context given a schema name
        :param raw_name: the schema name
        :return: the corresponding context url
        """
        context_url = "https://raw.githubusercontent.com/ISA-tools/isa-api/develop/isatools/" \
                      "resources/json-context/%s/isa_" % self.ontology
        filename = "_%s_context.jsonld" % self.ontology
        return context_url + "isa_" + raw_name.replace("_schema.json", filename)

    @staticmethod
    def _get_any_of_ref(input_val):
        """
        Return the corresponding schema reference or false
        :param input_val: value to evaluate
        :return: False or a the schema reference string
        """
        return input_val.split("#")[1].split("/")[0] + "_schema.json"

    @staticmethod
    def _get_context_key(name):
        """
        Get the @type value of the LD injection given a string name
        :param name: string to extract the type from
        :return: the @type value to inject
        """
        name = name.replace("_schema.json", "").replace("#", "")
        return "".join([x.capitalize() for x in name.split("_")])
