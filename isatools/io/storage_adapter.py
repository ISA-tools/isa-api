from abc import ABCMeta, abstractmethod
from urllib.parse import urljoin
from lxml import etree
from jsonschema import RefResolver, Draft4Validator
from io import BytesIO, StringIO
from zipfile import ZipFile
import requests
import json
import os
import pathlib
import base64
import pdb

__author__ = 'massi'

DIR_NAME = os.path.dirname(__file__)

INVESTIGATION_SCHEMA_FILE = os.path.abspath(os.path.join(DIR_NAME, '..', 'schemas', 'isa_model_version_1_0_schemas',
                                                         'core', 'investigation_schema.json'))
CONFIGURATION_SCHEMA_FILE = os.path.join(DIR_NAME, '..', 'schemas', 'isatab_configurator.xsd')

GITHUB_API_BASE_URL = 'https://api.github.com'
GITHUB_RAW_MEDIA_TYPE = 'application/vnd.github.VERSION.raw'
REPOS = 'repos'
CONTENTS = 'contents'


def validate_xml_against_schema(xml_str, xml_schema_file):
    """
    Validate an XML string against an XML schema definition
    :param xml_str str
    :param xml_schema_file str - valid file path to the XSD file
    """
    with open(xml_schema_file, 'rb') as schema_file:
        schema_root = etree.XML(schema_file.read())
    schema = etree.XMLSchema(schema_root)
    xml = etree.fromstring(xml_str)
    if not schema.validate(xml):
        raise etree.DocumentInvalid("Retrieved file does not validate against ISA configuration xsd")
    else:
        return etree.parse(StringIO(xml_str))


def validate_json_against_schema(json_dict, schema_src):
    """
    Validate a JSON dictionary against the provided JSON schema
    :param json_dict dict
    :param schema_src str - file path to the JSON schema file
    """
    with open(schema_src) as schema_file:
        schema = json.load(schema_file)
    resolver = RefResolver(pathlib.Path(os.path.abspath(schema_src)).as_uri(), schema)
    validator = Draft4Validator(schema, resolver=resolver)
    return validator.validate(json_dict, schema)


class IsaStorageAdapter(metaclass=ABCMeta):

    @abstractmethod
    def download(self, source, destination=None, owner=None, repository=None):
        pass

    @abstractmethod
    def retrieve(self, source, destination=None):
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

    AUTH_ENDPOINT = urljoin(GITHUB_API_BASE_URL, 'authorizations')

    def __init__(self, username=None, password=None, note=None, scopes=('gist', 'repo')):
        """
        Constructor for IsaGitHubStorageAdapter.
        Initialize an ISA Storage Adapter to perform CRUD operations on a remote GitHub repository

        If credentlials are provided (username, password) th recommended use is in a with command, to allow correct
        authrization management.
        For instance:

        with IsaGitHubStorageAdapter('user', 'passw', 'test auth') as adapter:
            print(adapter.is_authorized)
            # do stuff
            ...

        :param username: str - the (optional) GitHub user login
        :param password: str - the (optional) Github password for user
        :param note str - an (optional) note explaining the nature of the authorizations.
        :param scopes tuple - a tuple containing the scopes (see https://developer.github.com/v3/oauth/#scopes)
                              for the current authorization (if username and password are provided.
        """
        self._authorization = {}
        if username and password:
            self._username = username
            self._password = password
            payload = {
                "scopes": list(scopes),
                "note": note or "Authorization to access the ISA data sets"
            }
            headers = {
                "content-type": "application/json",
                "accept": "application/json"

            }
            # retrieve all the existing authorizations for user
            res = requests.get(self.AUTH_ENDPOINT, headers=headers, auth=(self._username, self._password))
            if res.status_code == requests.codes.ok:
                auths = json.loads(res.text)

                # filter the existing authorizations according to thw provided criteria (note and scopes)
                auths = [auth for auth in auths
                         if auth['note'] == payload['note'] and auth['scopes'] == payload['scopes']]

                # if the required authorization already exists, delete it
                if len(auths) > 0:
                    requests.delete(auths[0]['url'], headers=headers, auth=(username, password))

                # require a new authorization
                res = requests.post(self.AUTH_ENDPOINT,  json=payload, headers=headers, auth=(username, password))

                if res.status_code == requests.codes.created:
                    self._authorization = json.loads(res.text or res.content)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Delete the authorization on destruction, if it was created by the constructor
        """
        self.close()

    @property
    def authorization_uri(self):
        return self._authorization['url'] if 'url' in self._authorization else None

    @property
    def token(self):
        return self._authorization['token'] if 'token' in self._authorization else None

    @property
    def is_authenticated(self):
        if 'token' in self._authorization:
            return True
        else:
            return False

    def close(self):
        """
        Method to delete the authorization, if it was created by the constructor
        """
        if not self.is_authenticated:
            return
        headers = {
            'accept': 'application/json'
        }
        r = requests.delete(self.authorization_uri, headers=headers, auth=(self._username, self._password))
        print(r)
        return r.raise_for_status()

    def download(self, source, destination='isa-target', owner='ISA-tools', repository='isa-api', validate_json=False):
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
        get_content_frag = '/'.join([REPOS, owner, repository, CONTENTS, source])
        headers = {
            'Authorization': 'token %s' % self.token,
            'Accept': GITHUB_RAW_MEDIA_TYPE
        }
        res = requests.get(urljoin(GITHUB_API_BASE_URL, get_content_frag), headers=headers)

        if res.status_code == requests.codes.ok:

            # try to parse the response payload as JSON
            try:
                res_payload = json.loads(res.text)

                # if it is a directory
                if isinstance(res_payload, list):
                    # then download all the items in the directory
                    return self._download_dir(source.split('/')[-1], destination, res_payload)

                # if it is an object it's the file content to be stored
                else:
                    # validate against JSON schema
                    if validate_json:
                        validate_json_against_schema(res_payload, INVESTIGATION_SCHEMA_FILE)

                    # save it to disk
                    os.makedirs(destination, exist_ok=True)
                    with open(os.path.join(destination, source.split('/')[-1]), 'w+') as out_file:
                        json.dump(res_payload, out_file)
                    return True
            # if it is not a JSON
            except ValueError:
                # try to parse the response payload as XML
                try:
                    with open(CONFIGURATION_SCHEMA_FILE, 'rb') as schema_file:
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

    def retrieve(self, source, destination='isa-target', owner='ISA-tools', repository='isa-api', ref='master',
                 validate_json=False, decode_content=True, write_to_file=True):
        """
        Call to retrieve a resource from a remote GitHub repository
        Parameters
            :param source: str - URLish path to the source (within the GitHub repository)
            :param destination str - Local file path. Can be absolute or relative to the working directory
            :param owner str - the owner (user or organization) of the target GitHub repo. Defaults to 'ISA-tools'
            :param repository str - the name of the target repository. Defaults to 'isa-api'
            :param ref str - the name of commit/branch/tag. Defaults to 'master'
            :param validate_json bool - if True perform validation against a JSON schema (i.e. investigation schema).
                                   Valid only for JSON datasets. Defaults to False
            :param decode_content bool - if True it will decode the content encoded in the payload, otherwise it will fire a
                                    a second request to retrieve the raw file. Defaults to True
            :param write_to_file bool - if True writes the file to the specified destination directory. Defaults to True

        Returns:
            :return dict - if the retrieved file contains a (valid) json document
            :return XMLElement - if the retrieved file contains a valid ISA XML configuration file
            :return io.BytesIO - if the target is a directory of a ZIP file. If it is a directory the zipped content of
                                 it is returned as a binary stream.
            :return False - if the file downloaded is of an unauthorized type. These file are not saved to disk

        Raises:
            :raise requests.exceptions.HTTPException when the request to GitHub fails
        """
        get_content_frag = '/'.join([REPOS, owner, repository, CONTENTS, source])

        headers = {'Authorization': 'token %s' % self.token} if self.token else {}

        req_payload = {
            'ref': ref
        }

        r = requests.get(urljoin(GITHUB_API_BASE_URL, get_content_frag), headers=headers, params=req_payload)

        if r.status_code == requests.codes.ok:
            res_payload = json.loads(r.text)

            # if it is a directory
            if isinstance(res_payload, list):
                return self._download_dir(source.split('/')[-1], destination, res_payload, write_to_file)

            # if it is an object decode the content (if the option is available)
            elif decode_content:
                processed_payload = self._handle_content(res_payload)

            # if it is an object the retrieve or download it
            else:
                processed_payload = self._retrieve_file(res_payload['download_url'])

            if write_to_file and ('content' in processed_payload or 'text' in processed_payload):
                (out_data, modality) = (processed_payload['text'], 'w+') if 'text' in processed_payload \
                    else (processed_payload['content'], 'wb+')
                os.makedirs(destination, exist_ok=True)
                with open(os.path.join(destination, source.split('/')[-1]), modality) as out_file:
                    out_file.write(out_data)

            # return the JSON or XML content if available
            if processed_payload and isinstance(processed_payload, dict):
                return processed_payload['json'] if 'json' in processed_payload else processed_payload['xml'] \
                    if 'xml' in processed_payload else True

        else:
            # raise the HTTP error returned by the response
            r.raise_for_status()

        return False

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def _download_dir(self, directory, destination, dir_items, write_to_directory):
        """
        Retrieves the full content of a directory
        """
        headers = {'Authorization': 'token %s' % self.token} if self.token else {}
        # filter the items to keep only files
        files = [item for item in dir_items if item['type'] == 'file']
        buf = BytesIO()

        with ZipFile(buf, 'w') as zip_file:

            for file in files:
                file_name = file["name"]
                res = requests.get(file['download_url'], headers=headers)

                # if request went fine and the payload is a regular (ISA) text file write it to file
                if res.status_code == requests.codes.ok and res.headers['Content-Type'].split(";")[0] == 'text/plain':

                    # zip the text payload
                    zip_file.writestr(os.path.join(directory, file["name"]), res.text)

                    # write to a target dir
                    if write_to_directory:
                        dir_path = os.path.join(destination, directory)
                        os.makedirs(dir_path, exist_ok=True)
                        with open(os.path.join(dir_path, file_name), 'w+') as out_file:
                            out_file.write(res.text)

        buf.seek(0)
        return buf

    def _handle_content(self, payload, validate_json=False, char_set='utf-8'):
        """
        Handle file content, decoding its 'content' property, without firing another GET request to GitHub
        """
        # determine decoding strategy
        if payload['encoding'] == 'base64':
            decode_cmd = base64.b64decode
        elif payload['encoding'] == 'base32':
            decode_cmd = base64.b32decode

        decoded_content = decode_cmd(payload['content'])
        file_name = payload['name']
        file_ext = file_name.split('.')[-1]

        # if file is JSON
        if file_ext == 'json':
            # try to parse the content as JSON and validate (if required)
            decoded_content = decoded_content.decode(char_set)
            json_content = json.loads(decoded_content)
            if validate_json:
                validate_json_against_schema(json_content, INVESTIGATION_SCHEMA_FILE)
            return {
                'json': json_content,
                'text': decoded_content
            }

        # if file is XML
        elif file_ext == 'xml':
            # try to parse the content as XML against configuration schema
            decoded_content = decoded_content.decode(char_set)
            xml = validate_xml_against_schema(decoded_content, CONFIGURATION_SCHEMA_FILE)
            return {
                'xml': xml,
                'text': decoded_content
            }

        # if ZIP file return raw content
        elif file_ext == 'zip':
            return {
                'content': decoded_content
            }

        else:
            return {}

    def _retrieve_file(self, file_uri, validate_json=False):
        """
        Retrieve the raw file for further processing
        """
        headers = {'Authorization': 'token %s' % self.token} if self.token else {}
        r = requests.get(file_uri, headers=headers)
        if r.status_code == requests.codes.ok:

            content_type = r.headers['content-type'].split(';')[0]

            # if content is a text file it might be a JSON or XML
            if content_type == 'text/plain':
                try:
                    json_payload = json.loads(r.text or r.content)
                    if validate_json:
                        validate_json_against_schema(json_payload, INVESTIGATION_SCHEMA_FILE)
                    return {
                        'json': json_payload,
                        'text': r.text or r.content
                    }
                except ValueError:
                    try:
                        xml_payload = validate_xml_against_schema(r.text or r.content, CONFIGURATION_SCHEMA_FILE)
                        return {
                            'xml': xml_payload,
                            'text': r.text or r.content
                        }
                    except etree.XMLSyntaxError:
                        pass

            # if content is a zip file
            elif content_type == 'application/zip':
                return {
                    'content': r.content
                }

        return {}











