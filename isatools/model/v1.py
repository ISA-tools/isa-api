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
    def __init__(self, name="", value="", isa_element=None):
        self.name = name
        self.value = value
        self.isa_element = isa_element

class IsaObject(object):
    """ An ISA Object is an abstract class to enable containment of Comments
    
    Attributes:
        comments: Comments associated with the implementing ISA class (all ISA classes)
    """
    def __init__(self, comments=None):
        if comments is None:
            self.comments = []
        else:
            self.comments = comments

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

    def __init__(self, identifier="", title="", description="", submissionDate=datetime.date,
                 publicReleaseDate=datetime.date, ontologySourceReferences=None, publications=None, contacts=None,
                 studies=None, comments=None):
        super(Investigation, self).__init__(comments)
        self.identifier = identifier
        self.title = title
        self.description = description
        self.submissionDate = submissionDate
        self.publicReleaseDate = publicReleaseDate
        if ontologySourceReferences is None:
            self.ontologySourceReferences = []
        else:
            self.ontologySourceReferences = ontologySourceReferences
        if publications is None:
            self.publications = []
        else:
            self.publications = publications
        if contacts is None:
            self.contacts = []
        else:
            self.contacts = contacts
        if studies is None:
            self.studies = []
        else:
            self.studies = studies


class OntologySourceReference(IsaObject):
    """This annotation section is identical to that in the MAGE-TAB format.

    Attributes:
        name: The name of the source of a term; i.e. the source controlled vocabulary or ontology.
        file: A file name or a URI of an official resource.
        version: The version number of the Term Source to support terms tracking.
        description: Use for disambiguating resources when homologous prefixes have been used.
    """

    def __init__(self, name="", file="", version="", description="", comments=None):
        super(OntologySourceReference, self).__init__(comments)
        self.name = name
        self.file = file
        self.version = version
        self.description = description

class OntologyAnnotation(IsaObject):
    """An ontology term annotation reference

    Attributes:
        termSource: The abbreviated ontology name. It should correspond to one of the sources as specified in the
        ontologySourceReference section of the Investigation.
        termAccession: URI
    """

    def __init__(self, name="", termSource=None, termAccession="", comments=None):
        super(OntologyAnnotation, self).__init__(comments)
        self.name = name
        if termSource is None:
            self.termSource = OntologySourceReference()
        else:
            self.termSource = termSource
        self.termAccession = termAccession


class Publication(IsaObject):
    """A publication associated with an investigation or study.

    Attributes:
        pubMedID: The PubMed IDs of the described publication(s) associated with this investigation.
        DOI: A Digital Object Identifier (DOI) for that publication (where available).
        authorList: The list of authors associated with that publication.
        title: The title of publication associated with the investigation.
        status: A term describing the status of that publication (i.e. submitted, in preparation, published).
    """

    def __init__(self, pubMedID="", DOI="", authorList="", title="", status=None, comments=None):
        super(Publication, self).__init__(comments)
        self.pubMedID = pubMedID
        self.DOI = DOI
        self.authorList = authorList
        self.title = title
        if status is None:
            self.status = OntologyAnnotation()
        else:
            self.status = status


class Contact(IsaObject):
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

    def __init__(self, firstName="", lastName="", midInitials="", email="", phone="", fax="", address="",
                 affiliation="", roles="", comments=None):
        super(Contact, self).__init__(comments)
        self.lastName = lastName
        self.firstName = firstName
        self.midInitials = midInitials
        self.email = email
        self.phone = phone
        self.fax = fax
        self.address = address
        self.affiliation = affiliation
        self.roles = roles


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

    def __init__(self, identifier="", title="", description="", submissionDate=datetime.date,
                 publicReleaseDate=datetime.date, fileName="", designDescriptors=None, publications=None,
                 contacts=None, factors=None, protocols=None, assays=None, comments=None):
        super(Study, self).__init__(comments)
        self.identifier = identifier
        self.title = title
        self.description = description
        self.submissionDate = submissionDate
        self.publicReleaseDate = publicReleaseDate
        self.fileName = fileName
        if designDescriptors is None:
            self.designDescriptors = []
        else:
            self.designDescriptors = designDescriptors
        if publications is None:
            self.publications = []
        else:
            self.publications = publications
        if contacts is None:
            self.contacts = []
        else:
            self.contacts = contacts
        if factors is None:
            self.factors = []
        else:
            self.factors = factors
        if protocols is None:
            self.protocols = []
        else:
            self.protocols = protocols
        if assays is None:
            self.assays = []
        else:
            self.assays = assays


class StudyDesignDescriptor(IsaObject):
    """A Study Design Descriptor provides a term allowing the classification of the study based on the overall
    experimental design. The term can be free text (Attribute: name) or from, for example, a controlled vocabulary or
    an ontology (Attribute: ontologyReference).

    Attributes:
        name: Free text name for the term
        ontologyAnnotation: A representation of an ontology annotation
    """

    def __init__(self, name="", ontologyAnnotation=None, comments=None):
        super(StudyDesignDescriptor, self).__init__(comments)
        self.name = name
        if ontologyAnnotation is None:
            self.ontologyAnnotation = OntologyAnnotation()
        else:
            self.ontologyAnnotation = ontologyAnnotation


class StudyFactor(IsaObject):
    """A Study Factor corresponds to an independent variable manipulated by the experimentalist with the intention to
    affect biological systems in a way that can be measured by an assay.

    Attributes:
        name: Free text name for the term
        type: Study factor type as free text
        ontologyReference: A representation of an ontology source reference
    """

    def __init__(self, name="", type="", ontologyAnnotation=None, comments=None):
        super(StudyFactor, self).__init__(comments)
        self.name = name
        self.type = type
        if ontologyAnnotation is None:
            self.ontologyAnnotation = OntologyAnnotation()
        else:
            self.ontologyAnnotation = ontologyAnnotation


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
    def __init__(self, measurementType=None, technologyType=None, fileName="", comments=None):
        super(Assay, self).__init__(comments)
        if measurementType is None:
            self.measurementType = OntologyAnnotation()
        else:
            self.measurementType = measurementType
        if technologyType is None:
            self.technologyType = OntologyAnnotation()
        else:
            self.technologyType = technologyType
        self.fileName = fileName
