from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.database.models.relationships import (
    study_publications,
    study_design_descriptors,
    study_protocols,
)
from isatools.database.utils import Base


class Study(Base):
    __tablename__: str = 'study'

    # Base fields
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    identifier: str = Column(String)
    description: str = Column(String)
    filename: str = Column(String)
    submission_date: datetime = Column(String)
    public_release_date: datetime = Column(String)

    # Relationships back reference
    investigation = relationship("Investigation", back_populates="studies")
    investigation_id = Column(Integer, ForeignKey('investigation.id'))

    # Relationships: one-to-many
    process_sequence = relationship("Process", back_populates="study")
    contacts = relationship('Person', back_populates='study')
    comments = relationship('Comment', back_populates='study')

    # Relationships: many-to-many
    publications: relationship = relationship(
        'Publication', secondary=study_publications, back_populates='studies')
    study_design_descriptors = relationship(
        'OntologyAnnotation', secondary=study_design_descriptors, back_populates='studies')
    protocols = relationship(
        'Protocol', secondary=study_protocols, back_populates='studies'
    )

    def to_json(self):
        return {
            'title': self.title,
            "filename": self.filename,
            "identifier": self.identifier,
            "description": self.description,
            "submissionDate": self.submission_date,
            "publicReleaseDate": self.public_release_date,
            'people': [p.to_json() for p in self.contacts],
            'comments': [c.to_json() for c in self.comments],
            'publications': [p.to_json() for p in self.publications],
            'designDescriptors': [oa.to_json() for oa in self.study_design_descriptors],
            'protocols': [p.to_json() for p in self.protocols]
        }
