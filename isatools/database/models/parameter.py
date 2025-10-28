from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, Session, relationship

from isatools.database.models.relationships import protocol_parameters
from isatools.database.models.utils import make_get_table_method
from isatools.database.utils import Base
from isatools.model import ProtocolParameter as ParameterModel


class Parameter(Base):
    """The SQLAlchemy model for the Parameter table"""

    __tablename__: str = "parameter"
    __allow_unmapped__ = True

    # Base fields
    parameter_id: Mapped[str] = Column(String, primary_key=True)

    # Relationships back-ref
    protocols: Mapped[list["Protocol"]] = relationship(
        "Protocol", secondary=protocol_parameters, back_populates="protocol_parameters"
    )

    # Relationships many-to-one
    ontology_annotation_id: Mapped[str] = Column(String, ForeignKey("ontology_annotation.ontology_annotation_id"))
    ontology_annotation: Mapped[list["OntologyAnnotation"]] = relationship("OntologyAnnotation", backref="parameters")

    def to_json(self) -> dict:
        """Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            "@id": self.parameter_id,
            "parameterName": self.ontology_annotation.to_json() if self.ontology_annotation else None,
        }


def make_parameter_methods() -> None:
    """This function will dynamically add the methods to the Parameter class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """

    def to_sql(self, session: Session) -> Parameter:
        """Convert the Parameter object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Parameter object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        parameter = session.get(Parameter, self.id)
        if parameter:
            return parameter
        parameter = Parameter(parameter_id=self.id, ontology_annotation=self.parameter_name.to_sql(session))
        session.add(parameter)
        return parameter

    setattr(ParameterModel, "to_sql", to_sql)
    setattr(ParameterModel, "get_table", make_get_table_method(Parameter))
