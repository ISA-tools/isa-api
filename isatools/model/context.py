from __future__ import annotations

from os import path
from re import sub
from abc import ABCMeta
import requests
from json import loads

from isatools.model.identifiable import Identifiable


LOCAL_PATH = path.join(path.dirname(__file__), '..', 'resources', 'json-context')
REMOTE_PATH = 'https://raw.githubusercontent.com/ISA-tools/isa-api/master/isatools/resources/json-context'
DEFAULT_CONTEXT = 'obo'

EXCEPTIONS = {
    'OntologySource': 'OntologySourceReference',
    'Characteristic': 'MaterialAttributeValueNumber',
    'StudyFactor': 'Factor',
    'DataFile': "Data",
    'RawDataFile': "RawData"
}


def get_name(name: str) -> str:
    """ Get the name of the class to include in the context name.
    :param name: the name of the class.
    :return: the name of the class to include in the context name.
    """
    if name in EXCEPTIONS:
        return EXCEPTIONS[name]
    return name


def camelcase2snakecase(camelcase: str) -> str:
    """ Convert a camelcase string to snakecase.
    :param camelcase: the camelcase string to convert
    :return: the snakecase string
    """
    return sub(r'(?<!^)(?=[A-Z])', '_', camelcase).lower()


def gen_id(classname: str) -> str:
    """ Generate an identifier based on the class name
    :param classname: the name of the class
    :return: the identifier
    """
    from uuid import uuid4
    prefix = '#' + camelcase2snakecase(classname) + '/'
    return prefix + str(uuid4())


class ContextPath:
    """
    A class to manage the context of the JSON-LD serialization. This should not be used directly. Use the `context`
    object and `set_context()` function instead.
    """

    def __init__(self) -> None:
        """ Initialize the context path. """
        self.__context = 'obo'
        self.all_in_one = True
        self.local = True
        self.include_contexts = False
        self.contexts = {}
        self.get_context()

    @property
    def context(self) -> str:
        return self.__context

    @context.setter
    def context(self, val: str) -> None:
        allowed_context = ['obo', 'sdo', 'wdt']
        if val not in allowed_context:
            raise ValueError('Context name must be one in %s but got %s' % (allowed_context, val))
        self.__context = val

    def get_context(self, classname: str = 'allinone') -> str | dict:
        """ Get the context needed to serialize ISA to JSON-LD. Will either return a URL to the context of resolve the
        context and include it in the instance.
        :param classname: the name of the class to get the context for.
        """
        classname = get_name(classname)
        classname = camelcase2snakecase(classname)
        name = self.__context
        path_source = path.join(LOCAL_PATH, name) if self.local else REMOTE_PATH + '/%s/' % name
        filename = 'isa_%s_%s_context.jsonld' % (classname, name)
        if self.all_in_one:
            filename = 'isa_allinone_%s_context.jsonld' % name

        context_path = path.join(path_source, filename) if self.local else path_source + filename
        return context_path if not self.include_contexts else self.load_context(context_path)

    def load_context(self, context_path: str) -> dict:
        """
        Load the context from the given path or URL. If the context is already loaded, return it.
        :param context_path: the path or URL to the context.
        """
        if context_path in self.contexts:
            return self.contexts[context_path]
        if self.local:
            with open(context_path, 'r') as f:
                return loads(f.read())
        return requests.get(context_path).json()

    def __repr__(self) -> str:
        return self.__context

    def __str__(self) -> str:
        return self.__context


context = ContextPath()


def set_context(
        vocab: str = 'obo',
        all_in_one: bool = True,
        local: bool = True,
        include_contexts: bool = False
) -> None:
    """ Set the context properties necessary for the serialization of the ISA model to JSON-LD.
    :param vocab: the vocabulary to use for the serialization. Allowed values are 'obo', 'sdo' and 'wdt'.
    :param all_in_one: if True, combine all the contexts into one. If False, use the context for each class.
    :param local: if True, use the local context files. If False, use the remote context files.
    :param include_contexts: if True, include the context files in the JSON-LD output.
    """
    context.all_in_one = all_in_one
    context.local = local
    context.context = vocab
    context.include_contexts = include_contexts


class LDSerializable(metaclass=ABCMeta):
    """ A mixin used by ISA objects to provide utility methods for JSON-LD serialization. """

    def __init__(self) -> None:
        self.context = context

    def gen_id(self) -> str:
        """ Generate an identifier for the object. """
        if isinstance(self, Identifiable):
            return self.id
        return gen_id(self.__class__.__name__)

    def get_context(self) -> str | dict:
        """ Get the context for the object. """
        return self.context.get_context(classname=self.__class__.__name__)

    def get_ld_attributes(self) -> dict:
        """ Generate and return the LD attributes for the object. """
        return {
            '@type': get_name(self.__class__.__name__).replace('Number', ''),
            '@context': self.get_context(),
            '@id': self.gen_id()
        }

    def update_isa_object(self, isa_object, ld=False) -> object:
        """ Update the ISA object with the LD attributes if necessary. Needs to be called
        after serialization the object.
        :param isa_object: the ISA object to update.
        :param ld: if True, update the object with the LD attributes, else return the object before injection
        """
        if not ld:
            return isa_object
        isa_object.update(self.get_ld_attributes())
        return isa_object
