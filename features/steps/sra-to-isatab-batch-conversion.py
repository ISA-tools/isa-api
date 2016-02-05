from behave import *

use_step_matcher("parse")


@given('A list of comma separated access numbers "{access_numbers}"')
def step_impl(context, access_numbers):
    """
    :type context: behave.runner.Context
    :type access_numbers: str
    """
    pass


@when("the SRA to ISA tab conversion is invoked")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("it should return a ZIP file object")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("the ZIP file should contain as many directories as the element in the list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass