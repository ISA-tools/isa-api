import datetime
import csv
__author__ = 'dj'

class Comment(object):
    """A comment allows arbitrary annotation of all ISA classes
    
    Attributes:
        name: The name of the comment (as mapped to Comment[SomeName]) to give context to the comment field
        value: A value for the corresponding comment, as a string encoded in some way
        isa_element: If applicable, the ISA class attribute the comment relates to. If blank, it is assumed
            that the comment relates to the ISA class
    """
    def __init__(self):
        self.name = ""
        self.value = ""
        self.isa_element = ""

class IsaObject(object):
    """ An ISA Object is an abstract class to enable containment of Comments
    
    Attributes:
        comments: Comments associated with the implementing ISA class (all ISA classes)
    """
    def __init__(self):
        self.comments = []

class Investigation(IsaObject):
    """An investigation maintains metadata about the project context and links to one or more studies. There can only
    be 1 Investigation in an ISA package. Investigations has the following properties:

    Attributes:
        identifier: A locally unique identifier or an accession number provided by a repository.
        title: A concise name given to the investigation
        description: A textual description of the investigation
        submissionDate: The date on which the investigation was reported to the repository.
        publicReleaseDate: The date on which the investigation should be released publicly
        ontologySourceReferences: This annotation section is identical to that in the MAGE-TAB format.
        publications: Publications associated with an Investigation.
        contacts: People/contacts associated with an Investigation.
        studies: Study is the central unit, containing information on the subject under study, its characteristics and
        any treatments applied.
    """

    def __init__(self):
        """Return an empty Investigation object with default set to empty values."""
        self.identifier = ""
        self.title = ""
        self.description = ""
        self.submissionDate = datetime.date
        self.publicReleaseDate = datetime.date
        self.ontologySourceReferences = []
        self.publications = []
        self.contacts = []
        self.studies = []


class OntologySourceReference(IsaObject):
    """This annotation section is identical to that in the MAGE-TAB format.

    Attributes:
        name: The name of the source of a term; i.e. the source controlled vocabulary or ontology.
        file: A file name or a URI of an official resource.
        version: The version number of the Term Source to support terms tracking.
        description: Use for disambiguating resources when homologous prefixes have been used.
    """

    def __init__(self):
        """Returns an empty OntologySourceReference object with default set to empty values"""
        self.name = ""
        self.file = ""
        self.version = ""
        self.description = ""

class OntologyAnnotation(IsaObject):
    """An ontology term annotation reference

    Attributes:
        termSource: The abbreviated ontology name. It should correspond to one of the sources as specified in the
        ontologySourceReference section of the Investigation.
        termAccession: URI
    """

    def __init__(self):
        self.termSource = ""
        self.ontologySourceReference = ""


class Publication(IsaObject):
    """A publication associated with an investigation or study.

    Attributes:
        pubMedID: The PubMed IDs of the described publication(s) associated with this investigation.
        DOI: A Digital Object Identifier (DOI) for that publication (where available).
        authorList: The list of authors associated with that publication.
        title: The title of publication associated with the investigation.
        status: A term describing the status of that publication (i.e. submitted, in preparation, published).
    """

    def __init__(self):
        """Return an empty Publication object with default set to empty"""
        self.pubMedID = ""
        self.DOI = ""
        self.authorList = ""
        self.title = ""
        self.status = ""


class Person(IsaObject):
    """A person/contact that can be attributed to an Investigation or Study.

    Attributes:
        lastName: The last name of a person associated with the investigation.
        firstName: The first name of a person associated with the investigation.
        midInitials: The middle initials of a person associated with the investigation.
        email: The email address of a person associated with the investigation.
        phone: The telephone number of a person associated with the investigation.
        fax: The fax number of a person associated with the investigation.
        address: The address of a person associated with the investigation.
        affiliation: The organization affiliation for a person associated with the investigation.
        roles: Term to classify the role(s) performed by this person in the context of the investigation,
        which means that the roles reported here need not correspond to roles held withing their
        affiliated organization.
    """

    def __init__(self):
        """Return an empty Person object with default set to empty"""
        self.lastName = ""
        self.firstName = ""
        self.midInitials = ""
        self.email = ""
        self.phone = ""
        self.fax = ""
        self.address = ""
        self.affiliation = ""
        self.roles = ""


class Study(IsaObject):
    """Study is the central unit, containing information on the subject under study, its characteristics
    and any treatments applied.

    Attributes:
        identifier: A unique identifier: either a temporary identifier supplied by users or one generated by a
        repository or other database.
        title: A concise phrase used to encapsulate the purpose and goal of the study.
        description: A textual description of the study, with components such as objective or goals.
        submissionDate: The date on which the study is submitted to an archive.
        publicReleaseDate: The date on which the study should be released publicly.
        fileName: A field to specify the name of the Study file corresponding the definition of that Study.
        designDescriptors: Classifications of the study based on the overall experimental design.
        publications: Publications associated with a Study.
        contacts: People/contacts associated with a Study.
        factors: A factor corresponds to an independent variable manipulated by the experimentalist with the intention
        to affect biological systems in a way that can be measured by an assay.
        protocols: Protocols used within the ISA artifact.
        assays: An Assay represents a portion of the experimental design.
    """

    def __init__(self):
        """Return an empty Study object with default set to empty"""
        self.identifier = ""
        self.title = ""
        self.description = ""
        self.submissionDate = datetime.date
        self.publicReleaseDate = datetime.date
        self.fileName = ""
        self.designDescriptors = []
        self.publications = []
        self.contacts = []
        self.factors = []
        self.protocols = []
        self.assays = []


class StudyDesignDescriptor(IsaObject):
    """A Study Design Descriptor provides a term allowing the classification of the study based on the overall
    experimental design. The term can be free text (Attribute: name) or from, for example, a controlled vocabulary or
    an ontology (Attribute: ontologyReference).

    Attributes:
        name: Free text name for the term
        ontologyAnnotation: A representation of an ontology annotation
    """

    def __init__(self):
        self.name = ""
        self.ontologyAnnotation = OntologyAnnotation()


class StudyFactor(IsaObject):
    """A Study Factor corresponds to an independent variable manipulated by the experimentalist with the intention to
    affect biological systems in a way that can be measured by an assay.

    Attributes:
        name: Free text name for the term
        type: Study factor type as free text
        ontologyReference: A representation of an ontology source reference
    """

    def __init__(self):
        self.name = ""
        self.type = ""
        self.ontologyAnnotation = OntologyAnnotation()


class Assay(IsaObject):
    """A Study Assay declares and describes each of the Assay files associated with the current Study.

    Attributes:
    Measurement Type: A term to qualify the endpoint, or what is being measured (e.g. gene expression profiling or
    protein identification). The term can be free text or from, for example, a controlled vocabulary or an ontology.
    Technology Type: Term to identify the technology used to perform the measurement, e.g. DNA microarray, mass
    spectrometry. The term can be free text or from, for example, a controlled vocabulary or an ontology.
    Technology Platform: Manufacturer and platform name, e.g. Bruker AVANCE
    File Name: A field to specify the name of the Assay file corresponding the definition of that assay.
    """
    def __init__(self):
        self.measurementType = OntologyAnnotation()
        self.technologyType = OntologyAnnotation()
        self.fileName = ""


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
                i.ontologySourceReferences.append(o)
            row = next(rows)
        if row[0] == "Term Source File":
            for x in range(1, last_col):
                setattr(i.ontologySourceReferences[x-1], "file", row[x])
            row = next(rows)
        if row[0] == "Term Source Version":
            for x in range(1, last_col):
                setattr(i.ontologySourceReferences[x-1], "version", row[x])
            row = next(rows)
        if row[0] == "Term Source Description":
            for x in range(1, last_col):
                setattr(i.ontologySourceReferences[x-1], "description", row[x])
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
            submission_date = datetime.date(row[1])
            i.submissionDate = submission_date
            row = next(rows)
        if row[0] == "Investigation Public Release Date":
            public_release_date = datetime.date(row[1])
            i.publicReleaseDate = public_release_date
    row = next(rows)
    if row[0] == "INVESTIGATION PUBLICATIONS":
        # Create Publication objects and add to Investigation object
        row = next(rows)
        cols = len(row)
        last_col = cols -1
        if row[0] == "Investigation PubMed ID":
            for x in range(1, last_col):
                p = Publication()
                p.pubMedID = row[x]
                i.publications.append(p)
            row = next(rows)
        if row[0] == "Investigation Publication DOI":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "authorList", row[x])
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
                c = Person()
                c.lastName = row[x]
                i.contacts.append(c)
            row = next(rows)
        if row[0] == "Investigation Person First Name":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "firstName", row[x])
            row = next(rows)
        if row[0] == "Investigation Person Mid Initials":
            for x in range(1, last_col):
                setattr(i.publications[x-1], "midInitials", row[x])
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
            s.submissionDate = datetime.date(row[1])
            row = next(rows)
        if row[0] == "Study Public Release Date":
            s.publicReleaseDate = datetime.date(row[1])
            row = next(rows)
        if row[0] == "Study File Name":
            s.fileName = datetime.date(row[1])
            row = next(rows)
        if row[0] == "STUDY DESIGN DESCRIPTORS":
            row = next(rows)
            cols = len(row)
            last_col = cols -1
            if row[0] == "Study Design Type":
                for x in range(1, last_col):
                    d = StudyDesignDescriptor
                    d.name = row[x]
                    s.designDescriptors.append(d)
                row = next(rows)
        if row[0] == "STUDY PUBLICATIONS":
            # Create Publication objects and add to Investigation object
            row = next(rows)
            cols = len(row)
            last_col = cols-1
            if row[0] == "Study PubMed ID":
                for x in range(1, last_col):
                    p = Publication()
                    p.pubMedID = row[x]
                    s.publications.append(p)
                row = next(rows)
            if row[0] == "Study Publication DOI":
                for x in range(1, last_col):
                    setattr(s.publications[x-1], "authorList", row[x])
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
                    a.measurementType = row[x]
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



def write_isarchive(loc):
    # Write out an ISA archive to a given location
    pass