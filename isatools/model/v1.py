from datetime import date
import abc

__author__ = 'dj'


class Comment(object):
    """A comment allows arbitrary annotation of all ISA classes
    
    Attributes:
        name: The name of the comment (as mapped to Comment[SomeName]) to give context to the comment field
        value: A value for the corresponding comment, as a string encoded in some way
    """
    def __init__(self, name="", value=""):
        self.name = name
        self.value = value


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
        submission_date: The date on which the investigation was reported to the repository.
        public_release_date: The date on which the investigation should be released publicly
        ontology_source_references: This annotation section is identical to that in the MAGE-TAB format.
        publications: Publications associated with an Investigation.
        contacts: People/contacts associated with an Investigation.
        studies: Study is the central unit, containing information on the subject under study, its characteristics and
        any treatments applied.
    """

    def __init__(self, identifier="", title="", description="", submission_date=date.today(),
                 public_release_date=date.today(), ontology_source_references=None, publications=None,
                 contacts=None, studies=None, created_with_configuration="", last_opened_with_configuration=""):
        super().__init__()
        self.identifier = identifier
        self.title = title
        self.description = description
        self.submission_date = submission_date
        self.public_release_date = public_release_date
        if ontology_source_references is None:
            self.ontology_source_references = []
        else:
            self.ontology_source_references = ontology_source_references
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
        self.created_with_configuration = Comment(name="Created With Configuration", value=created_with_configuration)
        self.last_opened_with_configuration = Comment(name="Last Opened With Configuration", value=last_opened_with_configuration)


class OntologySourceReference(IsaObject):
    """This annotation section is identical to that in the MAGE-TAB format.

    Attributes:
        name: The name of the source of a term; i.e. the source controlled vocabulary or ontology.
        file: A file name or a URI of an official resource.
        version: The version number of the Term Source to support terms tracking.
        description: Use for disambiguating resources when homologous prefixes have been used.
    """

    def __init__(self, name="", file="", version="", description="", comments=None):
        super().__init__(comments)
        self.name = name
        self.file = file
        self.version = version
        self.description = description


class OntologyAnnotation(IsaObject):
    """An ontology term annotation reference

    Attributes:
        term_source: The abbreviated ontology name. It should correspond to one of the sources as specified in the
        ontology_source_reference section of the Investigation.
        term_accession: URI
    """

    def __init__(self, name="", term_source=None, term_accession="", comments=None):
        super().__init__(comments)
        self.name = name
        if term_source is None:
            self.term_source = OntologySourceReference()
        else:
            self.term_source = term_source
        self.term_accession = term_accession


class Publication(IsaObject):
    """A publication associated with an investigation or study.

    Attributes:
        pubmed_id: The PubMed IDs of the described publication(s) associated with this investigation.
        doi: A Digital Object Identifier (DOI) for that publication (where available).
        author_list: The list of authors associated with that publication.
        title: The title of publication associated with the investigation.
        status: A term describing the status of that publication (i.e. submitted, in preparation, published).
    """

    def __init__(self, pubmed_id="", doi="", author_list="", title="", status=None, comments=None):
        super().__init__(comments)
        self.pubmed_id = pubmed_id
        self.doi = doi
        self.author_list = author_list
        self.title = title
        if status is None:
            self.status = OntologyAnnotation()
        else:
            self.status = status


class Person(IsaObject):
    """A person/contact that can be attributed to an Investigation or Study.

    Attributes:
        last_name: The last name of a person associated with the investigation.
        first_name: The first name of a person associated with the investigation.
        mid_initials: The middle initials of a person associated with the investigation.
        email: The email address of a person associated with the investigation.
        phone: The telephone number of a person associated with the investigation.
        fax: The fax number of a person associated with the investigation.
        address: The address of a person associated with the investigation.
        affiliation: The organization affiliation for a person associated with the investigation.
        roles: Term to classify the role(s) performed by this person in the context of the investigation,
        which means that the roles reported here need not correspond to roles held withing their
        affiliated organization.
    """

    def __init__(self, first_name="", last_name="", mid_initials="", email="", phone="", fax="", address="",
                 affiliation="", roles=None, comments=None):
        super().__init__(comments)
        self.last_name = last_name
        self.first_name = first_name
        self.mid_initials = mid_initials
        self.email = email
        self.phone = phone
        self.fax = fax
        self.address = address
        self.affiliation = affiliation
        if roles is None:
            self.roles = []
        else:
            self.roles = roles


class Study(IsaObject):
    """Study is the central unit, containing information on the subject under study, its characteristics
    and any treatments applied.

    Attributes:
        identifier: A unique identifier: either a temporary identifier supplied by users or one generated by a
        repository or other database.
        title: A concise phrase used to encapsulate the purpose and goal of the study.
        description: A textual description of the study, with components such as objective or goals.
        submission_date: The date on which the study is submitted to an archive.
        public_release_date: The date on which the study should be released publicly.
        file_name: A field to specify the name of the Study file corresponding the definition of that Study.
        design_descriptors: Classifications of the study based on the overall experimental design.
        publications: Publications associated with a Study.
        contacts: People/contacts associated with a Study.
        factors: A factor corresponds to an independent variable manipulated by the experimentalist with the intention
        to affect biological systems in a way that can be measured by an assay.
        protocols: Protocols used within the ISA artifact.
        assays: An Assay represents a portion of the experimental design.
        data: Data files associated with the study
    """

    def __init__(self, identifier="", title="", description="", submission_date=date.today(),
                 public_release_date=date.today(), file_name="", design_descriptors=None, publications=None,
                 contacts=None, factors=None, protocols=None, assays=None, sources=None, samples=None,
                 process_sequence=None, data=None, comments=None):
        super().__init__(comments)
        self.identifier = identifier
        self.title = title
        self.description = description
        self.submission_date = submission_date
        self.public_release_date = public_release_date
        self.file_name = file_name
        if design_descriptors is None:
            self.design_descriptors = []
        else:
            self.design_descriptors = design_descriptors
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
        if sources is None:
            self.sources = []
        else:
            self.sources = sources
        if samples is None:
            self.samples = []
        else:
            self.samples = samples
        if process_sequence is None:
            self.process_sequence = []
        else:
            self.process_sequence = process_sequence
        if data is None:
            self.data = []
        else:
            self.data = data


class StudyFactor(IsaObject):
    """A Study Factor corresponds to an independent variable manipulated by the experimentalist with the intention to
    affect biological systems in a way that can be measured by an assay.

    Attributes:
        ontology_annotation: A representation of an ontology source reference
    """

    def __init__(self, name="", factor_type=None, comments=None):
        super().__init__(comments)
        self.name = name
        if factor_type is None:
            self.factor_type = OntologyAnnotation()
        else:
            self.factor_type = factor_type


class Assay(IsaObject):
    """A Study Assay declares and describes each of the Assay files associated with the current Study.

    Attributes:
        measurement_type: A term to qualify the endpoint, or what is being measured (e.g. gene expression profiling or
        protein identification). The term can be free text or from, for example, a controlled vocabulary or an ontology.
        technology_type: Term to identify the technology used to perform the measurement, e.g. DNA microarray, mass
        spectrometry. The term can be free text or from, for example, a controlled vocabulary or an ontology.
        technology_platform: Manufacturer and platform name, e.g. Bruker AVANCE
        file_name: A field to specify the name of the Assay file corresponding the definition of that assay.
    """
    def __init__(self, measurement_type=None, technology_type=None, technology_platform="", file_name="",
                 process_sequence=None, comments=None):
        super().__init__(comments)
        if measurement_type is None:
            self.measurement_type = OntologyAnnotation()
        else:
            self.measurement_type = measurement_type
        if technology_type is None:
            self.technology_type = OntologyAnnotation()
        else:
            self.technology_type = technology_type
        self.technology_platform = technology_platform
        self.file_name = file_name
        if process_sequence is None:
            self.process_sequence = []
        else:
            self.process_sequence = process_sequence


class Protocol(IsaObject):
    """A Protocol.

    Attributes:
        name:
        protocol_type:
        description:
        uri:
        version:
        parameters:
        components:
    """
    def __init__(self, name="", protocol_type=None, description="", uri="", version="", parameters=None, comments=None):
        super().__init__(comments)
        self.name = name
        if protocol_type is None:
            self.protocol_type = OntologyAnnotation()
        else:
            self.protocol_type = protocol_type
        self.description = description
        self.uri = uri
        self.version = version
        if parameters is None:
            self.parameters = []
        else:
            self.parameters = parameters
        self.components = []


class ProtocolParameter(IsaObject):
    """A Protocol Parameter.

    Attributes:
        name:
        unit:
    """
    def __init__(self, parameter_name=None, unit=None, comments=None):
        super().__init__(comments)
        if parameter_name is None:
            self.name = OntologyAnnotation()
        else:
            self.parameter_name = parameter_name
        self.parameter_name = parameter_name
        if unit is None:
            self.unit = OntologyAnnotation()
        else:
            self.unit = unit


class ParameterValue(IsaObject):
    """A Parameter Value
    """
    def __init__(self, parameter_name="", parameter_value=None, unit=None):
        self.parameter_name = parameter_name
        if parameter_value is None:
            self.parameter_value = OntologyAnnotation()
        else:
            self.parameter_value = parameter_value
        self.unit = unit


class Process(IsaObject):
    """A Process.

    Attributes:
        name:
        executes_protocol:
        parameters:
        inputs:
        outputs:
    """
    def __init__(self, name="", executes_protocol=None, date_=date.today(), performer="", parameters=None, inputs=None, outputs=None, comments=None):
        super().__init__(comments)
        self.name = name
        if executes_protocol is None:
            self.executes_protocol = Protocol()
        else:
            self.executes_protocol = executes_protocol
        self.date = date_
        self.performer = performer
        if parameters is None:
            self.parameters = list()
        else:
            self.parameters = parameters
        if inputs is None:
            self.inputs = list()
        else:
            self.inputs = inputs
        if outputs is None:
            self.outputs = list()
        else:
            self.outputs = outputs


class Source(IsaObject):
    """A Source.

    Attributes:
        name:
        characteristics:
    """
    def __init__(self, name="", characteristics=None, comments=None):
        super().__init__(comments)
        self.name = name
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics


class FactorValue(IsaObject):
    def __init__(self, factorName="", value=None, unit=None, comments=None):
        super().__init__(comments)
        self.factorName = factorName
        self.value = value
        self.unit = unit


class Characteristic(IsaObject):
    def __init__(self, category="", value=None, unit=None, comments=None):
        super().__init__(comments)
        self.category = category
        self.value = value
        self.unit = unit


class Material(IsaObject):
    """A Material.

    Attributes:
        name:
        characteristics:
    """
    def __init__(self, name="", comments=None):
        super().__init__(comments)
        self.name = name
        self.characteristics = []


class MaterialAttribute(IsaObject):
    """A MaterialAttribute.

    Attributes:
        characteristic:
        unit:
    """
    def __init__(self, characteristic=None, unit=None, comments=None):
        super().__init__(comments)
        if characteristic is None:
            self.characteristic = OntologyAnnotation()
        else:
            self.characteristic = characteristic
        if unit is None:
            self.unit = OntologyAnnotation()
        else:
            self.unit = unit


class Data(IsaObject):
    """A Data.

    Attributes:
        name:
    """
    def __init__(self, name="", type_="", comments=None):
        super().__init__(comments)
        self.name = name
        self.type_ = type_


class Sample(IsaObject):
    """A Sample.

    Attributes:
        name:
        characteristics:
        factors:
    """
    def __init__(self, name="", factor_values=None, characteristics=None, derives_from=None, comments=None):
        super().__init__(comments)
        self.name = name
        self.derives_from = derives_from
        if factor_values is None:
            self.factor_values = []
        else:
            self.factor_values = factor_values
        if characteristics is None:
            self.characteristics = []
        else:
            self.characteristics = characteristics
