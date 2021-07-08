from isatools.create.model import *

NAME = 'name'



rna_seq_dict = OrderedDict([
    ('measurement_type', 'transcription profiling'),
    ('technology_type', 'nucleic acid sequencing'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'total RNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'mRNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'ncRNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'miRNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('nucleic_acid_sequencing', {
                'platform': ['454','Illumina','Ion Torrent','AB Solid','Oxford Nanopore'],
                'instrument': ["454 GS","454 GS 20","454 GS FLX","454 GS FLX Plus","454 GS FLX Titanium","454 GS Junior","Illumina Genome Analyzer II",
    "Illumina Genome Analyzer Iix",
    "Illumina HiSeq 1000",
    "Illumina HiSeq  2000",
    "Illumina HiSeq",
    "Illumina HiSeq 2500",
    "Illumina HiSeq 3000",
    "Illumina HiSeq 4000",
    "Illumina HiScanSQ",
    "Illumina MiSeq",
    "HiSeq X Five",
    "HiSeq X Ten",
    "NextSeq 500",
    "NextSeq 550",
    "Ion Torrent PGM",
    "Ion Torrent Proton",
    "AB 3730xL Genetic Analyzer",
    "AB SOLiD System",
    "AB SOLiD System 2.0",
    "AB SOLiD System 3.0",
    "AB SOLiD 3 Plus System",
    "AB SOLiD 4 System",
    "AB SOLiD 4hq System",
    "AB SOLiD 5500",
    "AB SOLiD 5500xl",
    "AB 5500 Genetic Analyzer",
    "AB 5500xl Genetic analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 3130xL Genetic Analyzer",
    "AB 3130 Genetic Analyzer",
    "AB 310 Genetic Analyzer",
    "unspecified",
    "MinIon",
    "GridIon"],
                'library_strategy': ["AMPLICON","RNA-Seq","ssRNA-seq","miRNA-Seq","ncRNA-Seq","FL-cDNA","EST","OTHER"],
                'library_layout': ['single','paired'],
                'library_selection': ["RANDOM","PCR","RT-PCR","RANDOM PCR","cDNA","cDNA_randomPriming","cDNA_oligo_dT","PolyA,Oligo-dT","Inverse rRNA","Inverse rRNA selection","CAGE","RACE","other","unspecified"]
            }),
    ('raw_data_file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'technical_replicates': 1,
            'is_input_to_next_protocols': False
        }
    ])

])


chip_seq_dict = rna_seq_dic = OrderedDict([
    ('measurement_type', 'chromatin modification profiling'),
    ('technology_type', 'nucleic acid sequencing'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'single cell genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'METAGENOMIC',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'miRNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('nucleic_acid_sequencing', {
                'platform': ['454','Illumina','Ion Torrent','AB Solid','Oxford Nanopore'],
                'instrument': ["454 GS","454 GS 20","454 GS FLX","454 GS FLX Plus","454 GS FLX Titanium","454 GS Junior","Illumina Genome Analyzer II",
    "Illumina Genome Analyzer Iix",
    "Illumina HiSeq 1000",
    "Illumina HiSeq  2000",
    "Illumina HiSeq",
    "Illumina HiSeq 2500",
    "Illumina HiSeq 3000",
    "Illumina HiSeq 4000",
    "Illumina HiScanSQ",
    "Illumina MiSeq",
    "HiSeq X Five",
    "HiSeq X Ten",
    "NextSeq 500",
    "NextSeq 550",
    "Ion Torrent PGM",
    "Ion Torrent Proton",
    "AB 3730xL Genetic Analyzer",
    "AB SOLiD System",
    "AB SOLiD System 2.0",
    "AB SOLiD System 3.0",
    "AB SOLiD 3 Plus System",
    "AB SOLiD 4 System",
    "AB SOLiD 4hq System",
    "AB SOLiD 5500",
    "AB SOLiD 5500xl",
    "AB 5500 Genetic Analyzer",
    "AB 5500xl Genetic analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 3130xL Genetic Analyzer",
    "AB 3130 Genetic Analyzer",
    "AB 310 Genetic Analyzer",
    "unspecified",
    "MinIon",
    "GridIon"],
                'library_strategy': ["Hi-C","ATAC-seq","ChIP-Seq","Targeted Capture","Tethered Chromatin Conformation Capture","OTHER"],
                'library_layout': ['single','paired'],
                'library_selection': ["MDA","ChIP","Hybrid Selection","Reduced Representation","Restriction digest","padlock probes capture method","other","unspecified","other","unspecified"]
            }),
    ('raw_data_file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'technical_replicates': 1,
            'is_input_to_next_protocols': False
        }
    ])

])


meth_seq_dict = OrderedDict([
    ('measurement_type', 'DNA methylation profiling'),
    ('technology_type', 'nucleic acid sequencing'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'single cell genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'METAGENOMIC',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'miRNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('nucleic_acid_sequencing', {
                'platform': ['454','Illumina','Ion Torrent','AB Solid','Oxford Nanopore'],
                'instrument': ["454 GS","454 GS 20","454 GS FLX","454 GS FLX Plus","454 GS FLX Titanium","454 GS Junior","Illumina Genome Analyzer II",
    "Illumina Genome Analyzer Iix",
    "Illumina HiSeq 1000",
    "Illumina HiSeq  2000",
    "Illumina HiSeq",
    "Illumina HiSeq 2500",
    "Illumina HiSeq 3000",
    "Illumina HiSeq 4000",
    "Illumina HiScanSQ",
    "Illumina MiSeq",
    "HiSeq X Five",
    "HiSeq X Ten",
    "NextSeq 500",
    "NextSeq 550",
    "Ion Torrent PGM",
    "Ion Torrent Proton",
    "AB 3730xL Genetic Analyzer",
    "AB SOLiD System",
    "AB SOLiD System 2.0",
    "AB SOLiD System 3.0",
    "AB SOLiD 3 Plus System",
    "AB SOLiD 4 System",
    "AB SOLiD 4hq System",
    "AB SOLiD 5500",
    "AB SOLiD 5500xl",
    "AB 5500 Genetic Analyzer",
    "AB 5500xl Genetic analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 3130xL Genetic Analyzer",
    "AB 3130 Genetic Analyzer",
    "AB 310 Genetic Analyzer",
    "unspecified",
    "MinIon",
    "GridIon"],
                'library_strategy': ["Bisulfite-Seq","MRE-Seq","MeDIP-Seq","MBD-Seq","MNase-Seq","DNase-Hypersensitivity","RAD-Seq","OTHER"],
                'library_layout': ['single','paired'],
                'library_selection': ["MDA","PCR","HMPR","MF","MSLL","Restriction Digest","MNas","DNase","ChIP","5-methylcytidine antibody","MBD2 protein methyl-CpG binding domain","Hybrid Selection","Reduced Representation","padlock probes capture method","other","unspecified"]
            }),
    ('raw_data_file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'technical_replicates': 1,
            'is_input_to_next_protocols': False
        }
    ])

])



exom_seq_dict = OrderedDict([
    ('measurement_type', 'exome sequencing'),
    ('technology_type', 'nucleic acid sequencing'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'single cell genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'METAGENOMIC',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'miRNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('nucleic_acid_sequencing', {
                'platform': ['454','Illumina','Ion Torrent','AB Solid','Oxford Nanopore'],
                'instrument': ["454 GS","454 GS 20","454 GS FLX","454 GS FLX Plus","454 GS FLX Titanium","454 GS Junior","Illumina Genome Analyzer II",
    "Illumina Genome Analyzer Iix",
    "Illumina HiSeq 1000",
    "Illumina HiSeq  2000",
    "Illumina HiSeq",
    "Illumina HiSeq 2500",
    "Illumina HiSeq 3000",
    "Illumina HiSeq 4000",
    "Illumina HiScanSQ",
    "Illumina MiSeq",
    "HiSeq X Five",
    "HiSeq X Ten",
    "NextSeq 500",
    "NextSeq 550",
    "Ion Torrent PGM",
    "Ion Torrent Proton",
    "AB 3730xL Genetic Analyzer",
    "AB SOLiD System",
    "AB SOLiD System 2.0",
    "AB SOLiD System 3.0",
    "AB SOLiD 3 Plus System",
    "AB SOLiD 4 System",
    "AB SOLiD 4hq System",
    "AB SOLiD 5500",
    "AB SOLiD 5500xl",
    "AB 5500 Genetic Analyzer",
    "AB 5500xl Genetic analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 3130xL Genetic Analyzer",
    "AB 3130 Genetic Analyzer",
    "AB 310 Genetic Analyzer",
    "unspecified",
    "MinIon",
    "GridIon"],
                'library_strategy': ["WGX","OTHER"],
                'library_layout': ['single','paired'],
                'library_selection': ["MDA","Hybrid Selection","PCR","Reduced Representation","other","unspecified"]
            }),
    ('raw_data_file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'technical_replicates': 1,
            'is_input_to_next_protocols': False
        }
    ])

])



whole_genome_seq_dict = OrderedDict([
    ('measurement_type', 'genome sequencing'),
    ('technology_type', 'nucleic acid sequencing'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'single cell genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'METAGENOMIC',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'miRNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('nucleic_acid_sequencing', {
                'platform': ['454','Illumina','Ion Torrent','AB Solid','Oxford Nanopore'],
                'instrument': ["454 GS","454 GS 20","454 GS FLX","454 GS FLX Plus","454 GS FLX Titanium","454 GS Junior","Illumina Genome Analyzer II",
    "Illumina Genome Analyzer Iix",
    "Illumina HiSeq 1000",
    "Illumina HiSeq  2000",
    "Illumina HiSeq",
    "Illumina HiSeq 2500",
    "Illumina HiSeq 3000",
    "Illumina HiSeq 4000",
    "Illumina HiScanSQ",
    "Illumina MiSeq",
    "HiSeq X Five",
    "HiSeq X Ten",
    "NextSeq 500",
    "NextSeq 550",
    "Ion Torrent PGM",
    "Ion Torrent Proton",
    "AB 3730xL Genetic Analyzer",
    "AB SOLiD System",
    "AB SOLiD System 2.0",
    "AB SOLiD System 3.0",
    "AB SOLiD 3 Plus System",
    "AB SOLiD 4 System",
    "AB SOLiD 4hq System",
    "AB SOLiD 5500",
    "AB SOLiD 5500xl",
    "AB 5500 Genetic Analyzer",
    "AB 5500xl Genetic analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 3130xL Genetic Analyzer",
    "AB 3130 Genetic Analyzer",
    "AB 310 Genetic Analyzer",
    "unspecified",
    "MinIon",
    "GridIon"],
                'library_strategy': ["WGS","OTHER"],
                'library_layout': ['single','paired'],
                'library_selection': ["RANDOM","other","unspecified"]
            }),
    ('raw_data_file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'technical_replicates': 1,
            'is_input_to_next_protocols': False
        }
    ])

])




env_gene_survey_dict = OrderedDict([
    ('measurement_type', 'environmental gene survey'),
    ('technology_type', 'nucleic acid sequencing'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'single cell genomic DNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'METAGENOMIC',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'miRNA',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('library_construction', {
        'target_taxon': ["Archeae","Bacteria","Eukaryota"],
        'target_gene': ["16S rRNA","18S rRNA","RBCL","mat","COX1","ITS1-5.8S-ITS2"],
        'target_subfragment': ["V6","V9","ITS"],
        'pcr_cond':[],
        'mid':[],
    }),

    ('nucleic_acid_sequencing', {
                'platform': ['454','Illumina','Ion Torrent','AB Solid','Oxford Nanopore'],
                'instrument': ["454 GS","454 GS 20","454 GS FLX","454 GS FLX Plus","454 GS FLX Titanium","454 GS Junior","Illumina Genome Analyzer II",
    "Illumina Genome Analyzer Iix",
    "Illumina HiSeq 1000",
    "Illumina HiSeq  2000",
    "Illumina HiSeq",
    "Illumina HiSeq 2500",
    "Illumina HiSeq 3000",
    "Illumina HiSeq 4000",
    "Illumina HiScanSQ",
    "Illumina MiSeq",
    "HiSeq X Five",
    "HiSeq X Ten",
    "NextSeq 500",
    "NextSeq 550",
    "Ion Torrent PGM",
    "Ion Torrent Proton",
    "AB 3730xL Genetic Analyzer",
    "AB SOLiD System",
    "AB SOLiD System 2.0",
    "AB SOLiD System 3.0",
    "AB SOLiD 3 Plus System",
    "AB SOLiD 4 System",
    "AB SOLiD 4hq System",
    "AB SOLiD 5500",
    "AB SOLiD 5500xl",
    "AB 5500 Genetic Analyzer",
    "AB 5500xl Genetic analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 5500xl-W Genetic Analysis System",
    "AB 3730 Genetic Analyzer",
    "AB 3130xL Genetic Analyzer",
    "AB 3130 Genetic Analyzer",
    "AB 310 Genetic Analyzer",
    "unspecified",
    "MinIon",
    "GridIon"],
                'library_strategy': ["AMPLICON"],
                'library_layout': ['single','paired'],
                'library_selection': ["RANDOM","other","unspecified"]
            }),
    ('raw_data_file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'technical_replicates': 1,
            'is_input_to_next_protocols': False
        }
    ])

])









nmr_assay_dict = OrderedDict([
    ('measurement_type', 'metabolite profiling'),
    ('technology_type', 'nmr spectroscopy'),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': SAMPLE,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': SAMPLE,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('nmr_spectroscopy', {
                'instrument': ['Bruker AvanceII 1 GHz'],
                'acquisition_mode': ['1D 13C NMR','1D 1H NMR','2D 13C-13C NMR'],
                'pulse_sequence': ['CPMG','TOCSY','HOESY','watergate']
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 1,
                    'is_input_to_next_protocols': False
                }
            ])
        ])

sirm_nmr_assay_dict = OrderedDict([
    ('measurement_type', 'isotopomer analysis'),
    ('technology_type', 'nmr spectroscopy'),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': SAMPLE,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': SAMPLE,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('nmr_spectroscopy', {
                'instrument': ['Bruker AvanceII 1 GHz'],
                'acquisition_mode': ['1D 13C NMR','1D 1H NMR','2D 13C-13C NMR'],
                'pulse_sequence': ['CPMG','TOCSY','HOESY','watergate']
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


ms_assay_dict = OrderedDict([
    ('measurement_type', 'metabolite profiling'),
    ('technology_type', 'mass spectrometry'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'polar fraction',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'lipids',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('labelling', {}),
    ('labelled extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'labelled extract type',
            'characteristics_value': '',
            'size': 2,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('mass spectrometry', {
        'instrument': ['Agilent QTQF §'],
        'injection_mode': ['FIA', 'LC'],
        'acquisition_mode': ['positive mode']
    }),
    ('raw spectral data file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'technical_replicates': 2,
            'is_input_to_next_protocols': False
        }
    ])
])

sirm_ms_assay_dict = OrderedDict([
    ('measurement_type', 'isotopologue analysis'),
    ('technology_type', 'mass spectrometry'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'polar fraction',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'extract type',
            'characteristics_value': 'lipids',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('labelling', {}),
    ('labelled extract', [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'labelled extract type',
            'characteristics_value': '',
            'size': 2,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
    ]),
    ('mass spectrometry', {
        'instrument': ['Agilent QTQF §'],
        'injection_mode': ['FIA', 'LC'],
        'acquisition_mode': ['positive mode']
    }),
    ('raw spectral data file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'technical_replicates': 2,
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
                    'node_type': SAMPLE,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': SAMPLE,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('phenotyping by high throughput imaging', {
                'instrument': ['lemnatech gigant'],
                'acquisition_mode': ['UV light','near-IR light','far-IR light','visible light'],
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
                    'node_type': SAMPLE,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': SAMPLE,
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

