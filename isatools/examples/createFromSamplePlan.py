from __future__ import absolute_import

from isatools import isatab
from isatools.create.model import (
    IsaModelObjectFactory,
    SampleAssayPlan,
    TreatmentFactory,
    TreatmentSequence,
)
from isatools.model import Investigation, OntologyAnnotation, StudyFactor


def create_descriptor():
    """Returns a ISA-Tab descriptor using a simple sample plan for
    illustration."""
    investigation = Investigation(identifier='I1')
    plan = SampleAssayPlan()
    plan.add_sample_type('liver')
    plan.add_sample_plan_record('liver', 5)
    plan.add_sample_type('blood')
    plan.add_sample_plan_record('blood', 3)
    plan.group_size = 2
    f1 = StudyFactor(name='AGENT', factor_type=OntologyAnnotation(
        term='pertubation agent'))
    f2 = StudyFactor(name='INTENSITY', factor_type=OntologyAnnotation(
        term='intensity'))
    f3 = StudyFactor(name='DURATION', factor_type=OntologyAnnotation(
        term='time'))
    treatment_factory = TreatmentFactory(factors=[f1, f2, f3])
    treatment_factory.add_factor_value(f1, {'cocaine', 'crack', 'aether'})
    treatment_factory.add_factor_value(f2, {'low', 'medium', 'high'})
    treatment_factory.add_factor_value(f3, {'short', 'long'})
    ffactorial_design_treatments = treatment_factory\
        .compute_full_factorial_design()
    treatment_sequence = TreatmentSequence(
        ranked_treatments=ffactorial_design_treatments)
    # treatment_factory.add_factor_value('intensity', 1.05)
    study = IsaModelObjectFactory(plan, treatment_sequence)\
        .create_study_from_plan()
    study.filename = 's_study.txt'
    investigation.studies = [study]
    print(isatab.dumps(investigation))


if __name__ == '__main__':
    create_descriptor()
