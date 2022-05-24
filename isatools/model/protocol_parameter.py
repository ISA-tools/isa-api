from isatools.model.comments import Commentable
from isatools.model.ontology_annotation import OntologyAnnotation


class ProtocolParameter(Commentable):
    """A parameter used by a protocol.

    Attributes:
        parameter_name: A parameter name as an ontology term
        comments: Comments associated with instances of this class.
    """

    def __init__(self, id_='', parameter_name=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.__parameter_name = None
        self.parameter_name = parameter_name

    @property
    def parameter_name(self):
        """:obj:`OntologyAnnotation`: an ontology annotation representing the
        parameter name"""
        return self.__parameter_name

    @parameter_name.setter
    def parameter_name(self, val):
        if val is None or isinstance(val, OntologyAnnotation):
            self.__parameter_name = val
        elif isinstance(val, str):
            self.__parameter_name = OntologyAnnotation(term=val)
        else:
            error_msg = ('ProtocolParameter.parameter_name must be either a string or an OntologyAnnotation or None; '
                         'got {0}:{1}').format(val, type(val))
            raise AttributeError(error_msg)

    def __repr__(self):
        return ('isatools.model.ProtocolParameter('
                'parameter_name={parameter_name}, '
                'comments={parameter.comments})').format(parameter=self, parameter_name=repr(self.parameter_name))

    def __str__(self):
        parameter_name = self.parameter_name.term if self.parameter_name else ''
        return ("ProtocolParameter(\n\t"
                "parameter_name={parameter_name}\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(parameter_name=parameter_name, num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return (isinstance(other, ProtocolParameter)
                and self.parameter_name == other.parameter_name
                and self.comments == other.comments)

    def __ne__(self, other):
        return not self == other
