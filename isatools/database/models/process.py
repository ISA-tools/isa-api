from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from isatools.model import Process as ProcessModel
from isatools.database.utils import Base
from isatools.database.models.utils import make_get_table_method


class Process(Base):
    __tablename__ = 'process'

    id = Column(String, primary_key=True)
    name = Column(String)
    performer = Column(String)
    date = Column(Date)
    # executes_protocol = Column(String)
    # parameter_values= Column(String)
    # input = Column(String)
    # output = Column(String)

    previous_process = Column(Integer, ForeignKey('process.id'))
    next_process = Column(Integer, ForeignKey('process.id'))

    study_id = Column(Integer, ForeignKey('study.id'))
    study = relationship('Study', back_populates='process_sequence')

    comments = relationship('Comment', back_populates='process')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'performer': self.performer,
            'date': str(self.date),
            # 'input': self.input,
            # 'output': self.output,
            'previous_process': self.previous_process,
            'next_process': self.next_process,
            'study_id': self.study_id,
            'comments': [c.to_json() for c in self.comments],
        }


def make_process_methods():
    def to_sql(self):
        return Process(
            id=self.id,
            name=self.name,
            performer=self.performer,
            date=datetime.strptime(self.date) if self.date else None,
            comments=[comment.to_sql() for comment in self.comments]
        )

    setattr(ProcessModel, 'to_sql', to_sql)
    setattr(ProcessModel, 'get_table', make_get_table_method(Process))
