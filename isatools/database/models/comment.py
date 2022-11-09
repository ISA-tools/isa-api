from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import Comment as CommentModel
from isatools.database.utils import Base
from isatools.database.constraints import build_comment_constraints
from isatools.database.models.utils import make_get_table_method


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (build_comment_constraints(), )

    # Base fields
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)

    # Back references
    investigation_id = Column(Integer, ForeignKey('investigation.id'))
    investigation = relationship('Investigation', back_populates='comments')

    study_id = Column(Integer, ForeignKey('study.id'))
    study = relationship('Study', back_populates='comments')

    process_id = Column(Integer, ForeignKey('process.id'))
    process = relationship('Process', back_populates='comments')

    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='comments')

    publication_id = Column(Integer, ForeignKey('publication.id'))
    publication = relationship('Publication', back_populates='comments')

    ontology_source_id = Column(Integer, ForeignKey('ontology_source.id'))
    ontology_source = relationship('OntologySource', back_populates='comments')

    ontology_annotation_id = Column(Integer, ForeignKey('ontology_annotation.id'))
    ontology_annotation = relationship('OntologyAnnotation', back_populates='comments')

    protocol_id = Column(Integer, ForeignKey('protocol.id'))
    protocol = relationship('Protocol', back_populates='comments')

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'value': self.value}


def make_comment_methods() -> None:
    def to_sql(self) -> Comment:
        return Comment(name=self.name, value=self.value)

    setattr(CommentModel, 'to_sql', to_sql)
    setattr(CommentModel, 'get_table', make_get_table_method(Comment))

