from behave import *

use_step_matcher("parse")


@given('An access number {access_number}')
def step_impl(context, access_number):
    """
    :type access_number: str
    :type context: behave.runner.Context
    """
    context.access_number = access_number
    print(context.access_number)


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


@step("nothing else")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("Nothing else")