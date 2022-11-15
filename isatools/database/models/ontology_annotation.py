from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from isatools.model import OntologyAnnotation as OntologyAnnotationModel
from isatools.database.models.relationships import (
    study_design_descriptors,
    study_characteristic_categories,
    study_unit_categories,
    person_roles,
    assay_unit_categories, assay_characteristic_categories
)
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class OntologyAnnotation(Base):
    """ The SQLAlchemy model for the OntologyAnnotation table """

    __tablename__: str = 'ontology_annotation'

    ontology_annotation_id: str = Column(String, primary_key=True)
    annotation_value: str = Column(String)
    term_accession: str = Column(String)

    # Relationships back-ref
    design_descriptors: relationship = relationship(
        'Study', secondary=study_design_descriptors, back_populates='study_design_descriptors')
    characteristic_categories: relationship = relationship(
        'Study', secondary=study_characteristic_categories, back_populates='characteristic_categories')
    unit_categories: relationship = relationship(
        'Study', secondary=study_unit_categories, back_populates='unit_categories')
    roles: relationship = relationship('Person', secondary=person_roles, back_populates='roles')
    assays_units: relationship = relationship(
        'Assay', secondary=assay_unit_categories, back_populates='unit_categories')
    assays_characteristics: relationship = relationship(
        'Assay', secondary=assay_characteristic_categories, back_populates='characteristic_categories')

    # Relationships many-to-one
    term_source_id: int = Column(Integer, ForeignKey('ontology_source.ontology_source_id'))
    term_source: relationship = relationship('OntologySource', backref='ontology_annotations')

    # References: one-to-many
    comments: relationship = relationship('Comment', back_populates='ontology_annotation')

    def to_json(self):
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            "@id": self.ontology_annotation_id,
            'annotationValue': self.annotation_value,
            'termSource': self.term_source_id if self.term_source_id else None,
            'termAccession': self.term_accession,
            'comments': [c.to_json() for c in self.comments]
        }


def make_ontology_annotation_methods() -> None:
    """ This function will dynamically add the methods to the OntologyAnnotation class that are required to interact
    with the database. This is done to avoid circular imports and to extra dependencies in the models package.
    It's called in the init of the database models package.
    """
    def to_sql(self, session):
        """ Convert the OntologyAnnotation object to a SQLAlchemy object and adds it to the session. If the object
        already exists in the database session, it will be returned instead. This is done to avoid duplicates.

        :param self: the OntologyAnnotation object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        oa = session.query(OntologyAnnotation).get(self.id)
        if oa:
            return oa
        oa = OntologyAnnotation(
            ontology_annotation_id=self.id,
            annotation_value=self.term,
            term_accession=self.term_accession,
            term_source_id=self.term_source.name if self.term_source else None,
            comments=[comment.to_sql() for comment in self.comments]
        )
        session.add(oa)
        return oa
    setattr(OntologyAnnotationModel, 'to_sql', to_sql)
    setattr(OntologyAnnotationModel, 'get_table', make_get_table_method(OntologyAnnotation))
