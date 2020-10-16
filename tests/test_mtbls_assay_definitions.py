from __future__ import absolute_import
import unittest
from isatools.tests import utils
import os
import pandas as pd
import logging
import json
import shutil
import tempfile

from isatools.net.mtbls2assaydict import *


log = logging.getLogger('isatools')

__author__ = 'proccaserra@gmail.com'

MTBLS_DIR = os.path.join(os.path.dirname(__file__), '../isatools/net/resources', 'mtbls')
MTBLS_FILE = 'MetaboLightsAssayMaster-TEST.tsv'
MTBLS_CV_FILE = os.path.join(MTBLS_DIR, 'StudyTerms4Curators-template.xlsx')
MTLBS_CV_OWL = os.path.join(MTBLS_DIR, 'Metabolights.owl')

MTBLS_ASSAY_DEF_FILE = os.path.join(MTBLS_DIR, MTBLS_FILE)

print(MTBLS_ASSAY_DEF_FILE)

XLS_LOOKUP = pd.ExcelFile(MTBLS_CV_FILE)

logging.basicConfig()
logger = logging.getLogger('logger')
logger.warning('warning-message')


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class mtbls_isa_assay_definitionTest(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_mtbls_isa_assay_definition(self):

        nmr_Assay_Dict = {
            "id": 12,
            "name": "metabolite profiling by NMR",
            "icon": "fas fa-atom",
            "color": "orange",
            "measurement_type": "metabolite profiling",
            "technology_type": "NMR spectroscopy",
            "workflow": [
                [
                    {
                        "term": "sample collection",
                        "iri": None,
                        "source": None
                    }
                ],
                [
                    "sample",
                    {
                        "node_type": "sample",
                        "characteristics_category": "sample type",
                        "characteristics_value": {
                            "options": [
                                "aliquot",
                                "other"
                            ],
                            "values": []
                        },
                        "is_input_to_next_protocols": {
                            "value": True
                        }
                    }
                ],
                [
                    {
                        "term": "extraction",
                        "iri": None,
                        "source": None
                    },
                    {
                        "replicates": {
                            "value": 1
                        },
                        "Extraction Method": {
                            "options": [],
                            "values": []
                        }
                    }
                ],
                [
                    "extract",
                    {
                        "node_type": "extract",
                        "characteristics_category": "extract type",
                        "characteristics_value": {
                            "options": [
                                "polar fraction",
                                "nonpolar fraction"
                            ],
                            "values": []
                        },
                        "is_input_to_next_protocols": {
                            "value": True
                        }
                    }
                ],
                [
                    {
                        "term": "nmr sample",
                        "iri": None,
                        "source": None
                    },
                    {
                        "replicates": {
                            "value": 1
                        },
                        "NMR tube type": {
                            "options": [
                                {
                                    "term": "1.7 mm SampleJet",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1.7 mm standard",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1.7 mm (Norell)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2.5 mm standard",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "3 mm standard",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "3 mm (Norell)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "3 mm SampleJet",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "4 mm standard MAS rotor",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "4 mm Zirconia MAS rotor",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "4.25 mm (Bruker BioSpin)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "4.25 mm standard",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm (New Era)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm (Norell Inc.)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm (Wilmad-LabGlass)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm 541-pp",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm 7 in (Wilmad-LabGlass)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm 7 in 507-grade",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm SampleJet",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm Shigemi D2O matched",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm short",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm ST500-7 (Norell)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm standard",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "10 mm standard",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                }
                            ],
                            "values": []
                        },
                        "NMR solvent": {
                            "options": [
                                {
                                    "term": "0.05 mM phosphate buffered D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.01 M phosphate buffered D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.07 M phosphate buffered D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.1 M phosphate buffered D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.15 M phosphate buffered D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.2 M phosphate buffered D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.5 M phosphate buffered D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1 M phosphate buffered D2O/H2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "CD3OD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.04 M phosphate buffered D2O/H2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.07 M phosphate buffered D2O/H2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.1 M phosphate buffered D2O/H2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "phosphate sodium buffer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "CDCL3",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "H20 + D20",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "CD3OD + phosphate sodium buffer D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.2 M potassium phosphate buffered D2O + 0.128 mM TSP",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "D2O + 0.35 mM TSP",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.9% NaCl in D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.3 M saline D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "phosphate-buffered saline D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.2 M potassium phosphate buffered D2O + 5 mM maleic acid ",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "0.154 M saline D20",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "saline D2O",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                }
                            ],
                            "values": []
                        },
                        "Sample pH": {
                            "options": [],
                            "values": []
                        },
                        "Temperature": {
                            "options": [],
                            "values": []
                        }
                    }
                ],
                [
                    {
                        "term": "nmr spectroscopy",
                        "iri": None,
                        "source": None
                    },
                    {
                        "replicates": {
                            "value": 1
                        },
                        "NMR Instrument": {
                            "options": [
                                {
                                    "term": "Agilent DD2 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker 400 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker 500 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker 600 MHz Ultrashield spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker Ascend 700 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE 500 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE 700 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE 850 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE 900 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE AV 500 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE AV 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE DRX 500 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE DRX 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE DRX 700 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE HD 700 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE II 500 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE II 500 MHz Ultrashield spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE II+ 500 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE II+ 800 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE II 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE II 700 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE II 800 MHz US2 spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE III 400 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE III 500 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE III 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE III 700 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE III 800 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE III HD 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE III HD 700 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Bruker AVANCE III HD 800 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Varian Mercury AS400 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Varian Unity Inova 400 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Varian Unity Inova 500 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Varian Unity Inova 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Varian VNMR 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Varian VNMRS 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "Varian VNMRS DirectDrive 600 MHz spectrometer",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                }
                            ],
                            "values": []
                        },
                        "NMR probe": {
                            "options": [
                                {
                                    "term": "1.7 mm CPTCI 1H-13C/15N/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1.7 mm CPTCI 1H/13C/15N/D Z-GRD cryorobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2.5 mm BBO-1H/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2.5 mm QXI 1H/15N/13C/31P/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "3 mm BB 1H",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "3 mm BB 1H/X",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "3 mm 1H(X)-PFG inverse configuration",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "3.2 mm MAS BB/1H",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "4 mm HRMAS 1H/13C/2H Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "4 mm HRMAS 1H/13C/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "4 mm HRMAS 1H/13C/15N/2H Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "4 mm HR-MAS dual inverse 1H/13C with a Magic Angle gradient",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm 1H-13C cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm ATMA cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm BBI",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm BBI 1H",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm BBI 1H-BB Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm BBI 1H/D-BB Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm BBI double resonance",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm BBO-1H Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm BBO-1H/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm BBO H&F cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPBBO BB-1H/19F/D Z-GRD cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPBBO BB-1H/19F/15N/D Z/GRD cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPP 1H/19F-13C/15N/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H-13C/15N/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H/13C/15N/D Z-GRD cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H/13C/31P",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H/13C/31P Z-GRD cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H-13C/31P/D cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H-13C/31P/D Z-GRD cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H/19F-13C/15N/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H-31P/13C/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 1H-31P/13C/D Z-GRD cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTXI 1H-13C/15N/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTXO 13C/D-1H/15N Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPQCI 1H/19F-13C/15N/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPQCI 1H-31P/13C/15N/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm cryogenic",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm HCN triple resonance",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm HCN Z-gradient PFG RT",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm HRMAS BB/2H-1H MAS-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm HX",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm inverse",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm inverse 1H/13C/15N/D cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm PABBI 1H-BB/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm PABBI 1H/D-BB Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm PABBO BB-1H/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm PADUL 13C-1H/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm PATBO BB-1H/19F/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm PATXI 1H/D-13C/15N Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm PATXI 1H-13C/15N XYZ-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm PATXI 1H-13C/15N/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm QNP 1H/13C/15N/31P",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm QXI 1H/15N/13C/31P/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm TBI 1H-BB XYZ-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm TBO BB-1H/19F/D Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm Triple 1H-13C/15N/D",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm triple resonance cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm TXI",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm TXI 1H/13C/15N/D Z/GRD cryoprobe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm TXI 1H/D-13C/15N XYZ-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm TXI ATMA",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm TXI D/1H-13C/15N Z-GRD",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm TXI HCN CryoProbe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm Triple-resonance cryoprobe with z-gradients",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm Triple-resonance salt tolerant cold probe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm 4-Nucleus (13C/31P-1H/19F) (Standard Probe)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm 1H{13C,15N} triple resonance PFG salt tolerant cold probe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm 1H{13C,15N} tunable triple resonance PFG probe",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "BBI",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm CPTCI 700S4 H&F/C/N-D-05 Z",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "5 mm AutoX DB",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                }
                            ],
                            "values": []
                        },
                        "Number of transients": {
                            "options": [],
                            "values": []
                        },
                        "NMR Pulse Sequence Name": {
                            "options": [
                                {
                                    "term": "1D 1H spectrum (zg)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D 1H spectrum (zg30)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D 1H 30 deg excitation with f2 presaturation without spoiling gradient (zg30_f2pr)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D 1H T2-filter sequence eliminating J-modulation with water presaturation",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D 1H with presaturation (presat)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D 1H with presaturation (wet)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D 1H with presaturation (zgpr)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D 1H with water suppression using excitation sculpting with gradients (zgesgp)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D 13C with power-gated decoupling (zgpg)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D CPMG with presaturation (cpmgpr1d)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D CPMG with T2 filter and presaturation (ereticcpmgpr1d)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D homonuclear MQS with selective pulses, without gradients, selects both ZQC and DQC (SSelMQC_refoc_ph)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D NOESY with presaturation (metnoesy)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D NOESY with presaturation (noesypr1d)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D NOESY with presaturation (modified) (pusenoesypr1d)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D NOESY with presaturation (tnnoesy)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D NOESY with presaturation and spoil gradients (noesygppr1d)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D NOESY with presaturation during relaxation delay and mixing time and spoil gradient (noesygppr1d_kr)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D NOESY 12C custom filtered with presaturation, phase-sensitive gradients, and 13C decoupling (c12filternoesygpc13cpd)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D NOESY 12C 13C custom filtered with presaturation, phase-sensitive gradients, and 13C decoupling (c12c13filternoesygpc13cpd)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "1D PROJECT with presaturation (projectedpr)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D 1H-13C HSQC (hsqcetgppr)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D homonuclear correlation via dipolar coupling (noesyesgpph)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D HSQC with presaturation (hsqcphpr)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D HSQC using echo-antiecho detection and gradient pulses (hsqcedetgp)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D HSQC using echo-antiecho and adiabatic pulses for inversion and refocusing (hsqcetgpsp.2)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D HSQC using echo-antiecho and adiabatic pulses for inversion and refocusing with additional water suppression (hsqcetgpsp.2.cl)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D HSQC using echo-antiecho-TPPI gradient selection, constant time, trim pulses, shaped pulses for inversion, no refocussing, off-resonance pulse (hsqcctetgpsp.2)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D HSQC using PEP and adiabatic pulses for inversion and refocusing with gradients in back-inept (hsqcetgpsisp2.2)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D HSQC using PEP and adiabatic pulses for inversion and refocusing with gradients in back-inept and suppression of COSY type artefacts (hsqcetgpsisp2.3)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D Interleaved Ultrafast COSY (iufcosy)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D JRES with excitation sculpting & additional water suppression (jresesgp2)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D JRES with homonuclear J-resolved 2D correlation (jresesgp)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D JRES with homonuclear J-resolved 2D correlation, presaturation during relaxation delay with gradients (jresgpprqf)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D TOCSY with phase sensitive water suppression using MLEV (mlevesgpph)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D TOCSY with presaturation using MLEV (mlevphpr)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "2D Zero-quantum-filtered total correlation spectra (zTOCSY-em-3)",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                },
                                {
                                    "term": "M3S COSY",
                                    "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                    "source": None
                                }
                            ],
                            "values": []
                        },
                        "NMR Magnetic field strength": {
                            "options": [],
                            "values": []
                        }
                    }
                ],
                [
                    {
                        "term": "raw spectral data file",
                        "iri": "http://nmrML.org/nmrCV#NMR:1400119",
                        "source": None
                    },
                    {
                        "node_type": "data file",
                        "is_input_to_next_protocols": {
                            "value": True
                        }
                    }
                ],
                [
                    {
                        "term": "nmr assay",
                        "iri": None,
                        "source": None
                    }
                ],
                [
                    {
                        "term": "data transformation",
                        "iri": None,
                        "source": None
                    }
                ],
                [
                    {
                        "term": "metabolite identification",
                        "iri": None,
                        "source": None
                    }
                ]
            ],
            "@context": {
                "measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
                "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521",
                "NMR tube type": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                "NMR solvent": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                "NMR Instrument": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                "NMR probe": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                "NMR Pulse Sequence Name": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854"
            }
        }

        # test_assay_dict = parse_mtbls_assay_def(MTBLS_ASSAY_DEF_FILE)
        test_assay_dict = json.dumps(parse_mtbls_assay_def(MTBLS_ASSAY_DEF_FILE), indent=4)
        self.assertTrue(test_assay_dict, nmr_Assay_Dict)


if __name__ == '__main__':
    unittest.main()
