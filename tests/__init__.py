__author__ = 'althonos'


import sys

if sys.version_info[0]==2:

    import os
    import importlib

    _testdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, _testdir)
    # import all tests in current directory
    for filename in os.listdir(_testdir):
        if filename.startswith("test_") and filename.endswith(".py"):
            importlib.import_module(filename[:-3])
