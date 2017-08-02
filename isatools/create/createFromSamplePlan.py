from __future__ import absolute_import

from isatools.create.models import *
from isatools.model import *
from isatools import isatab


def main():
    investigation = Investigation(identifier='I1')
    plan = SampleAssayPlan()
    plan.add_sample_type('liver')
    plan.add_sample_plan_record('liver', 5)
    plan.add_sample_type('blood')
    plan.add_sample_plan_record('blood', 3)
    plan.group_size = 2
    study = IsaModelObjectFactory(plan).create_study_from_plan()
    study.filename = 's_study.txt'
    investigation.studies = [study]
    print(isatab.dumps(investigation))

if __name__ == '__main__':
    main()
