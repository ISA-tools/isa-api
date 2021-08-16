from graphene import InputObjectType, Argument, ID, List, String


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


class AssayParameters(InputObjectType):
    measurementType = Argument(StringComparator, name="measurementType", description="Type of measurement to filter on")
    executesProtocol = Argument(StringComparator,
                                name="executesProtocol",
                                description="Type of protocol the process should executes")
    technologyType = Argument(StringComparator, name="technologyType", description="Type of technology to filter on")
    treatmentGroup = Argument(List(ExposureParameters, description="Name/value representing the exposure factor value"),
                              description="List of factor values representing an exposure to filter on",
                              name="treatmentGroup")


class ProcessSequenceParameters(InputObjectType):
    executesProtocol = Argument(StringComparator, name="executesProtocol")
    treatmentGroup = Argument(List(ExposureParameters), name="treatmentGroup")


class OutputsParameters(InputObjectType):
    target = String(required=True, name="on", description="Type of output to apply the filters to")
    label = StringComparator(name="type", description="Name of the output to filter on")
    treatmentGroup = Argument(List(ExposureParameters),
                              name="treatmentGroup",
                              description="List of exposure to filter on")

    @property
    def is_valid(self):
        if self.target not in ["Material", "DataFile", "Sample"]:
            raise Exception("Outputs 'on' argument should be Material, DataFile or Sample")
        if self.target != "Sample" and self.treatmentGroup:
            raise Exception("Outputs 'treatmentGroup' argument can only be applied to Sample")
        if self.label and (self.target == "Sample" or not self.target):
            raise Exception("Outputs 'type' argument can only be applied to Material and DataFile")
        return True


class InputsParameters(InputObjectType):
    target = String(required=True, name="on", description="Type of input to apply the filter to")
    treatmentGroup = Argument(List(ExposureParameters),
                              name="treatmentGroup",
                              description="List describing the sample exposure")
    # characteristics = Argument(List(??), description="List of sample characteristics to filter on")
    characteristics = String()
    # TODO: implement characteristics input object when characteristics will be correctly deserialized.

    @property
    def is_valid(self):
        """
        => should be filterable by characteristics on Source/Sample/Material only
        """
        if self.target not in ["Material", "DataFile", "Sample", "Source"]:
            raise Exception("Inputs 'on' argument should be Material, DataFile, Sample or Source")
        if self.treatmentGroup and self.target != "Sample":
            raise Exception("Inputs 'treatmentGroup' argument can only be applied to Sample")
        return True
