from os.path import dirname, join

try:
    import json
except ImportError as e:
    raise RuntimeError("eukaryotecell data requires json to be installed")

eukaryotecell = json.load(join(dirname(__file__), 'eukaryotecell.json'))
