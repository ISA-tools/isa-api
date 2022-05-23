"""ISA Model 1.0 implementation in Python.

This module implements the ISA Abstract Model 1.0 as Python classes, as
specified in the `ISA Model and Serialization Specifications 1.0`_, and
additional classes to support compatibility between ISA-Tab and ISA-JSON.

Todo:
    * Check consistency with published ISA Model
    * Finish docstringing rest of the module
    * Add constraints on attributes throughout, and test

.. _ISA Model and Serialization Specs 1.0: http://isa-specs.readthedocs.io/

"""
from __future__ import absolute_import

from isatools.model.assay import Assay
from isatools.model.characteristic import Characteristic
from isatools.model.comments import Commentable, Comment
from isatools.model.datafile import (
    DataFile,
    RawDataFile,
    DerivedDataFile,
    RawSpectralDataFile,
    DerivedArrayDataFile,
    ArrayDataFile,
    DerivedSpectralDataFile,
    ProteinAssignmentFile,
    PeptideAssignmentFile,
    DerivedArrayDataMatrixFile,
    PostTranslationalModificationAssignmentFile,
    AcquisitionParameterDataFile,
    FreeInductionDecayDataFile
)
from isatools.model.factor_value import FactorValue, StudyFactor
from isatools.model.investigation import Investigation
from isatools.model.logger import log
from isatools.model.material import Material, Extract, LabeledExtract
from isatools.model.mixins import MetadataMixin, StudyAssayMixin, _build_assay_graph
from isatools.model.ontologies import OntologySource, OntologyAnnotation
from isatools.model.parameter_value import ParameterValue
from isatools.model.person import Person
from isatools.model.process import Process
from isatools.model.process_sequence import ProcessSequenceNode
from isatools.model.protocol import Protocol, ProtocolParameter, load_protocol_types_info
from isatools.model.publication import Publication
from isatools.model.sample import Sample
from isatools.model.source import Source
from isatools.model.study import Study


class ProtocolComponent(Commentable):
    """A component used in a protocol.

    Attributes:
        name: A component name.
        component_type: The classifier as a term for the component.
        comments: Comments associated with instances of this class.
    """

    def __init__(self, id_='', name='', component_type=None, comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name

        if component_type is None:
            self.__component_type = OntologyAnnotation()
        else:
            self.__component_type = component_type

    @property
    def name(self):
        """:obj:`str`: the name of the protocol component"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'ProtocolComponent.name must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__name = val

    @property
    def component_type(self):
        """ :obj:`OntologyAnnotation`: a component_type for the protocol
        component"""
        return self.__component_type

    @component_type.setter
    def component_type(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise AttributeError(
                'ProtocolComponent.component_type must be a '
                'OntologyAnnotation, or None; got {0}:{1}'.format(
                    val, type(val)))
        else:
            self.__component_type = val

    def __repr__(self):
        return "isatools.model.ProtocolComponent(name='{component.name}', " \
               "category={component_type}, " \
               "comments={component.comments})".format(
            component=self, component_type=repr(self.component_type))

    def __str__(self):
        return """ProtocolComponent(
    name={component.name}
    category={component_type}
    comments={num_comments} Comment objects
)""".format(component=self, component_type=self.component_type.term if
        self.component_type else '', num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ProtocolComponent) \
               and self.name == other.name \
               and self.component_type == other.component_type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


def _deep_copy(isa_object):
    """
    Re-implementation of the deepcopy function that also increases and sets the object identifiers for copied objects.
    :param {Object} isa_object: the object to copy
    """
    from copy import deepcopy
    new_obj = deepcopy(isa_object)
    new_obj.assign_identifier()
    return new_obj


def batch_create_materials(material=None, n=1):
    """Creates a batch of material objects (Source, Sample or Material) from a
    prototype material object

    :param material: existing material object to use as a prototype
    :param n: Number of material objects to create in the batch
    :returns: List of material objects

    :Example:

        # Create 10 sample materials derived from one source material

        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material', derives_from=source)
        batch = batch_create_materials(prototype_sample, n=10)

        [Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>,
        Sample<>, Sample<>, Sample<>, ]

    """
    material_list = list()
    if isinstance(material, (Source, Sample, Material)):
        for x in range(0, n):
            new_obj = _deep_copy(material)
            new_obj.name = material.name + '-' + str(x)
            if hasattr(material, 'derives_from'):
                new_obj.derives_from = material.derives_from

            material_list.append(new_obj)

    return material_list


def batch_create_assays(*args, n=1):
    """Creates a batch of assay process sequences (Material->Process->Material)
    from a prototype sequence (currently works only as flat end-to-end
    processes of Material->Process->Material->...)

    :param *args: An argument list representing the process sequence prototype
    :param n: Number of process sequences to create in the batch
    :returns: List of process sequences replicating the prototype sequence

    :Example:

        # Create 3 assays of (Sample -> Process -> Material -> Process ->
        LabeledExtract)

        sample = Sample(name='sample')
        data_acquisition = Process(name='data acquisition')
        material = Material(name='material')
        labeling = Process(name='labeling')
        extract = LabeledExtract(name='lextract')
        batch = batch_create_assays(sample, data_acquisition, material,
        labeling, extract, n=3)

        [Process<> Process<>, Process<> Process<>, Process<>, Process<>]

        # Create 3 assays of ([Sample, Sample] -> Process -> [Material,
        Material])

        sample1 = Sample(name='sample')
        sample2 = Sample(name='sample')
        process = Process(name='data acquisition')
        material1 = Material(name='material')
        material2 = Material(name='material')
        batch = batch_create_assays([sample1, sample2], process, [material1,
        material2], n=3)

    """
    process_sequence = []
    materialA = None
    process = None
    materialB = None
    for x in range(0, n):
        for arg in args:
            if isinstance(arg, list) and len(arg) > 0:
                if isinstance(arg[0], (Source, Sample, Material)):
                    if materialA is None:
                        materialA = _deep_copy(arg)
                        y = 0
                        for material in materialA:
                            material.name = \
                                material.name + '-' + str(x) + '-' \
                                + str(y)
                            y += 1
                    else:
                        materialB = _deep_copy(arg)
                        y = 0
                        for material in materialB:
                            material.name = \
                                material.name + '-' + str(x) + '-' \
                                + str(y)
                            y += 1
                elif isinstance(arg[0], Process):
                    process = _deep_copy(arg)
                    y = 0
                    for p in process:
                        p.name = p.name + '-' + str(x) + '-' + str(y)
                        y += 1
            if isinstance(arg, (Source, Sample, Material)):
                if materialA is None:
                    materialA = _deep_copy(arg)
                    materialA.name = materialA.name + '-' + str(x)
                else:
                    materialB = _deep_copy(arg)
                    materialB.name = materialB.name + '-' + str(x)
            elif isinstance(arg, Process):
                process = _deep_copy(arg)
                process.name = process.name + '-' + str(x)
            if materialA is not None and materialB is not None \
                    and process is not None:
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
    """
    Function to create a link between two processes nodes of the isa graph
    :param Process p1: node 1
    :param Process p2: node 2
    """
    if isinstance(p1, Process) and isinstance(p2, Process):
        p1.next_process = p2
        p2.prev_process = p1
