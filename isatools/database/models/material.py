from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Session

from isatools.model import Material as MaterialModel
from isatools.database.models.constraints import build_material_constraints
from isatools.database.models.relationships import study_materials, materials_characteristics
from isatools.database.models.inputs_outputs import InputOutput
from isatools.database.models.utils import make_get_table_method


class Material(InputOutput):
    """ The SQLAlchemy model for the Material table """

    __tablename__: str = 'material'
    __mapper_args__: dict = {"polymorphic_identity": "material", "concrete": True}
    __table_args__: tuple = (build_material_constraints(),)

    # Base fields
    material_id: str = Column(String, primary_key=True)
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

    def to_json(self) -> dict:
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            '@id': self.material_id,
            'name': self.name,
            'type': self.material_type,
            'characteristics': [c.to_json() for c in self.characteristics]
        }


def make_material_methods():
    """ This function will dynamically add the methods to the Material class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self, session: Session) -> Material:
        """ Convert the Material object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Material object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        material = session.query(Material).get(self.id)
        if material:
            return material

        return Material(
            material_id=self.id,
            name=self.name,
            material_type=self.type,
            characteristics=[c.to_sql(session) for c in self.characteristics]
        )

    setattr(MaterialModel, 'to_sql', to_sql)
    setattr(MaterialModel, 'get_table', make_get_table_method(Material))
