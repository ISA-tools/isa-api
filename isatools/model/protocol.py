import os
from collections.abc import Iterable
from pprint import pprint
from yaml import load, FullLoader
from isatools.constants import SYNONYMS
from isatools.model.comments import Commentable
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.protocol_component import ProtocolComponent
from isatools.model.identifiable import Identifiable
from isatools.model.loader_indexes import loader_states


class Protocol(Commentable, Identifiable):
    """An experimental Protocol used in the study.

    Attributes:
        name: The name of the protocol used
        protocol_type: Term to classify the protocol.
        description: A free-text description of the protocol.
        uri: Pointer to protocol resources externally that can be accessed by
            their Uniform Resource Identifier (URI).
        version: An identifier for the version to ensure protocol tracking.
        parameters: A list of ProtocolParameter describing the list of
            parameters required to execute the protocol.
        components: A list of OntologyAnnotation describing a protocol's
            components; e.g. instrument names, software names, and reagents
            names.
        comments: Comments associated with instances of this class.
    """

    def __init__(self,
                 id_='',
                 name='',
                 uri='',
                 description='',
                 version='',
                 protocol_type=None,
                 parameters=None,
                 components=None,
                 comments=None):
        super().__init__(comments=comments)

        self.id = id_
        self.__name = name
        self.__protocol_type = None
        self.__parameters = None
        self.__components = None

        self.protocol_type = protocol_type

        self.__description = description
        self.__uri = uri
        self.__version = version

        self.__parameters = []
        self.__components = []

        if parameters is not None:
            self.parameters = parameters

        if components is not None:
            self.components = components

    @staticmethod
    def show_allowed_protocol_types():
        """
        Pretty prints the allowed values (i.e. the values that pass the ISA-tab validation using the default
        XML validations) for Protocol Types
        """
        protocol_types_dict = load_protocol_types_info()
        pprint(protocol_types_dict)

    @property
    def name(self):
        """:obj:`str`: the name of the protocol"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Protocol.name must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        self.__name = val

    @property
    def protocol_type(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        study protocol type"""
        return self.__protocol_type

    @protocol_type.setter
    def protocol_type(self, val):
        if val is not None and not isinstance(val, (str, OntologyAnnotation)):
            raise AttributeError('Protocol.protocol_type must be a OntologyAnnotation, a string or None; got {0}:{1}'
                                 .format(val, type(val)))
        elif isinstance(val, str) or val is None:
            if val is None:
                val = ''
            self.__protocol_type = OntologyAnnotation(term=val)
        else:
            self.__protocol_type = val

    @property
    def description(self):
        """:obj:`str`: the description of the protocol"""
        return self.__description

    @description.setter
    def description(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Protocol.description must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__description = val

    @property
    def uri(self):
        """:obj:`str`: the uri of the protocol"""
        return self.__uri

    @uri.setter
    def uri(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('Protocol.uri must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__uri = val

    @property
    def version(self):
        """:obj:`str`: the version of the protocol"""
        return self.__version

    @version.setter
    def version(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('Protocol.version must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__version = val

    @property
    def parameters(self):
        """:obj:`list` of :obj:`ProtocolParameter`: Container for protocol
        parameters"""
        return self.__parameters

    @parameters.setter
    def parameters(self, val):
        if val is None or not isinstance(val, Iterable):
            raise AttributeError('Protocol.parameters must be an iterable containing ProtocolParameters')
        for el in val:
            self.add_param(el)

    def add_param(self, parameter_name=''):
        if self.get_param(parameter_name=parameter_name) is not None:
            pass
        else:
            if isinstance(parameter_name, str):
                self.__parameters.append(ProtocolParameter(
                    parameter_name=OntologyAnnotation(term=parameter_name)))
            elif isinstance(parameter_name, ProtocolParameter):
                self.__parameters.append(parameter_name)
            else:
                raise AttributeError('Parameter name must be either a string or a ProtocolParameter')

    def get_param(self, parameter_name):
        ''' not a DOCTSTRING
            try:
               param = next(x for x in self.parameters if
                            x.parameter_name.term == parameter_name)
           except StopIteration:
               pass
           except AttributeError:
               log.error('Error caught: parameters: {0} - parameter_name: {1}'.format(self.parameters, parameter_name))
        '''
        param = None
        try:
            param = self.parameters[[param.parameter_name.term for param in self.parameters].index(parameter_name)]
        except ValueError:
            pass
        return param

    @property
    def components(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for protocol
        components"""
        return self.__components

    @components.setter
    def components(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation) for x in val):
                self.__components = list(val)
        else:
            raise AttributeError('Protocol.components must be iterable containing OntologyAnnotations')

    def __repr__(self):
        return ("isatools.model.Protocol(name='{protocol.name}', "
                "protocol_type={protocol_type}, "
                "uri='{protocol.uri}', version='{protocol.version}', "
                "parameters={protocol.parameters}, "
                "components={protocol.components}, "
                "comments={protocol.comments})"
                ).format(protocol=self, protocol_type=repr(self.protocol_type))

    def __str__(self):
        return ("Protocol(\n\t"
                "name={protocol.name}\n\t"
                "protocol_type={protocol_type}\n\t"
                "uri={protocol.uri}\n\t"
                "version={protocol.version}\n\t"
                "parameters={num_parameters} ProtocolParameter objects\n\t"
                "components={num_components} OntologyAnnotation objects\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(protocol=self,
                         protocol_type=self.protocol_type.term if self.protocol_type else '',
                         num_parameters=len(self.parameters),
                         num_components=len(self.components) if self.components else 0,
                         num_comments=len(self.comments) if self.comments else 0)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return (isinstance(other, Protocol)
                and self.name == other.name
                and self.protocol_type == other.protocol_type
                and self.uri == other.uri
                and self.version == other.version
                and self.parameters == other.parameters
                and self.components == other.components
                and self.comments == other.comments)

    def __ne__(self, other):
        return not self == other

    def to_dict(self, ld=False):
        protocol = {
            '@id': self.id,
            'name': self.name,
            'description': self.description,
            'uri': self.uri,
            'version': self.version,
            'comments': [comment.to_dict(ld=ld) for comment in self.comments],
            'parameters': [protocol_parameter.to_dict(ld=ld) for protocol_parameter in self.parameters],
            'protocolType': self.protocol_type.to_dict(ld=ld) if self.protocol_type else {},
            'components': []
        }
        return self.update_isa_object(protocol, ld=ld)

    def from_dict(self, protocol):
        self.id = protocol.get('@id', '')
        self.name = protocol.get('name', '')
        self.description = protocol.get('description', '')
        self.uri = protocol.get('uri', '')
        self.version = protocol.get('version', '')
        self.load_comments(protocol.get('comments', []))

        # Protocol type
        protocol_type_data = protocol.get('protocolType', None)
        if protocol_type_data:
            protocol_type = OntologyAnnotation()
            protocol_type.from_dict(protocol_type_data)
            self.protocol_type = protocol_type

        # Parameters
        for parameter_data in protocol.get('parameters', []):
            parameter = ProtocolParameter()
            parameter.from_dict(parameter_data)
            self.parameters.append(parameter)
            loader_states.add_parameter(parameter)

        # Components
        for component_data in protocol.get('components', []):
            component = ProtocolComponent()
            component.from_dict(component_data)
            self.components.append(component)


def load_protocol_types_info() -> dict:
    """ Load the protocol types info from the YAML protocol types file

    Returns:
        A dictionary of protocol types
    """
    filepath = os.path.join(os.path.dirname(__file__), '..', 'resources', 'config', 'yaml', 'protocol-types.yml')
    with open(filepath) as yaml_file:
        return load(yaml_file, Loader=FullLoader)

    
    
