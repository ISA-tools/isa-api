from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Session

from isatools.model import Sample as SampleModel
from isatools.database.models.relationships import (
    study_samples,
    sample_characteristics,
    sample_derives_from,
    sample_factor_values,
    assay_samples
)
from isatools.database.models.inputs_outputs import InputOutput
from isatools.database.models.utils import make_get_table_method


class Sample(InputOutput):
    """ The SQLAlchemy model for the Sample table """

    __tablename__: str = 'sample'
    __mapper_args__: dict = {
        "polymorphic_identity": "sample",
        "concrete": True,
    }

    # Base fields
    sample_id: str = Column(String, primary_key=True)
    name: str = Column(String)

    # Relationships back-ref
    studies: relationship = relationship('Study', secondary=study_samples, back_populates='samples')
    assays: relationship = relationship('Assay', secondary=assay_samples, back_populates='samples')

    # Relationships: many-to-many
    characteristics: relationship = relationship(
        'Characteristic', secondary=sample_characteristics, back_populates='samples'
    )
    derives_from: relationship = relationship(
        'Source', secondary=sample_derives_from, back_populates='samples'
    )
    factor_values: relationship = relationship('FactorValue', secondary=sample_factor_values, back_populates='samples')

    # Factor values, derives from
    comments = relationship('Comment', back_populates='sample')

    def to_json(self) -> dict:
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            '@id': self.sample_id,
            'name': self.name,
            'characteristics': [c.to_json() for c in self.characteristics],
            'factorValues': [fv.to_json() for fv in self.factor_values],
            'derives_from': [{"@id": source.source_id} for source in self.derives_from],
            'comments': [c.to_json() for c in self.comments]
        }


def make_sample_methods():
    """ This function will dynamically add the methods to the Sample class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self, session: Session) -> Sample:
        """ Convert the Sample object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Sample object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        sample = session.query(Sample).get(self.id)
        if sample:
            return sample
        return Sample(
            sample_id=self.id,
            name=self.name,
            characteristics=[c.to_sql(session) for c in self.characteristics],
            derives_from=[s.to_sql(session) for s in self.derives_from],
            factor_values=[fv.to_sql(session) for fv in self.factor_values],
            comments=[c.to_sql() for c in self.comments]
        )

    setattr(SampleModel, 'to_sql', to_sql)
    setattr(SampleModel, 'get_table', make_get_table_method(Sample))
