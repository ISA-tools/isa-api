from isatools.model.comments import Commentable
from isatools.model.ontology_annotation import OntologyAnnotation


class ProtocolComponent(Commentable):
    """A component used in a protocol.

    Attributes:
        name: A component name.
        component_type: The classifier as a term for the component.
        comments: Comments associated with instances of this class.
    """

    def __init__(self, id_='', name='', component_type=None, comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name

        if component_type is None:
            self.__component_type = OntologyAnnotation()
        else:
            self.__component_type = component_type

    @property
    def name(self):
        """:obj:`str`: the name of the protocol component"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('ProtocolComponent.name must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__name = val

    @property
    def component_type(self):
        """ :obj:`OntologyAnnotation`: a component_type for the protocol
        component"""
        return self.__component_type

    @component_type.setter
    def component_type(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise AttributeError(
                'ProtocolComponent.component_type must be a '
                'OntologyAnnotation, or None; got {0}:{1}'.format(
                    val, type(val)))
        else:
            self.__component_type = val

    def __repr__(self):
        return "isatools.model.ProtocolComponent(name='{component.name}', " \
               "category={component_type}, " \
               "comments={component.comments})".format(
            component=self, component_type=repr(self.component_type))

    def __str__(self):
        return """ProtocolComponent(
    name={component.name}
    category={component_type}
    comments={num_comments} Comment objects
)""".format(component=self, component_type=self.component_type.term if
        self.component_type else '', num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ProtocolComponent) \
               and self.name == other.name \
               and self.component_type == other.component_type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    def from_dict(self, protocol_component):
        self.name = protocol_component.get('componentName', '')
        self.load_comments(protocol_component.get('comments', []))

        # component type
        component_type_data = protocol_component.get('componentType', None)
        if component_type_data:
            component_type = OntologyAnnotation()
            component_type.from_dict(component_type_data)
            self.component_type = component_type
