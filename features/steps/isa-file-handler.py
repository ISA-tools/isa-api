from datetime import datetime, timezone

import hashlib
import httpretty
import json
import os
from behave import *
from sure import expect
from zipfile import is_zipfile
from urllib.parse import urljoin
from isatools.io.storage_adapter import IsaGitHubStorageAdapter

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
    context.destination_path = os.path.join(os.path.expanduser('~'), destination_dir)
    print(context.destination_path)


@when("the file object is a directory")
@httpretty.activate
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    file_name = '_'.join([context.owner_name, context.repo_name, context.source_path]).replace('/', '_')
    file_name += '.json'
    print("file_name: ", file_name)
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures', file_name))
    print(file_path)
    with open(file_path) as json_file:
        payload = json.load(json_file)
        download_url = '/'.join([GITHUB_API_URL, 'repos', context.owner_name, context.repo_name,
                                'contents', context.source_path])
        httpretty.register_uri(httpretty.GET, download_url, content_type='application/json', body=json.dumps(payload))
        context.isa_adapter.download(context.source_path, context.destination_path, context.owner_name,
                                     context.repo_name)
    expect(httpretty.has_request()).to.be.true


@then("it should download the whole directory it as an archived file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    source_name = context.source_path.split('/')[-1] + '.zip'
    file_path = os.path.join(context.destination_path, source_name)
    expect(os.path.exists(file_path)).to.be.true
    file_stat = os.stat(file_path)
    expect(file_stat.st_size).to.be.greater_than(0)
    expect(is_zipfile(file_path)).to.be.true


@when("the file object is an archive \(i.e. a ZIP file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should download it as an archive \(i\.e\. a ZIP file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("the source file points to an \(ISA-TAB\) JSON file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should download it as a JSON file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("the source file points to an \(ISA-TAB\) XML configuration file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should download it as an XML file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("it is a different file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should raise an error \(validation error\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given('a valid path in the in the remote repository "/path/to/source"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("the source path points to a JSON file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should store/load a Python dictionary containing the whole ISA dataset")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("the source points to an XML configuration file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should load the XML document in memory")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("it is a different file or a directory")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should raise an error")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("the source path is not correct")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass
