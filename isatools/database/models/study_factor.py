from typing import Optional
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped

from isatools.database.models.relationships import study_factors
from isatools.database.models.utils import make_get_table_method
from isatools.database.utils import Base
from isatools.model import StudyFactor as StudyFactorModel


class StudyFactor(Base):
    """The SQLAlchemy model for the StudyFactor table"""

    __tablename__: str = "factor"
    __allow_unmapped__ = True
    # Base fields
    factor_id: Mapped[str] = Column(String, primary_key=True)
    name: Mapped[str] = Column(String, nullable=True)

    # Relationships back-ref
    studies: Mapped[list['Study']] = relationship("Study", secondary=study_factors, back_populates="study_factors")

    # Relationships: one-to-many
    comments: Mapped[list['Comment']] = relationship("Comment", back_populates="study_factor")

    # Relationships many-to-one
    factor_type_id: Mapped[Optional[str]] = Column(String, ForeignKey("ontology_annotation.ontology_annotation_id"), nullable=True)
    factor_type: Mapped[Optional['OntologyAnnotation']] = relationship("OntologyAnnotation", backref="factor_values")

    def to_json(self):
        return {
            "@id": self.factor_id,
            "factorName": self.name,
            "factorType": self.factor_type.to_json(),
            "comments": [c.to_json() for c in self.comments],
        }


def make_study_factor_methods():
    def to_sql(self, session):
        factor = session.get(StudyFactor, self.id)
        if factor:
            return factor
        factor = StudyFactor(
            factor_id=self.id,
            name=self.name,
            factor_type=self.factor_type.to_sql(session),
            comments=[c.to_sql() for c in self.comments],
        )

        session.add(factor)
        return factor

    setattr(StudyFactorModel, "to_sql", to_sql)
    setattr(StudyFactorModel, "get_table", make_get_table_method(StudyFactor))
