from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import StudyFactor as StudyFactorModel
from isatools.database.models.relationships import study_factors
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class StudyFactor(Base):
    __tablename__: str = 'factor'

    # Base fields
    id: str = Column(String, primary_key=True)
    factor_name: str = Column(String)

    # Relationships back-ref
    studies: relationship = relationship(
        'Study', secondary=study_factors, back_populates='study_factors')

    # Relationships: one-to-many
    comments = relationship('Comment', back_populates='study_factor')

    # Relationships many-to-one
    factor_type_id: str = Column(String, ForeignKey('ontology_annotation.id'))
    factor_type: relationship = relationship('OntologyAnnotation', backref='factor_values')

    def to_json(self):
        return {
            '@id': self.id,
            'factorName': self.factor_name,
            'factorType': self.factor_type.to_json(),
            'comments': [c.to_json() for c in self.comments]
        }


def make_factor_values_methods():
    def to_sql(self, session):
        return StudyFactor(
            id=self.id,
            factor_name=self.name,
            factor_type=self.factor_type.to_sql(session),
            comments=[c.to_sql() for c in self.comments]
        )
    setattr(StudyFactorModel, 'to_sql', to_sql)
    setattr(StudyFactorModel, 'get_table', make_get_table_method(StudyFactor))
