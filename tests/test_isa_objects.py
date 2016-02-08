from unittest import TestCase
from isatools.model.v1 import *


class ModelTests(TestCase):

    def test_object_comment(self):
        comment = Comment(
            name='',
            value=''
        )
        self.assertIsInstance(comment.name, str)
        self.assertIsInstance(comment.value, str)
        # TODO: Implement test on Comments in other objects

    def test_object_ontology_source_reference(self):
        ontology_source_reference = OntologySourceReference(
            name='',
            description='',
            file='',
            version=''
        )
        self.assertIsInstance(ontology_source_reference.name, str)
        self.assertIsInstance(ontology_source_reference.description, str)
        self.assertIsInstance(ontology_source_reference.file, str)
        self.assertIsInstance(ontology_source_reference.version, str)

    def test_object_ontology_annotation(self):
        ontology_annotation = OntologyAnnotation(
            name='',
            term_source=OntologySourceReference(),
            term_accession=''
        )
        self.assertIsInstance(ontology_annotation.name, str)
        self.assertIsInstance(ontology_annotation.term_source, OntologySourceReference)
        self.assertIsInstance(ontology_annotation.term_accession, str)

    def test_object_publication(self):
        publication = Publication(
            pubmed_id='',
            doi='',
            author_list='',
            title='',
            status=OntologyAnnotation()
        )
        self.assertIsInstance(publication.pubmed_id, str)
        self.assertIsInstance(publication.doi, str)
        self.assertIsInstance(publication.author_list, str)
        self.assertIsInstance(publication.title, str)
        self.assertIsInstance(publication.status, OntologyAnnotation)

    def test_object_contact(self):
        contact = Person(
            last_name='',
            first_name='',
            mid_initials='',
            address='',
            affiliation=''
        )
        contact.roles.append(OntologyAnnotation())
        self.assertIsInstance(contact.first_name, str)
        self.assertIsInstance(contact.mid_initials, str)
        self.assertIsInstance(contact.last_name, str)
        self.assertIsInstance(contact.address, str)
        self.assertIsInstance(contact.affiliation, str)
        self.assertIsInstance(contact.roles, list)
        self.assertIsInstance(contact.roles[0], OntologyAnnotation)

    def test_object_investigation(self):
        investigation = Investigation(
            identifier='',
            title='',
            description='',
            submission_date=date.today(),
            public_release_date=date.today()
        )
        investigation.ontology_source_references.append(OntologySourceReference())
        investigation.publications.append(Publication())
        investigation.contacts.append(Person())
        investigation.studies.append(Study())
        self.assertIsInstance(investigation.identifier, str)
        self.assertIsInstance(investigation.title, str)
        self.assertIsInstance(investigation.description, str)
        self.assertIsInstance(investigation.submission_date, date)
        self.assertIsInstance(investigation.public_release_date, date)
        self.assertIsInstance(investigation.ontology_source_references, list)
        self.assertIsInstance(investigation.ontology_source_references[0], OntologySourceReference)
        self.assertIsInstance(investigation.publications, list)
        self.assertIsInstance(investigation.publications[0], Publication)
        self.assertIsInstance(investigation.contacts, list)
        self.assertIsInstance(investigation.contacts[0], Person)
        self.assertIsInstance(investigation.studies, list)
        self.assertIsInstance(investigation.studies[0], Study)

    def test_object_protocol(self):
        protocol = Protocol(
            name='',
            protocol_type=OntologyAnnotation(),
            description='',
            uri='',
            version=''
        )
        protocol.parameters.append(OntologyAnnotation())
        protocol.components.append(OntologyAnnotation())
        self.assertIsInstance(protocol.name, str)
        self.assertIsInstance(protocol.protocol_type, OntologyAnnotation)
        self.assertIsInstance(protocol.description, str)
        self.assertIsInstance(protocol.uri, str)
        self.assertIsInstance(protocol.version, str)

    def test_object_material_attribute(self):
        material_attribute = MaterialAttribute(
            characteristic=OntologyAnnotation(),
            unit=OntologyAnnotation()
        )
        self.assertIsInstance(material_attribute.characteristic, OntologyAnnotation)
        self.assertIsInstance(material_attribute.unit, OntologyAnnotation)

    def test_object_source(self):
        source = Source(
            name=''
        )
        source.characteristics.append(MaterialAttribute())
        self.assertIsInstance(source.name, str)
        self.assertIsInstance(source.characteristics, list)
        self.assertIsInstance(source.characteristics[0], MaterialAttribute)

    def test_object_study_factor(self):
        factor = StudyFactor(
            name='',
            factor_type=OntologyAnnotation()
        )
        self.assertIsInstance(factor.name, str)
        self.assertIsInstance(factor.factor_type, OntologyAnnotation)

    def test_object_sample(self):
        sample = Sample(
            name=''
        )
        sample.characteristics.append(MaterialAttribute())
        sample.factor_values.append(StudyFactor())
        self.assertIsInstance(sample.name, str)
        self.assertIsInstance(sample.characteristics, list)
        self.assertIsInstance(sample.characteristics[0], MaterialAttribute)
        self.assertIsInstance(sample.factor_values, list)
        self.assertIsInstance(sample.factor_values[0], StudyFactor)

    def test_object_material(self):
        material = Material(name='')
        material.characteristics.append(MaterialAttribute())
        self.assertIsInstance(material.name, str)
        self.assertIsInstance(material.characteristics, list)
        self.assertIsInstance(material.characteristics[0], MaterialAttribute)

    def test_object_data(self):
        data = Data(name='')
        self.assertIsInstance(data.name, str)

    def test_object_process(self):
        process = Process(
            name='',
            executes_protocol=Protocol(),
        )
        process.parameter_values.append(OntologyAnnotation())
        process.inputs.append(Material())
        process.inputs.append(Data())
        process.outputs.append(Material())
        process.outputs.append(Data())
        self.assertIsInstance(process.name, str)
        self.assertIsInstance(process.executes_protocol, Protocol)
        self.assertIsInstance(process.parameter_values, list)
        self.assertIsInstance(process.parameter_values[0], OntologyAnnotation)
        self.assertIsInstance(process.inputs, list)
        self.assertIsInstance(process.inputs[0], Material)
        self.assertIsInstance(process.inputs[1], Data)
        self.assertIsInstance(process.outputs, list)
        self.assertIsInstance(process.outputs[0], Material)
        self.assertIsInstance(process.outputs[1], Data)

    def test_object_assay(self):
        assay = Assay(
            filename='',
            measurement_type=OntologyAnnotation(),
            technology_type=OntologyAnnotation(),
            technology_platform=''
        )
        self.assertIsInstance(assay.filename, str)
        self.assertIsInstance(assay.measurement_type, OntologyAnnotation)
        self.assertIsInstance(assay.technology_type, OntologyAnnotation)
        self.assertIsInstance(assay.technology_platform, str)

    def test_object_study(self):
        study = Study(
            identifier='',
            title='',
            description='',
            submission_date=date.today(),
            public_release_date=date.today(),
            filename=''
        )
        study.publications.append(Publication())
        study.contacts.append(Person())
        study.design_descriptors.append(OntologyAnnotation())
        study.protocols.append(Protocol())
        study.materials['sources'].append(Source())
        study.materials['samples'].append(Sample())
        study.process_sequence.append(Process())
        study.assays.append(Assay())
        study.materials['samples'].append(Sample())
        self.assertIsInstance(study.identifier, str)
        self.assertIsInstance(study.title, str)
        self.assertIsInstance(study.description, str)
        self.assertIsInstance(study.submission_date, date)
        self.assertIsInstance(study.public_release_date, date)
        self.assertIsInstance(study.filename, str)
        self.assertIsInstance(study.publications, list)
        self.assertIsInstance(study.publications[0], Publication)
        self.assertIsInstance(study.contacts, list)
        self.assertIsInstance(study.contacts[0], Person)
        self.assertIsInstance(study.design_descriptors, list)
        self.assertIsInstance(study.design_descriptors[0], OntologyAnnotation)
        self.assertIsInstance(study.protocols, list)
        self.assertIsInstance(study.protocols[0], Protocol)
        self.assertIsInstance(study.materials['sources'], list)
        self.assertIsInstance(study.materials['sources'][0], Source)
        self.assertIsInstance(study.materials['samples'], list)
        self.assertIsInstance(study.materials['samples'][0], Sample)
        self.assertIsInstance(study.process_sequence, list)
        self.assertIsInstance(study.process_sequence[0], Process)
        self.assertIsInstance(study.assays, list)
        self.assertIsInstance(study.assays[0], Assay)
        self.assertIsInstance(study.materials['samples'], list)
        self.assertIsInstance(study.materials['samples'][0], Sample)

    def test_batch_create_materials(self):
        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material')
        batch = batch_create_materials(prototype_sample, n=10)
        batch_set_attr(batch, 'derives_from', source)
        self.assertEqual(len(batch), 10)
        self.assertIsInstance(batch, list)
        self.assertIsInstance(batch[0], Sample)
        self.assertIsInstance(batch[0].derives_from, Source)
        self.assertEqual(batch[0].derives_from, batch[9].derives_from)

