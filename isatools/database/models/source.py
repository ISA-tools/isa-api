from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Session

from isatools.model import Source as SourceModel
from isatools.database.models.relationships import study_sources, source_characteristics, sample_derives_from
from isatools.database.models.inputs_outputs import InputOutput
from isatools.database.models.utils import make_get_table_method


class Source(InputOutput):
    """ The SQLAlchemy model for the Source table """

    __tablename__: str = 'source'
    __mapper_args__: dict = {
        "polymorphic_identity": "source",
        "concrete": True,
    }

    # Base fields
    source_id: str = Column(String, primary_key=True)
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
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            '@id': self.source_id,
            'name': self.name,
            'characteristics': [c.to_json() for c in self.characteristics],
            'comments': [c.to_json() for c in self.comments]
        }


def make_source_methods():
    """ This function will dynamically add the methods to the Source class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self, session: Session) -> Source:
        """ Convert the Source object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Source object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        source = session.query(Source).get(self.id)
        if source:
            return source
        return Source(
            source_id=self.id,
            name=self.name,
            characteristics=[c.to_sql(session) for c in self.characteristics],
            comments=[c.to_sql() for c in self.comments]
        )

    setattr(SourceModel, 'to_sql', to_sql)
    setattr(SourceModel, 'get_table', make_get_table_method(Source))