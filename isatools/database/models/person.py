from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship, Mapped

from isatools.database.models.relationships import person_roles
from isatools.database.models.utils import make_get_table_method
from isatools.database.utils import Base
from isatools.model import Person as PersonModel


class Person(Base):
    """The SQLAlchemy model for the Person table"""

    __tablename__: str = "person"
    __allow_unmapped__ = True

    person_id: Mapped[int] = Column(Integer, primary_key=True)
    last_name: Mapped[str] = Column(String, nullable=True)
    first_name: Mapped[str] = Column(String, nullable=True)
    mid_initials: Mapped[str] = Column(String, nullable=True)
    email: Mapped[str] = Column(String, nullable=True)
    phone: Mapped[str] = Column(String, nullable=True)
    fax: Mapped[str] = Column(String, nullable=True)
    address: Mapped[str] = Column(String, nullable=True)
    affiliation: Mapped[str] = Column(String, nullable=True)

    investigation_id: Mapped[int] = Column(Integer, ForeignKey("investigation.investigation_id"), nullable=True)
    investigation: Mapped[list['Investigation']] = relationship("Investigation", back_populates="contacts")
    study_id: Mapped[int] = Column(Integer, ForeignKey("study.study_id"), nullable=True)
    study: Mapped[list['Study']]  = relationship("Study", back_populates="contacts")
    comments: Mapped[list['Comment']]  = relationship("Comment", back_populates="person")

    # Relationships many-to-many
    roles: Mapped[list['OntologyAnnotation']]  = relationship("OntologyAnnotation", secondary=person_roles, back_populates="roles")

    def to_json(self) -> dict:
        """Convert the SQLAlchemy object to a dictionary

        :return: The dictionary representation of the object taken from the database
        """
        return {
            "lastName": self.last_name,
            "firstName": self.first_name,
            "midInitials": self.mid_initials,
            "email": self.email,
            "phone": self.phone,
            "fax": self.fax,
            "address": self.address,
            "affiliation": self.affiliation,
            "roles": [r.to_json() for r in self.roles],
            "comments": [c.to_json() for c in self.comments],
        }


def make_person_methods():
    """This function will dynamically add the methods to the Person class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """

    def to_sql(self, session: Session) -> Person:
        """Convert the Person object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Person object. Will be injected automatically.
        :param session: The SQLAlchemy session to add the object to.

        :return: The SQLAlchemy object ready to be committed to the database session.
        """
        # print(self)
        # print(self.roles)
        # print(self.comments)

        return Person(
            first_name=self.first_name,
            last_name=self.last_name,
            mid_initials=self.mid_initials,
            email=self.email,
            phone=self.phone,
            fax=self.fax,
            address=self.address,
            affiliation=self.affiliation,
            roles=[role.to_sql(session) for role in self.roles],
            comments=[comment.to_sql() for comment in self.comments],
        )

    setattr(PersonModel, "to_sql", to_sql)
    setattr(PersonModel, "get_table", make_get_table_method(Person))
