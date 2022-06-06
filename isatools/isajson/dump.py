import re
from json import JSONEncoder

from isatools.model import (
    Investigation, OntologyAnnotation, OntologySource, Publication, Person, Study, Protocol, Characteristic, Material
)


class ISAJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.to_dict()
