from .model.v1 import Investigation


def load(fp):
    isa_obj = Investigation()
    return isa_obj


def dump(isa_obj, fp):
    s = isa_obj.to_json()
    return s


def loads(s):
    isa_obj = Investigation()
    return isa_obj


def dumps(isa_obj):
    s = isa_obj.to_json()
    return s
