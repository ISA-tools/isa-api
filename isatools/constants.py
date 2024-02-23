SYNONYMS = 'synonyms'

MATERIAL_LABELS = [
    'Source Name',
    'Sample Name',
    'Extract Name',
    'Labeled Extract Name'
]

_LABELS_MATERIAL_NODES = [
    'Source Name',
    'Sample Name',
    'Extract Name',
    'Labeled Extract Name'
]

OTHER_MATERIAL_LABELS = ['Extract Name', 'Labeled Extract Name']

DATA_FILE_LABELS = [
    'Raw Data File',
    'Raw Spectral Data File',
    'Derived Spectral Data File',
    'Derived Array Data File',
    'Derived Array Data Matrix File',
    'Array Data File',
    'Protein Assignment File',
    'Peptide Assignment File',
    'Post Translational Modification Assignment File',
    'Acquisition Parameter Data File',
    'Free Induction Decay Data File',
    'Image File',
    'Derived Data File',
    'Metabolite Assignment File',
    'Metabolite Identification File'
]

_LABELS_DATA_NODES = [
    'Raw Data File',
    'Raw Spectral Data File',
    'Derived Spectral Data File',
    'Derived Array Data File',
    'Derived Array Data Matrix File',
    'Array Data File',
    'Protein Assignment File',
    'Peptide Assignment File',
    'Post Translational Modification Assignment File',
    'Acquisition Parameter Data File',
    'Free Induction Decay Data File',
    'Image File',
    'Derived Data File',
    'Metabolite Assignment File',
    'Metabolite Identification File'
]

NODE_LABELS = MATERIAL_LABELS + OTHER_MATERIAL_LABELS + DATA_FILE_LABELS

ASSAY_LABELS = [
    'Assay Name',
    'MS Assay Name',
    'NMR Assay Name',
    'Array Design REF',
    'Hybridization Assay Name',
    'Scan Name',
    'Normalization Name',
    'Data Transformation Name'
]

_LABELS_ASSAY_NODES = [
    'Assay Name',
    'MS Assay Name',
    'NMR Assay Name',
    'Hybridization Assay Name',
    'Scan Name',
    'Normalization Name',
    'Data Transformation Name'
]

QUALIFIER_LABELS = [
    'Protocol REF',
    'Material Type',
    'Term Source REF',
    'Term Accession Number',
    'Unit'
]

ALL_LABELS = NODE_LABELS + ASSAY_LABELS + QUALIFIER_LABELS

ALL_LABELS.append('Protocol REF')
