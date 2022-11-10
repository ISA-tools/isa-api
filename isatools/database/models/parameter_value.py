from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import ParameterValue as ParameterValueModel
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.database.models.relationships import process_parameter_values
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class ParameterValue(Base):
    __tablename__: str = 'parameter_value'

    # Base fields
    id = Column(Integer, primary_key=True)
    value_int: int = Column(Integer)

    # Relationships: back-ref
    processes_parameter_values: relationship = relationship(
        'Process', secondary=process_parameter_values, back_populates='parameter_values'
    )

    # Relationships many-to-one
    value_id: int = Column(Integer, ForeignKey('ontology_annotation.id'))
    value_oa: relationship = relationship(
        'OntologyAnnotation', backref='parameter_values', foreign_keys=[value_id])
    unit_id: int = Column(Integer, ForeignKey('ontology_annotation.id'))
    unit: relationship = relationship(
        'OntologyAnnotation', backref='parameter_values_unit', foreign_keys=[unit_id])
    category_id: int = Column(Integer, ForeignKey('parameter.id'))
    category: relationship = relationship('Parameter', backref='parameter_values')

    def to_json(self):
        return {
            'value': self.value_int if self.value_int else {"@id": self.value_oa.id},
            'unit': {"@id": self.unit.id} if self.unit else None,
            'category': {"@id": self.category.id} if self.category else ''
        }


def make_parameter_value_methods():
    def to_sql(self, session):
        parameter_value = {
            'unit': self.unit.to_sql(session) if self.unit else None,
            'category_id': self.category.id
        }
        if isinstance(self.value, str):
            parameter_value['value_oa'] = OntologyAnnotation(term=self.value).to_sql()
        elif isinstance(self.value, OntologyAnnotation):
            parameter_value['value_oa'] = self.value
        elif isinstance(self.value, int):
            parameter_value['value_int'] = float(self.value)
        elif isinstance(self.value, float):
            parameter_value['value_int'] = self.value
        return ParameterValue(**parameter_value)

    setattr(ParameterValueModel, 'to_sql', to_sql)
    setattr(ParameterValueModel, 'get_table', make_get_table_method(ParameterValue))
