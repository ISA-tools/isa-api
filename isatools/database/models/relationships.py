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

study_samples = Table(
    "study_samples",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("sample_id", ForeignKey("sample.id"), primary_key=True),
    comment="Many to many relationship between Studies and Samples"
)

study_characteristic_categories = Table(
    "study_characteristic_categories",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("ontology_annotation_id", ForeignKey("ontology_annotation.id"), primary_key=True),
    comment="Many to many relationship between Studies and characteristic categories (Ontology Annotations)"
)

study_unit_categories = Table(
    "study_unit_categories",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("ontology_annotation_id", ForeignKey("ontology_annotation.id"), primary_key=True),
    comment="Many to many relationship between Studies and unit categories (Ontology Annotations)"
)

study_factors = Table(
    "study_factors",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("factor_id", ForeignKey("factor.id"), primary_key=True),
    comment="Many to many relationship between Studies and FactorsValues"
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

sample_characteristics = Table(
    "sample_characteristics",
    Base.metadata,
    Column("sample_id", ForeignKey("sample.id"), primary_key=True),
    Column("characteristic_id", ForeignKey("characteristic.id"), primary_key=True),
    comment="Many to many relationship between Samples and Characteristics"
)

sample_derives_from = Table(
    "sample_derives_from",
    Base.metadata,
    Column("sample_id", ForeignKey("sample.id"), primary_key=True),
    Column("source_id", ForeignKey("source.id"), primary_key=True),
    comment="Many to many relationship between Samples and Sources"
)

sample_factor_values = Table(
    "sample_factor_values",
    Base.metadata,
    Column("sample_id", ForeignKey("sample.id"), primary_key=True),
    Column("factor_value_id", ForeignKey("factor_value.id"), primary_key=True),
    comment="Many to many relationship between Samples and FactorValues"
)

study_materials = Table(
    "study_materials",
    Base.metadata,
    Column("study_id", ForeignKey("study.id"), primary_key=True),
    Column("material_id", ForeignKey("material.id"), primary_key=True),
    comment="Many to many relationship between Studies and Materials"
)

materials_characteristics = Table(
    "materials_characteristics",
    Base.metadata,
    Column("material_id", ForeignKey("material.id"), primary_key=True),
    Column("characteristic_id", ForeignKey("characteristic.id"), primary_key=True),
    comment="Many to many relationship between Materials and Characteristics"
)