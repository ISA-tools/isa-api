from os.path import dirname, join

# This is BII-I-1 "Growth control of the eukaryote cell: a systems biology study in yeast"

try:
    import json
except ImportError as e:
    raise RuntimeError("eukaryotecell data requires json to be installed")

#  returns json representation of eukaryotecell.json
eukaryotecell = json.load(join(dirname(__file__), 'eukaryotecell.json'))
