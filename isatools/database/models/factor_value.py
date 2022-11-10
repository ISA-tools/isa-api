from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import FactorValue as FactorValueModel
from isatools.database.models.relationships import sample_factor_values
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class FactorValue(Base):
    __tablename__: str = 'factor_value'

    # Base fields
    id: int = Column(Integer, primary_key=True)

    # Relationships back-ref
    samples: relationship = relationship('Sample', secondary=sample_factor_values, back_populates='factor_values')

    # Relationships many-to-one
    factor_name_id: str = Column(String, ForeignKey('factor.id'))
    factor_name: relationship = relationship('StudyFactor', backref='factor_values')

    def to_json(self) -> dict:
        category = ''
        if self.factor_name:
            category = {"@id": self.factor_name.id}
        return {
            'category': category,
        }


def make_factor_value_methods():
    def to_sql(self, session):
        return FactorValue(
            factor_name=self.factor_name.to_sql(session),
        )

    setattr(FactorValueModel, 'to_sql', to_sql)
    setattr(FactorValueModel, 'get_table', make_get_table_method(FactorValue))