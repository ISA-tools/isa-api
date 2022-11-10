from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from isatools.model import OntologyAnnotation as OntologyAnnotationModel
from isatools.database.models.relationships import (
    study_design_descriptors,
    study_characteristic_categories,
    study_unit_categories
)
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class OntologyAnnotation(Base):
    __tablename__: str = 'ontology_annotation'

    id: str = Column(String, primary_key=True)
    annotation_value: str = Column(String)
    term_accession: str = Column(String)

    # Relationships back-ref
    design_descriptors: relationship = relationship(
        'Study', secondary=study_design_descriptors, back_populates='study_design_descriptors')
    characteristic_categories = relationship(
        'Study', secondary=study_characteristic_categories, back_populates='characteristic_categories')
    unit_categories = relationship(
        'Study', secondary=study_unit_categories, back_populates='unit_categories')

    # Relationships many-to-one
    term_source_id: int = Column(Integer, ForeignKey('ontology_source.id'))
    term_source: relationship = relationship('OntologySource', backref='ontology_annotations')

    # References: one-to-many
    comments = relationship('Comment', back_populates='ontology_annotation')

    def to_json(self):
        return {
            'annotationValue': self.annotation_value,
            'termSource': {"@id": self.term_source_id} if self.term_source_id else None,
            'termAccession': self.term_accession,
            'comments': [c.to_json() for c in self.comments]
        }


def make_ontology_annotation_methods() -> None:
    def to_sql(self, session):
        oa = session.query(OntologyAnnotation).get(self.id)
        if oa:
            return oa
        oa = OntologyAnnotation(
            id=self.id,
            annotation_value=self.term,
            term_accession=self.term_accession,
            term_source_id=self.term_source.name if self.term_source else None,
            comments=[comment.to_sql() for comment in self.comments]
        )
        session.add(oa)
        return oa
    setattr(OntologyAnnotationModel, 'to_sql', to_sql)
    setattr(OntologyAnnotationModel, 'get_table', make_get_table_method(OntologyAnnotation))