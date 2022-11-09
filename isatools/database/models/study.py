from datetime import datetime
import dateutil.parser as date

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import Study as StudyModel
from isatools.database.models.relationships import (
    study_publications,
    study_design_descriptors,
    study_protocols,
    study_sources,
    study_characteristic_categories,
    study_unit_categories
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
    publications: relationship = relationship('Publication', secondary=study_publications, back_populates='studies')
    protocols = relationship('Protocol', secondary=study_protocols, back_populates='studies')
    sources = relationship('Source', secondary=study_sources, back_populates='studies')
    characteristic_categories = relationship(
        'OntologyAnnotation', secondary=study_characteristic_categories, back_populates='characteristic_categories')
    unit_categories = relationship(
        'OntologyAnnotation', secondary=study_unit_categories, back_populates='unit_categories')
    study_design_descriptors = relationship(
        'OntologyAnnotation', secondary=study_design_descriptors, back_populates='design_descriptor')

    # Sample and otherMaterials attributes

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
            'protocols': [p.to_json() for p in self.protocols],
            'characteristicCategories': [oa.to_json() for oa in self.characteristic_categories],
            'unitCategories': [oa.to_json() for oa in self.unit_categories],
            'sources': [s.to_json() for s in self.sources]
        }


def make_study_methods():
    def to_sql(self, session):
        submission_date: datetime or None = None
        public_release_date: datetime or None = None
        if self.submission_date:
            submission_date = date.parse(self.submission_date)
        if self.public_release_date:
            public_release_date = date.parse(self.public_release_date)

        return Study(
            title=self.title,
            description=self.description,
            filename=self.filename,
            identifier=self.identifier,
            submission_date=submission_date,
            public_release_date=public_release_date,
            contacts=[person.to_sql() for person in self.contacts],
            comments=[comment.to_sql() for comment in self.comments],
            publications=[publication.to_sql() for publication in self.publications],
            study_design_descriptors=[descriptor.to_sql(session) for descriptor in self.design_descriptors],
            protocols=[protocol.to_sql(session) for protocol in self.protocols],
            characteristic_categories=[category.to_sql(session) for category in self.characteristic_categories],
            unit_categories=[category.to_sql(session) for category in self.units],
            sources=[source.to_sql(session) for source in self.sources]
        )

    setattr(StudyModel, 'to_sql', to_sql)
    setattr(StudyModel, 'get_table', make_get_table_method(Study))
