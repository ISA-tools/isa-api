from datetime import datetime
import dateutil.parser as date

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship, Session

from isatools.model import Investigation as InvestigationModel
from isatools.database.models.relationships import investigation_publications, investigation_ontology_source
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Investigation(Base):
    """ The SQLAlchemy model for the Investigation table """

    __tablename__: str = 'investigation'

    # Base fields
    investigation_id: int = Column(Integer, primary_key=True)
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
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            'id': self.isa_identifier,
            'identifier': self.identifier,
            'title': self.title,
            'description': self.description,
            'submissionDate': str(self.submission_date) if self.submission_date else '',
            'publicReleaseDate': str(self.public_release_date) if self.public_release_date else '',
            'studies': [s.to_json() for s in self.studies],
            'comments': [c.to_json() for c in self.comments],
            'people': [p.to_json() for p in self.contacts],
            'publications': [p.to_json() for p in self.publications],
            'ontologySourceReferences': [osr.to_json() for osr in self.ontology_source_reference]
        }


def make_investigation_methods() -> None:
    """ This function will dynamically add the methods to the Investigation class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self, session: Session) -> Investigation:
        """ Convert the Investigation object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Investigation object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be added and committed to the database session.
        """
        submission_date: datetime or None = None
        if self.submission_date:
            submission_date = date.parse(self.submission_date)

        publication_date: datetime or None = None
        if self.public_release_date:
            publication_date = date.parse(self.public_release_date)

        return Investigation(
            isa_identifier=self.id, identifier=self.identifier, title=self.title, description=self.description,
            submission_date=submission_date, public_release_date=publication_date,
            comments=[comment.to_sql() for comment in self.comments],
            studies=[study.to_sql(session) for study in self.studies],
            contacts=[person.to_sql(session) for person in self.contacts],
            publications=[publication.to_sql(session) for publication in self.publications],
            ontology_source_reference=[
                ontology_source.to_sql(session) for ontology_source in self.ontology_source_references
            ]
        )

    setattr(InvestigationModel, 'to_sql', to_sql)
    setattr(InvestigationModel, 'get_table', make_get_table_method(Investigation))
