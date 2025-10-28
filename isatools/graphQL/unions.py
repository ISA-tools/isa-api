from graphene import Union

from isatools.graphQL.models import DataFile, Material, Sample, Source


class ProcessInputs(Union):
    class Meta:
        types = (Source, Sample, Material, DataFile)

    @classmethod
    def resolve_type(cls, instance, info):
        instance_type = type(instance).__name__
        if instance_type == "Source":
            return Source
        elif instance_type == "Sample":
            return Sample
        elif instance_type == "Material":
            return Material
        elif instance_type == "DataFile":
            return DataFile


class ProcessOutputs(Union):
    class Meta:
        types = (Sample, Material, DataFile)

    @classmethod
    def resolve_type(cls, instance, info):
        instance_type = type(instance).__name__
        if instance_type == "Sample":
            return Sample
        elif instance_type == "Material":
            return Material
        elif instance_type == "DataFile":
            return DataFile
