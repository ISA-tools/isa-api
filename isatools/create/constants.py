# NON TREATMENT TYPES
import os
import yaml
from isatools.model import OntologyAnnotation, StudyFactor, OntologySource, Characteristic

SCREEN = 'screen'
RUN_IN = 'run-in'
WASHOUT = 'washout'
FOLLOW_UP = 'follow-up'
OBSERVATION_PERIOD = 'observation period'
ELEMENT_TYPES = dict(
    SCREEN=SCREEN,
    RUN_IN=RUN_IN,
    WASHOUT=WASHOUT,
    FOLLOW_UP=FOLLOW_UP,
    OBSERVATION_PERIOD=OBSERVATION_PERIOD
)

# TREATMENT/INTERVENTION TYPES
INTERVENTIONS = dict(CHEMICAL='chemical intervention',
                     BEHAVIOURAL='behavioural intervention',
                     SURGICAL='surgical intervention',
                     BIOLOGICAL='biological intervention',
                     RADIOLOGICAL='radiological intervention',
                     DIETARY='dietary intervention',
                     UNSPECIFIED='unspecified intervention')

# FACTOR_TYPES
# The three base factors in our model are AGENT, INTENSITY, and DURATION
FACTOR_TYPES = dict(AGENT_VALUES='agent values',
                    INTENSITY_VALUES='intensity values',
                    DURATION_VALUES='duration values')
DURATION_FACTOR_ = dict(name='DURATION', type=OntologyAnnotation(term="time"),
                        display_singular='DURATION VALUE',
                        display_plural='DURATION VALUES', values=set())
DURATION_FACTOR = StudyFactor(name=DURATION_FACTOR_['name'], factor_type=DURATION_FACTOR_.get('type', None))
BASE_FACTORS_ = (
    dict(
        name='AGENT', type=OntologyAnnotation(term="perturbation agent"),
        display_singular='AGENT VALUE',
        display_plural='AGENT VALUES', values=set()
    ),
    dict(
        name='INTENSITY', type=OntologyAnnotation(term="intensity"),
        display_singular='INTENSITY VALUE',
        display_plural='INTENSITY VALUES', values=set()
    ),
    DURATION_FACTOR_
)
BASE_FACTORS = (
    StudyFactor(name=BASE_FACTORS_[0]['name'],
                factor_type=BASE_FACTORS_[0].get('type', None)),
    StudyFactor(name=BASE_FACTORS_[1]['name'],
                factor_type=BASE_FACTORS_[1].get('type', None)),
    DURATION_FACTOR,
)

# Is treatment EPOCH
IS_TREATMENT_EPOCH = 'study step with treatment'

# Sequence Order Study Factor
SEQUENCE_ORDER_FACTOR_ = dict(
    name='Sequence Order',
    type=OntologyAnnotation(term='sequence order')
)

SEQUENCE_ORDER_FACTOR = StudyFactor(
    name=SEQUENCE_ORDER_FACTOR_['name'],
    factor_type=SEQUENCE_ORDER_FACTOR_['type']
)

# Allowed types of product nodes in ISA create mode
SOURCE = 'source'
SAMPLE = 'sample'
EXTRACT = 'extract'
LABELED_EXTRACT = 'labeled extract'
DATA_FILE = 'data file'

# constant to specify the default sample assay name
DEFAULT_SAMPLE_ASSAY_PLAN_NAME = 'SAMPLE ASSAY PLAN'

# sample organism part category
ORGANISM_PART = 'organism part'

# constant for naming Groups, Subjects, Samples, AssayGraphs
GROUP_PREFIX = 'GRP'
SUBJECT_PREFIX = 'SBJ'
SAMPLE_PREFIX = 'SMP'
EXTRACT_PREFIX = 'EXTR'
LABELED_EXTRACT_PREFIX = 'LBLEXTR'
ASSAY_GRAPH_PREFIX = 'AT'   # AT stands for Assay Type

with open(os.path.join(os.path.dirname(__file__), '..', 'resources', 'config', 'yaml',
                       'study-creator-config.yml')) as yaml_file:
    yaml_config = yaml.load(yaml_file, Loader=yaml.FullLoader)
default_ontology_source_reference = OntologySource(**yaml_config['study']['ontology_source_references'][1])

# constants specific to the sampling plan in the study generation from the study design
RUN_ORDER = yaml_config['study']['protocols'][0]['parameters'][0]
STUDY_CELL = yaml_config['study']['protocols'][0]['parameters'][1]
with open(os.path.join(os.path.dirname(__file__), '..', 'resources', 'config', 'yaml',
                       'assay-options.yml')) as yaml_file:
    assays_opts = yaml.load(yaml_file, Loader=yaml.FullLoader)
DEFAULT_SOURCE_TYPE = Characteristic(
    category=OntologyAnnotation(
        term='Study Subject',
        term_source=default_ontology_source_reference,
        term_accession='http://purl.obolibrary.org/obo/NCIT_C41189'
    ),
    value=OntologyAnnotation(
        term='Human',
        term_source=default_ontology_source_reference,
        term_accession='http://purl.obolibrary.org/obo/NCIT_C14225'
    )
)

# CONSTANTS/PARAMS FOR QUALITY CONTROL
SOURCE_QC_SOURCE_NAME = 'source_QC'
QC_SAMPLE_NAME = 'sample_QC'
QC_SAMPLE_TYPE_PRE_RUN = 'QC sample type pre-run'
QC_SAMPLE_TYPE_POST_RUN = 'QC sample type post-run'
QC_SAMPLE_TYPE_INTERSPERSED = 'QC sample type interspersed'

# constant for padding digits in node names in isa documents creation
ZFILL_WIDTH = 3

# Default performer
DEFAULT_PERFORMER = 'Unknown'

# Default study identifier
DEFAULT_STUDY_IDENTIFIER = 's_01'
DEFAULT_INVESTIGATION_IDENTIFIER = 'i_01'

# Default file extension (no dot required)
DEFAULT_EXTENSION = 'raw'
