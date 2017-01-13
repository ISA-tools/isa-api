from os.path import dirname, join

# This is BII-I-1 "Growth control of the eukaryote cell: a systems biology study in yeast"

try:
    import json as j
except ImportError as e:
    raise RuntimeError("BII-I-1 data requires json to be installed")

#  returns json representation of eukaryotecell.json
json = j.load(open(join(dirname(__file__), 'BII-I-1.json')))
