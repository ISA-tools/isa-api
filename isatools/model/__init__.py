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
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.ontology_source import OntologySource
from isatools.model.parameter_value import ParameterValue
from isatools.model.person import Person
from isatools.model.process import Process
from isatools.model.process_sequence import ProcessSequenceNode
from isatools.model.protocol import Protocol, load_protocol_types_info
from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.publication import Publication
from isatools.model.sample import Sample
from isatools.model.source import Source
from isatools.model.study import Study
from isatools.model.logger import log
from isatools.model.utils import _build_assay_graph, plink, batch_create_assays, batch_create_materials, _deep_copy


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
