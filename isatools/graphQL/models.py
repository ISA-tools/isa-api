from graphene import (
    ObjectType,
    String,
    Schema as Sc,
    List,
    Field,
    Argument)
from isatools.graphQL.custom_scalars import DateTime, StringOrInt
from isatools.graphQL.utils import (
    find_exposure_value,
    compare_values,
    build_assays_filters,
    search_assays)
from isatools.graphQL.inputs import (
    AssayParameters,
    ProcessSequenceParameters,
    OutputsParameters,
    InputsParameters,
    StringComparator)


class Comment(ObjectType):
    name = String(name="name", description="Title of the comment")
    value = String(description="Content of the comment")


class ObjectType(ObjectType):
    comments = List(Comment, description="A list of comments attached to the object")


class OntologySourceReference(ObjectType):
    description = String(name='description')
    file = String()
    name = String(name="name")
    version = String()


class OntologyAnnotation(ObjectType):
    term = StringOrInt(name="annotationValue")
    term_source = Field(OntologySourceReference, name="termSource")
    term_accession = String(name="termAccession")


class Person(ObjectType):
    last_name = String(name="lastName", description="Person's last name")
    first_name = String(name="firstName", description="Person's first name")
    mid_initials = String(name="midInitials", description="Person's middle initials")
    email = String(description="Person's email")
    phone = String(description="Person's phone number")
    fax = String(description="Person's fax number")
    address = String(description="Person's full address")
    affiliation = String(description="Person's affiliation")
    roles = List(OntologyAnnotation, description="List of the roles this person has")


class Component(ObjectType):
    component_name = String(name="componentName")


class MaterialAttribute(ObjectType):
    characteristic_type = Field(OntologyAnnotation, name="characteristicType")


class MaterialAttributeValue(ObjectType):
    category = Field(OntologyAnnotation, name="characteristicType")
    unit = Field(OntologyAnnotation)
    value = Field(OntologyAnnotation)


class Factor(ObjectType):
    factor_name = String(name="factorName")
    factor_type = Field(OntologyAnnotation, name="factorType")


class FactorValue(ObjectType):
    category = Field(Factor)
    value = Field(OntologyAnnotation)
    unit = Field(OntologyAnnotation)


class Characteristic(ObjectType):
    category = Field(OntologyAnnotation)
    unit = Field(OntologyAnnotation)
    value = Field(OntologyAnnotation)


class Source(ObjectType):
    name = String(name="name")
    characteristics = List(Characteristic)


class Sample(Source):
    derives_from = List(Source, name="derivesFrom")
    factor_values = List(FactorValue, name="factorValues")


class Material(Source):
    type = String(name="type")
    derives_from = List(Source, name="derivesFrom")


class DataFile(ObjectType):
    filename = String(name="name")
    label = String(name="type")
    generated_from = List(Sample, name="generatedFrom")


class Materials(ObjectType):
    sources = List(Source)
    samples = List(Sample)
    other_material = List(Material, name="otherMaterials")


class Publication(ObjectType):
    pubMedID = String()
    doi = String()
    authorList = String()
    title = String()
    status = Field(OntologyAnnotation)


class ProtocolParameter(ObjectType):
    parameter_name = Field(OntologyAnnotation, name="parameterName")


class ProtocolParameterValue(ObjectType):
    category = Field(ProtocolParameter, name="characteristicType")
    unit = Field(OntologyAnnotation)
    value = Field(OntologyAnnotation)


class Protocol(ObjectType):
    name = String(name="name")
    protocol_type = Field(OntologyAnnotation, name="protocolType")
    description = String(name="description")
    uri = String()
    version = String()
    parameters = List(ProtocolParameter)
    components = List(Component)


class Process(ObjectType):
    from isatools.graphQL.unions import ProcessInputs, ProcessOutputs

    name = String(name="name")
    executes_protocol = Field(Protocol, name="executesProtocol")
    parameter_values = List(ProtocolParameterValue, name="parameterValues")
    performer = String()
    date = DateTime()
    previous_process = Field(lambda: Process, name="previousProcess")
    next_process = Field(lambda: Process, name="nextProcess")
    inputs = List(ProcessInputs, filters=Argument(InputsParameters, required=False))
    outputs = List(ProcessOutputs, filters=Argument(OutputsParameters, required=False))

    @staticmethod
    def resolve_inputs(parent, info, filters=None):
        """
        Can be Source, Sample, Material and DataFile
        => should be filterable by characteristics on Source/Sample/Material only
        => however, exposure can only filter Sample
        """
        if not filters:
            return parent.inputs
        outputs = []
        for input_data in parent.inputs:
            input_classname = type(input_data).__name__
            if input_classname == filters['target'] == "Sample" and 'treatmentGroup' in filters:
                found = []
                for factor in filters['treatmentGroup']:
                    found.append(find_exposure_value(input_data, factor, factor['name']))
                if False not in list(set(found)) or found == []:
                    outputs.append(input_data)
            if input_classname == filters['target'] \
                    and 'characteristics' in filters:
                # TODO: filter by characteristics
                print(input_data.characteristics)

        return outputs

    @staticmethod
    def resolve_outputs(parent, info, filters=None):
        if not filters:
            return parent.outputs

        if filters.is_valid:
            outputs = []
            for output in parent.outputs:
                if type(output).__name__ == filters['target'] == "DataFile":
                    operator = list(filters['label'].keys())[0]
                    if compare_values(output.label, filters['label'][operator], operator):
                        outputs.append(output)
                elif filters['target'] == type(output).__name__ == "Material":
                    operator = list(filters['label'].keys())[0]
                    if compare_values(output.type, filters['label'][operator], operator):
                        outputs.append(output)
                elif filters['target'] == type(output).__name__ == "Sample":
                    # TODO: Filter samples on exposure FV, needs a valid input (no samples in current assays outputs)
                    print("SAMPLE HERE, NOT DONE YET")
            return outputs


class Assay(ObjectType):
    filename = String()
    measurement_type = Field(OntologyAnnotation, name="measurementType")
    technology_type = Field(OntologyAnnotation, name="technologyType")
    technology_platform = String(name="technologyPlatform")
    data_files = List(DataFile, name="dataFiles", label=Argument(StringComparator, required=False))
    materials = Field(Materials)
    characteristic_categories = List(MaterialAttribute, name="characteristicCategories")
    unit_categories = List(OntologyAnnotation, name="unitCategories")
    process_sequence = List(Process,
                            name="processSequence",
                            filters=Argument(ProcessSequenceParameters, required=False),
                            operator=String(),
                            description="List of processes attached to the assay")

    @staticmethod
    def resolve_data_files(parent, info, label=None):
        if label:
            operator = list(label.keys())[0]
            return [x for x in parent.data_files if compare_values(x.label, label[operator], operator)]
        return parent.data_files

    @staticmethod
    def resolve_process_sequence(parent, info, filters=None, operator="AND"):

        if operator not in ['AND', 'OR']:
            return Exception("Operator should be AND or OR")

        if not filters:
            return parent.process_sequence

        exposition_factors = filters['treatmentGroup'] if 'treatmentGroup' in filters else None
        protocol = filters['executesProtocol'] if 'executesProtocol' in filters else None

        if not protocol and not exposition_factors:
            return parent.process_sequence

        process_sequence = []
        for process in parent.process_sequence:
            append_process = []
            match_exposure = []
            if not exposition_factors:
                match_exposure = [True]
            else:
                for input_data in process.inputs:
                    if type(input_data).__name__ == "Sample":
                        for factor in exposition_factors:
                            match_exposure.append(find_exposure_value(input_data, factor, factor['name']))
            if list(set(match_exposure)) == [True]:
                append_process.append(True)

            if not protocol:
                append_process.append(True)
            else:
                comparator = list(protocol.keys())[0]
                append_process.append(compare_values(process.executes_protocol.protocol_type.term,
                                                     protocol[comparator],
                                                     comparator))

            if operator == 'AND' and append_process == [True, True]:
                process_sequence.append(process)
            elif operator == 'OR' and True in append_process:
                process_sequence.append(process)

        return process_sequence


class Study(ObjectType):
    filename = String()
    identifier = String()
    title = String()
    description = String(name="description")
    submission_date = DateTime(name="submissionDate")
    public_release_date = DateTime(name="publicReleaseDate")
    publications = List(Publication)
    contacts = List(Person, name="people")
    design_descriptors = List(OntologyAnnotation, name="studyDesignDescriptors")
    protocols = List(Protocol)
    materials = Field(Materials)
    process_sequence = List(Process, name="processSequence")
    assays = List(Assay, filters=Argument(AssayParameters), operator=String())
    factors = List(Factor)
    characteristic_categories = List(OntologyAnnotation, name="characteristicCategories")
    units = List(OntologyAnnotation, name="unitCategories")

    @staticmethod
    def resolve_assays(parent, info, filters=None, operator="AND"):
        if operator not in ['AND', 'OR']:
            return Exception("Operator should be AND or OR")
        if not filters:
            return parent.assays
        filters = build_assays_filters(filters)
        return search_assays(parent.assays, filters, operator)


class Investigation(ObjectType):
    filename = String()
    identifier = String()
    title = String()
    description = String(name='description')
    submissionDate = DateTime()
    publicReleaseDate = DateTime()
    ontology_source_references = List(OntologySourceReference, name="ontologySourceReferences")
    publications = List(Publication)
    contacts = List(Person, name="people")
    studies = List(Study)


class IsaQuery(ObjectType):
    investigation = Field(Investigation)
    studies = List(Study)
    assays = List(Assay,
                  filters=Argument(AssayParameters, description="Filters to apply to the assays"),
                  operator=String(description="Should be AND or OR", default_value='AND'),
                  description="A query that concatenates studies assays into a single list")
    investigation_instance = None

    @staticmethod
    def resolve_investigation(parent, info):
        return IsaQuery.investigation_instance

    @staticmethod
    def resolve_studies(parent, info):
        return IsaQuery.investigation_instance.studies

    @staticmethod
    def resolve_assays(parent, info, filters=None, operator="AND"):
        if operator not in ['AND', 'OR']:
            return Exception("Operator should be AND or OR")
        filters = build_assays_filters(filters)
        investigation_object = IsaQuery.investigation_instance
        output = []
        for study in investigation_object.studies:
            found = search_assays(study.assays, filters, operator)
            if found:
                output += found
        return output


class Schema(Sc):

    @staticmethod
    def set_investigation(instance):
        IsaQuery.investigation_instance = instance


IsaSchema = Schema(IsaQuery, auto_camelcase=False)
