from graphene import InputObjectType, Argument, ID, List, String
from isatools.graphQL.utils.validate import (
    validate_input,
    validate_outputs,
    validate_characteristics
)


class StringComparator(InputObjectType):
    eq = ID(description="Equal operator")
    includes = ID(name="in", description="Includes operator")


class IntComparator(StringComparator):
    eq = ID(description="Equal operator")
    lte = ID(description="Lower than or equal to operator")
    lt = ID(description="Lower then operator")
    gte = ID(description="Greater than or equal to operator")
    gt = ID(description="Greater then operator")


class ExposureParameters(InputObjectType):
    name = Argument(IntComparator, description="name the factor value should have", name="name")
    value = Argument(IntComparator, description="value the factor value should have")
    unit = Argument(IntComparator, description="unit the factor value should have")


class ParameterValueInput(InputObjectType):
    category = Argument(IntComparator, description="category the parameter value should have")
    value = Argument(IntComparator, description="value the parameter value should have")
    unit = Argument(IntComparator, description="unit the parameter value should have")


class AssayParameters(InputObjectType):
    measurementType = Argument(StringComparator, name="measurementType", description="Type of measurement to filter on")
    executesProtocol = Argument(StringComparator,
                                name="executesProtocol",
                                description="Type of protocol the process should executes")
    technologyType = Argument(StringComparator, name="technologyType", description="Type of technology to filter on")
    treatmentGroup = Argument(List(ExposureParameters, description="Name/value representing the exposure factor value"),
                              description="List of factor values representing an exposure to filter on",
                              name="treatmentGroup")
    characteristics = Argument(List(ExposureParameters),
                               name="characteristics",
                               description="characteristics of the sample to filter on")
    target = String(required=False, name="on", description="Type of inputs to apply the characteristics to")
    parameterValues = Argument(ParameterValueInput,
                               name="parameterValues",
                               description="List specifying the parameters of the protocols to filter on ")

    @property
    def is_valid(self):
        return validate_input(self)


class ProcessSequenceParameters(InputObjectType):
    executesProtocol = Argument(StringComparator, name="executesProtocol")
    treatmentGroup = Argument(List(ExposureParameters), name="treatmentGroup")
    characteristics = Argument(List(ExposureParameters),
                               name="characteristics",
                               description="characteristics of the sample to filter on")
    target = String(required=False, name="on", description="Type of inputs to apply the characteristics to")
    parameterValues = Argument(ParameterValueInput,
                               name="parameterValues",
                               description="List specifying the parameters of the protocols to filter on ")

    @property
    def is_valid(self):
        return validate_characteristics(self)


class OutputsParameters(InputObjectType):
    target = String(required=False, name="on", description="Type of output to apply the filters to")
    label = StringComparator(name="type", description="Name of the output to filter on")
    treatmentGroup = Argument(List(ExposureParameters),
                              name="treatmentGroup",
                              description="List of exposure to filter on")

    @property
    def is_valid(self):
        return validate_outputs(self)


class InputsParameters(InputObjectType):
    target = String(required=False, name="on", description="Type of input to apply the filter to")
    treatmentGroup = Argument(List(ExposureParameters),
                              name="treatmentGroup",
                              description="List describing the sample exposure")
    characteristics = Argument(List(ExposureParameters),
                               name="characteristics",
                               description="characteristics of the sample to filter on")

    @property
    def is_valid(self):
        return validate_input(self)
