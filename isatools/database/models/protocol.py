from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.database.models.relationships import study_protocols, protocol_parameters
from isatools.database.utils import Base


class Protocol(Base):
    __tablename__: str = 'protocol'

    # Base fields
    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    description: str = Column(String)
    uri: str = Column(String)
    version: str = Column(String)

    # Relationships back-ref
    studies: relationship = relationship('Study', secondary=study_protocols, back_populates='protocols')

    # References: one-to-many
    comments = relationship('Comment', back_populates='protocol')

    # Relationships: many-to-many
    protocol_parameters: relationship = relationship(
        'Parameter', secondary=protocol_parameters, back_populates='protocols')

    # Relationships many-to-one
    protocol_type_id: int = Column(Integer, ForeignKey('ontology_annotation.id'))
    protocol_type: relationship = relationship('OntologyAnnotation', backref='protocols')

    def to_json(self) -> dict:
        return {
            '@id': self.id,
            'name': self.name,
            'description': self.description,
            'uri': self.uri,
            'version': self.version,
            'comments': [c.to_json() for c in self.comments],
            'parameters': [p.to_json() for p in self.protocol_parameters],
            'protocolType': self.protocol_type.to_json() if self.protocol_type else None,
            'components': []
        }
