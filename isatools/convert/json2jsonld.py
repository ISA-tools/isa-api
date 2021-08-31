import os
import json
import logging
from requests import get
import pandas as pd

log = logging.getLogger('isatools')


class ISALDSerializer:

    _instance = None

    # TODO: finish "all in one context" for sdo  domains similar to the wikidata and obo ones (a placeholder exists)

    def __init__(self, json_instance, ontology="wdt"):
        """
        Given an instance url, serializes it into a JSON-LD. You can find the output of the serializer in self.output.
        This is a soft singleton.
        :param {String|Object} json_instance: An ISA JSON instance or the URL of the instance.
        :param {String} ontology: name of the ontology used to build the context names
        """
        self.main_schema = "investigation_schema.json"
        self.instance = {}
        self.output = {}
        self.schemas = {}
        self.contexts = {}
        self.ontology = ontology
        self.context_url = "https://raw.githubusercontent.com/ISA-tools/isa-api/feature/isajson-context/isatools/" \
                           "resources/json-context/%s/" % ontology
        self.context_allineone = "https://raw.githubusercontent.com/ISA-tools/isa-api/DomISALD/isatools/" \
                                 "resources/json-context/%s/" % ontology + "isa-" + ontology + "-allinone-context.jsonld"
        self._resolve_network()
        self.set_instance(json_instance)
        # self.load_core_mapping(mapping_file="/Users/philippe/Documents/git/isa-api2/isa-api/isatools/resources/json-context/mapping_file.xlsx")

        current_mappings = ISALDSerializer.load_core_mapping()
        print("CURRENT:", current_mappings)

    def __new__(cls, json_instance, ontology="wdt"):
        if cls._instance is None:
            cls._instance = super(ISALDSerializer, cls).__new__(cls)
        return cls._instance

    def _resolve_network(self):
        """
        Resolves the network into self.schemas and self.contexts
        """
        schemas_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "../resources/schemas/isa_model_version_1_0_schemas/core/")
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
        """
        self.instance = instance
        if isinstance(instance, str) \
                and (instance.startswith('http://') or instance.startswith('https://')):
            self.instance = json.loads(get(instance).text)
        self.output = self._inject_ld(self.main_schema, {}, self.instance)

    def set_ontology(self, ontology):
        """
        Setter to change the ontology source used to build the context URLs
        :param {String} ontology: an ontology name (e.g.: "sdo")
        """
        self.ontology = ontology

    def load_core_mapping(mapping_file="/Users/philippe/Documents/git/isa-api2/isa-api/isatools/resources/json-context/mapping_file.xlsx"):
        try:
            df = pd.read_excel(mapping_file)
            current_mappings = df.set_index('isa').to_dict('index')
            return current_mappings
        except IOError as ioe:
            print("ERROR", ioe)

    def _inject_ld(self, schema_name, output, instance, reference=False, remote_context=False, ontology="sdo", mappings=load_core_mapping()):
        """
        Inject the LD properties at for the given instance or sub-instance
        :param schema_name: the name of the schema to get the properties from
        :param output: the output to add the properties to
        :param instance: the instance to get the values from
        :param reference: string indicating a fake reference for building the context url
        :param remote_context: a boolean to indicate use of remote context files(True) or embedded context (False)
        :param {String} ontology: an ontology name (e.g.: "sdo")
        :param mappings dictionary from resources file
        :return: the output of the LD injection
        """

        props = self.schemas[schema_name] if schema_name in self.schemas else self.schemas["material_schema.json"]
        if remote_context:
            if 'properties' in props.keys():
                props = props['properties']
            if isinstance(reference, str):
                output["@context"] = self._get_context_url(reference)
                context_key = schema_name.replace("_schema.json", "").replace("#", "")
            else:
                if 'schema.json' in schema_name:
                    context_key = self._get_context_key(schema_name)
                    output["@context"] = self._get_context_url(schema_name)
                else:
                    context_key = "Material"
                    output["@context"] = self.context_url + "isa_material_" + schema_name + "_" + self.ontology + "_context.jsonld"
        else:
            if 'properties' in props.keys():
                props = props['properties']
            if isinstance(reference, str):
                context_key = schema_name.replace("_schema.json", "").replace("#", "")
            else:
                if "investigation" in schema_name and remote_context is False:
                    try:
                        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               "../resources/json-context/", ontology,
                                               "isa-" + ontology + "-allinone-context.jsonld")) as single_context:
                            this_json_context = json.load(single_context)
                            output["@context"] = this_json_context["@context"]
                    except IOError as ioe:
                        log.error(ioe)
                if 'schema.json' in schema_name:
                    context_key = self._get_context_key(schema_name)
                else:
                    context_key = "Material"

        # Postprossing of the actual Node Type:

        if context_key in mappings.keys() and context_key != "Materials":
            # print("KEY: ",context_key)
            output["@type"] = ontology + ":" + mappings[context_key][ontology]
            # print(context_key,  output["@type"])
            # print("HERE:", mappings)
        else:
            context_key
            # print(context_key)

        for field in instance:
            if field in props:
                field_props = props[field]
                if 'type' in field_props.keys() and field_props['type'] == 'array':
                    if 'items' in field_props.keys() and '$ref' in field_props['items']:
                        ref = field_props['items']['$ref'].replace("#", "")
                        for value in instance[field]:
                            value = self._inject_ld(ref, value, value)
                    else:
                        if field == 'inputs':
                            for input_val in instance['inputs']:
                                ref = self._get_any_of_ref(input_val["@id"])
                                if ref:
                                    input_val = self._inject_ld(ref, input_val, input_val)
                        elif field == 'outputs':
                            for output_val in instance['outputs']:
                                ref = self._get_any_of_ref(output_val["@id"])
                                if ref:
                                    output_val = self._inject_ld(ref, output_val, output_val)
                        else:
                            ref = field + '_schema.json'
                            self.schemas[ref] = field_props
                            for value in instance[field]:
                                value = self._inject_ld(ref, value, value, schema_name)
                elif 'type' in field_props.keys() and field_props['type'] == 'object':
                    ref = field + '_schema.json'
                    self.schemas[ref] = field_props
                    instance[field] = self._inject_ld(ref, instance[field], instance[field])

                elif '$ref' in field_props.keys():
                    ref = field_props['$ref'].replace("#", "")
                    instance[field] = self._inject_ld(ref, instance[field], instance[field])
                elif 'anyOf' in field_props.keys() and field == 'value' and isinstance(instance[field], dict):
                    ref = [n for n in field_props['anyOf'] if '$ref' in n.keys()][0]['$ref'].replace("#", "")
                    instance[field] = self._inject_ld(ref, instance[field], instance[field])
            output[field] = instance[field]

        return output

    def _get_context_url(self, raw_name):
        """
        Build the url of the context given a schema name
        :param raw_name: the schema name
        :return: the corresponding context url
        """
        filename = "_%s_context.jsonld" % self.ontology
        return self.context_url + "isa_" + raw_name.replace("_schema.json", filename)

    @staticmethod
    def _get_any_of_ref(input_val):
        """
        Return the corresponding schema reference or false
        :param input_val: value to evaluate
        :return: False or a the schema reference string
        => #material/labeledextract-xxx => labeledextract
        => #material/extract-xxx => extract
        """
        output = input_val.split("#")[1].split("/")[0]
        if output != "material":
            return output + "_schema.json"
        else:
            return input_val.split("#")[1].split("/")[1].split("-")[0]

    @staticmethod
    def _get_context_key(name):
        """
        Get the @type value of the LD injection given a string name
        :param name: string to extract the type from
        :return: the @type value to inject
        """
        name = name.replace("_schema.json", "").replace("#", "")
        return "".join([x.capitalize() for x in name.split("_")])
