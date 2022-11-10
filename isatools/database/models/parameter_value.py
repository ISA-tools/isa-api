from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from isatools.model import ParameterValue as ParameterValueModel
from isatools.database.models.relationships import process_parameter_values
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class ParameterValue(Base):
    __tablename__: str = 'parameter_value'

    # Base fields
    id = Column(Integer, primary_key=True)

    # Relationships: back-ref
    processes_parameter_values: relationship = relationship(
        'Process', secondary=process_parameter_values, back_populates='parameter_values'
    )

    def to_json(self):
        return {
            'id': self.id
        }


def make_parameter_value_methods():
    def to_sql(self, session):
        return ParameterValue()

    setattr(ParameterValueModel, 'to_sql', to_sql)
    setattr(ParameterValueModel, 'get_table', make_get_table_method(ParameterValue))
