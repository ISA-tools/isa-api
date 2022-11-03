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
from isatools.model.assay import Assay
from isatools.model.characteristic import Characteristic
from isatools.model.comments import Commentable, Comment
from isatools.model.context import set_context
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
from isatools.model.protocol_component import ProtocolComponent
from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.publication import Publication
from isatools.model.sample import Sample
from isatools.model.source import Source
from isatools.model.study import Study
from isatools.model.logger import log
from isatools.model.utils import _build_assay_graph, plink, batch_create_assays, batch_create_materials, _deep_copy
