import unittest
import datetime
from isatools.model.v1 import Investigation, OntologySourceReference, Publication, OntologyAnnotation, Study, \
    StudyFactor, Assay, Contact, Protocol, Process, Source, Material, MaterialAttribute, Data, Sample, Comment


class ISAModelTests(unittest.TestCase):

    # FIXME: Does not test Comments yet

    def test_build_isa_objects(self):

        # comment = Comment(
        #     name="",
        #     value=""
        # )

        # ONTOLOGY SOURCE REFERENCE
        ontology_source_reference = OntologySourceReference(
            name="",
            description="",
            file="",
            version=""
        )

        # ONTOLOGY ANNOTATION
        ontology_annotation = OntologyAnnotation(
            name="",
            termSource=ontology_source_reference,
            termAccession=""
        )

        # PUBLICATION
        publication = Publication(
            pubMedID="",
            DOI="",
            authorList="",
            title="",
            status=ontology_annotation
        )

        # CONTACT
        contact = Contact(
            lastName="",
            firstName="",
            midInitials="",
            address="",
            affiliation=""
        )
        contact.roles.append(ontology_annotation)

        # INVESTIGATION
        investigation = Investigation(
            identifier="",
            title="",
            description="",
            submission_date=datetime.date,
            public_release_date=datetime.date
        )
        investigation.ontologySourceReferences.append(ontology_source_reference)
        investigation.publications.append(publication)
        investigation.contacts.append(contact)

        # PROTOCOL
        protocol = Protocol(
            name="",
            protocolType=ontology_annotation,
            description="",
            uri="",
            version=""
        )
        protocol.parameters.append(ontology_annotation)
        protocol.components.append(ontology_annotation)

        # MATERIAL ATTRIBUTE
        material_attribute = MaterialAttribute(
            ontologyAnnotation=ontology_annotation
        )

        # SOURCE
        source = Source(
            name=""
        )
        source.characteristics.append(material_attribute)

        # FACTOR
        factor = StudyFactor(
            name="",
            type=ontology_annotation
        )

        # SAMPLE
        sample = Sample(
            name=""
        )
        sample.characteristics.append(material_attribute)
        sample.factors.append(factor)

        # MATERIAL
        material = Material(name="")
        material.characteristics.append(material_attribute)

        # DATA
        data = Data(name="")

        # PROCESS
        process = Process(
            name="",
            executesProtocol=protocol,
        )
        process.parameters.append(ontology_annotation)
        process.inputs.append(material)
        process.inputs.append(data)
        process.outputs.append(material)
        process.outputs.append(data)

        #STUDY
        study = Study(
            identifier="",
            title="",
            description="",
            submission_date=datetime.date,
            public_release_date=datetime.date,
            file_name=""
        )
        study.publications.append(publication)
        study.contacts.append(contact)
        study.design_descriptors.append(ontology_annotation)
        study.protocols.append(protocol)
        study.sources.append(source)
        study.samples.append(sample)
        study.process_sequence.append(process)

        assay = Assay(
            fileName="",
            measurementType=ontology_annotation,
            technologyType=ontology_annotation,
            technologyPlatform=""
        )

        study.assays.append(assay)

        study.samples.append(sample)
        study.processSequence.append(process)
        investigation.studies.append(study)

        from json import dumps
        print(dumps(investigation, indent=4, sort_keys=True))

