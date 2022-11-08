from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from isatools.database.utils import Base
from isatools.database.constraints import build_person_constraints


class Person(Base):
    __tablename__: str = 'person'

    __table_args__: tuple = (build_person_constraints(),)

    id: int = Column(Integer, primary_key=True)
    isa_identifier: str = Column(String)
    last_name: str = Column(String)
    first_name: str = Column(String)
    mid_initials: str = Column(String)
    email: str = Column(String)
    phone: str = Column(String)
    fax: str = Column(String)
    address: str = Column(String)
    affiliation: str = Column(String)

    investigation_id: int = Column(Integer, ForeignKey('investigation.id'))
    investigation: relationship = relationship('Investigation', back_populates='contacts')
    study_id: int = Column(Integer, ForeignKey('study.id'))
    study: relationship = relationship('Study', back_populates='contacts')
    comments: relationship = relationship('Comment', back_populates='person')

    def to_json(self):
        return {
            'id': self.isa_identifier,
            'lastName': self.last_name,
            'firstName': self.first_name,
            'midInitials': self.mid_initials,
            'email': self.email,
            'phone': self.phone,
            'fax': self.fax,
            'address': self.address,
            'affiliation': self.affiliation,
            'comments': [c.to_json() for c in self.comments]
        }
