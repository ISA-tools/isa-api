from sqlalchemy.ext.declarative import ConcreteBase
from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from isatools.database.models.relationships import process_inputs
from isatools.database.utils import Base


class InputOutput(ConcreteBase, Base):
    """ Polymorphism base class for ISA-Tab inputs and outputs. This is used to create the relationship between
    process's inputs and outputs and multiple tables (sources, samples, material and data files) without relying on
    multiple through tables. """

    __tablename__: str = 'input_output'

    # Base fields
    id_: int = Column(Integer, primary_key=True)
    io_id: str = Column(String)
    io_type: str = Column(String)

    __mapper_args__: dict = {
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
