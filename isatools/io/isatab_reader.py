import csv
from isatools.model.v1 import *


def from_isarchive(isatab_dir):

    # build ISA objects from ISA-Tab ISArchive (zipped or not zipped?)
    print("Reading " + isatab_dir)
    # check that an investigation file is present. If more than one is present, throw an exception
    investigation_file = open(isatab_dir + "/i_investigation.txt")
    i = Investigation()
    # There is always everything in the Investigation file (for a valid ISATab), but portions can be empty
    rows = csv.reader(investigation_file, dialect="excel-tab")
    row = next(rows)
    # TODO Implement error checking to raise Exceptions when parsing picks up unexpected structure or content
    # TODO Handle Comments row parsing (can happen anywhere)
    # TODO Handle # comments
    # TODO Handle or skip OntologyAnnotations
    if row[0] == "ONTOLOGY SOURCE REFERENCE":
        # Create OntologySourceReference objects and add to Investigation object
        row = next(rows)
        cols = len(row)
        last_col = cols -1
        if row[0] == "Term Source Name":
            for x in range(1, last_col):
                o = OntologySourceReference()
                o.name = row[x]
                i.ontology_source_references.append(o)
            row = next(rows)
        if row[0] == "Term Source File":
            for x in range(1, last_col):
                setattr(i.ontology_source_references[x-1], "file", row[x])
            row = next(rows)
        if row[0] == "Term Source Version":
            for x in range(1, last_col):
                setattr(i.ontology_source_references[x-1], "version", row[x])
            row = next(rows)
        if row[0] == "Term Source Description":
            for x in range(1, last_col):
                setattr(i.ontology_source_references[x-1], "description", row[x])
    row = next(rows)
    if row[0] != "INVESTIGATION":
        # Populate Investigation object fields
        row = next(rows)
        if row[0] == "Investigation Identifier":
            i.identifier = row[1]
            row = next(rows)
        if row[0] == "Investigation Title":
            i.title = row[1]
            row = next(rows)
        if row[0] == "Investigation Description":
            i.description = row[1]
            row = next(rows)
        if row[0] == "Investigation Submission Date":
            submission_date = date(row[1])
            i.submissionDate = submission_date
            row = next(rows)
        if row[0] == "Investigation Public Release Date":
            public_release_date = date(row[1])
            i.publicReleaseDate = public_release_date
    row = next(rows)
    if row[0] == "INVESTIGATION PUBLICATIONS":
        # Create Publication objects and add to Investigation object
        row = next(rows)
        cols = len(row)
        last_col = cols - 1
        if row[0] == "Investigation PubMed ID":
            for x in range(1, last_col):
                p = Publication()
                p.pubmed_id = row[x]
                i.publications.append(p)
            row = next(rows)
        if row[0] == "Investigation Publication DOI":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "author_list", row[x])
            row = next(rows)
        if row[0] == "Investigation Publication Title":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "title", row[x])
            row = next(rows)
        if row[0] == "Investigation Publication Status":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "status", row[x])
        # TODO How to handle OntologyAnnotations?
    row = next(rows)
    if row[0] == "INVESTIGATION CONTACTS":
        # Create Publication objects and add to Investigation object
        row = next(rows)
        cols = len(row)
        last_col = cols -1
        if row[0] == "Investigation Person Last Name":
            for x in range(1, last_col):
                c = Contact()
                c.last_name = row[x]
                i.contacts.append(c)
            row = next(rows)
        if row[0] == "Investigation Person First Name":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "first_name", row[x])
            row = next(rows)
        if row[0] == "Investigation Person Mid Initials":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "mid_initials", row[x])
            row = next(rows)
        if row[0] == "Investigation Person Email":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "email", row[x])
            row = next(rows)
        if row[0] == "Investigation Person Phone":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "phone", row[x])
            row = next(rows)
        if row[0] == "Investigation Person Fax":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "fax", row[x])
            row = next(rows)
        if row[0] == "Investigation Person Address":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "address", row[x])
            row = next(rows)
        if row[0] == "Investigation Person Affiliation":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "affiliation", row[x])
            row = next(rows)
        if row[0] == "Investigation Person Roles":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "roles", row[x])
        # Currently missing OntologyAnnotation
    row = next(rows)
    while row[0] == "STUDY":
        row = next(rows)
        s = Study()
        if row[0] == "Study Identifier":
            s.identifier = row[1]
            row = next(rows)
        if row[0] == "Study Title":
            s.title = row[1]
            row = next(rows)
        if row[0] == "Study Description":
            s.description = row[1]
            row = next(rows)
        if row[0] == "Study Submission Date":
            s.submission_date = date(row[1])
            row = next(rows)
        if row[0] == "Study Public Release Date":
            s.public_release_date = date(row[1])
            row = next(rows)
        if row[0] == "Study File Name":
            s.file_name = date(row[1])
            row = next(rows)
        if row[0] == "STUDY DESIGN DESCRIPTORS":
            row = next(rows)
            cols = len(row)
            last_col = cols -1
            if row[0] == "Study Design Type":
                for x in range(1, last_col):
                    d = StudyDesignDescriptor()
                    d.name = row[x]
                    s.design_descriptors.append(d)
                row = next(rows)
        if row[0] == "STUDY PUBLICATIONS":
            # Create Publication objects and add to Investigation object
            row = next(rows)
            cols = len(row)
            last_col = cols-1
            if row[0] == "Study PubMed ID":
                for x in range(1, last_col):
                    p = Publication()
                    p.pubmed_id = row[x]
                    s.publications.append(p)
                row = next(rows)
            if row[0] == "Study Publication DOI":
                for x in range(1, last_col):
                    setattr(s.publications[x-1], "author_list", row[x])
                row = next(rows)
            if row[0] == "Study Publication Title":
                for x in range(1, last_col):
                    setattr(s.publications[x-1], "title", row[x])
                row = next(rows)
            if row[0] == "Study Publication Status":
                for x in range(1, last_col):
                    setattr(s.publications[x-1], "status", row[x])
        row = next(rows)
        if row[0] == "STUDY FACTORS":
            row = next(rows)
            cols = len(row)
            last_col = cols-1
            if row[0] == "Study Factor Name":
                for x in range(1, last_col):
                    f = StudyFactor()
                    f.name = row[x]
                    s.factors.append(f)
                row = next(rows)
            if row[0] == "Study Factor Type":
                for x in range(1, last_col):
                    setattr(s.factors[x-1], "type", row[x])
        row = next(rows)
        if row[0] == "STUDY ASSAYS":
            row = next(rows)
            cols = len(row)
            last_col = cols-1
            if row[0] == "Study Assay Measurement Type":
                for x in range(1, last_col):
                    a = Assay()
                    a.measurement_type = row[x]
                    s.assays.append(a)
                row = next(rows)
                if row[0] == "Study Assay Measurement Type Term Accession Number":
                    # Skip OntologyAnnotation.accessionNumber
                    pass
                row = next(rows)
                if row[0] == "Study Assay Technology Type":
                    # Skip OntologyAnnotation.sourceREF
                    pass
                row = next(rows)

        i.studies.append(s)
        return i
