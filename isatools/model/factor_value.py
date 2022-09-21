import os

from uuid import uuid4
from isatools.model.comments import Commentable
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.identifiable import Identifiable
from isatools.model.parameter_value import ParameterValue
from isatools.model.loader_indexes import loader_states as indexes
from isatools.model.utils import get_context_path


class FactorValue(Commentable):
    """A FactorValue represents the value instance of a StudyFactor.

    Attributes:
        factor_name: Reference to an instance of a relevant StudyFactor.
        value: The value of the factor at hand.
        unit: str/OntologyAnnotation. If numeric, the unit qualifier for the value. (?? what does this mean ??)
        comments: Comments associated with instances of this class.
    """

    def __init__(self, factor_name=None, value=None, unit=None, comments=None):
        super().__init__(comments)
        self.__factor_name = None
        self.__value = None
        self.__unit = None
        self.factor_name = factor_name
        self.value = value
        self.unit = unit

    @property
    def factor_name(self):
        """:obj:`StudyFactor`: a references to the StudyFactor the
        value applies to"""
        return self.__factor_name

    @factor_name.setter
    def factor_name(self, val):
        if val is not None and not isinstance(val, StudyFactor):
            raise AttributeError('FactorValue.factor_name must be a StudyFactor or None; got {0}:{1}'
                                 .format(val, type(val)))
        self.__factor_name = val

    @property
    def value(self):
        """:obj:`str` or :obj:`int` or :obj:`float`
        or :obj:`OntologyAnnotation`: a parameter value"""
        return self.__value

    @value.setter
    def value(self, val):
        if val is not None and not isinstance(val, (str, int, float, OntologyAnnotation)):
            raise AttributeError('FactorValue.value must be a string, numeric, an OntologyAnnotation, or None; '
                                 'got {0}:{1}'.format(val, type(val)))
        self.__value = val

    @property
    def unit(self):
        """ :obj:`OntologyAnnotation`: a unit for the parameter value"""
        return self.__unit

    @unit.setter
    def unit(self, val):
        # FIXME can this be a string as well?
        if val is not None and not isinstance(val, (OntologyAnnotation, str)):
            raise AttributeError(
                'FactorValue.unit must be an OntologyAnnotation, o string, or None; '
                'got {0}:{1}'.format(val, type(val)))
        self.__unit = val

    def __repr__(self):
        return ("isatools.model.FactorValue(factor_name={factor_name}, value={value}, unit={unit})"
                ).format(factor_name=repr(self.factor_name), value=repr(self.value), unit=repr(self.unit))

    def __str__(self):
        return ("FactorValue(\n\t"
                "factor_name={factor_name}\n\t"
                "value={value}\n\t"
                "unit={unit}\n)"
                ).format(factor_name=self.factor_name.name if self.factor_name else '',
                         value=self.value.term if isinstance(self.value, OntologyAnnotation) else repr(self.value),
                         unit=self.unit.term if self.unit else '')

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, FactorValue) \
               and self.factor_name == other.factor_name \
               and self.value == other.value \
               and self.unit == other.unit

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        category = ''
        if self.factor_name:
            category = {"@id": self.factor_name.id}

        value = self.value if self.value else ''
        if isinstance(value, OntologyAnnotation):
            value = value.to_dict()

        factor_value = {'category': category, 'value': value}

        if self.unit:
            id_ = '#unit/' + str(uuid4())
            if isinstance(self.unit, OntologyAnnotation):
                id_ = self.unit.id.replace('#ontology_annotation/', '#unit/')
            factor_value['unit'] = {"@id": id_}

        return factor_value

    def to_ld(self, context: str = "obo"):
        if context not in ["obo", "sdo", "wdt"]:
            raise ValueError("context should be obo, sdo or wdt but got %s" % context)

        context_path = get_context_path("factor_value", context)
        factor_value = self.to_dict()
        factor_value["@type"] = "FactorValue"
        factor_value["@context"] = context_path
        factor_value["@id"] = "#factor_value/" + self.id

    def from_dict(self, factor_value):
        self.factor_name = indexes.get_factor(factor_value["category"]["@id"])
        self.load_comments(factor_value.get('comments', []))

        value_data = factor_value.get('value', None)
        if value_data:
            if isinstance(value_data, dict):
                value = OntologyAnnotation()
                value.from_dict(value_data)
                self.value = value
            elif isinstance(value_data, (int, float)):
                try:
                    self.unit = indexes.get_unit(factor_value['unit']['@id'])
                except KeyError:
                    self.unit = None
                self.value = value_data
            elif not isinstance(value_data, str):
                raise IOError("Unexpected type in factor value")
            else:
                self.value = value_data
                self.unit = None


class StudyFactor(Commentable, Identifiable):
    """A Study Factor corresponds to an independent variable manipulated by the
    experimentalist with the intention to affect biological systems in a way
    that can be measured by an assay.

    Attributes:
        name: Study factor name
        factor_type: An ontology source reference of the study factor type
        comments: Comments associated with instances of this class.
    """

    def __init__(self, id_='', name='', factor_type=None, comments=None):
        super().__init__(comments=comments)

        self.id = id_
        self.__name = name

        # factor type can be initialized as a string but shouldn't
        self.__factor_type = OntologyAnnotation() if factor_type is None else factor_type

    @property
    def name(self):
        """:obj:`str`: the name of the study factor"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('StudyFactor.name must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__name = val

    @property
    def factor_type(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        study factor type"""
        return self.__factor_type

    @factor_type.setter
    def factor_type(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise AttributeError('StudyFactor.factor_type must be a OntologyAnnotation or None; got {0}:{1}'
                                 .format(val, type(val)))
        self.__factor_type = val

    def __repr__(self):
        return ("isatools.model.StudyFactor(name='{study_factor.name}', "
                "factor_type={factor_type}, comments={study_factor.comments})"
                ).format(study_factor=self, factor_type=repr(self.factor_type))

    def __str__(self):
        return ("StudyFactor(\n\t"
                "name={factor.name}\n\t"
                "factor_type={factor_type}\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(factor=self,
                         factor_type=self.factor_type.term if self.factor_type else '',
                         num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, StudyFactor) \
               and self.name == other.name \
               and self.factor_type == other.factor_type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {
            '@id': self.id,
            'factorName': self.name,
            'factorType': self.factor_type.to_dict() if self.factor_type else '',
            'comments': [comment.to_dict() for comment in self.comments]
        }

    def to_ld(self, context: str = "obo"):
        if context not in ["obo", "sdo", "wdt"]:
            raise ValueError("context should be obo, sdo or wdt but got %s" % context)

        context_path = get_context_path("factor", context)
        factor = self.to_dict()
        factor["@type"] = "Factor"
        factor["@context"] = context_path
        factor["@id"] = "#studyfactor/" + self.id

    def from_dict(self, factor):
        self.id = factor.get('@id', '')
        self.name = factor.get('factorName', '')
        self.load_comments(factor.get('comments', []))

        # factor type
        factor_type_data = factor.get('factorType', None)
        if factor_type_data:
            factor_type = OntologyAnnotation()
            factor_type.from_dict(factor_type_data)
            self.factor_type = factor_type
