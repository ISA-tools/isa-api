from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import ConcreteBase
from sqlalchemy.orm import Mapped, relationship

from isatools.database.models.relationships import process_inputs
from isatools.database.utils import Base


class InputOutput(ConcreteBase, Base):
    """Polymorphism base class for ISA-Tab inputs and outputs. This is used to create the relationship between
    process's inputs and outputs and multiple tables (sources, samples, material and data files) without relying on
    multiple through tables."""

    __tablename__: str = "input_output"
    __allow_unmapped__ = True

    # Base fields
    id_: Mapped[int] = Column(Integer, primary_key=True)
    io_id: Mapped[str] = Column(String)
    io_type: Mapped[str] = Column(String)

    __mapper_args__: dict = {"polymorphic_identity": "input", "concrete": True}

    # Relationships: back-ref
    processes_inputs: Mapped[list["Process"]] = relationship("Process", secondary=process_inputs, viewonly=True)
    processes_outputs: Mapped[list["Process"]] = relationship("Process", secondary=process_inputs, viewonly=True)
