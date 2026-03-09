from datetime import datetime
from typing import Optional

import dateutil.parser as date
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, Session, relationship

from isatools.database.models.relationships import (
    study_assays,
    study_characteristic_categories,
    study_design_descriptors,
    study_factors,
    study_materials,
    study_protocols,
    study_publications,
    study_samples,
    study_sources,
    study_unit_categories,
)
from isatools.database.models.utils import get_characteristic_categories, make_get_table_method
from isatools.database.utils import Base
from isatools.model import Study as StudyModel


class Study(Base):
    """The SQLAlchemy model for the Study table"""

    __tablename__: str = "study"
    __allow_unmapped__ = True

    # Base fields
    study_id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[Optional[str]] = Column(String, nullable=True)
    identifier: Mapped[Optional[str]] = Column(String, nullable=True)
    description: Mapped[Optional[str]] = Column(String, nullable=True)
    filename: Mapped[Optional[str]] = Column(String, nullable=True)
    submission_date: Mapped[Date] or None = Column(Date, nullable=True)
    public_release_date: Mapped[Date] or None = Column(Date, nullable=True)

    # Relationships back reference
    investigation: Mapped[Optional["Investigation"]] = relationship("Investigation", back_populates="studies")
    investigation_id: Mapped[int] = Column(Integer, ForeignKey("investigation.investigation_id"), nullable=True)

    # Relationships: one-to-many
    process_sequence: Mapped[list["Process"]] = relationship("Process", back_populates="study")
    contacts: Mapped[list["Person"]] = relationship("Person", back_populates="study")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="study")

    # Relationships: many-to-many
    publications: Mapped[list["Publication"]] = relationship(
        "Publication", secondary=study_publications, back_populates="studies"
    )
    protocols: Mapped[list["Protocol"]] = relationship("Protocol", secondary=study_protocols, back_populates="studies")
    characteristic_categories: Mapped[list["OntologyAnnotation"]] = relationship(
        "OntologyAnnotation", secondary=study_characteristic_categories, back_populates="characteristic_categories"
    )
    unit_categories: Mapped[list["OntologyAnnotation"]] = relationship(
        "OntologyAnnotation", secondary=study_unit_categories, back_populates="unit_categories"
    )
    study_design_descriptors: Mapped[list["OntologyAnnotation"]] = relationship(
        "OntologyAnnotation", secondary=study_design_descriptors, back_populates="design_descriptors"
    )
    study_factors: Mapped[list["StudyFactor"]] = relationship(
        "StudyFactor", secondary=study_factors, back_populates="studies"
    )
    sources: Mapped[list["Source"]] = relationship("Source", secondary=study_sources, back_populates="studies")
    samples: Mapped[list["Sample"]] = relationship("Sample", secondary=study_samples, back_populates="studies")
    materials: Mapped[list["Material"]] = relationship("Material", secondary=study_materials, back_populates="studies")
    assays: Mapped[list["Assay"]] = relationship("Assay", secondary=study_assays, back_populates="studies")

    def to_json(self) -> dict:
        """Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        characteristics_categories = get_characteristic_categories(self.characteristic_categories)
        return {
            "@id": str(self.study_id),
            "title": self.title,
            "filename": self.filename,
            "identifier": self.identifier,
            "description": self.description,
            "submissionDate": str(self.submission_date) if self.submission_date else "",
            "publicReleaseDate": str(self.public_release_date) if self.public_release_date else "",
            "people": [p.to_json() for p in self.contacts],
            "comments": [c.to_json() for c in self.comments],
            "publications": [p.to_json() for p in self.publications],
            "studyDesignDescriptors": [oa.to_json() for oa in self.study_design_descriptors],
            "protocols": [p.to_json() for p in self.protocols],
            "characteristicCategories": characteristics_categories,
            "unitCategories": [oa.to_json() for oa in self.unit_categories],
            "factors": [fv.to_json() for fv in self.study_factors],
            "materials": {
                "sources": [s.to_json() for s in self.sources],
                "samples": [s.to_json() for s in self.samples],
                "otherMaterials": [m.to_json() for m in self.materials],
            },
            "processSequence": [p.to_json() for p in self.process_sequence],
            "assays": [assay.to_json() for assay in self.assays],
        }


def make_study_methods():
    """This function will dynamically add the methods to the Study class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """

    def to_sql(self, session: Session) -> Study:
        """Convert the Study object to a SQLAlchemy object so that it can be added to the database.

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

        process_sequence = []
        ps = []
        for p in self.process_sequence:
            ps.append(p.to_sql(session))
            process_sequence.append(p)
        for process in process_sequence:
            process.update_plink(session)

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
            process_sequence=ps,
            assays=[assay.to_sql(session) for assay in self.assays],
        )

    setattr(StudyModel, "to_sql", to_sql)
    setattr(StudyModel, "get_table", make_get_table_method(Study))
