from abc import ABCMeta
from uuid import uuid4
from re import sub


class Identifiable(metaclass=ABCMeta):

    def __init__(self, id_: str = '', **kwargs):
        self.__id = None
        self.id = id_

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, val):
        camelcase_id_to_snakecase = '#' + sub(r'(?<!^)(?=[A-Z])', '_', type(self).__name__).lower() + '/'
        if val is not None and not isinstance(val, str):
            raise AttributeError('Identifiable.id must be a str or None; got {0}:{1}'.format(val, type(val)))
        if not val or val == '':
            val = camelcase_id_to_snakecase + str(uuid4())
        self.__id = val
