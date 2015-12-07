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

    def to_json(self):
        return {
            "name": self.name,
            "value": self.value,
        }


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

    def get_comments_json(self):
        comments_json = []
        for comment in self.comments:
            comments_json.append(comment.to_json())
        return comments_json

    @abc.abstractmethod
    def to_json(self):
        """Implement JSON serialization"""
        return


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

    def to_json(self):
        ontology_source_references_json = []
        for ontology_source_reference in self.ontology_source_references:
            ontology_source_references_json.append(ontology_source_reference.to_json())

        publications_json = []
        for publication in self.publications:
            publications_json.append(publication.to_json())

        contacts_json = []
        for contact in self.contacts:
            contacts_json.append(contact.to_json())

        studies_json = []
        for study in self.studies:
            studies_json.append(study.to_json())

        return {
            "identifier": self.identifier,
            "title": self.title,
            "description": self.description,
            "submissionDate": self.submission_date.isoformat(),
            "publicReleaseDate": self.public_release_date.isoformat(),
            "ontologySourceReferences": ontology_source_references_json,
            "publications": publications_json,
            "people": contacts_json,
            "studies": studies_json,
            "commentCreatedWithConfiguration": self.created_with_configuration.to_json(),
            "commentLastOpenedWithConfiguration": self.last_opened_with_configuration.to_json()
        }


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

    def to_json(self):
        return {
            "name": self.name,
            "file": self.file,
            "version": self.version,
            "description": self.description
            # "comments": self.get_comments_json()
        }


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

    def to_json(self):
        return {
            "name": self.name,
            "termSource": self.term_source.name,
            "termAccession": self.term_accession
            # "comments": self.get_comments_json()
        }


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

    def to_json(self):
        return {
            "pubMedID": self.pubmed_id,
            "doi": self.doi,
            "authorList": self.author_list,
            "title": self.title,
            "status": self.status.to_json()
            # "comments": self.get_comments_json()
        }


class Contact(IsaObject):
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

    def to_json(self):
        roles_json = []
        for role in self.roles:
            roles_json.append(role.to_json())
        return {
            "firstName": self.first_name,
            "midInitials": self.mid_initials,
            "lastName": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "fax": self.fax,
            "address": self.address,
            "affiliation": self.affiliation,
            "roles": roles_json
            # "comments": self.get_comments_json()
        }


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
    """

    def __init__(self, identifier="", title="", description="", submission_date=date.today(),
                 public_release_date=date.today(), file_name="", design_descriptors=None, publications=None,
                 contacts=None, protocols=None, assays=None, sources=None, samples=None,
                 process_sequence=None, comments=None):
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
        # if factors is None:
        #     self.factors = []
        # else:
        #     self.factors = factors
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

    def to_json(self):
        design_descriptors_json = []
        for design_descriptor in self.design_descriptors:
            design_descriptors_json.append(design_descriptor.to_json())

        publications_json = []
        for publication in self.publications:
            publications_json.append(publication.to_json())

        contacts_json = []
        for contact in self.contacts:
            contacts_json.append(contact.to_json())

        # factors_json = []
        # for factor in self.factors:
        #     factors_json.append(factor.to_json())

        protocols_json = []
        for protocol in self.protocols:
            protocols_json.append(protocol.to_json())

        assays_json = []
        for assay in self.assays:
            assays_json.append(assay.to_json())

        return {
            "identifier": self.identifier,
            "title": self.title,
            "description": self.description,
            "submissionDate": self.submission_date.isoformat(),
            "publicReleaseDate": self.public_release_date.isoformat(),
            # "fileName": self.file_name,
            # "comments": self.get_comments_json(),
            "studyDesignDescriptors": design_descriptors_json,
            "publications": publications_json,
            "people": contacts_json,
            "protocols": protocols_json,
            "assays": assays_json
        }


class StudyDesignDescriptor(IsaObject):
    """A Study Design Descriptor provides a term allowing the classification of the study based on the overall
    experimental design. The term can be free text (Attribute: name) or from, for example, a controlled vocabulary or
    an ontology.

    Attributes:
        name: Free text name for the term
        ontology_annotation: A representation of an ontology annotation
    """

    def __init__(self, name="", ontology_annotation=None, comments=None):
        super().__init__(comments)
        self.name = name
        if ontology_annotation is None:
            self.ontology_annotation = OntologyAnnotation()
        else:
            self.ontology_annotation = ontology_annotation

    def to_json(self):
        return {
            "name": self.name,
            "ontologyAnnotation": self.ontology_annotation.to_json()
            # "comments": self.get_comments_json()
        }


class StudyFactor(IsaObject):
    """A Study Factor corresponds to an independent variable manipulated by the experimentalist with the intention to
    affect biological systems in a way that can be measured by an assay.

    Attributes:
        ontology_annotation: A representation of an ontology source reference
    """

    def __init__(self, ontology_annotation=None, comments=None):
        super().__init__(comments)
        if ontology_annotation is None:
            self.ontology_annotation = OntologyAnnotation()
        else:
            self.ontology_annotation = ontology_annotation

    def to_json(self):
        return {
            "ontologyAnnotation": self.ontology_annotation.to_json(),
            # "comments": self.get_comments_json()
        }


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

    def to_json(self):
        return {
            "measurementType": self.measurement_type.to_json(),
            "technologyType": self.technology_type.to_json(),
            "technologyPlatform": self.technology_platform,
            "fileName": self.file_name
            # "comments": self.get_comments_json()
        }


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

    def to_json(self):
        parameters_json = []
        for parameter in self.parameters:
            parameters_json.append(parameter.to_json())
        components_json = []
        for component in self.components:
            components_json.append(component.to_json())
        return {
            "name": self.name,
            "protocolType": self.protocol_type.to_json(),
            "description": self.description,
            "uri": self.uri,
            "version": self.version,
            "parameters": parameters_json,
            "components": components_json
            # "comments": self.get_comments_json()
        }


class ProtocolParameter(IsaObject):
    """A Protocol Parameter.

    Attributes:
        name:
        unit:
    """
    def __init__(self, name="", unit=None, comments=None):
        super().__init__(comments)
        self.name=name
        if unit is None:
            self.unit = OntologyAnnotation()
        else:
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
    def __init__(self, name="", executes_protocol=None, comments=None):
        super().__init__(comments)
        self.name = name
        if executes_protocol is None:
            self.executes_protocol = Protocol()
        else:
            self.executes_protocol = executes_protocol
        self.parameters = []
        self.inputs = []
        self.outputs = []

    def to_json(self):
        parameters_json = []
        for parameter in self.parameters:
            parameters_json.append(parameter.to_json())
        inputs_json = []
        for input_ in self.inputs:
            inputs_json.append(input_.to_json())
        outputs_json = []
        for output in self.outputs:
            outputs_json.append(output.to_json())
        return {
            "name": self.name,
            "executesProtocol": self.executes_protocol.to_json(),
            "parameters": parameters_json,
            "inputs": inputs_json,
            "outputs": outputs_json
        }


class Source(IsaObject):
    """A Source.

    Attributes:
        name:
        characteristics:
    """
    def __init__(self, name="", comments=None):
        super().__init__(comments)
        self.name = name
        self.characteristics = []

    def to_json(self):
        characteristics_json = []
        for characteristic in self.characteristics:
            characteristics_json.append(characteristic.to_json())
        return {
            "name": self.name,
            "characteristics": characteristics_json
        }


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

    def to_json(self):
        characteristics_json = []
        for characteristic in self.characteristics:
            characteristics_json.append(characteristic.to_json())
        return {
            "name": self.name,
            "characteristics": characteristics_json
        }


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

    def to_json(self):
        return {
            "characteristic": self.characteristic.to_json(),
            "unit": self.characteristic.to_json(),
        }


class Data(IsaObject):
    """A Data.

    Attributes:
        name:
    """
    def __init__(self, name="", type_="", comments=None):
        super().__init__(comments)
        self.name = name
        self.type_ = type_

    def to_json(self):
        return {
            "name": self.name,
            "type": self.type_
        }


class Sample(IsaObject):
    """A Sample.

    Attributes:
        name:
        characteristics:
        factors:
    """
    def __init__(self, name="", comments=None):
        super().__init__(comments)
        self.name = name
        self.characteristics = []
        self.factors = []

    def to_json(self):
        characteristics_json = []
        for characteristic in self.characteristics:
            characteristics_json.append(characteristic.to_json())
        factors_json = []
        for factor in self.factors:
            factors_json.append(factor.to_json())
        return {
            "name": self.name,
            "characteristics": characteristics_json,
            "factors": factors_json
        }
