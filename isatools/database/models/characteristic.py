from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship, Session

from isatools.model import Characteristic as CharacteristicModel, OntologyAnnotation as OntologyAnnotationModel
from isatools.database.models.relationships import (
    source_characteristics,
    sample_characteristics,
    materials_characteristics
)
from isatools.database.models.constraints import build_characteristic_constraints
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Characteristic(Base):
    """ The SQLAlchemy model for the Characteristic table """

    __tablename__: str = 'characteristic'
    __table_args__: tuple = (*build_characteristic_constraints(), {"comment": "Characteristic table"})

    # Base fields
    characteristic_id: int = Column(Integer, primary_key=True)
    value_int: float = Column(Float, comment='Characteristic value as a float')
    unit_str: str = Column(String, comment='Characteristic unit as a string')
    category_str: str = Column(String, comment='Characteristic category as a string')

    # Relationships: back-ref
    sources: relationship = relationship('Source', secondary=source_characteristics, back_populates='characteristics')
    samples: relationship = relationship('Sample', secondary=sample_characteristics, back_populates='characteristics')
    materials: relationship = relationship(
        'Material', secondary=materials_characteristics, back_populates='characteristics')

    # Relationships many-to-one
    value_id: str = Column(String, ForeignKey(
        'ontology_annotation.ontology_annotation_id'), comment='Value of the characteristic as an OntologyAnnotation')
    value_oa: relationship = relationship(
        'OntologyAnnotation', backref='characteristics_value', foreign_keys=[value_id])

    unit_id: str = Column(
        String, ForeignKey('ontology_annotation.ontology_annotation_id'),
        comment='Characteristic unit as an ontology annotation')
    unit_oa: relationship = relationship('OntologyAnnotation', backref='characteristics_unit', foreign_keys=[unit_id])

    category_id: str = Column(
        String, ForeignKey('ontology_annotation.ontology_annotation_id'),
        comment='Characteristic category as an ontology annotation')
    category_oa: relationship = relationship(
        'OntologyAnnotation', backref='characteristics_category', foreign_keys=[category_id])

    # Relationships one-to-many
    comments: relationship = relationship('Comment', back_populates='characteristic')

    def to_json(self) -> dict:
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        comments = [c.to_json() for c in self.comments]

        unit = self.unit_str
        if self.unit_oa:
            unit = self.unit_oa.to_json()

        value = self.value_int
        if self.value_oa:
            value = self.value_oa.to_json()

        category = self.category_str
        if self.category_oa:
            category = self.category_oa.to_json()

        return {"value": value, "comments": comments, "unit": unit, "category": category}


def make_characteristic_methods():
    """ This function will dynamically add the methods to the Characteristic class that are required to interact with
    the database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self, session: Session) -> Characteristic:
        """ Convert the Characteristic object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Characteristic object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        characteristic = {"comments": [c.to_sql() for c in self.comments]}
        if isinstance(self.value, int) or isinstance(self.value, float):
            value = self.value
            if isinstance(self.value, int):
                value = float(self.value)
            characteristic["value_int"] = value
        elif not isinstance(self.value, str):
            characteristic["value_oa"] = self.value.to_sql(session)
        else:
            value = OntologyAnnotationModel(term=self.value)
            characteristic["value_oa"] = value.to_sql(session)

        if isinstance(self.unit, str):
            characteristic["unit_str"] = self.unit
        elif self.unit:
            characteristic["unit_id"] = self.unit.id

        if isinstance(self.category, str):
            characteristic["category_str"] = self.category
        else:
            characteristic["category_id"] = self.category.id
        return Characteristic(**characteristic)

    setattr(CharacteristicModel, 'to_sql', to_sql)
    setattr(CharacteristicModel, 'get_table', make_get_table_method(Characteristic))
