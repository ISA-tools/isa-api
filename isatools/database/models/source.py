from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from isatools.model import Source as SourceModel
from isatools.database.models.relationships import study_sources, source_characteristics, sample_derives_from
from isatools.database.models.inputs_outputs import InputOutput
from isatools.database.models.utils import make_get_table_method


class Source(InputOutput):
    __tablename__: str = 'source'
    __mapper_args__ = {
        "polymorphic_identity": "source",
        "concrete": True,
    }

    # Base fields
    id: str = Column(String, primary_key=True)
    name: str = Column(String)

    # Relationships back-ref
    studies: relationship = relationship('Study', secondary=study_sources, back_populates='sources')
    samples: relationship = relationship('Sample', secondary=sample_derives_from, back_populates='derives_from')

    # Relationships: many-to-many
    characteristics: relationship = relationship(
        'Characteristic', secondary=source_characteristics, back_populates='sources'
    )

    comments = relationship('Comment', back_populates='source')

    def to_json(self) -> dict:
        return {
            '@id': self.id,
            'name': self.name,
            'characteristics': [c.to_json() for c in self.characteristics],
            'comments': [c.to_json() for c in self.comments]
        }


def make_source_methods():
    def to_sql(self, session):
        source = session.query(Source).filter(Source.id == self.id).first()
        if source:
            return source
        return Source(
            id=self.id,
            name=self.name,
            characteristics=[c.to_sql(session) for c in self.characteristics],
            comments=[c.to_sql() for c in self.comments]
        )

    setattr(SourceModel, 'to_sql', to_sql)
    setattr(SourceModel, 'get_table', make_get_table_method(Source))