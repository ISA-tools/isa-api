#!/usr/bin/env python

from isatools.isatab import load, dumps
from isatools.model.v1 import *


def modify_investigation():
    """Load, edit, and dump an ISA-Tab 1.0 descriptor."""

    # Load an existing ISA-Tab investigation file. In this example, we load an unpopulated i_investigation.txt file

    with open('i_investigation.txt') as fp:
        investigation = load(fp, skip_load_tables=True)

        investigation.identifier = "i1"
        investigation.title = "My Simple ISA Investigation"
        investigation.description = "We could alternatively use the class constructor's parameters to set some default " \
                                    "values at the time of creation, however we want to demonstrate how to use the " \
                                    "object's instance variables to set values."
        investigation.submission_date = "2016-11-03"
        investigation.public_release_date = "2016-11-03"

        obi = OntologySource(name='OBI', description="Ontology for Biomedical Investigations")
        investigation.ontology_source_references.append(obi)

        study = Study(filename="s_study.txt")
        study.identifier = "s1"
        study.title = "My ISA Study"
        study.description = "Like with the Investigation, we could use the class constructor to set some default values, " \
                            "but have chosen to demonstrate in this example the use of instance variables to set initial " \
                            "values."
        study.submission_date = "2016-11-03"
        study.public_release_date = "2016-11-03"

        intervention_design = OntologyAnnotation(term_source=obi)
        intervention_design.term = "intervention design"
        intervention_design.term_accession = "http://purl.obolibrary.org/obo/OBI_0000115"
        study.design_descriptors.append(intervention_design)

        contact = Person(first_name="Alice", last_name="Robertson", affiliation="University of Life", roles=[OntologyAnnotation(term='submitter')])
        study.contacts.append(contact)
        publication = Publication(title="Experiments with Elephants", author_list="A. Robertson, B. Robertson")
        publication.pubmed_id = "12345678"
        publication.status = OntologyAnnotation(term="published")
        study.publications.append(publication)

        investigation.studies[0] = study  # replace the existing content with the new study we just created above

    return dumps(investigation, skip_dump_tables=True)  # dumps() writes out the ISA as a string representation of the ISA-Tab

if __name__ == '__main__':
    print(modify_investigation())  # print the result to stdout
