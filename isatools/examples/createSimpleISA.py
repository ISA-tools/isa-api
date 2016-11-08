#!/usr/bin/env python

from isatools.model.v1 import *


def create_descriptor():
    """Returns a simple but complete ISA-Tab 1.0 descriptor for illustration."""

    # Create an empty Investigation object and set some values to the instance variables.

    investigation = Investigation()
    investigation.title = "My Simple ISA Investigation"
    investigation.description = "We could alternatively use the class constructor's parameters to set some default " \
                                "values at the time of creation, however we want to demonstrate how to use the " \
                                "object's instance variables to set values."
    investigation.submission_date = "2016-11-03"
    investigation.public_release_date = "2016-11-03"

    # Create an empty Study object and set some values. The Study must have a filename, otherwise when we serialize it
    # to ISA-Tab we would not know where to write it. We must also attach the study to the investigation by adding it
    # to the 'investigation' object's list of studies.

    study = Study(filename="s_study.txt")
    study.title = "My ISA Study"
    study.description = "Like with the Investigation, we could use the class constructor to set some default values, " \
                        "but have chosen to demonstrate in this example the use of instance variables to set initial " \
                        "values."
    study.submission_date = "2016-11-03"
    study.public_release_date = "2016-11-03"
    investigation.studies.append(study)

    # Some instance variables are typed with different objects and lists of objects. For example, a Study can have a
    # list of design descriptors. A design descriptor is an Ontology Annotation describing the kind of study at hand.
    # Ontology Annotations should typically reference an Ontology Source. We demonstrate a mix of using the class
    # constructors and setting values with instance variables. Note that the OntologyAnnotation object
    # 'intervention_design' links its 'term_source' directly to the 'obi' object instance. To ensure the OntologySource
    # is encapsulated in the descriptor, it is added to a list of 'ontology_source_references' in the Investigation
    # object. The 'intervention_design' object is then added to the list of 'design_descriptors' held by the Study
    # object.

    obi = OntologySource(name='OBI', description="Ontology for Biomedical Investigations")
    investigation.ontology_source_references.append(obi)
    intervention_design = OntologyAnnotation(term_source=obi)
    intervention_design.term = "intervention design"
    intervention_design.term_accession = "http://purl.obolibrary.org/obo/OBI_0000115"
    study.design_descriptors.append(intervention_design)

    # Other instance variables common to both Investigation and Study objects include 'contacts' and 'publications',
    # each with lists of corresponding Person and Publication objects.

    contact = Person(first_name="Alice", last_name="Robertson", affiliation="University of Life")
    study.contacts.append(contact)
    publication = Publication(title="Experiments with Elephants", author_list="A. Robertson, B. Robertson")
    publication.pubmed_id = "12345678"
    publication.status = OntologyAnnotation(term="published")
    study.publications.append(publication)

    from isatools.isatab import dumps
    return dumps(investigation)  # dumps() writes out the ISA as a string representation of the ISA-Tab

if __name__ == '__main__':
    print(create_descriptor())
