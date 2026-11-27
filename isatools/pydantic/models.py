"""Pydantic models for ISA JSON documents.

The models mirror the JSON Schemas in ``isatools/resources/schemas/isa_model_version_1_0_schemas/core``.
All fields are optional because those schemas declare no required properties.
Example::

    from isatools.pydantic import Investigation

    investigation = Investigation.model_validate(document)
    json_document = investigation.model_dump(by_alias=True, exclude_none=True)
"""

from __future__ import annotations

import abc
import pathlib
import re
from collections.abc import Iterable, Mapping
from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, Literal, Optional, Union
from uuid import uuid4

from isatools.model import Investigation as ISAToolsInvestigation
from isatools.pydantic.constants import JSON_CONTEXT_ROOT_DIR, JSONLD_CONTEXT_FOLDER_MAPPING, JSONLD_RAW_DOWNLOAD_URL

if TYPE_CHECKING:
    from isatools.model import Investigation as ISAToolsInvestigation


jsonld_context_map: dict[str, dict[str, Union[None, str]]] = {}

JSONLD_ENABLED = False

try:
    import rdflib
    from pyld import FileDocumentLoader, jsonld

    FileDocumentLoader.__class__
    JSONLD_ENABLED = True
except ImportError as exc:
    pass
except TypeError as exc:
    pass

PYDANTIC_ENABLED = False
try:
    from pydantic import (
        BaseModel,
        ConfigDict,
        Field,
        SerializationInfo,
        StrictFloat,
        StrictInt,
        ValidationInfo,
        field_validator,
        model_serializer,
        model_validator,
    )
    from pydantic.alias_generators import to_camel, to_snake

    PYDANTIC_ENABLED = True
except ImportError as exc:
    pass

if PYDANTIC_ENABLED:
    URIString = Annotated[str, Field(description="URI or URI reference as specified by the source schema")]
    AnnotationValue = Annotated[
        Union[str, StrictInt, StrictFloat], Field(description="Ontology annotation value (string or number).")
    ]
    DateValue = Annotated[
        Union[date, datetime, Literal[""]],
        Field(description="A date-time string, date-only string, or empty string; the property may be omitted."),
    ]

    class JsonLdConfiguration(BaseModel):
        """Settings for locating JSON-LD contexts used by ISA model classes."""

        jsonld_dir: Union[Path, str]
        filename_match_pattern: str
        context_id_prefix: str

    class LoadOptions(BaseModel):
        """Options used when parsing ISA JSON into Pydantic models."""

        jsonld_config: Annotated[
            Optional[JsonLdConfiguration],
            Field(description="Context lookup settings used to attach JSON-LD metadata to recognized model types."),
        ] = None
        generate_ids: Annotated[
            Optional[bool],
            Field(description="Generate an identifier for ISA entities that do not already have one."),
        ] = None

    class SerializationOptions(BaseModel):
        """Options that control JSON-LD metadata and empty-field handling during serialization."""

        jsonld_config: Annotated[
            Optional[JsonLdConfiguration],
            Field(description="Context lookup settings used to include JSON-LD metadata for recognized model types."),
        ] = None
        ignore_empty_fields: Annotated[
            Optional[bool],
            Field(description="Omit fields whose values are null, empty strings, or empty collections."),
        ] = None

    class CamelCaseModel(BaseModel):
        """Base configuration for ISA JSON models, including camel-case aliases."""

        model_config = ConfigDict(
            alias_generator=to_camel,
            populate_by_name=True,
            from_attributes=True,
            extra="forbid",
        )

    class JsonLdModel(CamelCaseModel):
        """Adds optional JSON-LD context and type metadata to an ISA JSON model."""

        context: Annotated[Optional[str], Field(description="JSON-LD context property (@context).")] = Field(
            default=None, alias="@context"
        )
        object_type: Annotated[
            Optional[str], Field(description="JSON-LD object type property (@type).", alias="@type")
        ] = Field(default=None, alias="@type")

        @model_validator(mode="after")
        def set_contextual_fields(self, info: ValidationInfo) -> ISAModel:
            """Set JSON-LD fields when the load context maps this model's class."""
            context = info.context
            if isinstance(context, LoadOptions) and context.jsonld_config:
                object_type = type(self).__name__
                context_id = self.find_context_id(context.jsonld_config)
                if context_id:
                    self.object_type = object_type
                    self.context = context_id
                if hasattr(self, "id") and self.id in (None, "") and context.generate_ids:
                    self.id = f"#{to_snake(type(self).__name__)}/{uuid4()}"

            return self

        @model_serializer(mode="wrap")
        def manage_serialization(self, handler: Any, info: SerializationInfo) -> Any:
            """Control JSON-LD output using ``SerializationOptions``.

            When enabled, include ``@type`` only if the model's class has a
            non-empty context URL in ``jsonld_map``. When disabled, remove both
            JSON-LD metadata fields from the output.
            """

            serialized = handler(self)
            if not isinstance(serialized, dict):
                return serialized

            options = info.context if isinstance(info.context, SerializationOptions) else None
            ignore_empty_fields = bool(options and options.ignore_empty_fields)
            if ignore_empty_fields:
                ignored_keys = []
                for key, val in serialized.items():
                    if self._is_empty_value(val):
                        ignored_keys.append(key)
                for key in ignored_keys:
                    serialized.pop(key, None)

            updated_datetime_values = {}
            for key, val in serialized.items():
                if isinstance(val, (date, datetime)):
                    updated_datetime_values[key] = val.isoformat()
            for key, updated_val in updated_datetime_values.items():
                serialized[key] = updated_val

            enable_jsonld = bool(options and options.jsonld_config)
            use_aliases = bool(info.by_alias)
            fields = JsonLdModel.model_fields

            if not enable_jsonld:
                for field_name, field in fields.items():
                    key = (field.serialization_alias or field.alias or field_name) if use_aliases else field_name
                    serialized.pop(key, None)
                return serialized
            else:
                object_type = type(self).__name__
                type_field = fields["object_type"]
                type_key = (
                    (type_field.serialization_alias or type_field.alias or "object_type")
                    if use_aliases
                    else "object_type"
                )

                context_field = fields["context"]
                context_key = (
                    (context_field.serialization_alias or context_field.alias or "context")
                    if use_aliases
                    else "context"
                )
                context_id = self.find_context_id(options.jsonld_config)
                if context_id:
                    serialized[type_key] = object_type
                    serialized[context_key] = context_id
                else:
                    serialized.pop(type_key, None)
                    if getattr(self, "context", None) is None:
                        serialized.pop(context_key, None)

            return serialized

        def find_context_id(self, jsonld_config: JsonLdConfiguration):
            if not jsonld_config:
                return None
            context_map = fetch_jsonld_context_map(
                jsonld_dir=jsonld_config.jsonld_dir,
                filename_match_pattern=jsonld_config.filename_match_pattern,
                context_id_prefix=jsonld_config.context_id_prefix,
            )
            object_type = type(self).__name__
            variants = context_map.get(object_type, {})
            return variants.get(self.get_context_object_variant())

        @classmethod
        def _is_empty_value(cls, val: Any) -> bool:
            return val is None or (isinstance(val, Iterable) and not val)

        def get_context_object_variant(self) -> str:
            return ""

    class ISAModel(JsonLdModel):
        """Base class for ISA entities that can carry a JSON-LD identifier."""

        model_config = ConfigDict(
            alias_generator=to_camel,
            populate_by_name=True,
            from_attributes=True,
            extra="forbid",
        )

        id: Annotated[Optional[str], Field(description="JSON-LD identifier property (@id).")] = Field(
            default=None, alias="@id"
        )

        @model_validator(mode="after")
        def set_id_field(self, info: ValidationInfo) -> ISAModel:
            """Generate a UUID-based ID when requested and no ID was supplied."""
            context = info.context
            if isinstance(context, LoadOptions) and self.id is None and context.generate_ids:
                self.id = f"#{to_snake(type(self).__name__)}/{uuid4()}"
            return self

    class Comment(ISAModel):
        """A named free-text annotation attached to an ISA object."""

        name: Annotated[
            Optional[str], Field(description="Comment label, unique within its containing ISA section or object.")
        ] = None
        value: Annotated[Optional[str], Field(description="Text recorded for this comment label.")] = None

    class Commentable(ISAModel):
        """Mixin for ISA schema objects with a ``comments`` array."""

        comments: Annotated[
            Optional[list[Comment]],
            Field(description="Comments associated with this object, as defined by its schema."),
        ] = Field(default_factory=list)

    class OntologyAnnotation(Commentable):
        """An ontology-backed or free-text value with optional source and accession."""

        annotation_value: Annotated[
            Optional[AnnotationValue],
            Field(description="The term label or literal value; values may be text or numeric."),
        ] = None
        term_source: Annotated[
            Optional[str],
            Field(
                description="Short name of the terminology source, matching a declared ontology source when available.",
            ),
        ] = None
        term_accession: Annotated[
            Optional[URIString],
            Field(description="Accession or URI identifying the term in its terminology source."),
        ] = None

        @field_validator("term_source", mode="before")
        @classmethod
        def set_term_source_field(cls, val: Any) -> ISAModel:
            if isinstance(val, str):
                return val or None
            if isinstance(val, Mapping):
                return val.get("name") or None
            return str(val) or None

    ScalarValue = Annotated[
        Union[OntologyAnnotation, StrictInt, StrictFloat, str],
        Field(description="A value represented by an ontology annotation, text, integer, or decimal number."),
    ]

    class OntologySourceReference(Commentable):
        """A terminology or ontology resource used to qualify annotations in an investigation."""

        description: Annotated[
            Optional[str],
            Field(description="Text that distinguishes or describes this terminology resource."),
        ] = None
        file: Annotated[
            Optional[str],
            Field(description="Location of the terminology resource, given as a file name or URI."),
        ] = None
        name: Annotated[
            Optional[str],
            Field(description="Short name used to refer to this terminology source elsewhere in the investigation."),
        ] = None
        version: Annotated[
            Optional[str],
            Field(description="Version of the terminology resource used for the study."),
        ] = None

    class Organization(ISAModel):
        """An organization associated with an ISA person or investigation."""

        name: Annotated[Optional[str], Field(description="Organization name.")] = None

    class Person(Commentable):
        """A person associated with an investigation or study, including contact details and roles."""

        last_name: Annotated[Optional[str], Field(description="Person's family name.")] = None
        first_name: Annotated[Optional[str], Field(description="Person's given name.")] = None
        mid_initials: Annotated[
            Optional[str],
            Field(description="Middle initials, if provided."),
        ] = None
        email: Annotated[
            Optional[str],
            Field(description="Email address for contacting the person."),
        ] = None
        phone: Annotated[Optional[str], Field(description="Telephone number for contacting the person.")] = None
        fax: Annotated[Optional[str], Field(description="Fax number for contacting the person.")] = None
        address: Annotated[Optional[str], Field(description="Postal or institutional address for the person.")] = None
        affiliation: Annotated[
            Optional[str],
            Field(description="Organization or institution with which the person is affiliated."),
        ] = None
        roles: Annotated[
            Optional[list[OntologyAnnotation]],
            Field(description="One or more roles the person has in this ISA context."),
        ] = Field(default_factory=list)

    class Publication(Commentable):
        """A publication associated with an investigation or study."""

        pub_med_id: Annotated[
            Optional[str],
            Field(alias="pubMedID", description="PubMed identifier for the publication, when available."),
        ] = None
        doi: Annotated[Optional[str], Field(description="Digital Object Identifier (DOI) for the publication.")] = None
        author_list: Annotated[
            Optional[str],
            Field(description="Publication author list as text."),
        ] = None
        title: Annotated[Optional[str], Field(description="Title of the publication.")] = None
        status: Annotated[
            Optional[OntologyAnnotation],
            Field(description="Publication status, such as published, submitted, or in preparation."),
        ] = None

    class MaterialAttribute(ISAModel):
        """A category that names a material characteristic, such as organism or strain."""

        characteristic_type: Annotated[
            Optional[OntologyAnnotation],
            Field(description="Term naming the characteristic category."),
        ] = None

    class Factor(Commentable):
        """An experimental factor, or independent variable, declared for a study."""

        factor_name: Annotated[
            Optional[str],
            Field(description="Name used to identify this factor and its values."),
        ] = None
        factor_type: Annotated[
            Optional[OntologyAnnotation],
            Field(description="Term describing the kind of factor, such as dose or time."),
        ] = None

    class ProtocolParameter(Commentable):
        """A parameter category declared for a protocol and used to label parameter values."""

        parameter_name: Annotated[
            Optional[OntologyAnnotation],
            Field(description="Term naming this protocol parameter category."),
        ] = None

    class ProtocolComponent(Commentable):
        """A named instrument, software package, detector, reagent, or other protocol component."""

        component_name: Annotated[
            Optional[str],
            Field(description="Name of the protocol component."),
        ] = None
        component_type: Annotated[
            Optional[OntologyAnnotation],
            Field(description="Term classifying the protocol component, such as instrument or software."),
        ] = None

    class Protocol(Commentable):
        """A named procedure referenced by process records in a study or assay."""

        name: Annotated[
            Optional[str], Field(description="Protocol name used as a reference within the ISA document.")
        ] = None
        protocol_type: Annotated[
            Optional[OntologyAnnotation],
            Field(description="Term classifying the protocol, such as sample collection or extraction."),
        ] = None
        description: Annotated[
            Optional[str],
            Field(description="Free-text description of how the protocol is performed."),
        ] = None
        uri: Annotated[
            Optional[URIString], Field(description="URI for an external resource describing the protocol.")
        ] = None
        version: Annotated[Optional[str], Field(description="Protocol version identifier.")] = None
        parameters: Annotated[
            Optional[list[ProtocolParameter]],
            Field(description="Parameter categories whose values may be recorded when the protocol is applied."),
        ] = Field(default_factory=list)
        components: Annotated[
            Optional[list[ProtocolComponent]],
            Field(description="Components used by or associated with the protocol."),
        ] = Field(default_factory=list)

    class Data(Commentable):
        """A data file, such as raw, derived, image, or spectral data."""

        name: Annotated[Optional[str], Field(description="File name or URI identifying the data file.")] = None
        data_type: Annotated[
            Optional[
                Literal[
                    "Raw Data File",
                    "Derived Data File",
                    "Image File",
                    "Acquisition Parameter Data File",
                    "Derived Spectral Data File",
                    "Protein Assignment File",
                    "Raw Spectral Data File",
                    "Peptide Assignment File",
                    "Array Data File",
                    "Derived Array Data File",
                    "Post Translational Modification Assignment File",
                    "Derived Array Data Matrix File",
                    "Free Induction Decay Data File",
                    "Metabolite Assignment File",
                    "Array Data Matrix File",
                ]
            ],
            Field(description="Category of data represented by the file."),
        ] = Field(default=None, alias="type")

    class ScalarValueModel(Commentable, abc.ABC):
        """Shared value and unit fields for characteristics, factors, and parameters."""

        value: Annotated[
            Optional[ScalarValue],
            Field(description="Qualitative or quantitative value, optionally represented by an ontology term."),
        ] = None
        unit: Annotated[
            Optional[OntologyAnnotation],
            Field(description="Unit qualifying a numeric value, optionally represented by an ontology term."),
        ] = None

        def get_context_object_variant(self) -> str:
            if isinstance(self.value, OntologyAnnotation):
                return "ontology"
            if isinstance(self.value, (int, float)):
                return "number"
            if self.unit:
                return "number"
            return ""

    class MaterialAttributeValue(ScalarValueModel):
        """ISA material attribute value (characteristic) object.

        Defined by ``core/material_attribute_value_schema.json``. Its ``value``
        may be an ontology annotation, a string, or a number.
        """

        model_config = model_config = ConfigDict(
            alias_generator=to_camel,
            populate_by_name=True,
            from_attributes=True,
            extra="forbid",
        )

        category: Annotated[
            Optional[MaterialAttribute],
            Field(description="Characteristic category that gives this value its meaning."),
        ] = None

    class FactorValue(ScalarValueModel):
        """Value of a study factor for a material, such as a sample."""

        category: Annotated[
            Optional[Factor],
            Field(description="Factor declaration that gives this value its meaning."),
        ] = None

    class ProcessParameterValue(ScalarValueModel):
        """Value of a protocol parameter recorded for a process application."""

        category: Annotated[
            Optional[ProtocolParameter],
            Field(description="Protocol parameter declaration that gives this value its meaning."),
        ] = None

    class Source(Commentable):
        """Starting biological material from which samples in a study are derived."""

        name: Annotated[
            Optional[str], Field(description="Source name used to identify the material in the study graph.")
        ] = None
        characteristics: Annotated[
            Optional[list[MaterialAttributeValue]],
            Field(description="Characteristics describing the source material."),
        ] = Field(default_factory=list)

    class Sample(Commentable):
        """A material produced or used in a study, excluding assay extracts and labeled extracts."""

        name: Annotated[
            Optional[str], Field(description="Sample name used to identify the material in the study graph.")
        ] = None
        characteristics: Annotated[
            Optional[list[MaterialAttributeValue]],
            Field(description="Characteristics describing the sample material."),
        ] = Field(default_factory=list)
        factor_values: Annotated[
            Optional[list[FactorValue]],
            Field(description="Values assigned to study factors for this sample."),
        ] = Field(default_factory=list)
        derives_from: Annotated[
            Optional[list[Source]],
            Field(description="Source materials from which this sample derives."),
        ] = Field(default_factory=list)

    class Material(Commentable):
        """An assay material that is neither a source nor a sample, such as an extract."""

        name: Annotated[
            Optional[str], Field(description="Material name used to identify the extract or labeled extract.")
        ] = None
        material_type: Annotated[
            Optional[Literal["Extract Name", "Labeled Extract Name"]],
            Field(description="Whether this material is an extract or a labeled extract."),
        ] = Field(default=None, alias="type")
        characteristics: Annotated[
            Optional[list[MaterialAttributeValue]],
            Field(description="Characteristics describing the material."),
        ] = Field(default_factory=list)

    class Materials(CamelCaseModel):
        """Material nodes declared in the study: sources, samples, and other materials."""

        sources: Annotated[
            Optional[list[Source]],
            Field(description="Starting biological materials for the study."),
        ] = Field(default_factory=list)
        samples: Annotated[
            Optional[list[Sample]],
            Field(description="Samples declared for the study."),
        ] = Field(default_factory=list)
        other_materials: Annotated[
            Optional[list[Material]],
            Field(description="Other study materials, excluding sources and samples."),
        ] = Field(default_factory=list)

    class AssayMaterials(CamelCaseModel):
        """Material nodes declared in an assay: samples and other assay materials."""

        samples: Annotated[
            Optional[list[Sample]],
            Field(description="Samples that enter or are referenced by the assay workflow."),
        ] = Field(default_factory=list)
        other_materials: Annotated[
            Optional[list[Material]],
            Field(description="Other assay materials, such as extracts and labeled extracts."),
        ] = Field(default_factory=list)

    class Process(Commentable):
        """An application of a protocol that links input materials to output materials or data."""

        name: Annotated[Optional[str], Field(description="Optional name distinguishing this process application.")] = (
            None
        )
        executes_protocol: Annotated[
            Optional[Protocol],
            Field(description="Protocol applied by this process."),
        ] = None
        parameter_values: Annotated[
            Optional[list[ProcessParameterValue]],
            Field(description="Parameter values recorded for this protocol application."),
        ] = Field(default_factory=list)
        performer: Annotated[Optional[str], Field(description="Name of the operator who carried out the process.")] = (
            None
        )
        date: Annotated[
            Optional[DateValue], Field(description="Date the protocol was performed, preferably in ISO 8601 format.")
        ] = None
        previous_process: Annotated[
            Optional[Process],
            Field(description="Process that immediately precedes this process, when known."),
        ] = None
        next_process: Annotated[
            Optional[Process],
            Field(description="Process that immediately follows this process, when known."),
        ] = None
        inputs: Annotated[
            Optional[list[Union[Source, Sample, Data, Material]]],
            Field(description="Materials or data consumed by this process."),
        ] = Field(default_factory=list)
        outputs: Annotated[
            Optional[list[Union[Sample, Data, Material]]],
            Field(description="Samples, materials, or data produced by this process."),
        ] = Field(default_factory=list)

    class Assay(Commentable):
        """Metadata and workflow for one assay, including materials, processes, and data files."""

        filename: Annotated[
            Optional[str], Field(description="Name or URI of the assay table file, when available.")
        ] = None
        measurement_type: Annotated[
            Optional[OntologyAnnotation],
            Field(description="What the assay measures, such as gene expression or protein identification."),
        ] = None
        technology_type: Annotated[
            Optional[OntologyAnnotation],
            Field(description="Technology used to make the measurement, such as mass spectrometry."),
        ] = None
        technology_platform: Annotated[
            Optional[str], Field(description="Manufacturer and platform name used for the assay.")
        ] = None
        data_files: Annotated[
            Optional[list[Data]],
            Field(description="Raw, derived, image, or other data files associated with the assay."),
        ] = Field(default_factory=list)
        materials: Annotated[
            Optional[AssayMaterials],
            Field(description="Samples and other materials represented in the assay workflow."),
        ] = None
        characteristic_categories: Annotated[
            Optional[list[MaterialAttribute]],
            Field(description="Characteristic categories used by materials in this assay."),
        ] = Field(default_factory=list)
        unit_categories: Annotated[
            Optional[list[OntologyAnnotation]],
            Field(description="Units used by numeric values in this assay."),
        ] = Field(default_factory=list)
        process_sequence: Annotated[
            Optional[list[Process]], Field(description="Ordered process applications that make up the assay workflow.")
        ] = Field(default_factory=list)

    class Study(Commentable):
        """Study metadata and the materials, protocols, factors, processes, and assays it defines."""

        filename: Annotated[
            Optional[str], Field(description="Name or URI of the study table file, when available.")
        ] = None
        identifier: Annotated[
            Optional[str], Field(description="Study identifier, supplied by the user or an archive.")
        ] = None
        title: Annotated[Optional[str], Field(description="Concise title describing the study's purpose.")] = None
        description: Annotated[Optional[str], Field(description="Text describing the study's objectives or goals.")] = (
            None
        )
        submission_date: Annotated[
            Optional[DateValue], Field(description="Date the study was submitted to an archive.")
        ] = None
        public_release_date: Annotated[
            Optional[DateValue], Field(description="Date the study was or is intended to be released publicly.")
        ] = None
        publications: Annotated[
            Optional[list[Publication]], Field(description="Publications associated with this study.")
        ] = Field(default_factory=list)
        people: Annotated[
            Optional[list[Person]], Field(description="People associated with or responsible for the study.")
        ] = Field(default_factory=list)
        study_design_descriptors: Annotated[
            Optional[list[OntologyAnnotation]],
            Field(description="Terms classifying the overall experimental design."),
        ] = Field(default_factory=list)
        protocols: Annotated[
            Optional[list[Protocol]],
            Field(description="Protocols referenced by processes in the study and its assays."),
        ] = Field(default_factory=list)
        materials: Annotated[
            Optional[Materials], Field(description="Sources, samples, and other materials declared for the study.")
        ] = None
        process_sequence: Annotated[
            Optional[list[Process]], Field(description="Study-level process applications and their material flow.")
        ] = Field(default_factory=list)
        assays: Annotated[Optional[list[Assay]], Field(description="Assays associated with this study.")] = Field(
            default_factory=list
        )
        factors: Annotated[
            Optional[list[Factor]], Field(description="Independent variables declared for the study.")
        ] = Field(default_factory=list)
        characteristic_categories: Annotated[
            Optional[list[MaterialAttribute]],
            Field(description="Characteristic categories used by study materials."),
        ] = Field(default_factory=list)
        unit_categories: Annotated[
            Optional[list[OntologyAnnotation]],
            Field(description="Units used by numeric values in the study."),
        ] = Field(default_factory=list)

    class Investigation(Commentable):
        """Root ISA object containing investigation metadata, shared declarations, and studies.

        An investigation groups one or more studies and may declare shared
        publications, contacts, and terminology sources.
        """

        filename: Annotated[
            Optional[str], Field(description="Name or URI of the investigation file, when available.")
        ] = None
        identifier: Annotated[
            Optional[str], Field(description="Repository accession or other identifier for the investigation.")
        ] = None
        title: Annotated[Optional[str], Field(description="Concise title describing the investigation.")] = None
        description: Annotated[Optional[str], Field(description="Text describing the overall investigation.")] = None
        submission_date: Annotated[
            Optional[DateValue], Field(description="Date the investigation was submitted to a repository.")
        ] = None
        public_release_date: Annotated[
            Optional[DateValue], Field(description="Date the investigation was or is intended to be released publicly.")
        ] = None
        ontology_source_references: Annotated[
            Optional[list[OntologySourceReference]],
            Field(description="Terminology sources used to qualify terms elsewhere in the investigation."),
        ] = Field(default_factory=list)
        publications: Annotated[
            Optional[list[Publication]], Field(description="Publications associated with the investigation.")
        ] = Field(default_factory=list)
        people: Annotated[
            Optional[list[Person]], Field(description="People associated with or responsible for the investigation.")
        ] = Field(default_factory=list)
        studies: Annotated[Optional[list[Study]], Field(description="Studies grouped within this investigation.")] = (
            Field(default_factory=list)
        )
        comments: Annotated[
            Optional[list[Comment]], Field(description="Free-text comments attached to the investigation.")
        ] = Field(default_factory=list)

        @classmethod
        def from_dict(
            cls,
            investigation_dict: Annotated[
                dict[str, Any], Field(description="ISA JSON object containing investigation data.")
            ],
            options: Annotated[
                Union[None, LoadOptions],
                Field(description="Optional settings for JSON-LD metadata and generated identifiers during loading."),
            ] = None,
        ) -> Investigation:
            """Validate an ISA JSON-shaped dictionary as an Investigation."""
            return Investigation.model_validate(investigation_dict, context=options)

        @classmethod
        def from_bytes(
            cls,
            json_data: Annotated[Union[bytes, bytearray], Field(description="UTF-8 encoded ISA JSON document bytes.")],
            options: Annotated[
                Union[None, LoadOptions],
                Field(description="Optional settings for JSON-LD metadata and generated identifiers during loading."),
            ] = None,
        ) -> Investigation:
            """Parse serialized ISA JSON bytes into an Investigation."""
            return Investigation.model_validate_json(json_data, context=options)

        @classmethod
        def from_str(
            cls,
            json_data: Annotated[str, Field(description="Serialized ISA JSON document text.")],
            options: Annotated[
                Union[None, LoadOptions],
                Field(description="Optional settings for JSON-LD metadata and generated identifiers during loading."),
            ] = None,
        ) -> Investigation:
            """Parse serialized ISA JSON str into an Investigation."""
            return Investigation.model_validate_json(json_data, context=options)

        @classmethod
        def from_file(
            cls,
            file: Annotated[Union[str, Path], Field(description="Path to the ISA JSON document to read.")],
            options: Annotated[
                Union[None, LoadOptions],
                Field(description="Optional settings for JSON-LD metadata and generated identifiers during loading."),
            ] = None,
        ) -> Investigation:
            """Read and validate an ISA JSON document from a file path."""
            if isinstance(file, str):
                file = Path(file)
            return cls.from_bytes(file.read_bytes(), options=options)

        def to_dict(
            self,
            options: Annotated[
                Union[None, SerializationOptions],
                Field(description="Optional settings for JSON-LD metadata and empty-field handling."),
            ] = None,
        ) -> dict[str, Any]:
            """Serialize to a dictionary using ISA JSON aliases.

            Args:
                options: Optional settings controlling JSON-LD fields in the output.
            """
            return self.model_dump(context=options, by_alias=True, exclude_none=True)

        def to_file(
            self,
            file: Annotated[Union[str, Path], Field(description="Path where the ISA JSON document will be written.")],
            options: Annotated[
                Union[None, SerializationOptions],
                Field(description="Optional settings for JSON-LD metadata and empty-field handling."),
            ] = None,
        ) -> None:
            """Write this Investigation as ISA JSON to a file path."""
            if isinstance(file, str):
                file = Path(file)
            content = self.model_dump_json(context=options, by_alias=True, exclude_none=True)
            file.write_text(content)

        def to_bytes(
            self,
            options: Annotated[
                Union[None, SerializationOptions],
                Field(description="Optional settings for JSON-LD metadata and empty-field handling."),
            ] = None,
        ) -> bytes:
            """Serialize this Investigation to UTF-8 encoded ISA JSON bytes."""
            return self.to_str(options=options).encode()

        def to_str(
            self,
            options: Annotated[
                Union[None, SerializationOptions],
                Field(description="Optional settings for JSON-LD metadata and empty-field handling."),
            ] = None,
        ) -> str:
            """Serialize this Investigation to an ISA JSON string."""
            content = self.model_dump_json(context=options, indent=2, by_alias=True, exclude_none=True)
            return content

        def to_jsonld_expanded(
            self,
            ontology: Annotated[
                Union[None, Literal["obo", "sio", "w3c", "wdt", "isaterms"]],
                Field(description="Built-in JSON-LD context to use when serialization_options is not supplied."),
            ] = None,
            serialization_options: Annotated[
                Union[None, SerializationOptions],
                Field(description="Settings with a JSON-LD config; cannot be combined with ontology."),
            ] = None,
            jsonld_expand_options: Annotated[
                Union[None, dict[str, Any]], Field(description="Options passed to PyLD's JSON-LD expansion operation.")
            ] = None,
            use_file_context_id_prefix: Annotated[
                bool,
                Field(description="Use local file URLs as context ID prefixes when building the built-in context."),
            ] = False,
        ) -> list[dict]:
            """Serialize and expand this Investigation as JSON-LD.

            Provide either an ontology name to build a JSON-LD configuration,
            or ``serialization_options`` with an existing configuration.
            """
            if not JSONLD_ENABLED:
                raise Exception("install 'isatools[pydantic,jsonld]' and use python >=3.10")
            if (not ontology and not serialization_options) or (ontology and serialization_options):
                raise Exception("One of them must be provided: ontology, serialization_options")
            if serialization_options and not serialization_options.jsonld_config:
                raise Exception("JSONLD configuration is not provided in serialization_options")

            if not serialization_options:
                jsonld_config = self.get_jsonld_config(
                    ontology=ontology, use_file_context_id_prefix=use_file_context_id_prefix
                )
                serialization_options = SerializationOptions(jsonld_config=jsonld_config, ignore_empty_fields=True)
            inv_dict = self.to_dict(options=serialization_options)
            return jsonld.expand(inv_dict, options=jsonld_expand_options or {})

        def to_rdf_dataset(
            self,
            ontology: Annotated[
                Union[None, Literal["obo", "sio", "w3c", "wdt", "isaterms"]],
                Field(description="Built-in JSON-LD context to use when serialization_options is not supplied."),
            ] = None,
            serialization_options: Annotated[
                Union[None, SerializationOptions],
                Field(description="Settings with a JSON-LD config; cannot be combined with ontology."),
            ] = None,
            jsonld_expand_options: Annotated[
                Union[None, dict[str, Any]], Field(description="Options passed to PyLD's JSON-LD expansion operation.")
            ] = None,
            rdf_options: Annotated[
                Union[None, dict[str, Any]], Field(description="Options passed to PyLD's RDF conversion operation.")
            ] = None,
            use_file_context_id_prefix: Annotated[
                bool,
                Field(description="Use local file URLs as context ID prefixes when building the built-in context."),
            ] = False,
        ) -> rdflib.Dataset:
            """Convert this Investigation to an RDFLib dataset.

            The Investigation is serialized and expanded as JSON-LD, converted
            to N-Quads, and parsed into an ``rdflib.Dataset``. Provide either
            an ontology name to build a JSON-LD configuration, or
            ``serialization_options`` with an existing configuration.
            """
            if not JSONLD_ENABLED:
                raise Exception("install 'isatools[pydantic,jsonld]' and use python >=3.10")
            if (not ontology and not serialization_options) or (ontology and serialization_options):
                raise Exception("One of them must be provided: ontology, serialization_options")
            if serialization_options and not serialization_options.jsonld_config:
                raise Exception("JSONLD configuration is not provided in serialization_options")

            if not serialization_options:
                jsonld_config = self.get_jsonld_config(
                    ontology=ontology, use_file_context_id_prefix=use_file_context_id_prefix
                )
                _serialization_options = SerializationOptions(jsonld_config=jsonld_config, ignore_empty_fields=True)
            else:
                _serialization_options = serialization_options.model_copy()

            _serialization_options.ignore_empty_fields = True
            jsonld_document = self.to_jsonld_expanded(
                serialization_options=_serialization_options, jsonld_expand_options=jsonld_expand_options
            )
            rdf_options = dict(rdf_options or {})
            rdf_options["format"] = "application/n-quads"

            nquads = jsonld.to_rdf(jsonld_document, options=rdf_options)

            dataset = rdflib.Dataset()
            dataset.parse(data=nquads, format="nquads")
            return dataset

        @classmethod
        def from_isatools_model(
            cls,
            investigation: Annotated[
                ISAToolsInvestigation,
                Field(description="An existing isatools.model.Investigation instance to convert."),
            ],
        ) -> Investigation:
            """Create this model from an ``isatools.model.Investigation``.

            The ISA model's ``to_dict`` method supplies the JSON-compatible shape
            for nested objects and maps legacy contacts to the schema's people.
            """
            if not isinstance(investigation, ISAToolsInvestigation):
                raise TypeError("investigation must be an isatools.model.Investigation")

            def normalize_empty_dates(value: Any) -> Any:
                if isinstance(value, dict):
                    return {
                        key: normalize_empty_dates(item)
                        for key, item in value.items()
                        if not (key in {"submissionDate", "publicReleaseDate", "date"} and item == "")
                    }
                if isinstance(value, list):
                    return [normalize_empty_dates(item) for item in value]
                return value

            return cls.model_validate(normalize_empty_dates(investigation.to_dict()))

        def to_isatools_model(self) -> ISAToolsInvestigation:
            """Convert this object to an ``isatools.model.Investigation``."""
            from isatools.model import Investigation as ISAToolsInvestigation

            isa_investigation = ISAToolsInvestigation()
            isa_investigation.from_dict(self.model_dump(mode="json", by_alias=True, exclude_none=True))
            if self.filename is not None:
                isa_investigation.filename = self.filename
            return isa_investigation

        @classmethod
        def _remove_empty_fields(cls, value: Any) -> Any:
            """Recursively remove fields with ``None``, empty-string, or empty-list values.

            The same empty values are filtered from nested lists. Empty dictionaries,
            zero, and ``False`` are preserved.
            """
            if isinstance(value, dict):
                cleaned = {}
                for key, item in value.items():
                    cleaned_item = cls._remove_empty_fields(item)
                    if cleaned_item is None or cleaned_item == "" or cleaned_item == []:
                        continue
                    cleaned[key] = cleaned_item
                return cleaned

            if isinstance(value, list):
                cleaned = [cls._remove_empty_fields(item) for item in value]
                return [item for item in cleaned if not cls._is_empty_value(item)]

            return value

        @staticmethod
        def get_jsonld_config(
            ontology: Annotated[
                Literal["obo", "sio", "w3c", "wdt", "isaterms"],
                Field(description="Name of the built-in ontology context to load."),
            ],
            use_file_context_id_prefix: Annotated[
                bool, Field(description="Use local file URLs as context ID prefixes instead of remote URLs.")
            ] = False,
        ) -> JsonLdConfiguration:
            folder_name = JSONLD_CONTEXT_FOLDER_MAPPING.get(ontology)
            jsonld_dir = Path(JSON_CONTEXT_ROOT_DIR) / folder_name
            context_id_prefix = f"{JSONLD_RAW_DOWNLOAD_URL}/{folder_name}/"
            if use_file_context_id_prefix:
                context_id_prefix = f"file://{jsonld_dir}/"

            if not folder_name:
                raise Exception("Unsupported JSONLD context")
            return JsonLdConfiguration(
                jsonld_dir=jsonld_dir,
                filename_match_pattern=f"isa_(.+)_{folder_name}_context.jsonld",
                context_id_prefix=context_id_prefix,
            )

    __all__ = [
        "Assay",
        "AssayMaterials",
        "Comment",
        "Data",
        "Factor",
        "FactorValue",
        "ISAModel",
        "Investigation",
        "Material",
        "MaterialAttribute",
        "MaterialAttributeValue",
        "Materials",
        "OntologyAnnotation",
        "OntologySourceReference",
        "Organization",
        "Person",
        "Process",
        "ProcessParameterValue",
        "Protocol",
        "ProtocolComponent",
        "ProtocolParameter",
        "Publication",
        "Sample",
        "Source",
        "Study",
    ]

    JSONLD_CONTEXT_MODELS: list[Commentable] = [
        Assay,
        Comment,
        Data,
        Factor,
        FactorValue,
        Investigation,
        Material,
        MaterialAttribute,
        MaterialAttributeValue,
        OntologyAnnotation,
        OntologySourceReference,
        Organization,
        Person,
        Process,
        ProcessParameterValue,
        Protocol,
        ProtocolComponent,
        ProtocolParameter,
        Publication,
        Sample,
        Source,
        Study,
    ]

    def fetch_jsonld_context_map(
        jsonld_dir: Union[pathlib.Path, str], filename_match_pattern: str, context_id_prefix: str
    ) -> dict[str, Union[None, dict[str, str]]]:
        """Return model-name to context-file mappings.

        Args:
            jsonld_dir: Optional directory to search.

        Returns:
            A mapping from Pydantic model class name to its context file path.
        """
        context_map: Union[None, dict[str, str]] = jsonld_context_map.get(context_id_prefix, None)
        if context_map is not None:
            return context_map
        context_map = {}
        context_dir = jsonld_dir if isinstance(jsonld_dir, pathlib.Path) else pathlib.Path(jsonld_dir)

        files = sorted(context_dir.glob("*.jsonld"))

        for model in JSONLD_CONTEXT_MODELS:
            if isinstance(model, abc.ABC):
                continue
            model_name = model.__name__
            snake_name = to_snake(model_name)
            context_map[model_name] = None
            for path in files:
                match = re.match(filename_match_pattern, path.name)
                if match:
                    name = to_snake(match.groups()[0])
                    if name in (snake_name, f"{snake_name}_number", f"{snake_name}_ontology", f"{snake_name}_string"):
                        if not context_map.get(model_name):
                            context_map[model_name] = {}
                        variant = name.replace(snake_name, "", 1).strip("_")
                        context_map[model_name][variant] = context_id_prefix + path.name

        jsonld_context_map[context_id_prefix] = context_map
        return context_map
