from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from isatools.model import OntologySource as OntologySourceModel
from isatools.database.models.relationships import investigation_ontology_source
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class OntologySource(Base):
    """ The SQLAlchemy model for the OntologySourceReference table """

    __tablename__: str = 'ontology_source'

    ontology_source_id: str = Column(String, primary_key=True)
    name: str = Column(String)
    file: str = Column(String)
    version: str = Column(String)
    description: str = Column(String)

    # Back references
    investigations: relationship = relationship(
        'Investigation', secondary=investigation_ontology_source, back_populates='ontology_source_reference'
    )

    # References: one-to-many
    comments: relationship = relationship('Comment', back_populates='ontology_source')

    def to_json(self) -> dict:
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            'id': self.ontology_source_id,
            'name': self.name,
            'file': self.file,
            'version': self.version,
            'description': self.description,
            'comments': [c.to_json() for c in self.comments]
        }


def make_ontology_source_methods() -> None:
    """ This function will dynamically add the methods to the OntologySourceReference class that are required to
    interact with the database. This is done to avoid circular imports and to extra dependencies in the models package.
    It's called in the init of the database models package.
    """
    def to_sql(self, session) -> OntologySource:
        """ Convert the OntologySourceReference object to a SQLAlchemy object so that it can be added to the database.

        :param self: the OntologySourceReference object. Will be injected automatically.
        :param session: the SQLAlchemy session. Will be injected automatically.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        ontology_source = session.query(OntologySource).get(self.name)
        if ontology_source:
            return ontology_source
        return OntologySource(
            ontology_source_id=self.name,
            name=self.name,
            file=self.file,
            version=self.version,
            description=self.description,
        )
    setattr(OntologySourceModel, 'to_sql', to_sql)
    setattr(OntologySourceModel, 'get_table', make_get_table_method(OntologySource))
