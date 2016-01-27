from datetime import datetime, timezone

import hashlib
import httpretty
import json
import os
from zipfile import ZipFile
from behave import *
from sure import expect
from zipfile import is_zipfile
from urllib.parse import urljoin
from isatools.io.storage_adapter import IsaGitHubStorageAdapter, REPOS, CONTENTS
from lxml import etree
from io import StringIO

use_step_matcher("parse")

AUTH_ID = 1
GITHUB_API_URL = 'https://api.github.com'
AUTH_TOKEN = "som3ar4nd0mAcc3$$tok3n"

md5 = hashlib.md5()
md5.update(AUTH_TOKEN.encode('utf-8'))
auth_url = urljoin(GITHUB_API_URL, 'authorizations')
auth_res_body = {
    'id': AUTH_ID,
    'url': auth_url + '/' + str(AUTH_ID),
    'app': {
        "name": "test",
        "url": "https://developer.github.com/v3/oauth_authorizations/",
        "client_id": "00000000000000000000"
    },
    'token': AUTH_TOKEN,
    'hashed_token': md5.digest().decode('ISO-8859-1'),
    'token_last_eight': AUTH_TOKEN[-8:],
    'note': "test",
    'note_url': None,
    'created_at': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    'updated_at': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    'scopes': [
        "gist",
        "repo"
    ],
    'fingerprint': None
}
get_content_url = urljoin(GITHUB_API_URL, '')


@given('an optional user login "{test_user}"')
def step_impl(context, test_user):
    """
    :type test_user: str
    :type context: behave.runner.Context
    """
    context.username = test_user


@step('an optional user password "{test_password}"')
def step_impl(context, test_password):
    """
    :type test_password: str
    :type context: behave.runner.Context
    """
    context.password = test_password


@when("a storage adapter is created")
@httpretty.activate
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    httpretty.register_uri(httpretty.GET, auth_url, body=json.dumps([]), content_type='application/json')
    httpretty.register_uri(httpretty.POST, auth_url,
                           body=json.dumps(auth_res_body),
                           content_type='application/json',
                           status=201)
    context.isa_adapter = IsaGitHubStorageAdapter(context.username, context.password)
    expect(httpretty.has_request()).to.be.true


@then("it should instantiate an authenticated connector instance")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expect(context.isa_adapter.is_authenticated).to.be.true
    expect(context.isa_adapter.token).to.equal(AUTH_TOKEN)


@given("an authenticated storage adapter")
@httpretty.activate
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    httpretty.register_uri(httpretty.GET, auth_url, body=json.dumps([]), content_type='application/json')
    httpretty.register_uri(httpretty.POST, auth_url,
                           body=json.dumps(auth_res_body),
                           content_type='application/json',
                           status=201)
    context.isa_adapter = IsaGitHubStorageAdapter('uname', 'password')
    expect(context.isa_adapter.is_authenticated).to.be.true
    expect(context.isa_adapter.token).to.equal(AUTH_TOKEN)


@step('a file object named "{remote_source}" in the remote repository "{repo_name}" owned by "{owner_name}"')
def step_impl(context, remote_source, repo_name, owner_name):
    """
    :type owner_name: str
    :type repo_name: str
    :type remote_source: str
    :type context: behave.runner.Context
    """
    context.source_path = remote_source
    context.repo_name = repo_name
    context.owner_name = owner_name


@step('a destination directory "{destination_dir}" in your home folder')
def step_impl(context, destination_dir):
    """
    :type destination_dir: str
    :type context: behave.runner.Context
    """
    # set as a destination path a subfolder of 'features' where all the output will be collected
    destination_path = os.path.join(os.path.dirname(__file__), '..', 'test_outputs', destination_dir)
    context.destination_path = os.path.abspath(destination_path)
    print(context.destination_path)


@when("the file object is a directory")
@httpretty.activate
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    fixture_file_name = '_'.join([context.owner_name, context.repo_name, context.source_path]).replace('/', '_')
    fixture_file_name += '.json'
    fixture_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures', fixture_file_name))
    with open(fixture_file_path) as json_file:
        items_in_dir = json.load(json_file)
        download_url = '/'.join([GITHUB_API_URL, REPOS, context.owner_name, context.repo_name,
                                CONTENTS, context.source_path])
        httpretty.register_uri(httpretty.GET, download_url, body=json.dumps(items_in_dir))

        for item in items_in_dir:
            httpretty.register_uri(httpretty.GET, item['download_url'], body='test data\tfile\t'+item['name'],
                                   content_type='text/plain; charset=utf-8')

        context.items_in_dir = items_in_dir
        res = context.isa_adapter.retrieve(context.source_path, context.destination_path, context.owner_name,
                                     context.repo_name)

    expect(res).to.be.true
    expect(httpretty.has_request()).to.be.true


@then("it should download the files contained within the directory")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    out_dir = os.path.join(context.destination_path, context.source_path.split('/')[-1])
    # expect the destination to have been saved as a directory
    expect(os.path.isdir(out_dir)).to.be.true
    # expect each item in the directory to have been saved as a file
    [expect(os.path.isfile(os.path.join(out_dir, item['name']))).to.be.true for item in context.items_in_dir]


@when("the file object is a ZIP archive")
@httpretty.activate
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # build up the path to the fixture file (for the encoded data)
    fixture_file_name = '_'.join([context.owner_name, context.repo_name, context.source_path]).replace('/', '_')\
        .replace(' ', '_').replace('.zip', '.json')

    destination_name = context.source_path.split('/')[-1]
    fixture_file_path = os.path.abspath(os.path.join('features', 'fixtures', fixture_file_name))
    download_url = '/'.join([GITHUB_API_URL, REPOS, context.owner_name, context.repo_name,
                             CONTENTS, context.source_path])

    # get the encoded description
    with open(fixture_file_path) as json_file:
        context.zipped_dataset_encoded = json.load(json_file)
        httpretty.register_uri(httpretty.GET, download_url, body=json.dumps(context.zipped_dataset_encoded))

    fixture_file_path_raw = os.path.abspath(os.path.join('features', 'fixtures', destination_name))
    download_url = context.zipped_dataset_encoded['download_url']

    # get the raw zipped file
    with open(fixture_file_path_raw, 'rb') as zip_file:
        context.zip_content = zip_file.read()
        httpretty.register_uri(httpretty.GET, download_url, body=context.zip_content, content_type='application/zip')

    context.res = context.isa_adapter.retrieve(context.source_path, context.destination_path, context.owner_name,
                                               context.repo_name)

    expect(context.res).to.be.true
    expect(httpretty.has_request()).to.be.true


@then("it should download it as it is")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    out_file = os.path.join(context.destination_path, context.source_path.split('/')[-1])
    # file should have been saved
    expect(os.path.isfile(out_file)).to.be.true
    with open(out_file, 'rb') as zip_file:
        written_zip_content = zip_file.read()

    expect(written_zip_content).to.equal(context.zip_content)


@when("the source file points to an ISA-TAB JSON file")
@httpretty.activate
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    # build up the path to the file with the encoded dataset
    fixture_file_name = '_'.join([context.owner_name, context.repo_name, context.source_path]).replace('/', '_')
    fixture_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures', fixture_file_name))

    # build up the path to the fixtures RAW file
    fixture_file_frags = context.source_path.split('/')
    fixture_file_path_raw = os.path.abspath(os.path.join(*fixture_file_frags))

    # create the url to GET the encoded dataset
    download_url = '/'.join([GITHUB_API_URL, REPOS, context.owner_name, context.repo_name,
                             CONTENTS, context.source_path])
    with open(fixture_file_path) as json_file:
        context.json_isa_dataset_encoded = json.load(json_file)
        httpretty.register_uri(httpretty.GET, download_url, body=json.dumps(context.json_isa_dataset_encoded))

    # retrieve the url to GET the raw dataset
    download_url = context.json_isa_dataset_encoded['download_url']
    with open(fixture_file_path_raw) as json_file:
        context.json_isa_dataset_raw = json.load(json_file)
        httpretty.register_uri(httpretty.GET, download_url, body=json.dumps(context.json_isa_dataset_raw))

    context.res = context.isa_adapter.retrieve(context.source_path, context.destination_path, context.owner_name,
                                               context.repo_name)

    expect(httpretty.has_request()).to.be.true


@then("it should download it as a JSON file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    out_file = os.path.join(context.destination_path, context.source_path.split('/')[-1])
    expect(os.path.isfile(out_file)).to.be.true
    with open(out_file) as json_file:
        written_json_dataset = json.load(json_file)

    expect(written_json_dataset).to.equal(context.json_isa_dataset_raw)


@step("it should return the JSON content as a dictionary")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expect(context.res).to.be.a(dict)
    expect(context.res).to.equal(context.json_isa_dataset_raw)


@when("the source file points to an ISA-TAB XML configuration file")
@httpretty.activate
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # build up the path to the file with the encoded dataset
    file_name = context.source_path.split('/')[-1].replace('.xml', '.json')
    fixture_file_name = '_'.join([context.owner_name, context.repo_name, file_name]).replace('/', '_')

    download_url = '/'.join([GITHUB_API_URL, 'repos', context.owner_name, context.repo_name,
                             'contents', context.source_path])

    fixture_file_path = os.path.abspath(os.path.join('features', 'fixtures', fixture_file_name))
    # open the json file containg the encoded xml
    with open(fixture_file_path) as json_file:
        context.xml_encoded = json.load(json_file)
    # httpretty.register_uri(httpretty.GET, download_url, body=etree.tostring(context.config_xml_content.getroot()))
        httpretty.register_uri(httpretty.GET, download_url, body=json.dumps(context.xml_encoded))

    # build up the path to the fixtures RAW XML file
    fixture_file_frags = context.source_path.split('/')
    fixture_file_path_raw = os.path.abspath(os.path.join(*fixture_file_frags))
    download_url = context.xml_encoded['download_url']

    # get the raw zipped file
    with open(fixture_file_path_raw) as xml_file:
        context.xml_text = xml_file.read()
        httpretty.register_uri(httpretty.GET, download_url, body=context.xml_text, content_type='text/plain')
        context.xml = etree.parse(StringIO(context.xml_text))

    context.res = context.isa_adapter.retrieve(context.source_path, context.destination_path, context.owner_name,
                                               context.repo_name)

    expect(httpretty.has_request()).to.be.true


@then("it should download it as an XML file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    out_file_path = os.path.join(context.destination_path, context.source_path.split('/')[-1])
    # written_xml_config_content = etree.parse(out_file)
    # expect(set(written_xml_config_content.getroot().itertext()))\
    #    .to.equal(set(context.config_xml_content.getroot().itertext()))
    with open(out_file_path) as xml_file:
        written_xml_text = xml_file.read()
    # test equality of input and output
    expect(written_xml_text).to.equal(context.xml_text)
    # test that the stored output is valid XML
    xml = etree.parse(StringIO(written_xml_text))
    expect(xml).to.be.an(etree._ElementTree)


@step("it should return it as an XML object")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expect(etree.tostring(context.res)).to.equal(etree.tostring(context.xml))


@when("it is none of the allowed file types - JSON, XML, ZIP - nor a directory")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    file_name = context.source_path.split('/')[-1].replace('.py', '.json')
    fixture_file_name = '_'.join([context.owner_name, context.repo_name, file_name]).replace('/', '_')

    download_url = '/'.join([GITHUB_API_URL, 'repos', context.owner_name, context.repo_name,
                             'contents', context.source_path])
    fixture_file_path = os.path.abspath(os.path.join('features', 'fixtures', fixture_file_name))

    with open(fixture_file_path) as json_file:
        context.text_encoded = json.load(json_file)
        httpretty.register_uri(httpretty.GET, download_url, body=json.dumps(context.text_encoded),
                               content_type='text/plain')

    fixture_file_frags = context.source_path.split('/')
    fixture_file_path_raw = os.path.abspath(os.path.join(*fixture_file_frags))
    download_url = context.text_encoded['download_url']

    with open(fixture_file_path_raw) as text_file:
        context.text_file = text_file.read()
        httpretty.register_uri(httpretty.GET, download_url, body=context.text_file, content_type='text/plain')

    context.res = context.isa_adapter.retrieve(context.source_path, context.destination_path, context.owner_name,
                                               context.repo_name)


@then("it should not save the file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    out_file_path = os.path.join(context.destination_path, context.source_path.split('/')[-1])
    expect(os.path.exists(out_file_path)).to.be.false


@step("it should return a falsey value")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expect(context.res).to.be.false
