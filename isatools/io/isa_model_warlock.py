import warlock
import json
import os
from jsonschema import RefResolver

JSONv1_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../schemas/isa_model_version_1_0_schemas")
investigation_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'investigation_schema.json')))
study_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'study_schema.json')))
ontology_source_reference_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'ontology_source_reference_schema.json')))
publication_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'publication_schema.json')))
ontology_annotation_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'ontology_annotation_schema.json')))
study_factor_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'factor_schema.json')))
assay_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'assay_schema.json')))
study_protocol_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'protocol_schema.json')))
contact_schema = json.load(open(os.path.join(JSONv1_SCHEMA_PATH, 'person_schema.json')))
schemas_path = 'file://' + JSONv1_SCHEMA_PATH + '/'
resolver = RefResolver(schemas_path, None)


def ontology_source_reference_factory(**kwargs):
    """This annotation section is identical to that in the MAGE-TAB format.

    Attributes:
        name (string): The name of the source of a term; i.e. the source controlled vocabulary or ontology. These names
            will be used in all corresponding Term Source REF fields.
        file (string): A file name or a URI of an official resource.
        version (string): The version number of the Term Source to support terms tracking.
        description (string): Use for disambiguating resources when homologous prefixes have been used.

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        a OntologySourceReference object - get and set properties above as normal

    References:
        Schema - ontology_source_reference_schema.json
        Specification - ISA-TAB RC1 v1.0 November 2008, section 4.1.1

    """
    OntologySourceReference = warlock.model_factory(ontology_source_reference_schema, resolver=resolver, name='OntologySourceReference')
    obj = OntologySourceReference(kwargs)
    return obj


def ontology_annotation_factory(**kwargs):
    """An annotation for use in different parts of the ISA description.

    Attributes:
        name (string): A term allowing the classification of the related object.  The term can be free text or from, for
            example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and
            Term Source REF fields below are required.
        termAccession (string): The accession number from the Term Source associated with the selected term.
        termSource (string): Identifies the controlled vocabulary or ontology that this term comes from. The Term
            Source REF has to match one the Term Source Name declared in an Investigation's OntologySourceReferences.

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        a OntologyAnnotation object - get and set properties above as normal

    References:
        Schema - ontology_annotation_schema.json
        Specification - ISA-TAB RC1 v1.0 November 2008, section 4.1.2.2 (Investigation Contacts, Investigation Person
            Roles) 4.1.2.3 (Investigation Contacts, Investigation Person Roles), 4.1.3.2 (Study Design Descriptors),
            4.1.3.3 (Study Publications, Study Publication Status) ...

    """
    OntologyAnnotation = warlock.model_factory(ontology_annotation_schema, resolver=resolver, name='OntologyAnnotation')
    obj = OntologyAnnotation(kwargs)
    return obj


def publication_factory(**kwargs):
    """Each publication associated with an Investigation has its own Publication object. Such publications are
        specifically dealing with the investigation as a whole. Publications relating to the specific Studies may be
        referenced in the Study objects.

    Attributes:
        pubMedID (string): The PubMed IDs of the described publication(s) associated with this investigation.
        doi (string): A Digital Object Identifier (DOI) for that publication (where available).
        authorList (string): The list of authors associated with that publication.
        title (string): The title of publication associated with the investigation.
        status (OntologyAnnotation): A term annotation describing the status of that publication (i.e. submitted, in
            preparation, published).

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        a Publication object - get and set properties above as normal

    References:
        Schema - publications.json
        Specification - ISA-TAB RC1 v1.0 November 2008, section 4.1.2.2 (Investigation Publications) and 4.1.3.3 (Study
            Publications)

    """
    Publication = warlock.model_factory(publication_schema, resolver=resolver, name='Publication')
    obj = Publication(kwargs)
    return obj


def study_factor_factory(**kwargs):
    """A factor corresponds to an independent variable manipulated by the experimentalist with the intention to affect
    biological systems in a way that can be measured by an assay. The value of a factor is given in the Study or Assay
    file, accordingly. If both Study and Assay have a Factor Value (see section 4.2.5 and 4.3.1.5 in the spec,
    respectively), these must be different.

    Attributes:
        name (string): he name of one factor used in the Study and/or Assay files.
        ontologyAnnotation (OntologyAnnotation): A term allowing the classification of this factor into categories.

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        a Publication object - get and set properties above as normal

    References:
        Schema - publications.json
        Specification - ISA-TAB RC1 v1.0 November 2008, section 4.1.2.2 (Investigation Publications) and 4.1.3.3 (Study
            Publications)

    """
    StudyFactor = warlock.model_factory(study_factor_schema, resolver=resolver, name='StudyFactor')
    obj = StudyFactor(kwargs)
    return obj


def study_protocol_factory(**kwargs):
    """Study Protocol

    Attributes:
        name (string): The name of the protocols used within the ISA-TAB document. The names are used as identifiers within
            the ISA-TAB document and will be referenced in the Study and Assay files in the Protocol REF columns. Names
            can be either local identifiers, unique within the ISA Archive which contains them, or fully qualified
            external accession numbers.
        protocolType (OntologyAnnotation): Term to classify the protocol.
        description (string): A free-text description of the protocol.
        uri (string): Pointer to protocol resources external to the ISA-TAB that can be accessed by their Uniform
            Resource Identifier (URI).
        version (string): An identifier for the version to ensure protocol tracking.
        parameters (array of Parameter): A list of Parameters used as an identifier within the ISA-TAB
            document. These names are used in the Study and Assay files (in the "Parameter Value [<parameter name>]"
            column heading) to list the values used for each protocol parameter. Refer to section Multiple values
            fields in the Investigation File on how to encode multiple values in one field and match term sources.
            Parameters optionally include OntologyAnnotations.
        components (array of Component): A list of a protocol's components; e.g. instrument names, software names, and
            reagents names. Refer to section Multiple values fields in the Investigation File on how to encode multiple
            components in one field and match term sources. Components optionally include OntologyAnnotations.

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        a StudyProtocol object - get and set properties above as normal

    References:
        Schema - protocol_schema.json
        Specification - ISA-TAB RC1 v1.0 November 2008, section 4.1.3.6 (Study Protocols)

    """
    StudyProtocol = warlock.model_factory(study_protocol_schema, resolver=resolver, name='StudyProtocol')
    obj = StudyProtocol(kwargs)
    obj.parameters = []
    obj.components = []
    return obj


def contact_factory(**kwargs):
    """A contact is a person in the context of an investigation or study.

    Attributes:
    lastName (string): The last name of a person associated with the investigation.
    firstName (string): The first name of a person associated with the investigation.
    midInitials (string): The middle initials of a person associated with the investigation.
    email (string): The email address of a person associated with the investigation.
    phone (string): The telephone number of a person associated with the investigation.
    fax (string): The fax number of a person associated with the investigation.
    address (string): The address of a person associated with the investigation.
    affiliation (Organization): The organization affiliation for a person associated with the investigation.
    roles: Term to classify the role(s) performed by this person in the context of the investigation, which means that
        the roles reported here need not correspond to roles held withing their affiliated organization.

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        a Contact object - get and set properties above as normal

    References:
        Schema - person_schema.json
        Specification - ISA-TAB RC1 v1.0 November 2008, section 4.1.2.3 (Investigation Contacts), 4.1.3.7 (Study
            Contacts)

    """
    Contact = warlock.model_factory(contact_schema, resolver=resolver, name='Contact')
    obj = Contact(kwargs)
    obj.roles = []
    return obj


def investigation_factory(**kwargs):
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

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        an Investigation object - get and set properties above as normal

    References:
        Schema - investigation_schema.json
        Specification - ISA-TAB RC1 v1.0 November 2008, section 4.1.2

    """
    Investigation = warlock.model_factory(investigation_schema, resolver=resolver, name='Investigation')
    obj = Investigation(kwargs)
    obj.ontologySourceReferences = []
    obj.publications = []
    obj.studies = []
    return obj


def study_factory(**kwargs):
    """Study is the central unit, containing information on the subject under study, its characteristics
        and any treatments applied.

    Attributes:
        identifier (string): A unique identifier: either a temporary identifier supplied by users or one generated by a
            repository or other database.
        title (string): A concise phrase used to encapsulate the purpose and goal of the study.
        description (string): A textual description of the study, with components such as objective or goals.
        submissionDate (date-time): The date on which the study is submitted to an archive.
        publicReleaseDate (date-time): The date on which the study should be released publicly.
        fileName (string): A field to specify the name of the Study file corresponding the definition of that Study.
        designDescriptors (array of OntologyAnnotation): Classifications of the study based on the overall experimental
            design.
        publications (array of Publication): Publications associated with a Study.
        contacts (array of Contact): People/contacts associated with a Study.
        factors(array of StudyFactor): A factor corresponds to an independent variable manipulated by the
            experimentalist with the intention to affect biological systems in a way that can be measured by an assay.
        protocols (array of StudyProtocol: Protocols used within the ISA artifact.
        assays (array of Assay): An Assay represents a portion of the experimental design.

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        a Study object - get and set properties above as normal

    References:
        Schema - study_schema.json
        Specification - ISA-TAB RC1 v1.0 November 2008, section 4.1.3 (Study section)

    """
    Study = warlock.model_factory(study_schema, resolver=resolver, name='Study')
    obj = Study(kwargs)
    obj.studyDesignDescriptors = []
    obj.publications = []
    obj.studyFactors = []
    obj.assays = []
    obj.protocols = []
    obj.contacts = []
    return obj


def assay_factory(**kwargs):
    """A study Assay declares and describes each of the Assay files associated with the current Study.

    Attributes:
        measurementType (OntologyAnnotation): A term to qualify the endpoint, or what is being measured (e.g. gene
            expression profiling or protein identification).
        technologyType (OntologyAnnnotation): Term to identify the technology used to perform the measurement, e.g.
            DNA microarray, mass spectrometry.
        technologyPlatform (string): Manufacturer and platform name, e.g. Bruker AVANCE
        fileName (string): A field to specify the name of the Assay file corresponding the definition of that assay.
            There can be only one file per cell.

    Args:
        A list of parameters of any of the above. Ignores any params we don't know about

    Returns:
        an Assay object - get and set properties above as normal

    References:
        Schema - assay_schema.json
        Specification - ISA-TAB RC1 v1.0 November 2008, 4.1.3.5 (Study Assays)

    """
    Assay = warlock.model_factory(assay_schema, resolver=resolver, name='Assay')
    obj = Assay(kwargs)
    return obj
