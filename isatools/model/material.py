from abc import ABCMeta
from isatools.model.comments import Commentable
from isatools.model.sample import Sample
from isatools.model.process_sequence import ProcessSequenceNode
from isatools.model.characteristic import Characteristic
from isatools.model.identifiable import Identifiable
from isatools.model.loader_indexes import loader_states as indexes


class Material(Commentable, ProcessSequenceNode, Identifiable, metaclass=ABCMeta):
    """Represents a generic material in an experimental graph.
    """

    def __init__(self, name='', id_='', type_='', characteristics=None, derives_from=None,
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
        self.__derives_from = []
        if derives_from:
            self.__derives_from = derives_from

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

    def yield_characteristics(self, category: str = None) -> filter:
        """Gets an iterator of matching comments for a given name.
    
        Args:
            name: Comment name
    
        Returns:
            :obj:`filter` of :obj:`Comments` that can be iterated on.
        """
        return filter(lambda x: x.category == category if category else x, self.characteristics)

    def load_characteristics(self, characteristics_data):
        characteristics = []
        for characteristic_data in characteristics_data:
            characteristic = Characteristic()
            characteristic.from_dict(characteristic_data)
            characteristics.append(characteristic)
        self.characteristics = characteristics

    @property
    def derives_from(self):
        """:obj:`list` of :obj:`Sample or Material`: a list of references from this sample
        material to a source material(s)"""
        return self.__derives_from

    @derives_from.setter
    def derives_from(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Sample) or isinstance(x, Extract) for x in val):
                self.__derives_from = list(val)
        else:
            raise AttributeError(
                'Sample.derives_from must be iterable containing Sources')

    def to_dict(self):
        return {
            '@id': self.id,
            "name": self.name,
            "type": self.type,
            "characteristics": [characteristic.to_dict() for characteristic in self.characteristics],
            "derivesFrom": [],
            "comments": [comment.to_dict() for comment in self.comments]
        }


class Extract(Material):
    """Represents a extract material in an experimental graph."""

    def __init__(self, name='', id_='', characteristics=None, derives_from=None, comments=None):
        super().__init__(name=name, id_=id_, characteristics=characteristics, derives_from=derives_from,
                         comments=comments)

        self.type = 'Extract Name'

    def __repr__(self):
        return ("isatools.model.Extract(name='{extract.name}', "
                "type='{extract.type}', "
                "characteristics={extract.characteristics}, "
                "derivesFrom={extract.derivesFrom}"
                "comments={extract.comments})").format(extract=self)

    def __str__(self):
        return ("Extract(\n\t"
                "name={extract.name}\n\t"
                "type={extract.type}\n\t"
                "characteristics={num_characteristics} Characteristic objects\n\t"
                "derivesFrom={num_samples} Sample objects\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(extract=self,
                         num_characteristics=len(self.characteristics),
                         num_samples=len(self.derives_from),
                         num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Extract) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.type == other.type \
               and self.derives_from == other.derives_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    def from_dict(self, other):
        self.id = other.get('@id', '')
        self.name = other.get('name', '').replace('extract-', '-')
        if other.get('type', '') == "Extract Name":
            self.type = other.get('type', '')
        self.load_comments(other.get('comments', []))

        # characteristics
        for characteristic_data in other.get('characteristics', []):
            id_ = characteristic_data.get('category', {}).get('@id', '')
            data = {
                'comments': characteristic_data.get('comments', []),
                'category': indexes.get_characteristic_category(id_),
                'value': characteristic_data['value'],
                'unit': characteristic_data.get('unit', '')
            }
            characteristic = Characteristic()
            characteristic.from_dict(data)
            self.characteristics.append(characteristic)

        for derives_data in other.get('derivesFrom', []):
            self.derives_from.append(indexes.get_sample(derives_data["@id"]))


class LabeledExtract(Material):
    """Represents a labeled extract material in an experimental graph."""

    def __init__(self, name='', id_='', characteristics=None, derives_from=None, comments=None):
        super().__init__(name=name, id_=id_, characteristics=characteristics, derives_from=derives_from,
                         comments=comments)

        self.type = 'Labeled Extract Name'

    def __repr__(self):
        return "isatools.model.LabeledExtract(name='{labeled_extract.name}'," \
               "type='Labeled Extract Name', " \
               "characteristics={labeled_extract.characteristics}, " \
               "derivesFrom={labeled_extract.derivesFrom}" \
               "comments={labeled_extract.comments})" \
            .format(labeled_extract=self)

    def __str__(self):
        return ("LabeledExtract(\n\t"
                "name={labeled_extract.name}\n\t"
                "type=Labeled Extract Name\n\t"
                "characteristics={num_characteristics} Characteristic objects\n\t"
                "derivesFrom={num_extracts} Extract objects\n\t"
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
               and self.derives_from == other.derives_from \
               and self.type == other.type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    def from_dict(self, other):
        self.id = other.get('@id', '')
        self.name = other.get('name', '').replace('labeledextract-', '-')
        if other.get('type', '') == "Labeled Extract Name":
            self.type = other.get('type', '')
        self.load_comments(other.get('comments', []))

        # characteristics
        for characteristic_data in other.get('characteristics', []):
            id_ = characteristic_data.get('category', {}).get('@id', '')
            data = {
                'comments': characteristic_data.get('comments', []),
                'category': indexes.get_characteristic_category(id_),
                'value': characteristic_data['value'],
                'unit': characteristic_data.get('unit', '')
            }
            characteristic = Characteristic()
            characteristic.from_dict(data)
            self.characteristics.append(characteristic)

        for derives_data in other.get('derivesFrom', []):
            self.derives_from.append(indexes.get_other_material(derives_data["@id"]))
