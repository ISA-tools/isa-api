from behave import *

use_step_matcher("re")


@given('an optional user login (?P<test_user>.+)')
def step_impl(context, test_user):
    """
    :type test_user: str
    :type context: behave.runner.Context
    """
    context.test_user = test_user


@step('an optional user password (?P<test_password>.+)')
def step_impl(context, test_password):
    """
    :type test_password: str
    :type context: behave.runner.Context
    """
    context.test_password = test_password


@when("a storage adapter is created")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.isa_adapter = GitHubIsaAdapter(context.username, context.password)


@then("it should instantiate an authenticated connector instance")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.isa_adapter.is_authenticated() is True


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