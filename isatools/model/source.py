from isatools.model.comments import Commentable
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.characteristic import Characteristic
from isatools.model.process_sequence import ProcessSequenceNode
from isatools.model.identifiable import Identifiable
from isatools.model.loader_indexes import loader_states as indexes


class Source(Commentable, ProcessSequenceNode, Identifiable):
    """Represents a Source material in an experimental graph.

    Attributes:
        name: A name/reference for the source material.
        characteristics: A list of Characteristics used to qualify the material
            properties.
        comments: Comments associated with instances of this class.
    """

    def __init__(self, name='', id_='', characteristics=None, comments=None):
        # super().__init__(comments)
        Commentable.__init__(self, comments)
        ProcessSequenceNode.__init__(self)
        Identifiable.__init__(self)

        self.id = id_
        self.__name = name

        self.__characteristics = []
        if characteristics:
            self.characteristics = characteristics

    @property
    def name(self):
        """:obj:`str`: the name of the source material"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('Source.name must be a str or None; got {0}:{1}'
                                 .format(val, type(val)))
        else:
            self.__name = val

    @property
    def characteristics(self):
        """:obj:`list` of :obj:`Characteristic`: Container for source material
        characteristics"""
        return self.__characteristics

    @characteristics.setter
    def characteristics(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Characteristic) for x in val):
                self.__characteristics = list(val)
        else:
            raise AttributeError('Source.characteristics must be iterable containing Characteristics')

    def has_char(self, char):
        if isinstance(char, str):
            char = Characteristic(category=OntologyAnnotation(term=char))
        if isinstance(char, Characteristic):
            return char in self.characteristics
        return False

    def get_char(self, name):
        hits = [x for x in self.characteristics if x.category.term == name]
        try:
            result = next(iter(hits))
        except StopIteration:
            result = None
        return result

    def __repr__(self):
        return("isatools.model.Source(name='{source.name}', " 
               "characteristics={source.characteristics}, " 
               "comments={source.comments})".format(source=self))

    def __str__(self):
        return("Source(\n\t"
               "name={source.name}\n\t"
               "characteristics={num_characteristics} Characteristic objects\n\t"
               "comments={num_comments} Comment objects\n)"
               ).format(source=self, num_characteristics=len(self.characteristics), num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Source) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {
            '@id': self.id,
            'name': self.name,
            'characteristics': [char.to_dict() for char in self.characteristics],
            'comments': [comment.to_dict() for comment in self.comments]
        }

    def from_dict(self, source):
        self.id = source.get('@id', '')
        self.name = source.get('name', '')
        self.load_comments(source.get('comments', []))

        # characteristics
        for characteristic_data in source.get('characteristics', []):
            id_ = characteristic_data.get('category', {}).get('@id', '')
            data = {
                'comments': characteristic_data.get('comments', []),
                'category': indexes.get_characteristic_category(id_),
                'value': characteristic_data['value'],
                'unit': characteristic_data['unit']
            }
            characteristic = Characteristic()
            characteristic.from_dict(data)
            self.characteristics.append(characteristic)


