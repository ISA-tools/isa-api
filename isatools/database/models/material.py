from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from isatools.model import Material as MaterialModel
from isatools.database.models.relationships import study_materials, materials_characteristics
from isatools.database.models.inputs_outputs import InputOutput
from isatools.database.models.utils import make_get_table_method


class Material(InputOutput):
    __tablename__: str = 'material'
    __mapper_args__ = {
        "polymorphic_identity": "material",
        "concrete": True,
    }

    # Base fields
    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    material_type: str = Column(String)

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
            'type': self.material_type,
            'characteristics': [c.to_json() for c in self.characteristics]
        }


def make_material_methods():
    def to_sql(self, session):
        return Material(
            id=self.id,
            name=self.name,
            material_type=self.type,
            characteristics=[c.to_sql(session) for c in self.characteristics]
        )

    setattr(MaterialModel, 'to_sql', to_sql)
    setattr(MaterialModel, 'get_table', make_get_table_method(Material))
