from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

from isatools.model import Protocol as ProtocolModel
from isatools.database.models.relationships import study_protocols, protocol_parameters
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Protocol(Base):
    """ The SQLAlchemy model for the Protocol table """

    __tablename__: str = 'protocol'

    # Base fields
    protocol_id: str = Column(String, primary_key=True)
    name: str = Column(String)
    description: str = Column(String)
    uri: str = Column(String)
    version: str = Column(String)

    # Relationships back-ref
    studies: relationship = relationship('Study', secondary=study_protocols, back_populates='protocols')

    # References: one-to-many
    comments = relationship('Comment', back_populates='protocol')

    # Relationships: many-to-many
    protocol_parameters: relationship = relationship(
        'Parameter', secondary=protocol_parameters, back_populates='protocols')

    # Relationships many-to-one
    protocol_type_id: int = Column(Integer, ForeignKey('ontology_annotation.ontology_annotation_id'))
    protocol_type: relationship = relationship('OntologyAnnotation', backref='protocols')

    def to_json(self) -> dict:
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            '@id': self.protocol_id,
            'name': self.name,
            'description': self.description,
            'uri': self.uri,
            'version': self.version,
            'comments': [c.to_json() for c in self.comments],
            'parameters': [p.to_json() for p in self.protocol_parameters],
            'protocolType': self.protocol_type.to_json() if self.protocol_type else None,
            'components': []
        }


def make_protocol_methods():
    """ This function will dynamically add the methods to the Protocol class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self: ProtocolModel, session: Session) -> Protocol:
        """ Convert the Protocol object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Protocol object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        protocol = session.query(Protocol).get(self.id)
        if protocol:
            return protocol
        return Protocol(
            protocol_id=self.id,
            name=self.name,
            description=self.description,
            uri=self.uri if self.uri else '',
            version=self.version if self.version else '',
            comments=[comment.to_sql() for comment in self.comments],
            protocol_parameters=[parameter.to_sql(session) for parameter in self.parameters],
            protocol_type=self.protocol_type.to_sql(session) if self.protocol_type else None
        )

    setattr(ProtocolModel, 'to_sql', to_sql)
    setattr(ProtocolModel, 'get_table', make_get_table_method(Protocol))
