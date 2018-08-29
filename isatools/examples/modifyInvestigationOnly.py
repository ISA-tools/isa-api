#!/usr/bin/env python

from isatools.isatab import load, dumps
from isatools.model import *


def modify_investigation(fp):
    """Load, edit, and dump an ISA-Tab 1.0 descriptor."""

    # Load an existing ISA-Tab investigation file. In this example, we load an
    # unpopulated i_investigation.txt file
    investigation = load(fp, skip_load_tables=True)
    investigation.identifier = "i1"
    investigation.title = "My Simple ISA Investigation"
    investigation.description = \
        "We could alternatively use the class constructor's parameters to " \
        "set some default values at the time of creation, however we want " \
        "to demonstrate how to use the object's instance variables to set " \
        "values."
    investigation.submission_date = "2016-11-03"
    investigation.public_release_date = "2016-11-03"

    study = Study(filename="s_study.txt")
    study.identifier = "s1"
    study.title = "My ISA Study"
    study.description = \
        "Like with the Investigation, we could use the class constructor to " \
        "set some default values, but have chosen to demonstrate in this " \
        "example the use of instance variables to set initial values."
    study.submission_date = "2016-11-03"
    study.public_release_date = "2016-11-03"
    investigation.studies[0] = study

    obi = OntologySource(name='OBI',
                         description="Ontology for Biomedical Investigations")
    investigation.ontology_source_references.append(obi)
    intervention_design = OntologyAnnotation(term_source=obi)
    intervention_design.term = "intervention design"
    intervention_design.term_accession = \
        "http://purl.obolibrary.org/obo/OBI_0000115"
    study.design_descriptors.append(intervention_design)

    # Other instance variables common to both Investigation and Study objects
    # include 'contacts' and 'publications' each with lists of corresponding
    # Person and Publication objects.

    contact = Person(first_name="Alice", last_name="Robertson",
                     affiliation="University of Life",
                     roles=[OntologyAnnotation(term='submitter')])
    study.contacts.append(contact)
    publication = Publication(title="Experiments with Elephants",
                              author_list="A. Robertson, B. Robertson")
    publication.pubmed_id = "12345678"
    publication.status = OntologyAnnotation(term="published")
    study.publications.append(publication)

    source = Source(name='source_material')
    study.sources.append(source)

    prototype_sample = Sample(name='sample_material', derives_from=[source])
    ncbitaxon = OntologySource(name='NCBITaxon', description="NCBI Taxonomy")
    characteristic_organism = Characteristic(
        category=OntologyAnnotation(term="Organism"),
        value=OntologyAnnotation(
            term="Homo Sapiens", term_source=ncbitaxon,
            term_accession="http://purl.bioontology.org/ontology/NCBITAXON/"
            "9606"))
    prototype_sample.characteristics.append(characteristic_organism)

    study.samples = batch_create_materials(prototype_sample, n=3)
    # creates a batch of 3 samples

    sample_collection_protocol = Protocol(
        name="sample collection",
        protocol_type=OntologyAnnotation(
            term="sample collection"))
    study.protocols.append(sample_collection_protocol)
    sample_collection_process = Process(
        executes_protocol=sample_collection_protocol)

    for src in study.sources:
        sample_collection_process.inputs.append(src)
    for sam in study.samples:
        sample_collection_process.outputs.append(sam)

    study.process_sequence.append(sample_collection_process)

    assay = Assay(filename="a_assay.txt")
    extraction_protocol = Protocol(
        name='extraction',
        protocol_type=OntologyAnnotation(term="material extraction"))
    study.protocols.append(extraction_protocol)
    sequencing_protocol = Protocol(
        name='sequencing',
        protocol_type=OntologyAnnotation(term="material sequencing"))
    study.protocols.append(sequencing_protocol)

    for i, sample in enumerate(study.samples):
        extraction_process = Process(executes_protocol=extraction_protocol)

        extraction_process.inputs.append(sample)
        material = Material(name="extract-{}".format(i))
        material.type = "Extract Name"
        extraction_process.outputs.append(material)

        sequencing_process = Process(executes_protocol=sequencing_protocol)
        sequencing_process.name = "assay-name-{}".format(i)
        sequencing_process.inputs.append(extraction_process.outputs[0])

        datafile = DataFile(filename="sequenced-data-{}".format(i),
                            label="Raw Data File")
        sequencing_process.outputs.append(datafile)

        extraction_process.next_process = sequencing_process
        sequencing_process.prev_process = extraction_process

        assay.samples.append(sample)
        assay.data_files.append(datafile)
        assay.other_material.append(material)
        assay.process_sequence.append(extraction_process)
        assay.process_sequence.append(sequencing_process)
        assay.measurement_type = OntologyAnnotation(term="gene sequencing")
        assay.technology_type = \
            OntologyAnnotation(term="nucleotide sequencing")

    study.assays.append(assay)

    # dumps() writes out the ISA as a string representation of the ISA-Tab,
    # but we are skipping writing tables
    return dumps(investigation, skip_dump_tables=True)


if __name__ == '__main__':
    with open('i_investigation.txt') as fp:
        print(modify_investigation(fp))  # print the result to stdout
