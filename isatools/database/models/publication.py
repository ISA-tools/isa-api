from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from isatools.model import Publication as PublicationModel
from isatools.database.models.relationships import investigation_publications, study_publications
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Publication(Base):
    __tablename__: str = 'publication'

    # Base fields
    id: str = Column(String, primary_key=True)
    author_list: str = Column(String, nullable=True)
    doi: str = Column(String, nullable=True)
    pubmed_id: str = Column(String, nullable=True)
    title: str = Column(String, nullable=True)

    # Relationships
    comments: relationship = relationship('Comment', back_populates='publication')

    # Relationships: back-ref
    investigations: relationship = relationship(
        'Investigation', secondary=investigation_publications, back_populates='publications'
    )
    studies: relationship = relationship(
        'Study', secondary=study_publications, back_populates='publications'
    )

    # status = OntologyAnnotation()

    def to_json(self) -> dict:
        return {
            "authorList": self.author_list,
            "doi": self.doi,
            "pubMedID": self.pubmed_id,
            "title": self.title,
            "comments": [comment.to_json() for comment in self.comments]
        }


def make_publication_methods():
    def to_sql(self):
        return Publication(
            id=self.doi,
            author_list=self.author_list,
            doi=self.doi,
            pubmed_id=self.pubmed_id,
            title=self.title,
            comments=[comment.to_sql() for comment in self.comments]
        )

    setattr(PublicationModel, 'to_sql', to_sql)
    setattr(PublicationModel, 'get_table', make_get_table_method(Publication))
