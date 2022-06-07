from json import JSONEncoder


class ISAJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_dict'):
            method = getattr(o, 'to_dict')
            if callable(method):
                return o.to_dict()
        return JSONEncoder.default(self, o)
