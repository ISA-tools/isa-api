# -*- coding: utf-8 -*-
"""ISA Model 1.0 implementation in Python.

This module implements the ISA Abstract Model 1.0 as Python classes, as
specified in the `ISA Model and Serialization Specifications 1.0`_, and
additional classes to support compatibility between ISA-Tab and ISA-JSON.

Todo:
    * Check consistency with published ISA Model
    * Finish docstringing rest of the module
    * Add constraints on attributes throughout, and test

.. _ISA Model and Serialization Specifications 1.0: http://isa-specs.readthedocs.io/

"""

import networkx as nx


def _build_assay_graph(process_sequence=list()):
    G = nx.DiGraph()
    for process in process_sequence:
        if process.next_process is not None or len(
                process.outputs) > 0:  # first check if there's some valid outputs to connect
            if len([n for n in process.outputs if not isinstance(n, DataFile)]) > 0:
                for output in [n for n in process.outputs if not isinstance(n, DataFile)]:
                    G.add_edge(process, output)
            else:  # otherwise just connect the process to the next one
                G.add_edge(process, process.next_process)
        if process.prev_process is not None or len(process.inputs) > 0:
            if len(process.inputs) > 0:
                for input_ in process.inputs:
                    G.add_edge(input_, process)
            else:
                G.add_edge(process.prev_process, process)
    return G


class Comment(object):
    """A comment allows arbitrary annotation of all ISA classes

    Comments are implemented in ISA-Tab and ISA-JSON formats.

    Attributes:
        name (str): The name of the comment (as mapped to Comment[SomeName] in ISA-Tab) to give context to the comment field.
        value (str, int, float, NoneType): A value for the corresponding comment, as a string or number.
    """
    def __init__(self, name, value=''):
        self.name = name
        self.value = value


class Commentable(object):
    """ An ISA Object is an abstract class to enable containment of Comments

    Attributes:
        comments (list, NoneType): Comments associated with the implementing ISA class (all ISA classes).
    """
    def __init__(self, comments=None):
        if comments is None:
            self.comments = []
        else:
            self.comments = comments


class Investigation(Commentable):
    """An investigation maintains metadata about the project context and links to one or more studies. There can only
    be 1 Investigation in an ISA descriptor. Investigations has the following properties:

    Attributes:
        identifier (str): A locally unique identifier or an accession number provided by a repository.
        title (str): A concise name given to the investigation.
        description (str): A textual description of the investigation.
        submission_date (str): The date on which the investigation was reported to the repository. This should be ISO8601 formatted.
        public_release_date (str): The date on which the investigation should be released publicly. This should be ISO8601 formatted.
        ontology_source_references (list, NoneType): OntologySources to be referenced by OntologyAnnotations used in this ISA descriptor.
        publications (list, NoneType): A list of Publications associated with an Investigation.
        contacts (list, NoneType): A list of People/contacts associated with an Investigation.
        studies (list, NoneType): Study is the central unit, containing information on the subject under study.
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, id_='', filename='', identifier="", title="", description="", submission_date='',
                 public_release_date='', ontology_source_references=None, publications=None,
                 contacts=None, studies=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.filename = filename
        self.identifier = identifier
        self.title = title
        self.description = description
        self.submission_date = submission_date
        self.public_release_date = public_release_date
        if ontology_source_references is None:
            self.ontology_source_references = list()
        else:
            self.ontology_source_references = ontology_source_references
        if publications is None:
            self.publications = list()
        else:
            self.publications = publications
        if contacts is None:
            self.contacts = list()
        else:
            self.contacts = contacts
        if studies is None:
            self.studies = list()
        else:
            self.studies = studies
        if comments is None:
            self.comments = list()


class OntologySource(Commentable):
    """An OntologySource describes the resource from which the value of an OntologyAnnotation is derived from.

    Attributes:
        name (str): The name of the source of a term; i.e. the source controlled vocabulary or ontology.
        file (str): A file name or a URI of an official resource.
        version (str): The version number of the Term Source to support terms tracking.
        description (str): A free text description of the resource.
        comments (list,): Comments associated with instances of this class.
    """

    def __init__(self, name, file='', version='', description='', comments=''):
        super().__init__(comments)
        self.name = name
        self.file = file
        self.version = version
        self.description = description


class OntologyAnnotation(Commentable):
    """An ontology annotation

    Attributes:
        term (str, NoneType): A term taken from an ontology or controlled vocabulary.
        term_source (OntologySource, NoneType): Reference to the OntologySource from which the term is derived.
        term_accession (str, NoneType): A URI or resource-specific identifier for the term.
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, term=None, term_source=None, term_accession=None, comments=None, id_=''):
        super().__init__(comments)

        self.term = term
        self.term_source = term_source
        self.term_accession = term_accession
        self.id = id_

    @property
    def term(self):
        if self.__term is '':
            return None
        else:
            return self.__term

    @term.setter
    def term(self, term):
        if term is not None and not isinstance(term, str):
            raise AttributeError("OntologyAnnotation.term must be a str or None; got {}:{}".format(term, type(term)))
        else:
            self.__term = term

    @property
    def term_source(self):
        return self.__term_source

    @term_source.setter
    def term_source(self, term_source):
        if term_source is not None and not isinstance(term_source, OntologySource):
            raise AttributeError("OntologyAnnotation.term_source must be a OntologySource or None; got {}:{}".format(term_source, type(term_source)))
        else:
            self.__term_source = term_source

    @property
    def term_accession(self):
        if self.__term is '':
            return None
        else:
            return self.__term_accession

    @term_accession.setter
    def term_accession(self, term_accession):
        if term_accession is not None and not isinstance(term_accession, str):
            raise AttributeError("OntologyAnnotation.term_accession must be a str or None")
        else:
            self.__term_accession = term_accession


class Publication(Commentable):
    """A publication associated with an investigation or study.

    Attributes:
        pubmed_id (str, NoneType): The PubMed IDs of the described publication(s) associated with this investigation.
        doi (str, NoneType): A Digital Object Identifier (DOI) for that publication (where available).
        author_list (str, NoneType): The list of authors associated with that publication.
        title (str, NoneType): The title of publication associated with the investigation.
        status(str, OntologyAnnotation, NoneType): A term describing the status of that publication (i.e. submitted, in preparation, published).
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, pubmed_id=None, doi=None, author_list=None, title=None, status=None, comments=None):
        super().__init__(comments)
        self.pubmed_id = pubmed_id
        self.doi = doi
        self.author_list = author_list
        self.title = title
        self.status = status

        @property
        def pubmed_id(self):
            if self.__pubmed_id is '':
                return None
            else:
                return self.__pubmed_id

        @pubmed_id.setter
        def pubmed_id(self, pubmed_id):
            if pubmed_id is not None and not isinstance(pubmed_id, str):
                raise AttributeError("Publication.pubmed_id must be a str or None")
            else:
                self.__pubmed_id = pubmed_id

        @property
        def doi(self):
            if self.__doi is '':
                return None
            else:
                return self.__doi

        @doi.setter
        def doi(self, doi):
            if doi is not None and not isinstance(doi, str):
                raise AttributeError("Publication.doi must be a str or None")
            else:
                self.__doi = doi

        @property
        def author_list(self):
            if self.__author_list is '':
                return None
            else:
                return self.__author_list

        @author_list.setter
        def doi(self, author_list):
            if author_list is not None and not isinstance(author_list, str):
                raise AttributeError("Publication.author_list must be a str or None")
            else:
                self.__author_list = author_list

        @property
        def status(self):
            if self.__status is '':
                return None
            else:
                return self.__status

        @status.setter
        def status(self, status):
            if status is not None and not isinstance(status, (OntologyAnnotation, str)):
                raise AttributeError("Publication.status must be a str, OntologyAnnotation or None")
            else:
                self.__status = status


class Person(Commentable):
    """A person/contact that can be attributed to an Investigation or Study.

    Attributes:
        last_name (str, NoneType): The last name of a person associated with the investigation.
        first_name (str, NoneType): The first name of a person associated with the investigation.
        mid_initials (str, NoneType): The middle initials of a person associated with the investigation.
        email (str, NoneType): The email address of a person associated with the investigation.
        phone (str, NoneType): The telephone number of a person associated with the investigation.
        fax (str, NoneType): The fax number of a person associated with the investigation.
        address (str, NoneType): The address of a person associated with the investigation.
        affiliation (str, NoneType): The organization affiliation for a person associated with the investigation.
        roles (list, NoneType): OntologyAnnotations to classify the role(s) performed by this person in the context of
        the investigation, which means that the roles reported here need not correspond to roles held withing their
        affiliated organization.
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, first_name='', last_name='', mid_initials='', email='', phone='', fax='',
                 address='', affiliation='', roles=[], comments=[], id_=''):
        super().__init__(comments)
        self.id = id_
        self.last_name = last_name
        self.first_name = first_name
        self.mid_initials = mid_initials
        self.email = email
        self.phone = phone
        self.fax = fax
        self.address = address
        self.affiliation = affiliation
        self.roles = roles


class Study(Commentable, object):
    """Study is the central unit, containing information on the subject under study, its characteristics
    and any treatments applied.

    Attributes:
        identifier (str): A unique identifier: either a temporary identifier supplied by users or one generated by a repository or other database.
        title (str): A concise phrase used to encapsulate the purpose and goal of the study.
        description (str): A textual description of the study, with components such as objective or goals.
        submission_date (str): The date on which the study was reported to the repository. This should be ISO8601 formatted.
        public_release_date (str): The date on which the study should be released publicly. This should be ISO8601 formatted.
        filename (str): A field to specify the name of the Study file corresponding the definition of that Study.
        design_descriptors (list, NoneType): Classifications of the study based on the overall experimental design, a list of OntologyAnnotations.
        publications (list, NoneType): A list of Publications associated with the Study.
        contacts (list, NoneType): A list of People/contacts associated with the Study.
        factors (list, NoneType): A factor corresponds to an independent variable manipulated by the experimentalist with the intention.
        to affect biological systems in a way that can be measured by an assay.  A list of StudyFactor objects.
        protocols (list, NoneType): Protocols used within the ISA artifact. A list of Protocol objects.
        assays (list, NoneType): An Assay represents a portion of the experimental design. A list of Assay objects.
        materials (dict): Materials associated with the study, lists of 'sources', 'samples' and 'other_material'.
        units (list, NoneType): A list of Units used in the annotation of material units in the study.
        characteristic_categories (list, NoneType): A list of OntologyAnnotation used in the annotation of material characteristics in the study.
        process_sequence (list, NoneType): A list of Process objects representing the experimental graphs at the study level.
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, id_='', filename="", identifier="",  title="", description="", submission_date='',
                 public_release_date='', contacts=None, design_descriptors=None, publications=None,
                 factors=None, protocols=None, assays=None, sources=None, samples=None,
                 process_sequence=None, other_material=None, characteristic_categories=None, comments=None, units=None):
        super().__init__(comments)
        self.id = id_
        self.filename = filename
        self.identifier = identifier
        self.title = title
        self.description = description
        self.submission_date = submission_date
        self.public_release_date = public_release_date

        if publications is None:
            self.publications = list()
        else:
            self.publications = publications

        if contacts is None:
            self.contacts = list()
        else:
            self.contacts = contacts

        if design_descriptors is None:
            self.design_descriptors = list()
        else:
            self.design_descriptors = design_descriptors

        if protocols is None:
            self.protocols = list()
        else:
            self.protocols = protocols

        if units is None:
            self.units = list()
        else:
            self.units = units

        self.materials = {
            'sources': list(),
            'samples': list(),
            'other_material': list()
        }
        if not (sources is None):
            self.materials['sources'] = sources
        if not (samples is None):
            self.materials['samples'] = samples
        if not (other_material is None):
            self.materials['other_material'] = other_material

        if process_sequence is None:
            self.process_sequence = list()
        else:
            self.process_sequence = process_sequence

        if assays is None:
            self.assays = list()
        else:
            self.assays = assays

        if factors is None:
            self.factors = list()
        else:
            self.factors = factors

        if characteristic_categories is None:
            self.characteristic_categories = list()
        else:
            self.characteristic_categories = characteristic_categories

    @property
    def graph(self):
        if len(self.process_sequence) > 0:
            self.__graph = _build_assay_graph(self.process_sequence)
        else:
            self.__graph = None
        return self.__graph

    @graph.setter
    def graph(self, graph):
        raise AttributeError("Study.graph is not settable")


class StudyFactor(Commentable):
    """A Study Factor corresponds to an independent variable manipulated by the experimentalist with the intention to
    affect biological systems in a way that can be measured by an assay.

    Attributes:
        name (str): Study factor name
        factor_type (OntologyAnnotation): An ontology source reference of the study factor type
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, id_='', name="", factor_type=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        if factor_type is None:
            self.factor_type = OntologyAnnotation()
        else:
            self.factor_type = factor_type


class Assay(Commentable):
    """An Assay represents a test performed either on material taken from a subject or on a whole initial subject,
    producing qualitative or quantitative measurements. An Assay groups descriptions of provenance of sample processing
    for related tests. Each test typically follows the steps of one particular experimental workflow described by a
    particular protocol.

    Attributes:
        measurement_type (OntologyAnnotation): An Ontology Annotation to qualify the endpoint, or what is being measured (e.g. gene expression profiling or protein identification).
        technology_type (OntologyAnnotation): An Ontology Annotation to identify the technology used to perform the measurement.
        technology_platform (str): Manufacturer and platform name, e.g. Bruker AVANCE.
        filename (str): A field to specify the name of the Assay file for compatibility with ISA-Tab.
        materials (dict): Materials associated with the Assay, lists of 'samples' and 'other_material'.
        units (list, NoneType): A list of Units used in the annotation of material units in the Assay.
        characteristic_categories (list, NoneType): A list of OntologyAnnotation used in the annotation of material characteristics in the Assay.
        process_sequence (list, NoneType): A list of Process objects representing the experimental graphs at the Assay level.
        comments (list, NoneType): Comments associated with instances of this class.
        graph (networkx.DiGraph): A graph representation of the process_sequence using the networkx package.
    """
    def __init__(self, measurement_type=None, technology_type=None, technology_platform="", filename="",
                 process_sequence=None, data_files=None, samples=None, other_material=None,
                 characteristic_categories=None, units=None, comments=None):
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
        self.filename = filename

        if process_sequence is None:
            self.process_sequence = list()
        else:
            self.process_sequence = process_sequence

        if data_files is None:
            self.data_files = list()
        else:
            self.data_files = data_files

        self.materials = {
            'samples': list(),
            'other_material': list()
        }

        if not (samples is None):
            self.materials['samples'].append(samples)

        if not (other_material is None):
            self.materials['other_material'].append(other_material)

        if characteristic_categories is None:
            self.characteristic_categories = list()
        else:
            self.characteristic_categories = characteristic_categories

        if units is None:
            self.units = list()
        else:
            self.units = units

    @property
    def graph(self):
        if len(self.process_sequence) > 0:
            self.__graph = _build_assay_graph(self.process_sequence)
        else:
            self.__graph = None
        return self.__graph

    @graph.setter
    def graph(self, graph):
        raise AttributeError("Assay.graph is not settable")


class Protocol(Commentable):
    """An experimental Protocol used in the study.

    Attributes:
        name (str): The name of the protocol used
        protocol_type (OntologyAnnotation, NoneType): Term to classify the protocol.
        description (str): A free-text description of the protocol.
        uri (str): Pointer to protocol resources externally that can be accessed by their Uniform Resource Identifier (URI).
        version (str): An identifier for the version to ensure protocol tracking.
        parameters (list, None): A list of ProtocolParameter describing the list of parameters required to execute the protocol.
        components (list, None): A list of OntologyAnnotation describing a protocol’s components; e.g. instrument names, software names, and reagents names.
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, id_='', name="", protocol_type=None, uri="", description="", version="", parameters=None,
                 components=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        if protocol_type is None:
            self.protocol_type = OntologyAnnotation()
        else:
            self.protocol_type = protocol_type
        self.description = description
        self.uri = uri
        self.version = version
        if parameters is None:
            self.parameters = list()
        else:
            self.parameters = parameters
        if components is None:
            self.components = list()
        else:
            self.components = components


class ProtocolParameter(Commentable):
    """A parameter used by a protocol.

    Attributes:
        name (OntologyAnnotation): A parameter name as a term
        unit (OntologyAnnotation): A unit, if applicable
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, id_='', parameter_name=None, unit=None, comments=None):
        super().__init__(comments)
        self.id = id_
        if parameter_name is None:
            self.parameter_name = OntologyAnnotation()
        else:
            self.parameter_name = parameter_name
        # if unit is None:
        #     self.unit = OntologyAnnotation()
        # else:
        #     self.unit = unit


class ParameterValue(object):
    """A ParameterValue represents the instance value of a ProtocolParameter, that is used in a Process.

    Attributes:
        category (ProtocolParameter): A link to the relevant ProtocolParameter that the value is set for.
        value (OntologyAnnotation): The value of the parameter.
        unit (OntologyAnnotation): The qualifying unit classifier, if the value is numeric.
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, category=None, value=None, unit=None):
        super().__init__()
        # if category is None:
        #     raise TypeError("You must specify a category")
        self.category = category
        self.value = value
        self.unit = unit


class ProtocolComponent(Commentable):
    """A component used in a protocol.

    Attributes:
        name (str): A component name.
        component_type (OntologyAnnotation): The classifier as a term for the component.
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, id_='', name='', component_type=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        if component_type is None:
            self.component_type = OntologyAnnotation()
        else:
            self.component_type = component_type


class Source(Commentable):
    """Represents a Source material in an experimental graph.

    Attributes:
        name (str): A name/reference for the source material.
        characteristics (list, NoneType): A list of Characteristics used to qualify the material properties.
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, name="", id_='', characteristics=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics


class Characteristic(Commentable):
    """A Characteristic acts as a qualifying property to a material object.

    Attributes:
        category (OntologyAnnotation, NoneType): The classifier of the type of characteristic being described.
        value (OntologyAnnotation, NoneType): The value of this instance of a characteristic as relevant to the attached material.
        unit (OntologyAnnotation, NoneType): If applicable, a unit qualifier for the value (if the value is numeric).
        """
    def __init__(self, category=None, value=None, unit=None, comments=None):
        super().__init__(comments)
        if category is None:
            self.category = OntologyAnnotation()
        else:
            self.category = category
        if value is None:
            self.value = OntologyAnnotation()
        else:
            self.value = value
        self.unit = unit


class Sample(Commentable):
    """Represents a Sample material in an experimental graph.

    Attributes:
        name (str): A name/reference for the sample material.
        characteristics (list, NoneType): A list of Characteristics used to qualify the material properties.
        factor_values (list, NoneType): A list of FactorValues used to qualify the material in terms of study factors/design.
        derives_from (Source): A link to the source material that the sample is derived from.
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, name="", id_='', factor_values=None, characteristics=None, derives_from=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        if factor_values is None:
            self.factor_values = list()
        else:
            self.factor_values = factor_values
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics
        if derives_from is None:
            self.derives_from = []
        else:
            self.derives_from = derives_from


class Material(Commentable):
    """Represents a generic material in an experimental graph.

    Attributes:
        name (str): A name/reference for the sample material.
        characteristics (list, NoneType): A list of Characteristics used to qualify the material properties.
        derives_from (Source): A link to the material that this material is derived from.
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, name="", id_='', type_='', characteristics=None, derives_from=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        self.type = type_
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics


class Extract(Material):

    def __init__(self, name="", id_='', characteristics=None, derives_from=None, comments=None):
        super().__init__(name=name, id_=id_, characteristics=characteristics, derives_from=derives_from,
                         comments=comments)
        self.type = "Extract Name"


class LabeledExtract(Material):

    def __init__(self, name="", id_='', characteristics=None, derives_from=None, comments=None):
        super().__init__(name=name, id_=id_, characteristics=characteristics, derives_from=derives_from,
                         comments=comments)
        self.type = "Labeled Extract Name"


class FactorValue(Commentable):
    """A FactorValue represents the value instance of a StudyFactor.

    Attributes:
        factor_name (StudyFactor): Reference to an instance of a relevant StudyFactor.
        value (OntologyAnnotation, NoneType): The value of the factor at hand.
        unit (OntologyAnnotation, NoneType): If numeric, the unit qualifier for the value.
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, factor_name=None, value=None, unit=None, comments=None):
        super().__init__(comments)
        self.factor_name = factor_name
        self.value = value
        self.unit = unit


class Process(Commentable):
    """Process nodes represent the application of a protocol to some input material (e.g. a Source) to produce some
    output (e.g.a Sample).

    Attributes:
        name (str): If relevant, a unique name for the process to disambiguate it from other processes.
        executes_protocol (Protocol): A reference to the Protocol that this process executes.
        date_ (str): A date formatted as an ISO8601 string corresponding to when the process event occurred.
        performer (str): The name of the person or organisation that carried out the process.
        parameter_values (list, NoneType): A list of ParameterValues relevant to the executing protocol.
        inputs (list, NoneType): A list of input materials, possibly Sources, Samples, Materials, DataFiles
        outputs (list, NoneType): A list of output materials, possibly Samples, Materials, DataFiles
        comments (list, NoneType): Comments associated with instances of this class.
    """
    def __init__(self, id_='', name="", executes_protocol=None, date_=None, performer=None,
                 parameter_values=None, inputs=None, outputs=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        if executes_protocol is None:
            self.executes_protocol = Protocol()
        else:
            self.executes_protocol = executes_protocol
        self.date = date_
        self.performer = performer
        if parameter_values is None:
            self.parameter_values = list()
        else:
            self.parameter_values = parameter_values
        if inputs is None:
            self.inputs = list()
        else:
            self.inputs = inputs
        if outputs is None:
            self.outputs = list()
        else:
            self.outputs = outputs
        self.additional_properties = dict()
        self.prev_process = None
        self.next_process = None


class DataFile(Commentable):
    """Represents a data file in an experimental graph.

        Attributes:
            filename (str): A name/reference for the data file.
            label (str):
            generated_from (Sample): The Sample the DataFile is generated from
            comments (list, NoneType): Comments associated with instances of this class.
        """
    def __init__(self, filename='', id_='', label='', generated_from=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.filename = filename
        self.label = label
        if generated_from is None:
            self.generated_from = []
        else:
            self.generated_from = generated_from


class RawDataFile(DataFile):

    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Raw Data File"


class DerivedDataFile(DataFile):

    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Derived Data File"


class RawSpectralDataFile(DataFile):

    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Raw Spectral Data File"


class DerivedArrayDataFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Derived Array Data File"


class ArrayDataFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Array Data File"


class DerivedSpectralDataFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Derived Spectral Data File"


class ProteinAssignmentFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Protein Assignment File"


class PeptideAssignmentFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Peptide Assignment File"


class DerivedArrayDataMatrixFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Derived Array Data Matrix File"


class PostTranslationalModificationAssignmentFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Post Translational Modification Assignment File"


class AcquisitionParameterDataFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Acquisition Parameter Data File"


class FreeInductionDecayDataFile(DataFile):
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_, generated_from=generated_from, comments=comments)
        self.label = "Free Induction Decay Data File"


def batch_create_materials(material=None, n=1):
    """Creates a batch of material objects (Source, Sample or Material) from a prototype material object

    :param material: existing material object to use as a prototype
    :param n: Number of material objects to create in the batch
    :returns: List of material objects

    :Example:

        # Create 10 sample materials derived from one source material

        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material', derives_from=source)
        batch = batch_create_materials(prototype_sample, n=10)

        [Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, ]

    """
    material_list = list()
    if isinstance(material, Source) or isinstance(material, Sample) or isinstance(material, Material):
        from copy import deepcopy
        for x in range(0, n):
            new_obj = deepcopy(material)
            new_obj.name = material.name + '-' + str(x)
            new_obj.derives_from = material.derives_from
            material_list.append(new_obj)
    return material_list


def batch_create_assays(*args, n=1):
    """Creates a batch of assay process sequences (Material->Process->Material) from a prototype sequence
    (currently works only as flat end-to-end processes of Material->Process->Material->...)

    :param *args: An argument list representing the process sequence prototype
    :param n: Number of process sequences to create in the batch
    :returns: List of process sequences replicating the prototype sequence

    :Example:

        # Create 3 assays of (Sample -> Process -> Material -> Process -> LabeledExtract)

        sample = Sample(name='sample')
        data_acquisition = Process(name='data acquisition')
        material = Material(name='material')
        labeling = Process(name='labeling')
        extract = LabeledExtract(name='lextract')
        batch = batch_create_assays(sample, data_acquisition, material, labeling, extract, n=3)

        [Process<> Process<>, Process<> Process<>, Process<>, Process<>]

        # Create 3 assays of ([Sample, Sample] -> Process -> [Material, Material])

        sample1 = Sample(name='sample')
        sample2 = Sample(name='sample')
        process = Process(name='data acquisition')
        material1 = Material(name='material')
        material2 = Material(name='material')
        batch = batch_create_assays([sample1, sample2], process, [material1, material2], n=3)

    """
    process_sequence = list()
    materialA = None
    process = None
    materialB = None
    from copy import deepcopy
    for x in range(0, n):
        for arg in args:
            if isinstance(arg, list) and len(arg) > 0:
                if isinstance(arg[0], Source) or isinstance(arg[0], Sample) or isinstance(arg[0], Material):
                    if materialA is None:
                        materialA = deepcopy(arg)
                        y = 0
                        for material in materialA:
                            material.name = material.name + '-' + str(x) + '-' + str(y)
                            y += 1
                    else:
                        materialB = deepcopy(arg)
                        y = 0
                        for material in materialB:
                            material.name = material.name + '-' + str(x) + '-' + str(y)
                            y += 1
                elif isinstance(arg[0], Process):
                    process = deepcopy(arg)
                    y = 0
                    for p in process:
                        p.name = p.name + '-' + str(x) + '-' + str(y)
                        y += 1
            if isinstance(arg, Source) or isinstance(arg, Sample) or isinstance(arg, Material):
                if materialA is None:
                    materialA = deepcopy(arg)
                    materialA.name = materialA.name + '-' + str(x)
                else:
                    materialB = deepcopy(arg)
                    materialB.name = materialB.name + '-' + str(x)
            elif isinstance(arg, Process):
                process = deepcopy(arg)
                process.name = process.name + '-' + str(x)
            if materialA is not None and materialB is not None and process is not None:
                if isinstance(process, list):
                    for p in process:
                        if isinstance(materialA, list):
                            p.inputs = materialA
                        else:
                            p.inputs.append(materialA)
                        if isinstance(materialB, list):
                            p.outputs = materialB
                            for material in materialB:
                                material.derives_from = materialA
                        else:
                            p.outputs.append(materialB)
                            materialB.derives_from = materialA
                else:
                    if isinstance(materialA, list):
                        process.inputs = materialA
                    else:
                        process.inputs.append(materialA)
                    if isinstance(materialB, list):
                        process.outputs = materialB
                        for material in materialB:
                            material.derives_from = materialA
                    else:
                        process.outputs.append(materialB)
                        materialB.derives_from = materialA
                    process_sequence.append(process)
                materialA = materialB
                process = None
                materialB = None
    return process_sequence


class ISADocument:


    valid_isajson = False

    def __init__(self, isa_obj):
        self._root = None
        if isinstance(isa_obj, Investigation):
            self._root = isa_obj
        elif isinstance(isa_obj, Study):
            self._root = Investigation(studies=[isa_obj])
        elif isinstance(isa_obj, Assay):
            self._root = Investigation(studies=[Study(assays=[isa_obj])])

    @property
    def valid_isatab(self):
        if self._root.filename is None or self._root.filename == '':
            return False
        for study in self._root.studies:
            if study.filename is None or study.filename == '':
                return False
            for assay in study.assays:
                if assay.filename is None or assay.filename == '':
                    return False
        return True

    @property
    def valid_isajson(self):
        return True

def plink(p1, p2):
    if isinstance(p1, Process) and isinstance(p2, Process):
        p1.next_process = p2
        p2.prev_process = p1