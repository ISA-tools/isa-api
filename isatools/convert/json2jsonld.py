import os
import json
from requests import get


def singleton(class_):
    """
    Decorator to create singleton
    :param class_:
    :return: the new object or the already existing instance
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class ISALDSerializer:

    def __init__(self, json_instance, ontology="obo"):
        """
        Given an instance url, serializes it into a JSON-LD. You can find the output of the serializer in self.output.
        This is a soft singleton.
        :param {String|Object} json_instance: An ISA JSON instance or the URL of the instance.
        :param {String} ontology: name of the ontology used to build the context names
        """
        self.main_schema = "investigation_schema.json"
        self.instance = None
        self.output = None
        self.schemas = {}
        self.contexts = {}
        self.set_ontology(ontology)
        self.__resolve_network()
        self.set_instance(json_instance)

    def __resolve_network(self):
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
                self.contexts[schema_name] = self.__get_context_url(schema_name)
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
        self.output = self.__inject_ld(self.main_schema, {}, self.instance)

    def set_ontology(self, ontology):
        """
        Setter to change the ontology source used to build the context URLs
        :param {String} ontology: an ontology name (e.g.: "sdo")
        """
        self.ontology = ontology

    def __inject_ld(self, schema_name, output, instance, reference=False):
        """
        Inject the LD properties at for the given instance or subinstance
        :param schema_name: the name of the schema to get the properties from
        :param output: the output to add the properties to
        :param instance: the instance to get the values from
        :param reference: string indicating a fake reference for building the context url
        :return: the output of the LD injection
        """
        props = self.schemas[schema_name]
        if 'properties' in self.schemas[schema_name].keys():
            props = self.schemas[schema_name]['properties']
        context_key = self.__get_context_key(schema_name)
        output["@context"] = self.__get_context_url(schema_name)
        if isinstance(reference, str):
            context_key = schema_name.replace("_schema.json", "").replace("#", "")
            output["@context"] = self.__get_context_url(reference)
        output["@type"] = context_key
        for field in instance:
            if field in props:
                if 'type' in props[field].keys() and props[field]['type'] == 'array':
                    if 'items' in props[field].keys() and '$ref' in props[field]['items']:
                        ref = props[field]['items']['$ref'].replace("#", "")
                        for value in instance[field]:
                            value = self.__inject_ld(ref, value, value)
                    else:
                        if field == 'inputs':
                            for input_val in instance['inputs']:
                                ref = self.__get_any_of_ref(input_val["@id"])
                                if ref:
                                    input_val = self.__inject_ld(ref, input_val, input_val)
                        elif field == 'outputs':
                            for output_val in instance['outputs']:
                                ref = self.__get_any_of_ref(output_val["@id"])
                                if ref:
                                    output_val = self.__inject_ld(ref, output_val, output_val)
                        else:
                            ref = field + '_schema.json'
                            self.schemas[ref] = props[field]
                            for value in instance[field]:
                                value = self.__inject_ld(ref, value, value, schema_name)
                elif 'type' in props[field].keys() and props[field]['type'] == 'object':
                    ref = field + '_schema.json'
                    self.schemas[ref] = props[field]
                    instance[field] = self.__inject_ld(ref, instance[field], instance[field], schema_name)
                elif '$ref' in props[field].keys():
                    ref = props[field]['$ref'].replace("#", "")
                    instance[field] = self.__inject_ld(ref, instance[field], instance[field])
                elif 'anyOf' in props[field].keys() and field == 'value' and isinstance(instance[field], dict):
                    ref = [n for n in props[field]['anyOf'] if '$ref' in n.keys()][0]['$ref'].replace("#", "")
                    instance[field] = self.__inject_ld(ref, instance[field], instance[field])
            output[field] = instance[field]
        return output

    def __get_context_url(self, raw_name):
        """
        Build the url of the context given a schema name
        :param raw_name: the schema name
        :return: the corresponding context url
        """
        context_url = "https://raw.githubusercontent.com/ISA-tools/isa-api/feature/isajson-context/isatools/" \
                      "resources/json-context/obo/"
        filename = "_%s_context.jsonld" % self.ontology
        return context_url + "isa_" + raw_name.replace("_schema.json", filename)

    @staticmethod
    def __get_any_of_ref(input_val):
        """
        Return the corresponding schema reference or false
        :param input_val: value to evaluate
        :return: False or a the schema reference string
        """
        return input_val.split("#")[1].split("/")[0] + "_schema.json"

    @staticmethod
    def __get_context_key(name):
        """
        Get the @type value of the LD injection given a string name
        :param name: string to extract the type from
        :return: the @type value to inject
        """
        name = name.replace("_schema.json", "").replace("#", "")
        return "".join([x.capitalize() for x in name.split("_")])
