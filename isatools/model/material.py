from abc import ABCMeta

from isatools.model.comments import Commentable
from isatools.model.process_sequence import ProcessSequenceNode
from isatools.model.characteristic import Characteristic
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.identifiable import Identifiable
from isatools.model.loader_indexes import loader_states as indexes


class Material(Commentable, ProcessSequenceNode, Identifiable, metaclass=ABCMeta):
    """Represents a generic material in an experimental graph.
    """

    def __init__(self, name='', id_='', type_='', characteristics=None,
                 comments=None):
        Commentable.__init__(self, comments=comments)
        ProcessSequenceNode.__init__(self)
        Identifiable.__init__(self)

        self.id = id_
        self.__name = name
        self.__type = type_

        self.__characteristics = []
        if characteristics:
            self.__characteristics = characteristics

    @property
    def name(self):
        """:obj:`str`: the name of the material"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('{0}.name must be a str or None; got {1}:{2}'
                                 .format(type(self).__name__, val, type(val)))
        self.__name = val

    @property
    def type(self):
        """:obj:`str`: the type of the material"""
        return self.__type

    @type.setter
    def type(self, val):
        # TODO: use json_schema to get these values
        if val is not None and (not isinstance(val, str) or val not in ['Extract Name', 'Labeled Extract Name']):
            raise AttributeError('{0}.type must be a str in ("Extract Name", "Labeled Extract Name") or None; '
                                 'got {1}:{2}'.format(type(self).__name__, val, type(val)))
        self.__type = val

    @property
    def characteristics(self):
        """:obj:`list` of :obj:`Characteristic`: Container for material
        characteristics"""
        return self.__characteristics

    @characteristics.setter
    def characteristics(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Characteristic) for x in val):
                self.__characteristics = list(val)
        else:
            raise AttributeError('{}.characteristics must be iterable containing Characteristics'
                                 .format(type(self).__name__))

    def __eq__(self, other):
        return isinstance(other, Material) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.type == other.type \
               and self.comments == other.comments

    def to_dict(self, ld=False):
        material = {
            '@id': self.id,
            "name": self.name,
            "type": self.type,
            "characteristics": [characteristic.to_dict(ld=ld) for characteristic in self.characteristics],
            "comments": [comment.to_dict(ld=ld) for comment in self.comments]
        }
        return self.update_isa_object(material, ld)

    def from_dict(self, material):
        self.id = material["@id"]
        self.name = material['name']
        self.type = material["type"]
        self.load_comments(material.get("comments", []))

        for characteristic_data in material["characteristics"]:
            characteristic = Characteristic()
            if isinstance(characteristic_data["value"], dict):
                characteristic.value = OntologyAnnotation()
                characteristic.value.from_dict(characteristic_data["value"])
                characteristic.category = indexes.get_characteristic_category(characteristic_data['category']['@id'])
            if isinstance(characteristic_data["value"], int or float):
                characteristic.value = characteristic_data["value"]
            if isinstance(characteristic_data["value"], str):
                characteristic.value = characteristic_data["value"]

            self.characteristics.append(characteristic)


class Extract(Material):
    """Represents a extract material in an experimental graph."""

    def __init__(self, name='', id_='', characteristics=None, comments=None):
        super().__init__(name=name, id_=id_, characteristics=characteristics,
                         comments=comments)

        self.type = 'Extract Name'

    def __repr__(self):
        return ("isatools.model.Extract(name='{extract.name}', "
                "type='{extract.type}', "
                "characteristics={extract.characteristics}, "
                "comments={extract.comments})").format(extract=self)

    def __str__(self):
        return ("Extract(\n\t"
                "name={extract.name}\n\t"
                "type={extract.type}\n\t"
                "characteristics={num_characteristics} Characteristic objects\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(extract=self,
                         num_characteristics=len(self.characteristics),
                         num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Extract) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.type == other.type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class LabeledExtract(Material):
    """Represents a labeled extract material in an experimental graph."""

    def __init__(self, name='', id_='', characteristics=None, comments=None):
        super().__init__(name=name, id_=id_, characteristics=characteristics,
                         comments=comments)

        self.type = 'Labeled Extract Name'

    def __repr__(self):
        return "isatools.model.LabeledExtract(name='{labeled_extract.name}'," \
               " type='Labeled Extract Name', " \
               "characteristics={labeled_extract.characteristics}, " \
               "comments={labeled_extract.comments})" \
            .format(labeled_extract=self)

    def __str__(self):
        return ("LabeledExtract(\n\t"
                "name={labeled_extract.name}\n\t"
                "type=Labeled Extract Name\n\t"
                "characteristics={num_characteristics} Characteristic objects\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(labeled_extract=self,
                         num_characteristics=len(self.characteristics),
                         num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, LabeledExtract) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.type == other.type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other
