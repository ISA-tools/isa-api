from os.path import dirname, join

try:
    import json
except ImportError as e:
    raise RuntimeError("gut-microflora data requires json to be installed")

microflora = json.load(join(dirname(__file__), 'gutmicroflora.json'))
