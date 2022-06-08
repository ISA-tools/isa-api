# Mapped TO material_attribute_value_schema.json

from __future__ import annotations

from typing import List
from uuid import uuid4

from isatools.model.comments import Commentable, Comment
from isatools.model.ontology_annotation import OntologyAnnotation


class Characteristic(Commentable):
    """A Characteristic acts as a qualifying property to a material object.

    Attributes:
        category: The classifier of the type of characteristic being described.
        value: The value of this instance of a characteristic as relevant to
            the attached material.
        unit: If applicable, a unit qualifier for the value (if the value is
            numeric).
        """

    def __init__(self, category=None, value=None, unit=None, comments: List[Comment] = None):

        super().__init__(comments)
        self.__category = None
        self.__value = None
        self.__unit = None

        if category is not None:
            self.category = category
        self.value = value
        self.unit = unit

    @property
    def category(self) -> OntologyAnnotation:
        """ :obj:`OntologyAnnotation`: a category for the characteristic
        component"""
        return self.__category

    @category.setter
    def category(self, val: OntologyAnnotation | str | None):
        if isinstance(val, OntologyAnnotation) or val is None:
            self.__category = val
        elif isinstance(val, str):
            self.__category = OntologyAnnotation(term=val)
        else:
            error_msg = 'Characteristic.category must be either a string ot an OntologyAnnotation, or None; got {0}:{1}'
            error_msg = error_msg.format(val, type(val))
            raise AttributeError(error_msg)

    @property
    def value(self):
        """:obj:`str` or :obj:`int` or :obj:`float`
        or :obj:`OntologyAnnotation`: a characteristic value"""
        return self.__value

    @value.setter
    def value(self, val: str | int | float | OntologyAnnotation | None):
        if val is not None and not isinstance(val, (str, int, float, OntologyAnnotation)):
            error_msg = 'Characteristic.value must be a string, numeric, an OntologyAnnotation, or None; got {0}:{1}'
            error_msg = error_msg.format(val, type(val))
            raise AttributeError(error_msg)
        self.__value = val

    @property
    def unit(self):
        """ :obj:`OntologyAnnotation`: a unit for the characteristic value"""
        return self.__unit

    @unit.setter
    def unit(self, val: OntologyAnnotation | str | None):
        if val is not None and not isinstance(val, (str, OntologyAnnotation)):
            error_msg = 'Characteristic.unit must be either a string ot an OntologyAnnotation, or None; got {0}:{1}'
            error_msg = error_msg.format(val, type(val))
            raise AttributeError(error_msg)
        self.__unit = val

    def __repr__(self):
        return ('isatools.model.Characteristic('
                'category={category}, value={value}, unit={unit}, comments={characteristic.comments})'
                ).format(characteristic=self,
                         category=repr(self.category),
                         value=repr(self.value),
                         unit=repr(self.unit))

    def __str__(self):
        value = self.value if isinstance(self.value, OntologyAnnotation) \
            else self.value if self.value is not None \
            else ''
        unit = self.unit.term if isinstance(self.unit, OntologyAnnotation) \
            else self.unit if self.unit is not None \
            else ''
        return ("Characteristic(\n\t"
                "category={category}\n\t"
                "value={value}\n\t"
                "unit={unit}\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(characteristic=self,
                         category=self.category.term if isinstance(self.category, OntologyAnnotation) else '',
                         value=value,
                         unit=unit,
                         num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Characteristic) \
               and self.category == other.category \
               and self.value == other.value \
               and self.unit == other.unit \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


    def to_dict(self):
        category = ''
        if self.category:
            category = {"@id": self.category.id.replace('#ontology_annotation/', '#characteristic_category/')}
        characteristic = {
            "category": category,
            "value": self.value.to_dict() if isinstance(self.value, OntologyAnnotation) else self.value,
            "comments": [comment.to_dict() for comment in self.comments]
        }
        if self.unit:
            id_ = "#unit/" + str(uuid4())
            if isinstance(self.unit, OntologyAnnotation):
                id_ = self.unit.id.replace('#ontology_annotation/', '#unit/')
            characteristic['unit'] = {"@id": id_}
        return characteristic

    def from_dict(self, characteristic):
        self.category =