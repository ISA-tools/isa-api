from datetime import datetime
import dateutil.parser as date

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

from isatools.model import Study as StudyModel
from isatools.database.models.utils import get_characteristic_categories
from isatools.database.models.relationships import (
    study_publications,
    study_design_descriptors,
    study_protocols,
    study_sources,
    study_characteristic_categories,
    study_unit_categories,
    study_factors, study_samples, study_materials,
    study_assays
)
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Study(Base):
    """ The SQLAlchemy model for the Study table """

    __tablename__: str = 'study'

    # Base fields
    study_id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    identifier: str = Column(String)
    description: str = Column(String)
    filename: str = Column(String)
    submission_date: datetime = Column(String)
    public_release_date: datetime = Column(String)

    # Relationships back reference
    investigation: relationship = relationship("Investigation", back_populates="studies")
    investigation_id: int = Column(Integer, ForeignKey('investigation.investigation_id'))

    # Relationships: one-to-many
    process_sequence: relationship = relationship("Process", back_populates="study")
    contacts: relationship = relationship('Person', back_populates='study')
    comments: relationship = relationship('Comment', back_populates='study')

    # Relationships: many-to-many
    publications: relationship = relationship('Publication', secondary=study_publications, back_populates='studies')
    protocols: relationship = relationship('Protocol', secondary=study_protocols, back_populates='studies')
    characteristic_categories: relationship = relationship(
        'OntologyAnnotation', secondary=study_characteristic_categories, back_populates='characteristic_categories')
    unit_categories: relationship = relationship(
        'OntologyAnnotation', secondary=study_unit_categories, back_populates='unit_categories')
    study_design_descriptors: relationship = relationship(
        'OntologyAnnotation', secondary=study_design_descriptors, back_populates='design_descriptors')
    study_factors: relationship = relationship('StudyFactor', secondary=study_factors, back_populates='studies')
    sources: relationship = relationship('Source', secondary=study_sources, back_populates='studies')
    samples: relationship = relationship('Sample', secondary=study_samples, back_populates='studies')
    materials: relationship = relationship('Material', secondary=study_materials, back_populates='studies')
    assays: relationship = relationship('Assay', secondary=study_assays, back_populates='studies')

    def to_json(self) -> dict:
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        characteristics_categories = get_characteristic_categories(self.characteristic_categories)
        return {
            'title': self.title,
            'filename': self.filename,
            'identifier': self.identifier,
            'description': self.description,
            'submissionDate': self.submission_date,
            'publicReleaseDate': self.public_release_date,
            'people': [p.to_json() for p in self.contacts],
            'comments': [c.to_json() for c in self.comments],
            'publications': [p.to_json() for p in self.publications],
            'studyDesignDescriptors': [oa.to_json() for oa in self.study_design_descriptors],
            'protocols': [p.to_json() for p in self.protocols],
            'characteristicCategories': characteristics_categories,
            'unitCategories': [oa.to_json() for oa in self.unit_categories],
            'factors': [fv.to_json() for fv in self.study_factors],
            'materials': {
                'sources': [s.to_json() for s in self.sources],
                'samples': [s.to_json() for s in self.samples],
                'otherMaterials': [m.to_json() for m in self.materials],
            },
            'processSequence': [p.to_json() for p in self.process_sequence],
            "assays": [assay.to_json() for assay in self.assays]
        }


def make_study_methods():
    """ This function will dynamically add the methods to the Study class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self, session: Session) -> Study:
        """ Convert the Study object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Study object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
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
            contacts=[person.to_sql(session) for person in self.contacts],
            comments=[comment.to_sql() for comment in self.comments],
            publications=[publication.to_sql(session) for publication in self.publications],
            study_design_descriptors=[descriptor.to_sql(session) for descriptor in self.design_descriptors],
            protocols=[protocol.to_sql(session) for protocol in self.protocols],
            characteristic_categories=[category.to_sql(session) for category in self.characteristic_categories],
            unit_categories=[category.to_sql(session) for category in self.units],
            study_factors=[factor.to_sql(session) for factor in self.factors],
            sources=[source.to_sql(session) for source in self.sources],
            samples=[sample.to_sql(session) for sample in self.samples],
            materials=[material.to_sql(session) for material in self.other_material],
            process_sequence=[process.to_sql(session) for process in self.process_sequence],
            assays=[assay.to_sql(session) for assay in self.assays]
        )

    setattr(StudyModel, 'to_sql', to_sql)
    setattr(StudyModel, 'get_table', make_get_table_method(Study))
