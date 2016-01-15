from abc import ABCMeta, abstractmethod

__author__ = 'massi'


class IsaJSONFileHandler(metaclass=ABCMeta):

    @abstractmethod
    def get_as_file(self):
        pass

    @abstractmethod
    def get_as_json(self):
        pass

    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class IsaTabFileHandler(metaclass=ABCMeta):

    @abstractmethod
    def get_as_archive(self):
        pass

    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class IsaConfigurationFileHandler(metaclass=ABCMeta):

    @abstractmethod
    def get(self):
        pass


class IsaJSONGithubFileHandler(IsaJSONFileHandler):

    def get_as_file(self):
        pass

    def get_as_json(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass







