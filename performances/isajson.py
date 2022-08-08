from cProfile import runctx
from os import path
import json

from isatools.isajson import load, validate
from isatools.model import Investigation


HERE_PATH = path.dirname(path.abspath(__file__))
OUTPUT_PATH = path.join(HERE_PATH, 'profiles')
DEFAULT_INPUT = path.join(HERE_PATH, '..', 'tests', 'data', 'json', 'BII-I-1/BII-I-1.json')


def profile_json_load(filename=None, output_path=None):
    input_data_path = filename if filename else DEFAULT_INPUT
    output_path = output_path if output_path else OUTPUT_PATH
    with open(input_data_path, 'r') as isajson_fp:
        output_data_path = path.join(output_path, 'isajson_load')
        runctx('load(isajson_fp)', globals(), locals(), output_data_path)


def profile_json_dump(filename=None, output_path=None):
    input_data_path = filename if filename else DEFAULT_INPUT
    output_path = output_path if output_path else OUTPUT_PATH
    with open(input_data_path, 'r') as fp:
        data = json.load(fp)
    investigation = Investigation()
    investigation.from_dict(data)
    output_data_path = path.join(output_path, 'isajson_dump')
    runctx('investigation.to_dict()', globals(), locals(), output_data_path)


def profile_validate(filename=None, output_path=None):
    input_data_path = filename if filename else DEFAULT_INPUT
    output_path = output_path if output_path else OUTPUT_PATH
    output_data_path = path.join(output_path, 'isajson_validate')
    with open(input_data_path, 'r') as fp:
        runctx('validate(fp)', globals(), locals(), output_data_path)


def profile_isajson(filename=None, output_path=None):
    profile_json_load(filename, output_path)
    profile_json_dump(filename, output_path)
    profile_validate(filename, output_path)
