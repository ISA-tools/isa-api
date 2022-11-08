from typing import List
from datetime import datetime
import dateutil.parser as date

from isatools.model import (
    Investigation as InvestigationModel,
    OntologyAnnotation as OntologyAnnotationModel,
    OntologySource as OntologySourceModel,
    ProtocolParameter as ParameterModel,
    Person as PersonModel,
    Process as ProcessModel,
    Protocol as ProtocolModel,
    Publication as PublicationModel,
    Study as StudyModel,

    Comment as CommentModel
)
from isatools.database.models import (
    Investigation as InvestigationTable,
    OntologyAnnotation as OntologyAnnotationTable,
    OntologySource as OntologySourceTable,
    Parameter as ParameterTable,
    Person as PersonTable,
    Process as ProcessTable,
    Protocol as ProtocolTable,
    Publication as PublicationTable,
    Study as StudyTable,

    Comment as CommentTable
)


def make_get_table_method(target: type) -> callable:
    @staticmethod
    def get_table():
        return target
    return get_table


def make_comment_methods() -> None:
    def to_sql(self) -> CommentTable:
        return CommentTable(name=self.name, value=self.value)

    setattr(CommentModel, 'to_sql', to_sql)
    setattr(CommentModel, 'get_table', make_get_table_method(CommentTable))


def make_investigation_methods() -> None:
    def to_sql(self) -> dict:
        identifier: str = self.identifier
        isa_identifier: str = self.id
        title: str = self.title
        description: str = self.description
        submission_date: datetime or None = None
        publication_date: datetime or None = None
        comments: List[CommentModel] = self.comments
        studies: List[StudyModel] = self.studies
        contacts: List[PersonModel] = self.contacts
        publications: List[PublicationModel] = self.publications
        ontology_source_references: List[OntologySourceModel] = self.ontology_source_references

        if self.submission_date:
            submission_date = date.parse(self.submission_date)
        if self.public_release_date:
            publication_date = date.parse(self.public_release_date)

        investigation: InvestigationTable = InvestigationTable(
            isa_identifier=isa_identifier, identifier=identifier, title=title, description=description,
            submission_date=submission_date, public_release_date=publication_date,
            comments=[comment.to_sql() for comment in comments],
            studies=[study.to_sql() for study in studies],
            contacts=[person.to_sql() for person in contacts],
            publications=[publication.to_sql() for publication in publications],
            ontology_source_reference=[ontology_source.to_sql() for ontology_source in ontology_source_references]
        )

        return investigation

    setattr(InvestigationModel, 'to_sql', to_sql)
    setattr(InvestigationModel, 'get_table', make_get_table_method(InvestigationTable))


def make_ontology_annotation_methods() -> None:
    def to_sql(self):
        return OntologyAnnotationTable(
            id=self.id,
            annotation_value=self.term,
            term_accession=self.term_accession,
            term_source_id=self.term_source.name if self.term_source else None,
            comments=[comment.to_sql() for comment in self.comments]
        )
    setattr(OntologyAnnotationModel, 'to_sql', to_sql)
    setattr(OntologyAnnotationModel, 'get_table', make_get_table_method(OntologyAnnotationTable))


def make_ontology_source_methods() -> None:
    def to_sql(self):
        return OntologySourceTable(
            id=self.name,
            name=self.name,
            file=self.file,
            version=self.version,
            description=self.description,
        )
    setattr(OntologySourceModel, 'to_sql', to_sql)
    setattr(OntologySourceModel, 'get_table', make_get_table_method(OntologySourceTable))


def make_parameter_methods() -> None:
    def to_sql(self):
        return ParameterTable(
            id=self.id,
            ontology_annotation=self.parameter_name.to_sql()
        )

    setattr(ParameterModel, 'to_sql', to_sql)
    setattr(ParameterModel, 'get_table', make_get_table_method(ParameterTable))


def make_person_methods():
    def to_sql(self):
        return PersonTable(
            first_name=self.first_name,
            last_name=self.last_name,
            mid_initials=self.mid_initials,
            email=self.email,
            phone=self.phone,
            fax=self.fax,
            address=self.address,
            affiliation=self.affiliation,
            comments=[comment.to_sql() for comment in self.comments]
        )

    setattr(PersonModel, 'to_sql', to_sql)
    setattr(PersonModel, 'get_table', make_get_table_method(PersonTable))


def make_process_methods():
    def to_sql(self):
        return ProcessTable(
            id=self.id,
            name=self.name,
            performer=self.performer,
            date=datetime.strptime(self.date) if self.date else None,
            comments=[comment.to_sql() for comment in self.comments]
        )

    setattr(ProcessModel, 'to_sql', to_sql)
    setattr(ProcessModel, 'get_table', make_get_table_method(ProcessTable))


def make_protocol_methods():
    def to_sql(self):
        return ProtocolTable(
            id=self.id,
            name=self.name,
            description=self.description,
            uri=self.uri if self.uri else None,
            version=self.version if self.version else None,
            comments=[comment.to_sql() for comment in self.comments],
            protocol_parameters=[parameter.to_sql() for parameter in self.parameters],
            protocol_type_id=self.protocol_type.id if self.protocol_type else None
        )

    setattr(ProtocolModel, 'to_sql', to_sql)
    setattr(ProtocolModel, 'get_table', make_get_table_method(ProtocolTable))


def make_publication_methods():
    def to_sql(self):
        return PublicationTable(
            id=self.doi,
            author_list=self.author_list,
            doi=self.doi,
            pubmed_id=self.pubmed_id,
            title=self.title,
            comments=[comment.to_sql() for comment in self.comments]
        )

    setattr(PublicationModel, 'to_sql', to_sql)
    setattr(PublicationModel, 'get_table', make_get_table_method(PublicationTable))


def make_study_methods():
    def to_sql(self):
        title: str = self.title
        description: str = self.description
        filename: str = self.filename
        identifier: str = self.identifier
        submission_date: datetime or None = None
        public_release_date: datetime or None = None
        comments: List[CommentModel] = self.comments
        contacts: List[PersonModel] = self.contacts
        publications: List[PublicationModel] = self.publications
        design_descriptors: List[OntologyAnnotationModel] = self.design_descriptors
        protocols: List[ProtocolModel] = self.protocols

        if self.submission_date:
            submission_date = date.parse(self.submission_date)
        if self.public_release_date:
            public_release_date = date.parse(self.public_release_date)

        return StudyTable(
            title=title,
            description=description,
            filename=filename,
            identifier=identifier,
            submission_date=submission_date,
            public_release_date=public_release_date,
            contacts=[person.to_sql() for person in contacts],
            comments=[comment.to_sql() for comment in comments],
            publications=[publication.to_sql() for publication in publications],
            study_design_descriptors=[descriptor.to_sql() for descriptor in design_descriptors],
            protocols=[protocol.to_sql() for protocol in protocols]
        )

    setattr(StudyModel, 'to_sql', to_sql)
    setattr(StudyModel, 'get_table', make_get_table_method(StudyTable))


def make_methods():
    make_comment_methods()
    make_ontology_source_methods()
    make_ontology_annotation_methods()
    make_publication_methods()
    make_person_methods()

    make_parameter_methods()
    make_protocol_methods()
    make_process_methods()

    make_study_methods()
    make_investigation_methods()


make_methods()
