from abc import ABCMeta, abstractmethod
from urllib.parse import urljoin
from xml.dom.minidom import parseString, Node
import requests
import json
import os

__author__ = 'massi'


class IsaStorageAdapter(metaclass=ABCMeta):

    @abstractmethod
    def download(self, source, destination, owner=None, repository=None):
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

    GITHUB_API_BASE_URL = 'https://api.github.com'
    AUTH_ENDPOINT = urljoin(GITHUB_API_BASE_URL, 'authorizations')
    GITHUB_RAW_MEDIA_TYPE = 'application/vnd.github.VERSION.raw'

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

    def download(self, source, destination, owner=None, repository=None):
        """
        Call to download a resource from a remote GitHub repository
        :type source: str - URLish path to the source (within the GitHub repository)
        :type destination str
        :type owner str
        :type repository str
        """
        # get the content at source as raw data
        get_content_frag = '/'.join(['repos', owner, repository, 'contents', source])
        headers = {
            'Authorization': 'token %s' % self.token,
            'Accept': self.GITHUB_RAW_MEDIA_TYPE
        }
        res = requests.get(urljoin(self.GITHUB_API_BASE_URL, get_content_frag), headers=headers)

        if res.status_code == requests.codes.ok:
            # try to parse the response payload as JSON
            try:
                res_payload = json.loads(res.text)

                # if it is a directory
                if isinstance(res_payload, list):
                    # then download it as an archive
                    self._download_dir_as_archive(source, destination, owner, repository)
                # if it is an object it's the file content to be stored

                else:
                    # TODO add validation against JSON schema
                    # save it to disk
                    with open(os.path.join(destination, source.split('/')[0]), 'w') as out_file:
                        json.dump(res_payload, out_file)
            # if it is not a JSON
            except ValueError:
                # try to parse the response payload as XML
                try:
                    res_payload = parseString(res.text)
                    # TODO additional checks on the XML??
                    # if it is a valid XML save it to disk
                    with open(os.path.join(destination, source.split('/')[0]), 'w') as out_file:
                        res_payload.writexml(out_file)

                except ValueError:
                    pass






        else:
            print("The request was not successfully fulfilled: ", res.status_code)

    def retrieve(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def _download_dir_as_archive(self, source, destination, owner, repository):
        pass







