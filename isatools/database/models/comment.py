from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import Comment as CommentModel
from isatools.database.utils import Base
from isatools.database.models.constraints import build_comment_constraints
from isatools.database.models.utils import make_get_table_method


class Comment(Base):
    """ The SQLAlchemy model for the Comment table """

    __tablename__: str = 'comment'
    __table_args__: tuple = (build_comment_constraints(), )

    # Base fields
    comment_id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    value: str = Column(String)

    # Back references
    assay_id: int = Column(Integer, ForeignKey('assay.assay_id'))
    assay: relationship = relationship('Assay', back_populates='comments')
    characteristic_id: int = Column(Integer, ForeignKey('characteristic.characteristic_id'))
    characteristic: relationship = relationship('Characteristic', back_populates='comments')
    factor_value_id: int = Column(Integer, ForeignKey('factor_value.factor_value_id'))
    factor_value: relationship = relationship('FactorValue', back_populates='comments')
    investigation_id: int = Column(Integer, ForeignKey('investigation.investigation_id'))
    investigation: relationship = relationship('Investigation', back_populates='comments')
    material_id: int = Column(Integer, ForeignKey('material.material_id'))
    material: relationship = relationship('Material', back_populates='comments')
    ontology_source_id: int = Column(Integer, ForeignKey('ontology_source.ontology_source_id'))
    ontology_source: relationship = relationship('OntologySource', back_populates='comments')
    ontology_annotation_id: int = Column(Integer, ForeignKey('ontology_annotation.ontology_annotation_id'))
    ontology_annotation: relationship = relationship('OntologyAnnotation', back_populates='comments')
    person_id: int = Column(Integer, ForeignKey('person.person_id'))
    person: relationship = relationship('Person', back_populates='comments')
    process_id: int = Column(Integer, ForeignKey('process.process_id'))
    process: relationship = relationship('Process', back_populates='comments')
    protocol_id: int = Column(Integer, ForeignKey('protocol.protocol_id'))
    protocol: relationship = relationship('Protocol', back_populates='comments')
    publication_id: int = Column(Integer, ForeignKey('publication.publication_id'))
    publication: relationship = relationship('Publication', back_populates='comments')
    sample_id: int = Column(Integer, ForeignKey('sample.sample_id'))
    sample: relationship = relationship('Sample', back_populates='comments')
    source_id: int = Column(Integer, ForeignKey('source.source_id'))
    source: relationship = relationship('Source', back_populates='comments')
    study_factor_id: int = Column(Integer, ForeignKey('factor.factor_id'))
    study_factor: relationship = relationship('StudyFactor', back_populates='comments')
    study_id: int = Column(Integer, ForeignKey('study.study_id'))
    study: relationship = relationship('Study', back_populates='comments')

    def to_json(self) -> dict:
        """ Return a JSON representation of the Comment object

        :return: JSON representation of the Comment object
        """
        return {'comment_id': self.comment_id, 'name': self.name, 'value': self.value}


def make_comment_methods() -> None:
    """ This function will dynamically add the methods to the Comment class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self) -> Comment:
        """ Convert the Comment object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Comment object. Will be injected automatically.

        :return: The SQLAlchemy object ready to committed to the database session.
        """
        return Comment(name=self.name, value=self.value)

    setattr(CommentModel, 'to_sql', to_sql)
    setattr(CommentModel, 'get_table', make_get_table_method(Comment))
