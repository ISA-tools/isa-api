from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import Comment as CommentModel
from isatools.database.utils import Base
from isatools.database.models.constraints import build_comment_constraints
from isatools.database.models.utils import make_get_table_method


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (build_comment_constraints(), )

    # Base fields
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)

    # Back references
    characteristic_id = Column(Integer, ForeignKey('characteristic.id'))
    characteristic = relationship('Characteristic', back_populates='comments')
    factor_value_id = Column(Integer, ForeignKey('factor_value.id'))
    factor_value = relationship('FactorValue', back_populates='comments')
    investigation_id = Column(Integer, ForeignKey('investigation.id'))
    investigation = relationship('Investigation', back_populates='comments')
    ontology_source_id = Column(Integer, ForeignKey('ontology_source.id'))
    ontology_source = relationship('OntologySource', back_populates='comments')
    ontology_annotation_id = Column(Integer, ForeignKey('ontology_annotation.id'))
    ontology_annotation = relationship('OntologyAnnotation', back_populates='comments')
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='comments')
    process_id = Column(Integer, ForeignKey('process.id'))
    process = relationship('Process', back_populates='comments')
    protocol_id = Column(Integer, ForeignKey('protocol.id'))
    protocol = relationship('Protocol', back_populates='comments')
    publication_id = Column(Integer, ForeignKey('publication.id'))
    publication = relationship('Publication', back_populates='comments')
    sample_id = Column(Integer, ForeignKey('sample.id'))
    sample = relationship('Sample', back_populates='comments')
    source_id = Column(Integer, ForeignKey('source.id'))
    source = relationship('Source', back_populates='comments')
    study_factor_id = Column(Integer, ForeignKey('factor.id'))
    study_factor = relationship('StudyFactor', back_populates='comments')
    study_id = Column(Integer, ForeignKey('study.id'))
    study = relationship('Study', back_populates='comments')

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'value': self.value}


def make_comment_methods() -> None:
    def to_sql(self) -> Comment:
        return Comment(name=self.name, value=self.value)

    setattr(CommentModel, 'to_sql', to_sql)
    setattr(CommentModel, 'get_table', make_get_table_method(Comment))
