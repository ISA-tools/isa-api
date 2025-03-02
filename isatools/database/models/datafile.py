from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Session

from isatools.model import DataFile as DataFileModel
from isatools.database.models.relationships import assay_data_files
from isatools.database.models.inputs_outputs import InputOutput
from isatools.database.models.utils import make_get_table_method


class Datafile(InputOutput):
    """ The SQLAlchemy model for the Material table """

    __tablename__: str = 'datafile'
    __allow_unmapped__ = True
    __mapper_args__: dict = {"polymorphic_identity": "Datafile", "concrete": True}

    # Base fields
    datafile_id: str = Column(String, primary_key=True)
    filename: str = Column(String)
    label: str = Column(String)

    # Relationships back-ref
    assays: relationship = relationship('Assay', secondary=assay_data_files, back_populates='datafiles')

    # Relationships: one-to-many
    comments: relationship = relationship('Comment', back_populates='datafile')

    def to_json(self):
        return {
            '@id': self.datafile_id,
            'name': self.filename,
            'type': self.label,
            'comments': [comment.to_json() for comment in self.comments]
        }


def make_datafile_methods():
    def to_sql(self, session: Session) -> Datafile:
        datafile = session.query(Datafile).get(self.id)
        if datafile:
            return datafile
        return Datafile(
            datafile_id=self.id,
            filename=self.filename,
            label=self.label,
            comments=[comment.to_sql() for comment in self.comments]
        )
    setattr(DataFileModel, 'to_sql', to_sql)
    setattr(DataFileModel, 'get_table', make_get_table_method(Datafile))
