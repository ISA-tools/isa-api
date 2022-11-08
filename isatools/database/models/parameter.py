from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.database.models.relationships import protocol_parameters
from isatools.database.utils import Base


class Parameter(Base):
    __tablename__: str = 'parameter'

    # Base fields
    id: str = Column(String, primary_key=True)

    # Relationships many-to-one
    ontology_annotation_id: str = Column(String, ForeignKey('ontology_annotation.id'))
    ontology_annotation: relationship = relationship('OntologyAnnotation', backref='parameters')

    # Relationships back-ref
    protocols: relationship = relationship(
        'Protocol', secondary=protocol_parameters, back_populates='protocol_parameters')

    def to_json(self):
        return {
            "@id": self.id,
            "parameterName": self.ontology_annotation.to_json() if self.ontology_annotation else None
        }

