from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from isatools.model import Process as ProcessModel
from isatools.database.utils import Base
from isatools.database.models.relationships import process_inputs, process_outputs, process_parameter_values
from isatools.database.models.inputs_outputs import InputOutput
from isatools.database.models.utils import make_get_table_method


class Process(Base):
    __tablename__ = 'process'

    id = Column(String, primary_key=True)
    name = Column(String)
    performer = Column(String)
    date = Column(Date)

    # Relationships self-referential
    previous_process_id = Column(Integer, ForeignKey('process.id'))
    next_process_id = Column(Integer, ForeignKey('process.id'))

    # Relationships back reference
    study_id = Column(Integer, ForeignKey('study.id'))
    study = relationship('Study', back_populates='process_sequence')

    # Relationships: many-to-one
    protocol_id = Column(Integer, ForeignKey('protocol.id'))
    protocol = relationship('Protocol', backref='processes')

    # Relationships: many-to-many
    inputs: relationship = relationship(
        'InputOutput', secondary=process_inputs, back_populates='processes_inputs'
    )
    outputs: relationship = relationship(
        'InputOutput', secondary=process_outputs, back_populates='processes_outputs'
    )
    parameter_values = relationship(
        'ParameterValue', secondary=process_parameter_values, back_populates='processes_parameter_values')

    # Relationships: one-to-many
    comments = relationship('Comment', back_populates='process')

    def to_json(self):
        inputs = [{"@id": data_input.id} for data_input in self.inputs if type(data_input).__name__ != 'InputOutput']
        outputs = [{"@id": output.id} for output in self.outputs if type(output).__name__ != 'InputOutput']
        return {
            'id': self.id,
            'name': self.name,
            'performer': self.performer,
            'date': str(self.date),
            'input': inputs,
            'output': outputs,
            # 'parameterValues': self.parameter_values,
            'previous_process': {"@id": self.self.previous_process_id} if self.previous_process_id else None,
            'next_process': {"@id": self.next_process_id} if self.next_process_id else None,
            'study_id': self.study_id,
            'comments': [c.to_json() for c in self.comments],
            'executesProtocol': {"@id": self.protocol.id}
        }


def make_process_methods():
    def to_sql(self, session):
        inputs = []
        outputs = []
        for data_input in self.inputs:
            inputs.append(InputOutput(id=data_input.id, type_='input'))
        for data_output in self.outputs:
            outputs.append(InputOutput(id=data_output.id, type_='output'))
        return Process(
            id=self.id,
            name=self.name,
            performer=self.performer,
            date=datetime.strptime(self.date) if self.date else None,
            comments=[comment.to_sql() for comment in self.comments],
            previous_process_id=self.prev_process.id if self.prev_process else None,
            next_process_id=self.next_process.id if self.next_process else None,
            protocol_id=self.executes_protocol.id,
            inputs=inputs,
            outputs=outputs,
            parameter_values=[parameter_value.to_sql(session) for parameter_value in self.parameter_values]
        )

    setattr(ProcessModel, 'to_sql', to_sql)
    setattr(ProcessModel, 'get_table', make_get_table_method(Process))
