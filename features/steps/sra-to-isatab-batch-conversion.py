from behave import *

use_step_matcher("re")


@given('A list of comma separated access numbers "(?P<access_numbers>.+)"')
def step_impl(context, access_numbers):
    """
    :type context: behave.runner.Context
    :type access_numbers: str
    """
    pass