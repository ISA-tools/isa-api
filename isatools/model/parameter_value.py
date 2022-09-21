from numbers import Number
from isatools.model.comments import Commentable
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.loader_indexes import loader_states as indexes
from isatools.model.utils import get_context_path


class ParameterValue(Commentable):
    """A ParameterValue represents the instance value of a ProtocolParameter,
    used in a Process.

    Attributes:
        category: A link to the relevant ProtocolParameter that the value is
            set for.
        value: The value of the parameter.
        unit: The qualifying unit classifier, if the value is numeric.
        comments: Comments associated with instances of this class.
    """

    def __init__(self, category=None, value=None, unit=None, comments=None):
        super().__init__(comments)

        self.__category = None
        self.__value = None
        self.__unit = None
        self.category = category

        # Shouldn't this be in the setter to avoid manually setting a non-numerical value when a unit is supplied ?
        if not isinstance(value, Number) and unit:
            raise ValueError("ParameterValue value mus be quantitative (i.e. numeric) if a unit is supplied")
        self.value = value
        self.unit = unit

    @property
    def category(self):
        """:obj:`ProtocolParameter`: a references to the ProtocolParameter the
        value applies to"""
        return self.__category

    @category.setter
    def category(self, val):
        if val is not None and not isinstance(val, ProtocolParameter):
            raise AttributeError('ParameterValue.category must be a ProtocolParameter or None; got {0}:{1}'
                                 .format(val, type(val)))
        self.__category = val

    @property
    def value(self):
        """:obj:`str` or :obj:`int` or :obj:`float`
        or :obj:`OntologyAnnotation`: a parameter value"""
        return self.__value

    @value.setter
    def value(self, val):
        if val is not None and not isinstance(val, (str, int, float, OntologyAnnotation)):
            raise AttributeError('ParameterValue.value must be a string, numeric, an OntologyAnnotation, or None; '
                                 'got {0}:{1}'.format(val, type(val)))
        self.__value = val

    @property
    def unit(self):
        """ :obj:`OntologyAnnotation`: a unit for the parameter value"""
        return self.__unit

    @unit.setter
    def unit(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise AttributeError('ParameterValue.unit must be a OntologyAnnotation, or None; got {0}:{1}'
                                 .format(val, type(val)))
        self.__unit = val

    def __repr__(self):
        return ('isatools.model.ParameterValue(category={category}, value={value}, unit={unit}, comments={comments})'
                ).format(category=repr(self.category),
                         value=repr(self.value),
                         unit=repr(self.unit),
                         comments=repr(self.comments))

    def __str__(self):
        return ("ParameterValue(\n\t"
                "category={category}\n\t"
                "value={value}\n\t"
                "unit={unit}\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(category=self.category.parameter_name.term if self.category else '',
                         value=self.value.term if isinstance(self.value, OntologyAnnotation) else repr(self.value),
                         unit=self.unit.term if self.unit else '',
                         num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ParameterValue) \
               and self.category == other.category \
               and self.value == other.value \
               and self.unit == other.unit \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    #TODO
    # def to_dict(self):

    def to_ld(self, context: str = "obo"):
        if context not in ["obo", "sdo", "wdt"]:
            raise ValueError("context should be obo, sdo or wdt but got %s" % context)

        context_path = get_context_path("parameter_value", context)
        parameter_value = self.to_dict()
        parameter_value["@type"] = "ParameterValue"
        parameter_value["@context"] = context_path
        parameter_value["@id"] = "#parameter_value/" + self.id

    def from_dict(self, parameter_value):
        self.load_comments(parameter_value.get('comments', []))
        self.category = indexes.get_parameter(parameter_value['category']['@id'])
        if isinstance(parameter_value['value'], (float, int)):
            self.value = parameter_value['value']
            self.unit = indexes.get_unit(parameter_value['unit']['@id'])
        else:
            self.value = OntologyAnnotation()
            if isinstance(parameter_value['value'], str):
                self.value.term = parameter_value['value']
            else:
                self.value.from_dict(parameter_value['value'])

