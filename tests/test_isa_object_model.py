import unittest
import datetime
from isatools.model.v1 import Investigation, OntologySourceReference, Publication, OntologyAnnotation, Study, \
    StudyFactor, Assay, StudyProtocol, Contact


class ISAModelTests(unittest.TestCase):

    # FIXME: Does not test Comments yet
    # FIXME: Does not use StudyProtocol yet?

    def test_build_isa_objects(self):

        # INVESTIGATION
        investigation = Investigation(
            identifier="",
            title="",
            description="",
            submissionDate="",
            publicReleaseDate=""
        )

        ontology_source_reference = OntologySourceReference(
            name="",
            description="",
            file="",
            version=""
        )

        investigation.ontologySourceReferences.append(ontology_source_reference)

        ontology_annotation = OntologyAnnotation(
            name="",
            termSource=ontology_source_reference,
            termAccession=""
        )

        publication = Publication(
            pubMedID="",
            DOI="",
            authorList="",
            title="",
            status=ontology_annotation
        )
        investigation.publications.append(publication)

        study = Study(
            identifier="",
            title="",
            description="",
            submissionDate=datetime.date,
            publicReleaseDate=datetime.date,
            fileName=""
        )
        design_descriptor = ontology_annotation
        study.designDescriptors.append(design_descriptor)
        study.publications.append(publication)

        factor = StudyFactor(
            name="",
            type=ontology_annotation
        )
        study.factors.append(factor)

        assay = Assay(
            fileName="",
            measurementType=ontology_annotation,
            technologyType=ontology_annotation,
            technologyPlatform=""
        )

        study.assays.append(assay)

        protocol = StudyProtocol(
            name="",
            protocolType=ontology_annotation,
            description=""
        )

        contact = Contact(
            lastName="",
            firstName="",
            midInitials="",
            address="",
            affiliation=""
        )
        contact.roles.append(ontology_annotation)

        study.contacts.append(contact)

        investigation.studies.append(study)

        from json import dumps
        print(dumps(investigation, indent=4, sort_keys=True))

