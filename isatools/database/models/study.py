from typing import List
from datetime import datetime
import dateutil.parser as date

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import (
    Study as StudyModel,
    Comment as CommentModel,
    Publication as PublicationModel,
    Person as PersonModel,
    OntologyAnnotation as OntologyAnnotationModel,
    Protocol as ProtocolModel
)
from isatools.database.models.relationships import (
    study_publications,
    study_design_descriptors,
    study_protocols,
)
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


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


def make_study_methods():
    def to_sql(self):
        title: str = self.title
        description: str = self.description
        filename: str = self.filename
        identifier: str = self.identifier
        submission_date: datetime or None = None
        public_release_date: datetime or None = None
        comments: List[CommentModel] = self.comments
        contacts: List[PersonModel] = self.contacts
        publications: List[PublicationModel] = self.publications
        design_descriptors: List[OntologyAnnotationModel] = self.design_descriptors
        protocols: List[ProtocolModel] = self.protocols

        if self.submission_date:
            submission_date = date.parse(self.submission_date)
        if self.public_release_date:
            public_release_date = date.parse(self.public_release_date)

        return Study(
            title=title,
            description=description,
            filename=filename,
            identifier=identifier,
            submission_date=submission_date,
            public_release_date=public_release_date,
            contacts=[person.to_sql() for person in contacts],
            comments=[comment.to_sql() for comment in comments],
            publications=[publication.to_sql() for publication in publications],
            study_design_descriptors=[descriptor.to_sql() for descriptor in design_descriptors],
            protocols=[protocol.to_sql() for protocol in protocols]
        )

    setattr(StudyModel, 'to_sql', to_sql)
    setattr(StudyModel, 'get_table', make_get_table_method(Study))
