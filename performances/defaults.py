from os import path

HERE_PATH = path.dirname(path.abspath(__file__))
OUTPUT_PATH = path.join(HERE_PATH, 'profiles')
DEFAULT_JSON_INPUT = path.join(HERE_PATH, '..', 'tests', 'data', 'json', 'BII-I-1/BII-I-1.json')
DEFAULT_TAB_INPUT = path.join(HERE_PATH, '..', 'tests', 'data', 'tab', 'BII-I-1/i_investigation.txt')
