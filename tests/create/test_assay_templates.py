import unittest

import isatools
from isatools.create import errors
from isatools.model import (
    OntologyAnnotation,
    StudyFactor,
    FactorValue,
    Characteristic,
    Sample,
    ProtocolParameter,
    ParameterValue,
    Study,
    Assay,
    Process
)
from isatools.create.model import (
    NonTreatment,
    Treatment,
    TreatmentFactory,
    StudyCell,
    ProductNode,
    ProtocolNode,
    SequenceNode,
    AssayGraph,
    SampleAndAssayPlan,
    StudyArm,
    StudyDesign,
    StudyDesignFactory,
    QualityControl,
    QualityControlSample,
    QualityControlService
)
from isatools.create.constants import (
    SCREEN, RUN_IN, WASHOUT, FOLLOW_UP, ELEMENT_TYPES, INTERVENTIONS, DURATION_FACTOR,
    BASE_FACTORS_, BASE_FACTORS, SOURCE, SAMPLE, EXTRACT, LABELED_EXTRACT, default_ontology_source_reference,
    DEFAULT_SOURCE_TYPE, QC_SAMPLE_TYPE_PRE_RUN, QC_SAMPLE_TYPE_INTERSPERSED, DEFAULT_STUDY_IDENTIFIER
)
from isatools.tests.create_sample_assay_plan_odicts import (
    sample_list,
    ms_assay_dict,
    lcdad_assay_dict,
    nmr_assay_dict
)

from isatools.create.assay_templates import create_new_ontology_annotation


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.processed_ontology_annotation = {}

    def test_create_new_ontology_annotation(self, term_name="something"):
        stuff = isatools.create.assay_templates.create_new_ontology_annotation(term_name),
        self.assertEqual(
            str(stuff),
            str(
                (isatools.model.OntologyAnnotation(
                    term='something',
                    term_source=isatools.model.OntologySource(
                        name='onto',
                        file='',
                        version='',
                        description='',
                        comments=[]
                    ),
                    term_accession='',
                    comments=[]
                ),
                )
            )
        )


