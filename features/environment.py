import os
import shutil

__author__ = 'massi'

TARGET_DIR = 'test_outputs'


def before_all(context):
    os.makedirs(TARGET_DIR, exist_ok=True)


def after_all(context):
    """
    Removes target directory after the tests are run
    NOTE: better to move this in the before_all ??
    """
    target_path = os.path.abspath(os.path.join(os.path.dirname(__file__), TARGET_DIR))
    print(target_path)
    shutil.rmtree(target_path)