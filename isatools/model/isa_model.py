# from __future__ import annotations
#
# import json
# from datetime import date, datetime
# from pathlib import Path
# from typing import Any, Literal
#
# from pydantic import BaseModel, ConfigDict, Field
#
#
# class ISAObject(BaseModel):
#     model_config = ConfigDict(extra="forbid", populate_by_name=True)
#
#     id_: str | None = Field(default=None, alias="@id")
#     context_: str | None = Field(default=None, alias="@context")
#     type_: str | None = Field(default=None, alias="@type")
#
#     @property
#     def id(self) -> str | None:
#         return self.id_
#
#     @property
#     def context(self) -> str | None:
#         return self.context_
#
#     @property
#     def type(self) -> str | None:
#         return self.type_
#
#
# DateLike = date | datetime | str
#
#
# class Comment(ISAObject):
#     name: str | None = None
#     value: str | None = None
#
#
# class OntologyAnnotation(ISAObject):
#     annotationValue: str | int | float | None = None
#     termSource: str | None = None
#     termAccession: str | None = None
#     comments: list[Comment] | None = None
#
#
# class OntologySourceReference(ISAObject):
#     comments: list[Comment] | None = None
#     description: str | None = None
#     file: str | None = None
#     name: str | None = None
#     version: str | None = None
#
#
# class Organization(ISAObject):
#     name: str | None = None
#
#
# class Person(ISAObject):
#     lastName: str | None = None
#     firstName: str | None = None
#     midInitials: str | None = None
#     email: str | None = None
#     phone: str | None = None
#     fax: str | None = None
#     address: str | None = None
#     affiliation: str | None = None
#     roles: list[OntologyAnnotation] | None = None
#     comments: list[Comment] | None = None
#
#
# class Publication(ISAObject):
#     pubMedID: str | None = None
#     doi: str | None = None
#     authorList: str | None = None
#     title: str | None = None
#     status: OntologyAnnotation | None = None
#     comments: list[Comment] | None = None
#
#
# class Factor(ISAObject):
#     factorName: str | None = None
#     factorType: OntologyAnnotation | None = None
#     comments: list[Comment] | None = None
#
#
# class FactorValue(ISAObject):
#     category: Factor | None = None
#     value: OntologyAnnotation | str | int | float | None = None
#     unit: OntologyAnnotation | None = None
#     comments: list[Comment] | None = None
#
#
# class MaterialAttribute(ISAObject):
#     characteristicType: OntologyAnnotation | None = None
#
#
# class MaterialAttributeValue(ISAObject):
#     category: MaterialAttribute | None = None
#     value: OntologyAnnotation | str | int | float | None = None
#     unit: OntologyAnnotation | None = None
#     comments: list[Comment] | None = None
#
#
# class Data(ISAObject):
#     name: str | None = None
#     data_type: Literal[
#         "Raw Data File",
#         "Derived Data File",
#         "Image File",
#         "Acquisition Parameter Data File",
#         "Derived Spectral Data File",
#         "Protein Assignment File",
#         "Raw Spectral Data File",
#         "Peptide Assignment File",
#         "Array Data File",
#         "Derived Array Data File",
#         "Post Translational Modification Assignment File",
#         "Derived Array Data Matrix File",
#         "Free Induction Decay Data File",
#         "Metabolite Assignment File",
#         "Array Data Matrix File",
#     ] | None = Field(default=None, alias="type")
#     comments: list[Comment] | None = None
#
#
# class Source(ISAObject):
#     name: str | None = None
#     characteristics: list[MaterialAttributeValue] | None = None
#     comments: list[Comment] | None = None
#
#
# class Sample(ISAObject):
#     name: str | None = None
#     characteristics: list[MaterialAttributeValue] | None = None
#     factorValues: list[FactorValue] | None = None
#     derivesFrom: list[Source] | None = None
#     comments: list[Comment] | None = None
#
#
# class Material(ISAObject):
#     name: str | None = None
#     material_type: Literal["Extract Name", "Labeled Extract Name"] | None = Field(default=None, alias="type")
#     characteristics: list[MaterialAttributeValue] | None = None
#     comments: list[Comment] | None = None
#
#
# class ProtocolParameter(ISAObject):
#     parameterName: OntologyAnnotation | None = None
#     comments: list[Comment] | None = None
#
#
# class ProtocolComponent(ISAObject):
#     componentName: str | None = None
#     componentType: OntologyAnnotation | None = None
#     comments: list[Comment] | None = None
#
#
# class Protocol(ISAObject):
#     name: str | None = None
#     protocolType: OntologyAnnotation | None = None
#     description: str | None = None
#     uri: str | None = None
#     version: str | None = None
#     parameters: list[ProtocolParameter] | None = None
#     components: list[ProtocolComponent] | None = None
#     comments: list[Comment] | None = None
#
#
# class ProcessParameterValue(ISAObject):
#     category: ProtocolParameter | None = None
#     value: OntologyAnnotation | str | int | float | None = None
#     unit: OntologyAnnotation | None = None
#     comments: list[Comment] | None = None
#
#
# class ProcessInputOutputItem(ISAObject):
#     pass
#
#
# class Process(ISAObject):
#     name: str | None = None
#     executesProtocol: Protocol | None = None
#     parameterValues: list[ProcessParameterValue] | None = None
#     performer: str | None = None
#     date: DateLike | None = None
#     previousProcess: "Process | None" = None
#     nextProcess: "Process | None" = None
#     inputs: list[Source | Sample | Data | Material] | None = None
#     outputs: list[Sample | Data | Material] | None = None
#     comments: list[Comment] | None = None
#
#
# class AssayMaterials(BaseModel):
#     model_config = ConfigDict(extra="forbid", populate_by_name=True)
#
#     samples: list[Sample] | None = None
#     otherMaterials: list[Material] | None = None
#
#
# class Assay(ISAObject):
#     filename: str | None = None
#     measurementType: OntologyAnnotation | None = None
#     technologyType: OntologyAnnotation | None = None
#     technologyPlatform: str | None = None
#     dataFiles: list[Data] | None = None
#     materials: AssayMaterials | None = None
#     characteristicCategories: list[MaterialAttribute] | None = None
#     unitCategories: list[OntologyAnnotation] | None = None
#     processSequence: list[Process] | None = None
#     comments: list[Comment] | None = None
#
#
# class StudyMaterials(BaseModel):
#     model_config = ConfigDict(extra="forbid", populate_by_name=True)
#
#     sources: list[Source] | None = None
#     samples: list[Sample] | None = None
#     otherMaterials: list[Material] | None = None
#
#
# class Study(ISAObject):
#     filename: str | None = None
#     identifier: str | None = None
#     title: str | None = None
#     description: str | None = None
#     submissionDate: DateLike | None = None
#     publicReleaseDate: DateLike | None = None
#     publications: list[Publication] | None = None
#     people: list[Person] | None = None
#     studyDesignDescriptors: list[OntologyAnnotation] | None = None
#     protocols: list[Protocol] | None = None
#     materials: StudyMaterials | None = None
#     processSequence: list[Process] | None = None
#     assays: list[Assay] | None = None
#     factors: list[Factor] | None = None
#     characteristicCategories: list[MaterialAttribute] | None = None
#     unitCategories: list[OntologyAnnotation] | None = None
#     comments: list[Comment] | None = None
#
#
# class Investigation(ISAObject):
#     filename: str | None = None
#     identifier: str | None = None
#     title: str | None = None
#     description: str | None = None
#     submissionDate: DateLike | None = None
#     publicReleaseDate: DateLike | None = None
#     ontologySourceReferences: list[OntologySourceReference] | None = None
#     publications: list[Publication] | None = None
#     people: list[Person] | None = None
#     studies: list[Study] | None = None
#     comments: list[Comment] | None = None
#
#     @classmethod
#     def from_json_file(cls, path: str | Path) -> "Investigation":
#         with Path(path).open("r", encoding="utf-8") as fp:
#             return cls.model_validate(json.load(fp))
#
#     def to_json(self, *, by_alias: bool = True, **kwargs: Any) -> str:
#         return self.model_dump_json(by_alias=by_alias, **kwargs)
#
#
# ISAInvestigation = Investigation
#
#
# __all__ = [
#     "Comment",
#     "OntologyAnnotation",
#     "OntologySourceReference",
#     "Organization",
#     "Person",
#     "Publication",
#     "Factor",
#     "FactorValue",
#     "MaterialAttribute",
#     "MaterialAttributeValue",
#     "Data",
#     "Source",
#     "Sample",
#     "Material",
#     "ProtocolParameter",
#     "ProtocolComponent",
#     "Protocol",
#     "ProcessParameterValue",
#     "Process",
#     "AssayMaterials",
#     "Assay",
#     "StudyMaterials",
#     "Study",
#     "Investigation",
#     "ISAInvestigation",
# ]
