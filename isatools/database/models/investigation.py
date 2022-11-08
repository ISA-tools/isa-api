from datetime import datetime

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from isatools.database.models.relationships import investigation_publications, investigation_ontology_source
from isatools.database.utils import Base


class Investigation(Base):
    __tablename__: str = 'investigation'

    # Base fields
    id: int = Column(Integer, primary_key=True)
    isa_identifier: str = Column(String, nullable=False)
    identifier: str = Column(String, nullable=False)
    title: str = Column(String, nullable=True)
    description: str = Column(String, nullable=True)
    submission_date: datetime or None = Column(Date, nullable=True)
    public_release_date: datetime or None = Column(Date, nullable=True)

    # Relationships: one-to-many
    studies: relationship = relationship('Study', back_populates="investigation")
    comments: relationship = relationship('Comment', back_populates='investigation')
    contacts: relationship = relationship('Person', back_populates='investigation')

    # Relationships: many-to-many
    publications: relationship = relationship(
        'Publication', secondary=investigation_publications, back_populates='investigations'
    )
    ontology_source_reference: relationship = relationship(
        'OntologySource', secondary=investigation_ontology_source, back_populates='investigations'
    )

    def to_json(self) -> dict:
        return {
            '@id': self.id,
            'id': self.isa_identifier,
            'identifier': str(self.identifier),
            'title': str(self.title),
            'description': str(self.description),
            'submissionDate': str(self.submission_date),
            'publicReleaseDate': str(self.public_release_date),
            'studies': [s.to_json() for s in self.studies],
            'comments': [c.to_json() for c in self.comments],
            'people': [p.to_json() for p in self.contacts],
            'publications': [p.to_json() for p in self.publications],
            'ontologySourceReferences': [osr.to_json() for osr in self.ontology_source_reference]
        }






