from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import StudyFactor as StudyFactorModel
from isatools.database.models.relationships import study_factors
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class StudyFactor(Base):
    """ The SQLAlchemy model for the StudyFactor table """

    __tablename__: str = 'factor'

    # Base fields
    factor_id: str = Column(String, primary_key=True)
    name: str = Column(String)

    # Relationships back-ref
    studies: relationship = relationship('Study', secondary=study_factors, back_populates='study_factors')

    # Relationships: one-to-many
    comments: relationship = relationship('Comment', back_populates='study_factor')

    # Relationships many-to-one
    factor_type_id: str = Column(String, ForeignKey('ontology_annotation.ontology_annotation_id'))
    factor_type: relationship = relationship('OntologyAnnotation', backref='factor_values')

    def to_json(self):
        return {
            '@id': self.factor_id,
            'factorName': self.name,
            'factorType': self.factor_type.to_json(),
            'comments': [c.to_json() for c in self.comments]
        }


def make_study_factor_methods():
    def to_sql(self, session):
        factor = session.query(StudyFactor).get(self.id)
        if factor:
            return factor
        return StudyFactor(
            factor_id=self.id,
            name=self.name,
            factor_type=self.factor_type.to_sql(session),
            comments=[c.to_sql() for c in self.comments]
        )
    setattr(StudyFactorModel, 'to_sql', to_sql)
    setattr(StudyFactorModel, 'get_table', make_get_table_method(StudyFactor))
