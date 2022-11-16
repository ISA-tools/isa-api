from sqlalchemy import Column, ForeignKey

from isatools.database.utils import Base, Table

""" ---------------------------------  ---------------------------------- --------------------------------
                                                INVESTIGATIONS
---------------------------------  ---------------------------------- -------------------------------- """

investigation_publications = Table(
    "investigation_publications",
    Base.metadata,
    Column("investigation_id", ForeignKey("investigation.investigation_id"), primary_key=True),
    Column("publication_id", ForeignKey("publication.publication_id"), primary_key=True),
    comment="Many to many relationship between Investigations and Publications",
)

investigation_ontology_source = Table(
    "investigation_ontology_source",
    Base.metadata,
    Column("investigation_id", ForeignKey("investigation.investigation_id"), primary_key=True),
    Column("ontology_source", ForeignKey("ontology_source.ontology_source_id"), primary_key=True),
    comment="Many to many relationship between Investigations and Ontology Sources",
)


""" ---------------------------------  ---------------------------------- --------------------------------
                                                STUDIES
---------------------------------  ---------------------------------- -------------------------------- """

study_publications = Table(
    "study_publications",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("publication_id", ForeignKey("publication.publication_id"), primary_key=True),
    comment="Many to many relationship between Studies and Publications"
)

study_design_descriptors = Table(
    "study_design_descriptors",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("ontology_annotation_id", ForeignKey("ontology_annotation.ontology_annotation_id"), primary_key=True),
    comment="Many to many relationship between Studies design descriptors (Ontology Annotations)"
)

study_protocols = Table(
    "study_protocols",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("protocol_id", ForeignKey("protocol.protocol_id"), primary_key=True),
    comment="Many to many relationship between Studies and Protocols"
)

study_sources = Table(
    "study_sources",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("source_id", ForeignKey("source.source_id"), primary_key=True),
    comment="Many to many relationship between Studies and Sources"
)

study_samples = Table(
    "study_samples",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("sample_id", ForeignKey("sample.sample_id"), primary_key=True),
    comment="Many to many relationship between Studies and Samples"
)

study_materials = Table(
    "study_materials",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("material_id", ForeignKey("material.material_id"), primary_key=True),
    comment="Many to many relationship between Studies and Materials"
)

study_characteristic_categories = Table(
    "study_characteristic_categories",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("ontology_annotation_id", ForeignKey("ontology_annotation.ontology_annotation_id"), primary_key=True),
    comment="Many to many relationship between Studies and characteristic categories (Ontology Annotations)"
)

study_unit_categories = Table(
    "study_unit_categories",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("ontology_annotation_id", ForeignKey("ontology_annotation.ontology_annotation_id"), primary_key=True),
    comment="Many to many relationship between Studies and unit categories (Ontology Annotations)"
)

study_factors = Table(
    "study_factors",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("factor_id", ForeignKey("factor.factor_id"), primary_key=True),
    comment="Many to many relationship between Studies and FactorsValues"
)

study_assays = Table(
    "study_assays",
    Base.metadata,
    Column("study_id", ForeignKey("study.study_id"), primary_key=True),
    Column("assay_id", ForeignKey("assay.assay_id"), primary_key=True),
    comment="Many to many relationship between Studies and Assays"
)


""" ---------------------------------  ---------------------------------- --------------------------------
                                                ASSAYS
---------------------------------  ---------------------------------- -------------------------------- """

assay_unit_categories = Table(
    "assay_unit_categories",
    Base.metadata,
    Column("assay_id", ForeignKey("assay.assay_id"), primary_key=True),
    Column("ontology_annotation_id", ForeignKey("ontology_annotation.ontology_annotation_id"), primary_key=True),
    comment="Many to many relationship between Assays and unit categories (Ontology Annotations)"
)

assay_characteristic_categories = Table(
    "assay_characteristic_categories",
    Base.metadata,
    Column("assay_id", ForeignKey("assay.assay_id"), primary_key=True),
    Column("ontology_annotation_id", ForeignKey("ontology_annotation.ontology_annotation_id"), primary_key=True),
    comment="Many to many relationship between Assays and characteristic categories (Ontology Annotations)"
)

assay_samples = Table(
    "assay_samples",
    Base.metadata,
    Column("assay_id", ForeignKey("assay.assay_id"), primary_key=True),
    Column("sample_id", ForeignKey("sample.sample_id"), primary_key=True),
    comment="Many to many relationship between Assays and Samples"
)

assay_materials = Table(
    "assay_materials",
    Base.metadata,
    Column("assay_id", ForeignKey("assay.assay_id"), primary_key=True),
    Column("material_id", ForeignKey("material.material_id"), primary_key=True),
    comment="Many to many relationship between Assays and Materials"
)

assay_data_files = Table(
    "assay_data_files",
    Base.metadata,
    Column("assay_id", ForeignKey("assay.assay_id"), primary_key=True),
    Column("data_file_id", ForeignKey("datafile.datafile_id"), primary_key=True),
    comment="Many to many relationship between Assays and Data Files"
)

""" ---------------------------------  ---------------------------------- --------------------------------
                                                PROTOCOLS
---------------------------------  ---------------------------------- -------------------------------- """

protocol_parameters = Table(
    "protocol_parameters",
    Base.metadata,
    Column("protocol_id", ForeignKey("protocol.protocol_id"), primary_key=True),
    Column("parameter_id", ForeignKey("parameter.parameter_id"), primary_key=True),
    comment="Many to many relationship between Protocols and Parameters"
)


""" ---------------------------------  ---------------------------------- --------------------------------
                                                MATERIALS
---------------------------------  ---------------------------------- -------------------------------- """

source_characteristics = Table(
    "source_characteristics",
    Base.metadata,
    Column("source_id", ForeignKey("source.source_id"), primary_key=True),
    Column("characteristic_id", ForeignKey("characteristic.characteristic_id"), primary_key=True),
    comment="Many to many relationship between Sources and Characteristics"
)

sample_characteristics = Table(
    "sample_characteristics",
    Base.metadata,
    Column("sample_id", ForeignKey("sample.sample_id"), primary_key=True),
    Column("characteristic_id", ForeignKey("characteristic.characteristic_id"), primary_key=True),
    comment="Many to many relationship between Samples and Characteristics"
)

sample_derives_from = Table(
    "sample_derives_from",
    Base.metadata,
    Column("sample_id", ForeignKey("sample.sample_id"), primary_key=True),
    Column("source_id", ForeignKey("source.source_id"), primary_key=True),
    comment="Many to many relationship between Samples and Sources"
)

sample_factor_values = Table(
    "sample_factor_values",
    Base.metadata,
    Column("sample_id", ForeignKey("sample.sample_id"), primary_key=True),
    Column("factor_value_id", ForeignKey("factor_value.factor_value_id"), primary_key=True),
    comment="Many to many relationship between Samples and FactorValues"
)

materials_characteristics = Table(
    "materials_characteristics",
    Base.metadata,
    Column("material_id", ForeignKey("material.material_id"), primary_key=True),
    Column("characteristic_id", ForeignKey("characteristic.characteristic_id"), primary_key=True),
    comment="Many to many relationship between Materials and Characteristics"
)


""" ---------------------------------  ---------------------------------- --------------------------------
                                                PROCESS
---------------------------------  ---------------------------------- -------------------------------- """

process_inputs = Table(
    "process_inputs",
    Base.metadata,
    Column("process_id", ForeignKey("process.process_id"), primary_key=True),
    Column("input_id", ForeignKey("input_output.io_id"), primary_key=True),
    comment="Many to many relationship between Processes and Inputs"
)

process_outputs = Table(
    "process_outputs",
    Base.metadata,
    Column("process_id", ForeignKey("process.process_id"), primary_key=True),
    Column("output_id", ForeignKey("input_output.io_id"), primary_key=True),
    comment="Many to many relationship between Processes and Outputs"
)

process_parameter_values = Table(
    "process_parameter_values",
    Base.metadata,
    Column("process_id", ForeignKey("process.process_id"), primary_key=True),
    Column("parameter_value_id", ForeignKey("parameter_value.parameter_value_id"), primary_key=True),
    comment="Many to many relationship between Processes and ParameterValues"
)


""" ---------------------------------  ---------------------------------- --------------------------------
                                                PERSON
---------------------------------  ---------------------------------- -------------------------------- """

person_roles = Table(
    "person_roles",
    Base.metadata,
    Column("person_id", ForeignKey("person.person_id"), primary_key=True),
    Column("role_id", ForeignKey("ontology_annotation.ontology_annotation_id"), primary_key=True),
    comment="Many to many relationship between Persons and Roles (Ontology Annotations)"
)