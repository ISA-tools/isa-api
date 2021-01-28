from collections import OrderedDict

from isatools.create.constants import SAMPLE, EXTRACT, LABELED_EXTRACT, DATA_FILE, ORGANISM_PART
from isatools.model import OntologyAnnotation

sample_list = [
        {
            'node_type': SAMPLE,
            'characteristics_category': OntologyAnnotation(term=ORGANISM_PART),
            'characteristics_value': 'liver',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': OntologyAnnotation(term=ORGANISM_PART),
            'characteristics_value': 'blood',
            'size': 5,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': OntologyAnnotation(term=ORGANISM_PART),
            'characteristics_value': 'heart',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
]

ms_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='metabolite profiling')),
    ('technology_type', OntologyAnnotation(term='mass spectrometry')),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': EXTRACT,
            'characteristics_category': OntologyAnnotation(term='extract type'),
            'characteristics_value': 'polar fraction',
            'size': 1,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': EXTRACT,
            'characteristics_category': OntologyAnnotation(term='extract type'),
            'characteristics_value': 'lipids',
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    ('labelling', {
        '#replicates': 2
    }),
    ('labelled extract', [
        {
            'node_type': LABELED_EXTRACT,
            'characteristics_category': OntologyAnnotation(term='labelled extract type'),
            'characteristics_value': '',
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    ('mass spectrometry', {
        '#replicates': 2,
        OntologyAnnotation(term='instrument'): ['Agilent QTQF 6510'],
        OntologyAnnotation(term='injection_mode'): ['FIA', 'LC'],
        OntologyAnnotation(term='acquisition_mode'): ['positive mode']
    }),
    ('raw spectral data file', [
        {
            'node_type': DATA_FILE,
            'size': 2,
            'is_input_to_next_protocols': False
        }
    ])
])

annotated_ms_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='metabolite profiling',
                                            term_accession='http://purl.obolibrary.org/obo/OBI_0000366')),
    ('technology_type', OntologyAnnotation(term='mass spectrometry',
                                           term_accession='http://purl.obolibrary.org/obo/OBI_0000470')),
    (OntologyAnnotation(
        term='extraction',
        term_accession='http://purl.obolibrary.org/obo/OBI_0302884'
    ), {}),
    (OntologyAnnotation(
        term='extract',
        term_accession='http://purl.obolibrary.org/obo/OBI_0000423'
    ), [
        {
            'node_type': EXTRACT,
            'characteristics_category': OntologyAnnotation(
                term='extract type',
                term_accession='http://purl.obolibrary.org/obo/NCIT_C82948'
            ),
            'characteristics_value': OntologyAnnotation(term='polar fraction'),
            'size': 1,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': EXTRACT,
            'characteristics_category': OntologyAnnotation(
                term='extract type',
                term_accession='http://purl.obolibrary.org/obo/NCIT_C82948'
            ),
            'characteristics_value': OntologyAnnotation(term='lipids'),
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    (OntologyAnnotation(
        term='labelling',
        term_accession='http://purl.obolibrary.org/obo/CHMO_0001675'
    ), {
        '#replicates': 2
    }),
    (OntologyAnnotation(
        term='labelled extract',
        term_accession='http://purl.obolibrary.org/obo/OBI_0000924'
    ), [
        {
            'node_type': LABELED_EXTRACT,
            'characteristics_category': OntologyAnnotation(
                term='labelled extract type',
                term_accession='http://purl.obolibrary.org/obo/NCIT_C43386'
            ),
            'characteristics_value': OntologyAnnotation(term=''),
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    (OntologyAnnotation(
        term='mass spectrometry',
        term_accession='http://purl.obolibrary.org/obo/OBI_0200085'
    ), {
        '#replicates': 2,
        OntologyAnnotation(term='instrument'): [OntologyAnnotation(
            term='Agilent QTQF 6510',
            term_accession='http://purl.obolibrary.org/obo/MS_1000676'
        )],
        OntologyAnnotation(term='injection_mode'): [
            OntologyAnnotation(
                term='FIA',
                term_accession='http://purl.obolibrary.org/obo/MS_1000058'
            ),
            OntologyAnnotation(
                term='LC',
                term_accession=''
            )
        ],
        OntologyAnnotation(term='acquisition_mode'): [
            OntologyAnnotation(
                term='positive mode',
                term_accession='http://purl.obolibrary.org/obo/MS_1002807'
            )
        ]
    }),
    (OntologyAnnotation(
        term='raw spectral data file',
        term_accession='http://purl.obolibrary.org/obo/MS_1003083'
    ), [
        {
            'node_type': DATA_FILE,
            'size': 2,
            'is_input_to_next_protocols': False
        }
    ])
])

phti_assay_dict = OrderedDict([
    ('measurement_type', 'phenotyping'),
    ('technology_type', 'high-throughput imaging'),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('phenotyping by high throughput imaging', {
                'instrument': ['lemnatech gigant'],
                'acquisition_mode': ['UV light', 'near-IR light', 'far-IR light', 'visible light'],
                'camera position': ['top','120 degree','240 degree','360 degree'],
                'imaging daily schedule': ['06.00','19.00']
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 2,
                    'is_input_to_next_protocols': False
                }
            ])
        ])

lcdad_assay_dict = OrderedDict([
    ('measurement_type', 'metabolite identification'),
    ('technology_type', 'liquid chromatography diode-array detector'),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('lcdad_spectroscopy', {
                'instrument': ['Shimadzu DAD 400'],
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 2,
                    'is_input_to_next_protocols': False
                }
            ])
        ])

nmr_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='metabolite profiling')),
    ('technology_type', OntologyAnnotation(term='nmr spectroscopy')),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': EXTRACT,
            'characteristics_category': OntologyAnnotation(term='extract type'),
            'characteristics_value': 'supernatant',
            'size': 1,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': EXTRACT,
            'characteristics_category': OntologyAnnotation(term='extract type'),
            'characteristics_value': 'pellet',
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    ('nmr spectroscopy', {
        '#replicates': 2,
        OntologyAnnotation(term='instrument'): ['Bruker AvanceII 1 GHz'],
        OntologyAnnotation(term='acquisition_mode'): ['1D 13C NMR', '2D 13C-13C NMR'],
        OntologyAnnotation(term='pulse_sequence'): ['CPMG', 'watergate']
        # 'acquisition_mode': ['1D 13C NMR', '1D 1H NMR', '2D 13C-13C NMR'],
        # 'pulse_sequence': ['CPMG', 'TOCSY', 'HOESY', 'watergate']
    }),
    ('raw spectral data file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'is_input_to_next_protocols': False
        }
    ])
])
