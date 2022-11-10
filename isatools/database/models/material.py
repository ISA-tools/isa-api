from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.model import Material as MaterialModel, Extract as ExtractModel, LabeledExtract as LabeledExtractModel
from isatools.database.models.relationships import study_materials, materials_characteristics
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Material(Base):
    __tablename__: str = 'material'

    # Base fields
    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    type: str = Column(String)

    # Relationships back-ref
    studies: relationship = relationship('Study', secondary=study_materials, back_populates='materials')

    # Relationships: many-to-many
    characteristics: relationship = relationship(
        'Characteristic', secondary=materials_characteristics, back_populates='materials'
    )

    # Relationships: one-to-many
    comments = relationship('Comment', back_populates='material')

    def to_json(self):
        return {
            '@id': self.id,
            'name': self.name,
            'type': self.type,
            'characteristics': [c.to_json() for c in self.characteristics]
        }


def make_material_methods():
    def to_sql(self, session):
        return Material(
            id=self.id,
            name=self.name,
            type=self.type,
            characteristics=[c.to_sql(session) for c in self.characteristics]
        )

    setattr(MaterialModel, 'to_sql', to_sql)
    setattr(MaterialModel, 'get_table', make_get_table_method(Material))
