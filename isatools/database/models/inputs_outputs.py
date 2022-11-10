from sqlalchemy.ext.declarative import ConcreteBase
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from isatools.database.models.relationships import process_inputs
from isatools.database.utils import Base


class InputOutput(ConcreteBase, Base):
    __tablename__: str = 'input_output'

    # Base fields
    id: str = Column(String, primary_key=True)
    type_: str = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'input',
        'concrete': True
    }

    # Relationships: back-ref
    processes_inputs: relationship = relationship(
        'Process', secondary=process_inputs, viewonly=True
    )
    processes_outputs: relationship = relationship(
        'Process', secondary=process_inputs, viewonly=True
    )
