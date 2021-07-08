# ERROR MESSAGES: PROTOCOL NODE
PARAMETER_VALUES_ERROR = 'The \'parameter_values\' property must be an iterable of isatools.model.ParameterValue ' \
                         'objects. {0} was supplied.'
REPLICATES_ERROR = 'Replicates must be a positive integer. {0} was supplied.'
PARAMETERS_CANNOT_BE_SET_ERROR = 'The \'parameters\' property cannot be set directly. Set parameter_values instead.'
COMPONENTS_CANNOT_BE_SET_ERROR = 'The \'components\' property cannot be set.'

# ERROR MESSAGES: PRODUCT NODE
NOT_ALLOWED_TYPE_ERROR = 'The provided ProductNode is not one of the allowed values: {0}'
PRODUCT_NODE_NAME_ERROR = 'ProductNode name must be a string, {0} supplied of type {1}'
SIZE_ERROR = 'ProductNode size must be a natural number, i.e integer >= 0'
CHARACTERISTIC_TYPE_ERROR = 'A characteristic must be either a string or a Characteristic, {0} supplied'
PRODUCT_NODE_EXTENSION_ERROR = 'ProductNode extension must be either a string or an OntologyAnnotation.'

# ERROR MESSAGES: QC SAMPLE (QUALITY CONTROL)
QC_SAMPLE_TYPE_ERROR = 'qc_sample_type must be one of {0}'

# ERROR MESSAGES: QUALITY CONTROL
PRE_BATCH_ATTRIBUTE_ERROR = 'Pre-batch must be an instance of ProductNode'
POST_BATCH_ATTRIBUTE_ERROR = 'Post-batch must be an instance of ProductNode'
INTERSPERSED_SAMPLE_TYPE_NODE_ERROR = 'Interspersed sample type must be an instance of ProductNode'
INTERSPERSED_SAMPLE_TYPE_INTERVAL_TYPE_ERROR = 'Sample type interval must be a positive integer'
INTERSPERSED_SAMPLE_TYPE_INTERVAL_VALUE_ERROR = 'Sample type interval must be a positive integer'

# ERROR MESSAGES: ASSAY GRAPH
INVALID_NODE_ERROR = 'Node must be instance of isatools.create.models.SequenceNode. {0} provided'
# INVALID_LINK_ERROR = "The link to be added is not valid. Link that can be created are ProductNode->ProtocolNode
# or ProtocolNode->ProductNode."
INVALID_LINK_ERROR = 'ProductNode->ProductNode links are not allowed in an assay workflow.'
INVALID_MEASUREMENT_TYPE_ERROR = '{0} is an invalid value for measurement_type. ' \
                                 'Please provide an OntologyAnnotation or string.'
INVALID_TECHNOLOGY_TYPE_ERROR = '{0} is an invalid value for technology_type. ' \
                                'Please provide an OntologyAnnotation or string.'
MISSING_NODE_ERROR = "Start or target node have not been added to the AssayGraph yet"
NODE_ALREADY_PRESENT = "The node {0.id} is already present in the AssayGraph"
QUALITY_CONTROL_ERROR = "The 'quality_control' must be a valid QualityControl object. {0} was supplied instead."

# ERROR MESSAGES: SAMPLE AND ASSAYPLAN
ASSAY_PLAN_NAME_ERROR = 'The attribute \'name\' must be a string. {0} provided'
MISSING_SAMPLE_IN_PLAN = 'ProductNode is missing from the sample_plan'
MISSING_ASSAY_IN_PLAN = 'AsssayGraph is missing from the assay_plan'

# ERROR MESSAGES: STUDY ARM
SCREEN_ERROR_MESSAGE = 'A SCREEN cell can only be inserted into an empty arm_map.'
RUN_IN_ERROR_MESSAGE = 'A RUN-IN cell can only be inserted into an arm_map containing a SCREEN.'
WASHOUT_ERROR_MESSAGE = 'A WASHOUT cell cannot be put next to a cell ending with a WASHOUT.'
COMPLETE_ARM_ERROR_MESSAGE = 'StudyArm complete. No more cells can be added after a FOLLOW-UP cell.'
FOLLOW_UP_ERROR_MESSAGE = 'A FOLLOW-UP cell cannot be put next to a SCREEN or a RUN-IN cell.'
FOLLOW_UP_EMPTY_ARM_ERROR_MESSAGE = 'A FOLLOW-UP cell cannot be put into an empty StudyArm.'
ARM_MAP_ASSIGNMENT_ERROR = 'arm_map must be an OrderedDict'
SOURCE_TYPE_ERROR = 'The source_type property must be either a string or a Characteristic. {0} was supplied.'

# ERROR MESSAGES: STUDY DESIGN
NAME_PROPERTY_ASSIGNMENT_ERROR = 'The value assigned to \'name\' must be a string'
DESIGN_TYPE_PROPERTY_ASSIGNMENT_ERROR = 'The value assigned to \'design_type\' must be a string or OntologyAnnotation'
DESCRIPTION_PROPERTY_ASSIGNMENT_ERROR = 'The value assigned to \'description\' must be text (i.e. string)'
STUDY_ARM_PROPERTY_ASSIGNMENT_ERROR = 'The value assigned to \'study_arms\' must be an iterable'
ADD_STUDY_ARM_PARAMETER_TYPE_ERROR = 'Not a valid study arm'
ADD_STUDY_ARM_NAME_ALREADY_PRESENT_ERROR = 'A StudyArm with the same name is already present in the StudyDesign'
GET_EPOCH_INDEX_OUT_OR_BOUND_ERROR = 'The Epoch you asked for is out of the bounds of the StudyDesign.'

# ERROR MESSAGES: STUDY DESIGN FACTORY
TREATMENT_MAP_ERROR = 'treatment_map must be a list containing tuples ' \
                      'with (Treatment, StudyAssayPlan) pairs.'
GROUP_SIZES_ERROR = 'no group sizes have been provided. Group size(s) must be provided either as an integer or as' \
                    'a tuple or list of integers'
GROUP_SIZE_ERROR = 'no group_size have been provided. Group size must be provided as an integer.'
