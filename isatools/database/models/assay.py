from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

from isatools.model import Assay as AssayModel
from isatools.database.models.utils import get_characteristic_categories
from isatools.database.models.relationships import (
    study_assays,
    assay_unit_categories,
    assay_characteristic_categories,
    assay_samples,
    assay_materials,
    assay_data_files
)
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Assay(Base):
    """ The SQLAlchemy model for the Assay table """

    __tablename__: str = 'assay'

    # Base fields
    assay_id: int = Column(Integer, primary_key=True)
    filename: str = Column(String)
    technology_platform: str = Column(String)

    # Relationships back reference
    studies: relationship = relationship('Study', secondary=study_assays, back_populates='assays')

    # Relationship many-to-one
    measurement_type_id: int = Column(Integer, ForeignKey('ontology_annotation.ontology_annotation_id'))
    measurement_type: relationship = relationship(
        'OntologyAnnotation', backref='measurement_type', foreign_keys=[measurement_type_id])
    technology_type_id: int = Column(Integer, ForeignKey('ontology_annotation.ontology_annotation_id'))
    technology_type: relationship = relationship(
        'OntologyAnnotation', backref='technology_type', foreign_keys=[technology_type_id])

    # Relationship manh-to-many
    # data files
    unit_categories: relationship = relationship(
        'OntologyAnnotation', secondary=assay_unit_categories, back_populates='assays_units')
    characteristic_categories: relationship = relationship(
        'OntologyAnnotation', secondary=assay_characteristic_categories, back_populates='assays_characteristics')
    samples: relationship = relationship('Sample', secondary=assay_samples, back_populates='assays')
    materials: relationship = relationship('Material', secondary=assay_materials, back_populates='assays')
    datafiles: relationship = relationship('DataFile', secondary=assay_data_files, back_populates='assays')

    # Relationships: one-to-many
    comments: relationship = relationship('Comment', back_populates='assay')
    process_sequence: relationship = relationship("Process", back_populates="assay")

    def to_json(self):
        characteristic_categories = get_characteristic_categories(self.characteristic_categories)
        return {
            'filename': self.filename,
            "technologyPlatform": self.technology_platform,
            'measurementType': self.measurement_type.to_json(),
            'technologyType': self.technology_type.to_json(),
            'unitCategories': [uc.to_json() for uc in self.unit_categories],
            'characteristicCategories': characteristic_categories,
            'materials': {
                'samples': [s.to_json() for s in self.samples],
                'otherMaterials': [m.to_json() for m in self.materials]
            },
            'dataFiles': [df.to_json() for df in self.datafiles],
            'processSequence': [p.to_json() for p in self.process_sequence],
            "comments": [comment.to_json() for comment in self.comments]
        }


def make_assay_methods():
    def to_sql(self: AssayModel, session: Session) -> Assay:
        """ Converts an Assay model object to a SQLAlchemy model object """
        return Assay(
            filename=self.filename,
            technology_platform=self.technology_platform,
            measurement_type=self.measurement_type.to_sql(session),
            technology_type=self.technology_type.to_sql(session),
            unit_categories=[uc.to_sql(session) for uc in self.units],
            characteristic_categories=[cc.to_sql(session) for cc in self.characteristic_categories],
            samples=[sample.to_sql(session) for sample in self.samples],
            materials=[material.to_sql(session) for material in self.other_material],
            datafiles=[datafile.to_sql(session) for datafile in self.data_files],
            process_sequence=[process.to_sql(session) for process in self.process_sequence],
            comments=[comment.to_sql(session) for comment in self.comments]
        )
    setattr(AssayModel, 'to_sql', to_sql)
    setattr(AssayModel, 'get_table', make_get_table_method(Assay))
