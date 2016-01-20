from abc import ABCMeta, abstractmethod
import requests
import json

__author__ = 'massi'


class IsaStorageAdapter(metaclass=ABCMeta):

    @abstractmethod
    def download(self, source, destination):
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

    def __init__(self, username=None, password=None, note=None, scopes=('gist', 'repo')):
        """
        Initialize an ISA Storage Adapter to perform CRUD operations on a remote GitHub repository
        :type username: str
        :type password: str
        :type note str
        """
        self._authorization = {}
        if username and password:
            payload = {
                "scopes": list(scopes),
                "note": note or "Authorization to access the ISA data sets"
            }
            headers = {
                "content-type": "application/json",
                "accept": "application/json"

            }
            # retrieve all the existing authorizations for user
            res = requests.get(self.AUTH_ENDPOINT, headers= headers, auth=(username, password))
            if res.status_code == requests.codes.ok:
                auths = json.loads(res.text)

                # filter the existing authorizations according to thw provided criteria (note and scopes)
                auths = [auth for auth in auths
                         if auth['note'] == payload['note'] and auth['scopes'] == payload['scopes']]

                # if the required authorization already exists use it
                if len(auths) > 0:
                    self._authorization = auths[0]

                # otherwise require a new authorization
                else:
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

    def download(self, source, destination):
        """
        Call to download a resource from a remote GitHub repository
        :type source: str
        :type destination str
        """
        pass

    def retrieve(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass







