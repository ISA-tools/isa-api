import unittest

import isatools
from isatools.create import errors
from isatools.create.assay_templates import create_new_ontology_annotation
from isatools.create.constants import (
    BASE_FACTORS,
    BASE_FACTORS_,
    DEFAULT_SOURCE_TYPE,
    DEFAULT_STUDY_IDENTIFIER,
    DURATION_FACTOR,
    ELEMENT_TYPES,
    EXTRACT,
    FOLLOW_UP,
    INTERVENTIONS,
    LABELED_EXTRACT,
    QC_SAMPLE_TYPE_INTERSPERSED,
    QC_SAMPLE_TYPE_PRE_RUN,
    RUN_IN,
    SAMPLE,
    SCREEN,
    SOURCE,
    WASHOUT,
    default_ontology_source_reference,
)
from isatools.create.model import (
    AssayGraph,
    NonTreatment,
    ProductNode,
    ProtocolNode,
    QualityControl,
    QualityControlSample,
    QualityControlService,
    SampleAndAssayPlan,
    SequenceNode,
    StudyArm,
    StudyCell,
    StudyDesign,
    StudyDesignFactory,
    Treatment,
    TreatmentFactory,
)
from isatools.model import (
    Assay,
    Characteristic,
    FactorValue,
    OntologyAnnotation,
    ParameterValue,
    Process,
    ProtocolParameter,
    Sample,
    Study,
    StudyFactor,
)
from isatools.tests.create_sample_assay_plan_odicts import lcdad_assay_dict, ms_assay_dict, nmr_assay_dict, sample_list


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.processed_ontology_annotation = {}

    def test_create_new_ontology_annotation(self, term_name="something"):
        stuff = (isatools.create.assay_templates.create_new_ontology_annotation(term_name),)
        self.assertEqual(
            str(stuff),
            str(
                (
                    isatools.model.OntologyAnnotation(
                        term="something",
                        term_source=isatools.model.OntologySource(
                            name="onto", file="", version="", description="", comments=[]
                        ),
                        term_accession="",
                        comments=[],
                    ),
                )
            ),
        )
