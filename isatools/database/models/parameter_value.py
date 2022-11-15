from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Session

from isatools.model import ParameterValue as ParameterValueModel
from isatools.model.ontology_annotation import OntologyAnnotation as OntologyAnnotationModel
from isatools.database.models.relationships import process_parameter_values
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class ParameterValue(Base):
    """ The SQLAlchemy model for the ParameterValue table """

    __tablename__: str = 'parameter_value'

    # Base fields
    parameter_value_id: int = Column(Integer, primary_key=True)
    value_int: int = Column(Integer)

    # Relationships: back-ref
    processes_parameter_values: relationship = relationship(
        'Process', secondary=process_parameter_values, back_populates='parameter_values'
    )

    # Relationships many-to-one
    value_id: int = Column(Integer, ForeignKey('ontology_annotation.ontology_annotation_id'))
    value_oa: relationship = relationship(
        'OntologyAnnotation', backref='parameter_values', foreign_keys=[value_id])
    unit_id: int = Column(Integer, ForeignKey('ontology_annotation.ontology_annotation_id'))
    unit: relationship = relationship(
        'OntologyAnnotation', backref='parameter_values_unit', foreign_keys=[unit_id])
    category_id: int = Column(Integer, ForeignKey('parameter.parameter_id'))
    category: relationship = relationship('Parameter', backref='parameter_values')

    def to_json(self) -> dict:
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            'value': self.value_int if self.value_int else {"@id": self.value_oa.ontology_annotation_id},
            'unit': {"@id": self.unit.ontology_annotation_id} if self.unit else None,
            'category': {"@id": self.category_id} if self.category_id else ''
        }


def make_parameter_value_methods():
    """ This function will dynamically add the methods to the ParameterValue class that are required to interact with
    the database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self, session: Session) -> ParameterValue:
        """ Convert the ParameterValue object to a SQLAlchemy object so that it can be added to the database.

        :param self: the ParameterValue object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        parameter_value = {
            'unit': self.unit.to_sql(session) if self.unit else None,
            'category_id': self.category.id
        }
        if isinstance(self.value, str):
            value = OntologyAnnotationModel(term=self.value)
            parameter_value['value_oa'] = value.to_sql(session=session)
        elif isinstance(self.value, OntologyAnnotationModel):
            parameter_value['value_oa'] = self.value.to_sql(session=session)
        elif isinstance(self.value, int):
            parameter_value['value_int'] = float(self.value)
        elif isinstance(self.value, float):
            parameter_value['value_int'] = self.value
        return ParameterValue(**parameter_value)

    setattr(ParameterValueModel, 'to_sql', to_sql)
    setattr(ParameterValueModel, 'get_table', make_get_table_method(ParameterValue))
