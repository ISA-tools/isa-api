from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from isatools.database.models.relationships import study_design_descriptors
from isatools.database.utils import Base


class OntologyAnnotation(Base):
    __tablename__: str = 'ontology_annotation'

    id: str = Column(String, primary_key=True)
    annotation_value: str = Column(String)
    term_accession: str = Column(String)

    # Relationships back-ref
    studies: relationship = relationship(
        'Study', secondary=study_design_descriptors, back_populates='study_design_descriptors'
    )

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
