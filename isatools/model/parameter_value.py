from numbers import Number
from isatools.model.comments import Commentable
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.protocol import ProtocolParameter


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
            raise AttributeError(
                'ParameterValue.category must be a ProtocolParameter '
                'or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__category = val

    @property
    def value(self):
        """:obj:`str` or :obj:`int` or :obj:`float`
        or :obj:`OntologyAnnotation`: a parameter value"""
        return self.__value

    @value.setter
    def value(self, val):
        if val is not None \
                and not isinstance(val, (str, int, float, OntologyAnnotation)):
            raise AttributeError(
                'ParameterValue.value must be a string, numeric, an '
                'OntologyAnnotation, or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__value = val

    @property
    def unit(self):
        """ :obj:`OntologyAnnotation`: a unit for the parameter value"""
        return self.__unit

    @unit.setter
    def unit(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise AttributeError(
                'ParameterValue.unit must be a OntologyAnnotation, or None; '
                'got {0}:{1}'.format(val, type(val)))
        else:
            self.__unit = val

    def __repr__(self):
        return 'isatools.model.ParameterValue(category={category}, ' \
               'value={value}, unit={unit}, comments={comments})'.format(
            category=repr(self.category), value=repr(self.value),
            unit=repr(self.unit), comments=repr(self.comments))

    def __str__(self):
        return """ParameterValue(
    category={category}
    value={value}
    unit={unit}
    comments={num_comments} Comment objects
)""".format(category=self.category.parameter_name.term
        if self.category else '',
            value=self.value.term if isinstance(
                self.value, OntologyAnnotation
            ) else repr(self.value),
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
