from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from isatools.model import OntologySource as OntologySourceModel
from isatools.database.models.relationships import investigation_ontology_source
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class OntologySource(Base):
    __tablename__: str = 'ontology_source'

    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    file: str = Column(String)
    version: str = Column(String)
    description: str = Column(String)

    # Back references
    investigations: relationship = relationship(
        'Investigation', secondary=investigation_ontology_source, back_populates='ontology_source_reference'
    )

    # References: one-to-many
    comments = relationship('Comment', back_populates='ontology_source')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'file': self.file,
            'version': self.version,
            'description': self.description,
            'comments': [c.to_json() for c in self.comments]
        }


def make_ontology_source_methods() -> None:
    def to_sql(self):
        return OntologySource(
            id=self.name,
            name=self.name,
            file=self.file,
            version=self.version,
            description=self.description,
        )
    setattr(OntologySourceModel, 'to_sql', to_sql)
    setattr(OntologySourceModel, 'get_table', make_get_table_method(OntologySource))