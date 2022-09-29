from os import path
from re import sub
from abc import ABCMeta


LOCAL_PATH = path.join(path.dirname(__file__), '..', 'resources', 'json-context')
REMOTE_PATH = 'https://raw.githubusercontent.com/ISA-tools/isa-api/master/isatools/resources/json-context'
DEFAULT_CONTEXT = 'obo'

EXCEPTIONS = {
    'OntologySource': 'OntologySourceReference'
}


def camelcase2snakecase(camelcase: str) -> str:
    return sub(r'(?<!^)(?=[A-Z])', '_', camelcase).lower()


def gen_id(classname: str) -> str:
    from uuid import uuid4
    prefix = '#' + camelcase2snakecase(classname) + '/'
    return prefix + str(uuid4())


class ContextPath(object):

    def __init__(self):
        self.__context = 'obo'
        self.all_in_one = True
        self.local = True
        self.get_context()

    @property
    def context(self) -> str:
        return self.__context

    @context.setter
    def context(self, val: str):
        allowed_context = ['obo', 'sdo', 'wdt']
        if val not in allowed_context:
            raise ValueError('Context name must be one in %s but got %s' % (allowed_context, val))
        self.__context = val

    def get_context(self, classname: str = 'allinone'):
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


def set_context(new_context='obo', combine=True, local=True):
    context.all_in_one = combine
    context.local = local
    context.context = new_context


class LDSerializable(metaclass=ABCMeta):
    def __init__(self):
        self.context = context

    def gen_id(self):
        return gen_id(self.__class__.__name__)

    def get_context(self):
        return self.context.get_context(classname=self.__class__.__name__)
