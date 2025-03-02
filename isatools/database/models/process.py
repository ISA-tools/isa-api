from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date, update
from sqlalchemy.orm import relationship, Session

from isatools.model import Process as ProcessModel
from isatools.database.utils import Base
from isatools.database.models.relationships import (process_inputs,
                                                    process_outputs,
                                                    process_parameter_values)
from isatools.database.models.inputs_outputs import InputOutput
from isatools.database.models.utils import make_get_table_method


class Process(Base):
    """ The SQLAlchemy model for the Process table """

    __tablename__: str = 'process'
    __allow_unmapped__ = True

    process_id: int = Column(String, primary_key=True)
    name: str = Column(String)
    performer: str = Column(String)
    date: datetime = Column(Date)

    # Relationships self-referential
    previous_process_id: str = Column(String, ForeignKey('process.process_id'))
    next_process_id: str = Column(String, ForeignKey('process.process_id'))

    # Relationships back reference
    study_id: int = Column(Integer, ForeignKey('study.study_id'))
    study: relationship = relationship('Study', back_populates='process_sequence')
    assay_id: int = Column(Integer, ForeignKey('assay.assay_id'))
    assay: relationship = relationship('Assay', back_populates='process_sequence')

    # Relationships: many-to-one
    protocol_id: str = Column(String, ForeignKey('protocol.protocol_id'))
    protocol: relationship = relationship('Protocol', backref='processes')

    # Relationships: many-to-many
    inputs: relationship = relationship('InputOutput', secondary=process_inputs, back_populates='processes_inputs')
    outputs: relationship = relationship('InputOutput', secondary=process_outputs, back_populates='processes_outputs')
    parameter_values: relationship = relationship(
        'ParameterValue', secondary=process_parameter_values, back_populates='processes_parameter_values')

    # Relationships: one-to-many
    comments: relationship = relationship('Comment', back_populates='process')

    def to_json(self) -> dict:
        """ Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            '@id': self.process_id,
            'name': self.name,
            'performer': self.performer,
            'date': str(self.date) if self.date else '',
            'inputs': [{"@id": data_input.io_id} for data_input in self.inputs],
            'outputs': [{"@id": data_output.io_id} for data_output in self.outputs],
            'parameterValues': [pv.to_json() for pv in self.parameter_values],
            'previous_process': {"@id": self.previous_process_id} if self.previous_process_id else None,
            'next_process': {"@id": self.next_process_id} if self.next_process_id else None,
            'study_id': self.study_id,
            'comments': [c.to_json() for c in self.comments],
            'executesProtocol': {"@id": self.protocol.protocol_id}
        }


def make_process_methods():
    """ This function will dynamically add the methods to the Process class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """
    def to_sql(self, session: Session) -> Process:
        """ Convert the Process object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Process object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        process = session.query(Process).get(self.id)
        if process:
            return process

        inputs = []
        for data_input in self.inputs:
            in_out = InputOutput()
            in_out.io_id = data_input.id
            in_out.io_type = 'input'
            inputs.append(in_out)

        outputs = []
        for data_output in self.outputs:
            out_in = InputOutput()
            out_in.io_id = data_output.id
            out_in.io_type = 'output'
            # outputs.append(InputOutput(io_id=data_output.id, io_type='output'))
            outputs.append(out_in)

        if self.date:
            cleaned_date = self.date
        else:
            cleaned_date = None

        return Process(
            process_id=self.id,
            name=self.name,
            performer=self.performer,
            date=cleaned_date,
            comments=[comment.to_sql() for comment in self.comments],
            protocol_id=self.executes_protocol.id,
            inputs=inputs,
            outputs=outputs,
            parameter_values=[parameter_value.to_sql(session) for parameter_value in self.parameter_values]
        )

    def update_plink(self, session: Session):
        """ Update the previous and next process links for the process.

        :param self: The Process object. Will be injected automatically.
        :param session: The SQLAlchemy session to use.
        """
        statement = update(Process).where(Process.process_id == self.id).values(
            previous_process_id=self.prev_process.id if self.prev_process else None,
            next_process_id=self.next_process.id if self.next_process else None
        )
        session.execute(statement)
        session.commit()

    setattr(ProcessModel, 'to_sql', to_sql)
    setattr(ProcessModel, 'update_plink', update_plink)
    setattr(ProcessModel, 'get_table', make_get_table_method(Process))
