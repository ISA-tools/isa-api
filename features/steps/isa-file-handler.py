from behave import *
from isatools.io.storage_adapter import IsaGitHubStorageAdapter
from sure import expect
from datetime import datetime, timezone
import httpretty, json, hashlib

use_step_matcher("re")

md5 = hashlib.md5()

AUTH_ID = 1
AUTH_URL = 'https://api.github.com/authorizations'
AUTH_TOKEN = "som3ar4nd0mAcc3$$tok3n"
md5.update(AUTH_TOKEN.encode('utf-8'))
AUTH_RES_BODY = {
    'id': AUTH_ID,
    'url': AUTH_URL + "/" + str(AUTH_ID),
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


@given('an optional user login (?P<test_user>.+)')
def step_impl(context, test_user):
    """
    :type test_user: str
    :type context: behave.runner.Context
    """
    context.username = test_user


@step('an optional user password (?P<test_password>.+)')
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

    httpretty.register_uri(httpretty.POST, AUTH_URL, body=json.dumps(AUTH_RES_BODY), content_type='application/json')
    context.isa_adapter = IsaGitHubStorageAdapter(context.username, context.password)
    expect(httpretty.has_request()).to.be.true


@then("it should instantiate an authenticated connector instance")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expect(context.isa_adapter.is_authenticated).to.be.true
    expect(context.isa_adapter.token).to.be(AUTH_TOKEN)


@given('a valid path in the remote repository "/path/to/source"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step('an \(optional\) destination directory "/path/to/destination"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("the source path points to directory")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should download the whole directory it as an archived file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("the source path points to an archive")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should save it as it is \(i\.e\. an archive\)")
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


@then("it should raise an error")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass