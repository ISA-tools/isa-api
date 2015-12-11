from os.path import dirname, join

# This is BII-S-3 "Metagenomes and Metatranscriptomes of phytoplankton blooms from an ocean acidification mesocosm
# experiment"

try:
    import json
except ImportError as e:
    raise RuntimeError("phytoplankton data requires json to be installed")

#  returns json representation of phytoplankton.json
bii_s_3 = json.load(join(dirname(__file__), 'BII-S-3.json'))
