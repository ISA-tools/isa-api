from abc import ABCMeta, abstractmethod
from urllib.parse import urljoin
from lxml import etree
from jsonschema import RefResolver, Draft4Validator
import requests
import json
import os
import pathlib

__author__ = 'massi'


def validate_json_against_schema(schema_src, json_dict):
    with open(schema_src) as schema_file:
        schema = json.load(schema_file)
    resolver = RefResolver(pathlib.Path(os.path.abspath(schema_src)).as_uri(), schema)
    validator = Draft4Validator(schema, resolver=resolver)
    return validator.validate(json_dict, schema)


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

    INVESTIGATION_SCHEMA_FILE = os.path.abspath(os.path.join('isatools', 'schemas', 'isa_model_version_1_0_schemas',
                                                             'core', 'investigation_schema.json'))
    CONFIGURATION_SCHEMA_FILE = os.path.join('isatools', 'schemas', 'isatab_configurator.xsd')
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

    def download(self, source, destination, owner=None, repository=None, validate_json=False):
        """
        Call to download a resource from a remote GitHub repository
        :type source: str - URLish path to the source (within the GitHub repository)
        :type destination str
        :type owner str
        :type repository str
        :type validate_json bool - if True perform validation against a JSON schema (i.e. investigation schema).
                                   Valid only for JSON datasets
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
                    # then download all the items in the directory
                    self._download_dir(source.split('/')[-1], destination, res_payload)
                    return True

                # if it is an object it's the file content to be stored
                else:
                    # validate against JSON schema
                    if validate_json:
                        validate_json_against_schema(self.INVESTIGATION_SCHEMA_FILE, res_payload)

                    # save it to disk
                    os.makedirs(destination, exist_ok=True)
                    with open(os.path.join(destination, source.split('/')[-1]), 'w+') as out_file:
                        json.dump(res_payload, out_file)
                    return True
            # if it is not a JSON
            except ValueError:
                # try to parse the response payload as XML
                try:
                    with open(self.CONFIGURATION_SCHEMA_FILE, 'rb') as schema_file:
                        schema_root = etree.XML(schema_file.read())
                    xml_parser = etree.XMLParser(schema=etree.XMLSchema(schema_root))
                    # try to parse XML to validate against schema
                    etree.fromstring(res.text, xml_parser)

                    # if it is a valid XML save it to disk
                    os.makedirs(destination, exist_ok=True)
                    with open(os.path.join(destination, source.split('/')[-1]), 'w+') as out_file:
                        out_file.write(res.text)
                    return True
                except etree.XMLSyntaxError:
                    return False
        else:
            print("The request was not successfully fulfilled: ", res.status_code)
            return False

    def retrieve(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def _download_dir(self, directory, destination, dir_items):
        headers = {
            'Authorization': 'token %s' % self.token
        }
        # filter the items to keep only files
        files = [item for item in dir_items if item['type'] == 'file']

        for file in files:
            file_name = file["name"]
            res = requests.get(file['download_url'], headers=headers)
            # if request went fine and the payload is a regular (ISA) text file write it to file
            if res.status_code == requests.codes.ok and res.headers['Content-Type'].split(";")[0] == 'text/plain':
                dir_path = os.path.join(destination, directory)
                os.makedirs(dir_path, exist_ok=True)
                with open(os.path.join(dir_path, file_name), 'w+') as out_file:
                    out_file.write(res.text)










