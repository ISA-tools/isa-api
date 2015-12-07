from os.path import dirname, join

try:
    import json
except ImportError as e:
    raise RuntimeError("phytoplankton data requires json to be installed")

phytoplankton = json.load(join(dirname(__file__), 'phytoplankton.json'))
