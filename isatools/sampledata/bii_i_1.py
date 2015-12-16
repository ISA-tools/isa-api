from os.path import dirname, join

# This is BII-I-1 "Growth control of the eukaryote cell: a systems biology study in yeast"

try:
    import json
except ImportError as e:
    raise RuntimeError("BII-I-1 data requires json to be installed")

#  returns json representation of eukaryotecell.json
bii_i_1 = json.load(join(dirname(__file__), 'BII-I-1.json'))
