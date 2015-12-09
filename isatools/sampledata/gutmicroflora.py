from os.path import dirname, join

# This is BII-S-7 "Gut microflora Metagenomes in 2 different population fed a different diet"

try:
    import json
except ImportError as e:
    raise RuntimeError("gut-microflora data requires json to be installed")

microflora = json.load(join(dirname(__file__), 'gutmicroflora.json'))
