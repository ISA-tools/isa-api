from networkx import DiGraph
from enum import Enum


def _build_assay_graph(process_sequence=list()):
    G = DiGraph()
    for process in process_sequence:
        if process.next_process is not None or len(process.outputs) > 0:  # first check if there's some valid outputs to connect
            if len(process.outputs) > 0:
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

    Attributes:
        name: The name of the comment (as mapped to Comment[SomeName]) to give context to the comment field
        value: A value for the corresponding comment, as a string encoded in some way
    """
    def __init__(self, name='', value=''):
        self.name = name
        self.value = value


class IsaObject(object):
    """ An ISA Object is an abstract class to enable containment of Comments

    Attributes:
        comments: Comments associated with the implementing ISA class (all ISA classes)
    """
    def __init__(self, comments=None):
        if comments is None:
            self.comments = list()
        else:
            self.comments = comments


class StudyConfigurableObject(object):

    def __init__(self):
        self._study_node_sequence = None

    def _validate_process_sequence(self, process_sequence):
        #  Take all of our process objects and try to create an end-to-end graph
        import networkx as nx
        graph = nx.DiGraph()
        prev_process_node = None
        for process in process_sequence:
            if len(process.inputs) == 0:  # If current process has no inputs, assume connect to prev process
                graph.add_edge(prev_process_node, process)
            for input_ in process.inputs:
                graph.add_edge(input_, process)
            for output in process.outputs:
                graph.add_edge(process, output)
            prev_process_node = process
        #  Next, check if graph nodes match _study_node_sequence
        i = 0
        for node in graph.nodes():
            class_type = self._study_node_sequence[i]
            if not isinstance(node, class_type):
                raise TypeError("Unexpected node in sequence")


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

    def __init__(self, id_='', name="", term_source=None, term_accession="", comments=None):
        super().__init__(comments)
        self.id = id_
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

    def __init__(self, id_='', first_name="", last_name="", mid_initials="", email="", phone="", fax="", address="",
                 affiliation="", roles=None, comments=None):
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
        if roles is None:
            self.roles = list()
        else:
            self.roles = roles


class Study(IsaObject, StudyConfigurableObject, object):
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
            self.materials['sources'].append(sources)
        if not (samples is None):
            self.materials['samples'].append(samples)
        if not (other_material is None):
            self.materials['other_material'].append(other_material)

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
        self.graph = None
    def build_graph(self):
        self.graph = _build_assay_graph(self.process_sequence)


class StudyFactor(IsaObject):
    """A Study Factor corresponds to an independent variable manipulated by the experimentalist with the intention to
    affect biological systems in a way that can be measured by an assay.

    Attributes:
        ontology_annotation: A representation of an ontology source reference
    """

    def __init__(self, id_='', name="", factor_type=None, comments=None):
        super().__init__(comments)
        self.id = id_
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
    def __init__(self, measurement_type=None, technology_type=None, technology_platform="", filename="",
                 process_sequence=None, data_files=None, samples=None, other_material=None,
                 characteristic_categories=None, comments=None):
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
        self.graph = None

    def build_graph(self):
        self.graph = _build_assay_graph(self.process_sequence)


class Protocol(IsaObject):
    """A Protocol.

    Attributes:
        name:
        protocol_type:
        description:
        version:
        parameters:
        components:
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


class ProtocolParameter(IsaObject):
    """A Protocol Parameter.

    Attributes:
        name:
        unit:
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


class ProtocolComponent(IsaObject):
    def __init__(self, id_='', name='', component_type=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        if component_type is None:
            self.component_type = OntologyAnnotation()
        else:
            self.component_type = component_type


class Source(IsaObject):
    """A Source.

    Attributes:
        name:
        characteristics:
    """
    def __init__(self, id_='', name="", characteristics=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics


class Characteristic(IsaObject):
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


class Sample(IsaObject):
    """A Sample.

    Attributes:
        name:
        characteristics:
        factors:
    """
    def __init__(self, id_='', name="", factor_values=None, characteristics=None, derives_from=None, comments=None):
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
        self.derives_from = derives_from


class Material(IsaObject):
    """A Material.

    Attributes:
        name:
        characteristics:
    """
    def __init__(self, id_='', name="", type_='', characteristics=None, derives_from=None, comments=None):
        super().__init__(comments)
        self.id = id_
        self.name = name
        self.type = type_
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics
        self.derives_from = derives_from


class Extract(Material):
    def __init__(self, id_='', name="", type_='', characteristics=None, derives_from=None, comments=None):
        super().__init__(id_, name, type_, characteristics, derives_from, comments)
        self.type = 'Extract Name'


class LabeledExtract(Extract):
    def __init__(self, id_='', name="", type_='', characteristics=None, derives_from=None, comments=None, label=None):
        super().__init__(id_, name, type_, characteristics, derives_from, comments)
        self.label = label


class FactorValue(IsaObject):
    def __init__(self, factor_name=None, value=None, unit=None, comments=None):
        super().__init__(comments)
        self.factor_name = factor_name
        self.value = value
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


class DataFile(IsaObject):
    def __init__(self, id_='', filename='', label='', comments=None):
        super().__init__(comments)
        self.id = id_
        self.filename = filename
        self.label = label


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
                if isinstance(arg[0], Sample) or isinstance(arg[0], Material):
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
            if isinstance(arg, Sample) or isinstance(arg, Material):
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


def batch_set_attr(l=list(), attr=None, val=None):
    for i in l:
        setattr(i, attr, val)


class ParameterValue(object):
    """A Parameter Value
    """
    def __init__(self, category=None, value=None, unit=None):
        super().__init__()
        # if category is None:
        #     raise TypeError("You must specify a category")
        self.category = category
        self.value = value
        self.unit = unit
