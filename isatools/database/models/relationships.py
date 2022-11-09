from sqlalchemy import Column, Table, ForeignKey

from isatools.database.utils import Base

""" ---------------------------------  ---------------------------------- --------------------------------
                                                INVESTIGATIONS
---------------------------------  ---------------------------------- -------------------------------- """

investigation_publications = Table(
    "investigation_publications",
    Base.metadata,
    Column("investigation_id", ForeignKey("investigation.id"), primary_key=True),
    Column("publication_id", ForeignKey("publication.id"), primary_key=True),
    comment="Many to many relationship between Investigations and Publications",
)

investigation_ontology_source = Table(
    "investigation_ontology_source",
    Base.metadata,
    Column("investigation_id", ForeignKey("investigation.id"), primary_key=True),
    Column("ontology_source", ForeignKey("ontology_source.id"), primary_key=True),
    comment="Many to many relationship between Investigations and Ontology Sources",
)


""" ---------------------------------  ---------------------------------- --------------------------------
                                                STUDIES
---------------------------------  ---------------------------------- -------------------------------- """

study_publications = Table(
    "study_publications",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("publication_id", ForeignKey("publication.id"), primary_key=True),
    comment="Many to many relationship between Studies and Publications"
)

study_design_descriptors = Table(
    "study_design_descriptors",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("ontology_annotation_id", ForeignKey("ontology_annotation.id"), primary_key=True),
    comment="Many to many relationship between Studies design descriptors (Ontology Annotations)"
)

study_protocols = Table(
    "study_protocols",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("protocol_id", ForeignKey("protocol.id"), primary_key=True),
    comment="Many to many relationship between Studies and Protocols"
)

study_sources = Table(
    "study_sources",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("source_id", ForeignKey("source.id"), primary_key=True),
    comment="Many to many relationship between Studies and Sources"
)


""" ---------------------------------  ---------------------------------- --------------------------------
                                                PROTOCOLS
---------------------------------  ---------------------------------- -------------------------------- """

protocol_parameters = Table(
    "protocol_parameters",
    Base.metadata,
    Column("protocol_id", ForeignKey("protocol.id"), primary_key=True),
    Column("parameter_id", ForeignKey("parameter.id"), primary_key=True),
    comment="Many to many relationship between Protocols and Parameters"
)


""" ---------------------------------  ---------------------------------- --------------------------------
                                                MATERIALS
---------------------------------  ---------------------------------- -------------------------------- """

source_characteristics = Table(
    "source_characteristics",
    Base.metadata,
    Column("source_id", ForeignKey("source.id"), primary_key=True),
    Column("characteristic_id", ForeignKey("characteristic.id"), primary_key=True),
    comment="Many to many relationship between Sources and Characteristics"
)
