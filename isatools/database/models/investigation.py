from typing import List
from datetime import datetime
import dateutil.parser as date

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from isatools.model import (
    Investigation as InvestigationModel,
    Comment as CommentModel,
    Study as StudyModel,
    Person as PersonModel,
    Publication as PublicationModel,
    OntologySource as OntologySourceModel

)
from isatools.database.models.relationships import investigation_publications, investigation_ontology_source
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


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


def make_investigation_methods() -> None:
    def to_sql(self) -> dict:
        identifier: str = self.identifier
        isa_identifier: str = self.id
        title: str = self.title
        description: str = self.description
        submission_date: datetime or None = None
        publication_date: datetime or None = None
        comments: List[CommentModel] = self.comments
        studies: List[StudyModel] = self.studies
        contacts: List[PersonModel] = self.contacts
        publications: List[PublicationModel] = self.publications
        ontology_source_references: List[OntologySourceModel] = self.ontology_source_references

        if self.submission_date:
            submission_date = date.parse(self.submission_date)
        if self.public_release_date:
            publication_date = date.parse(self.public_release_date)

        investigation: Investigation = Investigation(
            isa_identifier=isa_identifier, identifier=identifier, title=title, description=description,
            submission_date=submission_date, public_release_date=publication_date,
            comments=[comment.to_sql() for comment in comments],
            studies=[study.to_sql() for study in studies],
            contacts=[person.to_sql() for person in contacts],
            publications=[publication.to_sql() for publication in publications],
            ontology_source_reference=[ontology_source.to_sql() for ontology_source in ontology_source_references]
        )

        return investigation

    setattr(InvestigationModel, 'to_sql', to_sql)
    setattr(InvestigationModel, 'get_table', make_get_table_method(Investigation))
