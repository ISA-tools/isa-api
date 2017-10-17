"""Tests on serializing planning objects in isatools.create.models to JSON"""
import json
import unittest

from isatools.model import *
from isatools.create.models import *


def ordered(o):  # to enable comparison of JSONs with lists using ==
    if isinstance(o, dict):
        return sorted((k, ordered(v)) for k, v in o.items())
    if isinstance(o, list):
        return sorted(ordered(x) for x in o)
    else:
        return o


class EncodeToJsonTests(unittest.TestCase):

    def setUp(self):
        self.plan = SampleAssayPlan()
        self.plan.group_size = 20
        self.plan.add_sample_type('liver')
        self.plan.add_sample_type('tissue')
        self.plan.add_sample_plan_record('liver', 3)
        self.plan.add_sample_plan_record('tissue', 5)

        self.top_mods = AssayTopologyModifiers()
        self.top_mods.technical_replicates = 2
        self.top_mods.injection_modes = {'LC', 'GC'}
        self.top_mods.acquisition_modes = {'positive', 'negative'}
        self.top_mods.chromatography_instruments = {'Agilent Q12324A'}
        self.top_mods.instruments = {'Agilent QTOF'}
        self.top_mods.array_designs = {'A-AFFY-27', 'A-AFFY-28'}

        self.assay_type = AssayType(measurement_type='genome sequencing',
                                    technology_type='DNA microarray')

    def test_serialize_assay_default_topology_modifiers(self):
        expected = ordered(
            json.loads("""{
                "technical_replicates": 1,
                "instruments": [],
                "distinct_libraries": 0,
                "injection_modes": [],
                "chromatography_instruments": [],
                "pulse_sequences": [],
                "array_designs": [],
                "acquisition_modes": []
            }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(AssayTopologyModifiers(), cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)

    def test_serialize_assay_topology_modifiers(self):
        expected = ordered(
            json.loads("""{
                "distinct_libraries": 0,
                "instruments": ["Agilent QTOF"],
                "injection_modes": ["GC", "LC"],
                "acquisition_modes": ["negative", "positive"],
                "pulse_sequences": [],
                "array_designs": ["A-AFFY-27", "A-AFFY-28"],
                "chromatography_instruments": ["Agilent Q12324A"],
                "technical_replicates": 2
            }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(self.top_mods, cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)

    def test_serialize_default_assay_type(self):
        expected = ordered(
            json.loads("""{
                "measurement_type": "",
                "technology_type": "",
                "topology_modifiers": []
            }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(AssayType(), cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)

    def test_serialize_assay_type(self):
        expected = ordered(
            json.loads("""{
                "measurement_type": "genome sequencing",
                "technology_type": "DNA microarray",
                "topology_modifiers": []
            }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(self.assay_type, cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)

    def test_serialize_assay_type_with_top_mods(self):
        self.assay_type.topology_modifiers = self.top_mods

        expected = ordered(
            json.loads("""{
                "topology_modifiers": {
                    "acquisition_modes": ["negative", "positive"],
                    "pulse_sequences": [],
                    "chromatography_instruments": ["Agilent Q12324A"],
                    "injection_modes": ["GC", "LC"],
                    "instruments": ["Agilent QTOF"],
                    "technical_replicates": 2,
                    "distinct_libraries": 0,
                    "array_designs": ["A-AFFY-27", "A-AFFY-28"]
                },
                "measurement_type": "genome sequencing",
                "technology_type": "DNA microarray"
            }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(self.assay_type, cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)

    def test_serialize_default_sampleassayplan(self):
        expected = ordered(
            json.loads("""{
                "group_size": 0,
                "assay_types": [],
                "sample_plan": [],
                "sample_types": [],
                "sample_qc_plan": [],
                "assay_plan": []
            }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(SampleAssayPlan(), cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)

    def test_serialize_sampleplan(self):
        expected = ordered(
            json.loads("""{
                "group_size": 20,
                "assay_plan": [],
                "sample_plan": [
                    {
                        "sample_type": "liver",
                        "sampling_size": 3
                    },
                    {
                        "sample_type": "tissue",
                        "sampling_size": 5
                    }
                ],
                "sample_qc_plan": [],
                "assay_types": [],
                "sample_types": ["liver", "tissue"]
            }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(self.plan, cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)

    def test_serialize_sampleplan_with_qc(self):
        self.plan.add_sample_type('water')
        self.plan.add_sample_qc_plan_record('water', 8)

        expected = ordered(
            json.loads("""{
                        "group_size": 20,
                        "assay_plan": [],
                        "sample_plan": [
                            {
                                "sample_type": "liver",
                                "sampling_size": 3
                            },
                            {
                                "sample_type": "tissue",
                                "sampling_size": 5
                            }
                        ],
                        "sample_qc_plan": [
                            {
                                "sample_type": "water",
                                "injection_interval": 8
                            }
                        ],
                        "assay_types": [],
                        "sample_types": ["liver", "tissue", "water"]
                    }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(self.plan, cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)

    def test_serialize_sampleassayplan(self):
        self.plan.add_sample_type('water')
        self.plan.add_sample_qc_plan_record('water', 8)

        self.assay_type.topology_modifiers = self.top_mods

        self.plan.add_assay_type(self.assay_type)
        self.plan.add_assay_plan_record('liver', self.assay_type)
        self.plan.add_assay_plan_record('tissue', self.assay_type)

        expected = ordered(
            json.loads("""{
                "sample_types": ["liver", "tissue", "water"],
                "group_size": 20,
                "sample_plan": [
                    {
                        "sampling_size": 3,
                        "sample_type": "liver"
                    },
                    {
                        "sampling_size": 5,
                        "sample_type": "tissue"
                    }
                ],
                "sample_qc_plan": [
                    {
                        "injection_interval": 8,
                        "sample_type": "water"
                    }
                ],
                "assay_types": [
                    {
                        "topology_modifiers": {
                            "distinct_libraries": 0,
                            "technical_replicates": 2,
                            "acquisition_modes": ["negative", "positive"],
                            "instruments": ["Agilent QTOF"],
                            "injection_modes": ["GC", "LC"],
                            "array_designs": ["A-AFFY-27", "A-AFFY-28"],
                            "pulse_sequences": [],
                            "chromatography_instruments": ["Agilent Q12324A"]
                        }, 
                        "technology_type": "DNA microarray", 
                        "measurement_type": "genome sequencing"
                    }],
                "assay_plan": [
                    {
                        "sample_type": "liver",
                        "assay_type": {
                            "topology_modifiers": {
                                "distinct_libraries": 0,
                                "technical_replicates": 2,
                                "acquisition_modes": ["negative", "positive"],
                                "instruments": ["Agilent QTOF"],
                                "injection_modes": ["GC", "LC"],
                                "array_designs": ["A-AFFY-27", "A-AFFY-28"],
                                "pulse_sequences": [], 
                                "chromatography_instruments": ["Agilent Q12324A"]
                            },
                            "technology_type": "DNA microarray",
                            "measurement_type": "genome sequencing"
                        }
                    },
                    {
                        "sample_type": "tissue",
                        "assay_type": {
                            "topology_modifiers": {
                                "distinct_libraries": 0, 
                                "technical_replicates": 2, 
                                "acquisition_modes": ["negative", "positive"], 
                                "instruments": ["Agilent QTOF"], 
                                "injection_modes": ["GC", "LC"], 
                                "array_designs": ["A-AFFY-27", "A-AFFY-28"], 
                                "pulse_sequences": [], 
                                "chromatography_instruments": ["Agilent Q12324A"]
                            }, 
                            "technology_type": "DNA microarray", 
                            "measurement_type": "genome sequencing"
                        }
                    }
                ]
            }""")
        )

        actual = ordered(
            json.loads(
                json.dumps(self.plan, cls=SampleAssayPlanEncoder)
            )
        )
        self.assertTrue(expected == actual)


class DecodeFromJsonTests(unittest.TestCase):

    def setUp(self):
        self.plan = SampleAssayPlan()
        self.plan.group_size = 20
        self.plan.add_sample_type('liver')
        self.plan.add_sample_type('tissue')
        self.plan.add_sample_plan_record('liver', 3)
        self.plan.add_sample_plan_record('tissue', 5)

        self.top_mods = AssayTopologyModifiers()
        self.top_mods.technical_replicates = 2
        self.top_mods.injection_modes = {'LC', 'GC'}
        self.top_mods.acquisition_modes = {'positive', 'negative'}
        self.top_mods.chromatography_instruments = {'Agilent Q12324A'}
        self.top_mods.instruments = {'Agilent QTOF'}
        self.top_mods.array_designs = {'A-AFFY-27', 'A-AFFY-28'}

        self.assay_type = AssayType(measurement_type='genome sequencing',
                                    technology_type='DNA microarray')

    def test_decode_sample_assay_plan(self):
        from isatools.create.models import SampleAssayPlanDecoder
        decoder = SampleAssayPlanDecoder()
        from io import StringIO
        sample_assay_plan = decoder.load(StringIO("""{
                "sample_types": ["liver", "tissue", "water"],
                "group_size": 20,
                "sample_plan": [
                    {
                        "sampling_size": 3,
                        "sample_type": "liver"
                    },
                    {
                        "sampling_size": 5,
                        "sample_type": "tissue"
                    }
                ],
                "sample_qc_plan": [
                    {
                        "injection_interval": 8,
                        "sample_type": "water"
                    }
                ],
                "assay_types": [
                    {
                        "topology_modifiers": {
                            "distinct_libraries": 0,
                            "technical_replicates": 2,
                            "acquisition_modes": ["negative", "positive"],
                            "instruments": ["Agilent QTOF"],
                            "injection_modes": ["GC", "LC"],
                            "array_designs": ["A-AFFY-27", "A-AFFY-28"],
                            "pulse_sequences": [],
                            "chromatography_instruments": ["Agilent Q12324A"]
                        }, 
                        "technology_type": "DNA microarray", 
                        "measurement_type": "genome sequencing"
                    }],
                "assay_plan": [
                    {
                        "sample_type": "liver",
                        "assay_type": {
                            "topology_modifiers": {
                                "distinct_libraries": 0,
                                "technical_replicates": 2,
                                "acquisition_modes": ["negative", "positive"],
                                "instruments": ["Agilent QTOF"],
                                "injection_modes": ["GC", "LC"],
                                "array_designs": ["A-AFFY-27", "A-AFFY-28"],
                                "pulse_sequences": [], 
                                "chromatography_instruments": ["Agilent Q12324A"]
                            },
                            "technology_type": "DNA microarray",
                            "measurement_type": "genome sequencing"
                        }
                    },
                    {
                        "sample_type": "tissue",
                        "assay_type": {
                            "topology_modifiers": {
                                "distinct_libraries": 0, 
                                "technical_replicates": 2, 
                                "acquisition_modes": ["negative", "positive"], 
                                "instruments": ["Agilent QTOF"], 
                                "injection_modes": ["GC", "LC"], 
                                "array_designs": ["A-AFFY-27", "A-AFFY-28"], 
                                "pulse_sequences": [], 
                                "chromatography_instruments": ["Agilent Q12324A"]
                            }, 
                            "technology_type": "DNA microarray", 
                            "measurement_type": "genome sequencing"
                        }
                    }
                ]
            }"""))

        self.plan.add_sample_type('water')
        self.plan.add_sample_qc_plan_record('water', 8)

        self.assay_type.topology_modifiers = self.top_mods

        self.plan.add_assay_type(self.assay_type)
        self.plan.add_assay_plan_record('liver', self.assay_type)
        self.plan.add_assay_plan_record('tissue', self.assay_type)

        self.assertEqual(sample_assay_plan, self.plan)