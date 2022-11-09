from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from isatools.model import Characteristic as CharacteristicModel
from isatools.database.models.relationships import source_characteristics
from isatools.database.models.constraints import build_characteristic_constraints
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Characteristic(Base):
    __tablename__: str = 'characteristic'
    __table_args__ = build_characteristic_constraints()

    # Base fields
    id: int = Column(Integer, primary_key=True)
    value_int: float = Column(Float)
    unit_str: str = Column(String)
    category_str: str = Column(String)

    # Relationships: back-ref
    sources: relationship = relationship(
        'Source', secondary=source_characteristics, back_populates='characteristics'
    )

    # Relationships many-to-one
    value_id: int = Column(Integer, ForeignKey('ontology_annotation.id'))
    value_oa: relationship = relationship(
        'OntologyAnnotation', backref='characteristics_value', foreign_keys=[value_id]
    )
    unit_id: int = Column(Integer, ForeignKey('ontology_annotation.id'))
    unit_oa: relationship = relationship('OntologyAnnotation', backref='characteristics_unit', foreign_keys=[unit_id])
    category_id = Column(Integer, ForeignKey('ontology_annotation.id'))
    category_oa = relationship('OntologyAnnotation', backref='characteristics_category', foreign_keys=[category_id])

    # Relationships one-to-many
    comments = relationship('Comment', back_populates='characteristic')

    def to_json(self) -> dict:
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
    def to_sql(self, session):
        characteristic = {"comments": [c.to_sql() for c in self.comments]}

        if isinstance(self.value, int) or isinstance(self.value, float):
            value = self.value
            if isinstance(self.value, int):
                value = float(self.value)
            characteristic["value_int"] = value
        else:
            characteristic["value_oa"] = self.value.to_sql(session)

        if isinstance(self.unit, str):
            characteristic["unit_str"] = self.unit
        elif self.unit:
            characteristic["unit_oa"] = self.unit.to_sql(session)

        if isinstance(self.category, str):
            characteristic["category_str"] = self.category
        else:
            characteristic["category_oa"] = self.category.to_sql(session)
        return Characteristic(**characteristic)

    setattr(CharacteristicModel, 'to_sql', to_sql)
    setattr(CharacteristicModel, 'get_table', make_get_table_method(Characteristic))
