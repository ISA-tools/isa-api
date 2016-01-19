from abc import ABCMeta, abstractmethod
import requests
import json

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

    AUTH_ENDPOINT = 'https://api.github.com/authorizations'

    def __init__(self, username=None, password=None, note=None):
        self._authorization = {}
        if username and password:
            payload = {
                "scopes": ["gist", "repo"],
                "note": note or "Authorization to access the ISA data sets"
            }
            headers = {
                "content-type": "application/json",
                "accept": "application/json"

            }
            res = requests.post(self.AUTH_ENDPOINT,  json=payload, headers=headers, auth=(username, password))
            if res.status_code == requests.codes.created:
                self._authorization = json.loads(res.text or res.content)

    @property
    def token(self):
        return self._authorization['token'] if 'token' in self._authorization else None

    @property
    def is_authenticated(self):
        if 'token' in self._authorization:
            return True
        else:
            return False

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







