from typing import Optional
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship, Mapped, mapped_column

from isatools.database.models.constraints import build_comment_constraints
from isatools.database.models.utils import make_get_table_method
from isatools.database.utils import Base
from isatools.model import Comment as CommentModel


class Comment(Base):
    """The SQLAlchemy model for the Comment table"""

    __tablename__: str = "comment"
    __table_args__: tuple = (build_comment_constraints(),)
    __allow_unmapped__ = True

    # Base fields
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)

    # Back references
    assay_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("assay.assay_id"), nullable=True)
    assay: relationship = relationship("Assay", back_populates="comments")
    characteristic_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("characteristic.characteristic_id"), nullable=True)
    characteristic: Mapped[Optional['Characteristic']] = relationship("Characteristic", back_populates="comments")
    datafile_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("datafile.datafile_id"), nullable=True)
    datafile: Mapped[Optional['Datafile']] = relationship("Datafile", back_populates="comments")
    factor_value_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("factor_value.factor_value_id"), nullable=True)
    factor_value: Mapped[Optional['FactorValue']] = relationship("FactorValue", back_populates="comments")
    investigation_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("investigation.investigation_id"), nullable=True)
    investigation: Mapped[Optional['Investigation']] = relationship("Investigation", back_populates="comments")
    material_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("material.material_id"), nullable=True)
    material: Mapped[Optional['Material']] = relationship("Material", back_populates="comments")
    ontology_source_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("ontology_source.ontology_source_id"), nullable=True)
    ontology_source: Mapped[Optional['OntologySource']] = relationship("OntologySource", back_populates="comments")
    ontology_annotation_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("ontology_annotation.ontology_annotation_id"), nullable=True)
    ontology_annotation: Mapped[Optional['OntologyAnnotation']] = relationship("OntologyAnnotation", back_populates="comments")
    person_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("person.person_id"), nullable=True)
    person: Mapped[Optional['Person']] = relationship("Person", back_populates="comments")
    process_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("process.process_id"), nullable=True)
    process: Mapped[Optional['Process']] = relationship("Process", back_populates="comments")
    protocol_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("protocol.protocol_id"), nullable=True)
    protocol: Mapped[Optional['Protocol']] = relationship("Protocol", back_populates="comments")
    publication_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("publication.publication_id"), nullable=True)
    publication: Mapped[Optional['Publication']] = relationship("Publication", back_populates="comments")
    sample_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("sample.sample_id"), nullable=True)
    sample: Mapped[Optional['Sample']] = relationship("Sample", back_populates="comments")
    source_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("source.source_id"), nullable=True)
    source: Mapped[Optional['Source']] = relationship("Source", back_populates="comments")
    study_factor_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("factor.factor_id"), nullable=True)
    study_factor: Mapped[Optional['StudyFactor']] = relationship("StudyFactor", back_populates="comments")
    study_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("study.study_id"), nullable=True)
    study: Mapped[Optional['Study']] = relationship("Study", back_populates="comments")

    def to_json(self) -> dict:
        """Return a JSON representation of the Comment object

        :return: JSON representation of the Comment object
        """
        return {"comment_id": self.comment_id, "name": self.name, "value": self.value}


def make_comment_methods() -> None:
    """This function will dynamically add the methods to the Comment class that are required to interact with the
    database. This is done to avoid circular imports and to extra dependencies in the models package. It's called
    in the init of the database models package.
    """

    def to_sql(self) -> Comment:
        """Convert the Comment object to a SQLAlchemy object so that it can be added to the database.

        :param self: the Comment object. Will be injected automatically.

        :return: The SQLAlchemy object ready to committed to the database session.
        """
        return Comment(name=self.name, value=self.value)

    setattr(CommentModel, "to_sql", to_sql)
    setattr(CommentModel, "get_table", make_get_table_method(Comment))
