from abc import ABCMeta, abstractmethod
import requests

__author__ = 'massi'


class IsaStorageAdapter(metaclass=ABCMeta):

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def retrieve(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class IsaGitHubStorageAdapter(IsaStorageAdapter):

    def __init__(self, username = None, password = None):
        self._username = username
        self._password = password

    def download(self):
        pass

    def retrieve(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass







