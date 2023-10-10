from os import path
from re import sub
from abc import ABCMeta

from isatools.model.identifiable import Identifiable


LOCAL_PATH = path.join(path.dirname(__file__), '..', 'resources', 'json-context')
REMOTE_PATH = 'https://raw.githubusercontent.com/ISA-tools/isa-api/master/isatools/resources/json-context'
DEFAULT_CONTEXT = 'obo'

EXCEPTIONS = {
    'OntologySource': 'OntologySourceReference',
    'Characteristic': 'MaterialAttributeValueNumber',
    'StudyFactor': 'Factor'
}


def get_name(name):
    if name in EXCEPTIONS:
        return EXCEPTIONS[name]
    return name


def camelcase2snakecase(camelcase: str) -> str:
    return sub(r'(?<!^)(?=[A-Z])', '_', camelcase).lower()


def gen_id(classname: str) -> str:
    from uuid import uuid4
    prefix = '#' + camelcase2snakecase(classname) + '/'
    return prefix + str(uuid4())


class ContextPath:

    def __init__(self):
        self.__context = 'obo'
        self.all_in_one = True
        self.local = True
        self.get_context()
        self.prepend_url = None

    @property
    def context(self) -> str:
        return self.__context

    @context.setter

    def context(self, val: str) -> None:
        allowed_context = ['obo', 'sdo', 'wd', 'sio']
        if val not in allowed_context:
            raise ValueError('Context name must be one in %s but got %s' % (allowed_context, val))
        self.__context = val

    def get_context(self, classname: str = 'allinone'):
        classname = get_name(classname)
        classname = camelcase2snakecase(classname)
        name = self.__context
        path_source = path.join(LOCAL_PATH, name) if self.local else REMOTE_PATH + '/%s/' % name
        filename = 'isa_%s_%s_context.jsonld' % (classname, name)
        if self.all_in_one:
            filename = 'isa_allinone_%s_context.jsonld' % name

        return path.join(path_source, name, filename) if self.local else path_source + filename

    def __repr__(self):
        return self.__context

    def __str__(self):
        return self.__context


context = ContextPath()


def set_context(
        prepend_url: str = None,
        vocab: str = 'obo',
        all_in_one: bool = True,
        local: bool = True,
        include_contexts: bool = False,
) -> None:
    """ Set the context properties necessary for the serialization of the ISA model to JSON-LD.
    :param prepend_url: the URL to prepend to the identifiers.
    :param vocab: the vocabulary to use for the serialization. Allowed values are 'obo', 'sdo' and 'wdt'.
    :param all_in_one: if True, combine all the contexts into one. If False, use the context for each class.
    :param local: if True, use the local context files. If False, use the remote context files.
    :param include_contexts: if True, include the context files in the JSON-LD output.
    """
    context.all_in_one = all_in_one
    context.local = local
    context.context = vocab
    context.include_contexts = include_contexts
    context.prepend_url = prepend_url


class LDSerializable(metaclass=ABCMeta):
    def __init__(self):
        self.context = context

    def gen_id(self) -> str:
        """ Generate an identifier for the object. """
        prepend = self.context.prepend_url if self.context.prepend_url else ''

        if isinstance(self, Identifiable):
            return self.id if self.id.startswith('http') else prepend + self.id
        return prepend + gen_id(self.__class__.__name__)

    def get_context(self):
        return self.context.get_context(classname=self.__class__.__name__)

    def get_ld_attributes(self):
        return {
            '@type': get_name(self.__class__.__name__).replace('Number', ''),
            '@context': self.get_context(),
            '@id': self.gen_id()
        }

    def update_isa_object(self, isa_object, ld=False):
        if not ld:
            return isa_object
        isa_object.update(self.get_ld_attributes())
        return isa_object
