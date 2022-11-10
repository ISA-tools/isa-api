from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import FactorValue as FactorValueModel
from isatools.database.models.relationships import sample_factor_values
from isatools.database.utils import Base
from isatools.database.models.constraints import build_factor_value_constraints
from isatools.database.models.utils import make_get_table_method


class FactorValue(Base):
    __tablename__: str = 'factor_value'
    __table_args__: tuple = (build_factor_value_constraints(), )

    # Base fields
    id: int = Column(Integer, primary_key=True)
    value_int: int = Column(Integer)
    value_str: str = Column(String)

    # Relationships back-ref
    samples: relationship = relationship('Sample', secondary=sample_factor_values, back_populates='factor_values')

    # Relationships many-to-one
    factor_name_id: str = Column(String, ForeignKey('factor.id'))
    factor_name: relationship = relationship('StudyFactor', backref='factor_values_names')
    value_oa_id: str = Column(String, ForeignKey('ontology_annotation.id'))
    value_oa: relationship = relationship(
        'OntologyAnnotation', backref='factor_values_values', foreign_keys=[value_oa_id]
    )
    factor_unit_id: str = Column(String, ForeignKey('ontology_annotation.id'))
    factor_unit: relationship = relationship(
        'OntologyAnnotation', backref='factor_values_units', foreign_keys=[factor_unit_id]
    )

    # Relationship one-to-many
    comments = relationship('Comment', back_populates='factor_value')

    def to_json(self) -> dict:
        category = ''
        unit = None
        if self.value_int:
            value = self.value_int
        elif self.value_str:
            value = self.value_str
        else:
            value = self.value_oa.to_json()
        if self.factor_name:
            category = {"@id": self.factor_name.id}
        if self.factor_unit:
            unit = {"@id": self.factor_unit.id}
        return {'category': category, "value": value, "unit": unit, "comments": [c.to_json() for c in self.comments]}


def make_factor_value_methods():
    def to_sql(self, session):
        factor_value = {
            'factor_name': self.factor_name.to_sql(session),
            'comments': [comment.to_sql(session) for comment in self.comments]
        }
        value = self.value if self.value else ''
        if isinstance(value, int):
            factor_value['value_int'] = value
        elif isinstance(value, str):
            factor_value['value_str'] = value
        else:
            factor_value['value_oa'] = value.to_sql(session)
        if self.unit:
            factor_value['factor_unit'] = self.unit.to_sql(session)
        return FactorValue(**factor_value)

    setattr(FactorValueModel, 'to_sql', to_sql)
    setattr(FactorValueModel, 'get_table', make_get_table_method(FactorValue))