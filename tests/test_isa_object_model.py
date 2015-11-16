import unittest
import json
from jsonschema import RefResolver, Draft4Validator
import os
from datetime import date
from isatools.model.v1 import Investigation, OntologySourceReference, Publication, OntologyAnnotation, Study, \
    StudyFactor, Assay, Contact, Protocol, Process, Source, Material, MaterialAttribute, Data, Sample, Comment


class ISAObjectTests(unittest.TestCase):

    def test_object_comment(self):
        comment = Comment(
            name="",
            value=""
        )
        assert(isinstance(comment.name, str))
        assert(isinstance(comment.value, str))
        # TODO: Implement test on Comments in other objects

    def test_object_ontology_source_reference(self):
        ontology_source_reference = OntologySourceReference(
            name="",
            description="",
            file="",
            version=""
        )
        assert(isinstance(ontology_source_reference.name, str))
        assert(isinstance(ontology_source_reference.description, str))
        assert(isinstance(ontology_source_reference.file, str))
        assert(isinstance(ontology_source_reference.version, str))

    def test_object_ontology_annotation(self):
        ontology_annotation = OntologyAnnotation(
            name="",
            term_source=OntologySourceReference(),
            term_accession=""
        )
        assert(isinstance(ontology_annotation.name, str))
        assert(isinstance(ontology_annotation.term_source, OntologySourceReference))
        assert(isinstance(ontology_annotation.term_accession, str))

    def test_object_publication(self):
        publication = Publication(
            pubmed_id="",
            doi="",
            author_list="",
            title="",
            status=OntologyAnnotation()
        )
        assert(isinstance(publication.pubmed_id, str))
        assert(isinstance(publication.doi, str))
        assert(isinstance(publication.author_list, str))
        assert(isinstance(publication.title, str))
        assert(isinstance(publication.status, OntologyAnnotation))

    def test_object_contact(self):
        contact = Contact(
            last_name="",
            first_name="",
            mid_initials="",
            address="",
            affiliation=""
        )
        contact.roles.append(OntologyAnnotation())
        assert(isinstance(contact.first_name, str))
        assert(isinstance(contact.mid_initials, str))
        assert(isinstance(contact.last_name, str))
        assert(isinstance(contact.address, str))
        assert(isinstance(contact.affiliation, str))
        assert(isinstance(contact.roles[0], OntologyAnnotation))

    def test_object_investigation(self):
        investigation = Investigation(
            identifier="",
            title="",
            description="",
            submission_date=date.today(),
            public_release_date=date.today()
        )
        investigation.ontology_source_references.append(OntologySourceReference())
        investigation.publications.append(Publication())
        investigation.contacts.append(Contact())
        investigation.studies.append(Study())
        assert(isinstance(investigation.identifier, str))
        assert(isinstance(investigation.title, str))
        assert(isinstance(investigation.description, str))
        assert(isinstance(investigation.submission_date, date))
        assert(isinstance(investigation.public_release_date, date))
        assert(isinstance(investigation.ontology_source_references[0], OntologySourceReference))
        assert(isinstance(investigation.publications[0], Publication))
        assert(isinstance(investigation.contacts[0], Contact))
        assert(isinstance(investigation.studies[0], Study))

    def test_object_protocol(self):
        protocol = Protocol(
            name="",
            protocol_type=OntologyAnnotation(),
            description="",
            uri="",
            version=""
        )
        protocol.parameters.append(OntologyAnnotation())
        protocol.components.append(OntologyAnnotation())
        assert(isinstance(protocol.name, str))
        assert(isinstance(protocol.protocol_type, OntologyAnnotation))
        assert(isinstance(protocol.description, str))
        assert(isinstance(protocol.uri, str))
        assert(isinstance(protocol.version, str))

    def test_object_material_attribute(self):
        material_attribute = MaterialAttribute(
            ontology_annotation=OntologyAnnotation()
        )
        assert(isinstance(material_attribute.ontology_annotation, OntologyAnnotation))

    def test_object_source(self):
        source = Source(
            name=""
        )
        source.characteristics.append(MaterialAttribute())
        assert(isinstance(source.name, str))
        assert(isinstance(source.characteristics[0], MaterialAttribute))

    def test_object_study_factor(self):
        factor = StudyFactor(
            name="",
            type_=OntologyAnnotation()
        )
        assert(isinstance(factor.name, str))
        assert(isinstance(factor.type, OntologyAnnotation))

    def test_object_sample(self):
        sample = Sample(
            name=""
        )
        sample.characteristics.append(MaterialAttribute())
        sample.factors.append(StudyFactor())
        assert(isinstance(sample.name, str))
        assert(isinstance(sample.characteristics[0], MaterialAttribute))
        assert(isinstance(sample.factors[0], StudyFactor))

    def test_object_material(self):
        material = Material(name="")
        material.characteristics.append(MaterialAttribute())
        assert(isinstance(material.name, str))
        assert(isinstance(material.characteristics[0], MaterialAttribute))

    def test_object_data(self):
        data = Data(name="")
        assert(isinstance(data.name, str))

    def test_object_process(self):
        process = Process(
            name="",
            executes_protocol=Protocol(),
        )
        process.parameters.append(OntologyAnnotation())
        process.inputs.append(Material())
        process.inputs.append(Data())
        process.outputs.append(Material())
        process.outputs.append(Data())
        assert(isinstance(process.name, str))
        assert(isinstance(process.executes_protocol, Protocol))
        assert(isinstance(process.parameters[0], OntologyAnnotation))
        assert(isinstance(process.inputs[0], Material))
        assert(isinstance(process.inputs[1], Data))
        assert(isinstance(process.outputs[0], Material))
        assert(isinstance(process.outputs[1], Data))

    def test_object_assay(self):
        assay = Assay(
            file_name="",
            measurement_type=OntologyAnnotation(),
            technology_type=OntologyAnnotation(),
            technology_platform=""
        )
        assert(isinstance(assay.file_name, str))
        assert(isinstance(assay.measurement_type, OntologyAnnotation))
        assert(isinstance(assay.technology_type, OntologyAnnotation))
        assert(isinstance(assay.technology_platform, str))

    def test_object_study(self):
        study = Study(
            identifier="",
            title="",
            description="",
            submission_date=date.today(),
            public_release_date=date.today(),
            file_name=""
        )
        study.publications.append(Publication())
        study.contacts.append(Contact())
        study.design_descriptors.append(OntologyAnnotation())
        study.protocols.append(Protocol())
        study.sources.append(Source())
        study.samples.append(Sample())
        study.process_sequence.append(Process())
        study.assays.append(Assay())
        study.samples.append(Sample())
        assert(isinstance(study.identifier, str))
        assert(isinstance(study.title, str))
        assert(isinstance(study.description, str))
        assert(isinstance(study.submission_date, date))
        assert(isinstance(study.public_release_date, date))
        assert(isinstance(study.file_name, str))
        assert(isinstance(study.publications[0], Publication))
        assert(isinstance(study.contacts[0], Contact))
        assert(isinstance(study.design_descriptors[0], OntologyAnnotation))
        assert(isinstance(study.protocols[0], Protocol))
        assert(isinstance(study.sources[0], Source))
        assert(isinstance(study.samples[0], Sample))
        assert(isinstance(study.process_sequence[0], Process))
        assert(isinstance(study.assays[0], Assay))
        assert(isinstance(study.samples[0], Sample))


class ISAObjectJsonWriterTest(unittest.TestCase):

    """Tests to_json() implementations by validating against the schemas"""

    def setUp(self):
        self._schemas_path = "../isatools/schemas/isa_model_version_1_0_schemas/core/"

    def _validate(self, isa_object, schema_file_name):
        schema = json.load(open(os.path.join(self._schemas_path + schema_file_name)))
        resolver = RefResolver("file://" + self._schemas_path + schema_file_name, schema)
        Draft4Validator(schema, resolver=resolver).validate(isa_object.to_json(), schema)

    def test_ontology_source_reference_to_json(self):
        self._validate(OntologySourceReference(), "ontology_source_reference_schema.json")

    def test_ontology_annotation_to_json(self):
        self._validate(OntologyAnnotation(), "ontology_annotation_schema.json")

    def test_publication_to_json(self):
        self._validate(Publication(), "publication_schema.json")

    def test_contact_to_json(self):
        self._validate(Contact(), "person_schema.json")

    def test_investigation_to_json(self):
        self._validate(Investigation(), "investigation_schema.json")

    def test_protocol_to_json(self):
        self._validate(Protocol(), "protocol_schema.json")

    def test_material_to_json(self):
        self._validate(Material(), "material_schema.json")

    def test_source_to_json(self):
        self._validate(Source(), "source_schema.json")

    def test_sample_to_json(self):
        self._validate(Sample(), "sample_schema.json")

    def test_study_factor_to_json(self):
        self._validate(StudyFactor(), "factor_schema.json")

    def test_data_to_json(self):
        self._validate(Data(), "data_schema.json")

    def test_process_to_json(self):
        self._validate(Process(), "process_schema.json")

    def test_material_attribute_to_json(self):
        self._validate(MaterialAttribute(), "material_attribute_schema.json")

    def test_assay_attribute_to_json(self):
        self._validate(Assay(), "assay_schema.json")

    def test_study_attribute_to_json(self):
        self._validate(Study(), "study_schema.json")