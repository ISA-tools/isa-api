from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.database.models.relationships import investigation_ontology_source
from isatools.database.utils import Base


class OntologySource(Base):
    __tablename__: str = 'ontology_source'

    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    file: str = Column(String)
    version: str = Column(String)
    description: str = Column(String)

    # Back references
    investigations: relationship = relationship(
        'Investigation', secondary=investigation_ontology_source, back_populates='ontology_source_reference'
    )

    # References: one-to-many
    comments = relationship('Comment', back_populates='ontology_source')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'file': self.file,
            'version': self.version,
            'description': self.description,
            'comments': [c.to_json() for c in self.comments]
        }