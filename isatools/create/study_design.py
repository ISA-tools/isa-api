from itertools import product
from itertools import izip
from itertools import permutations
import uuid

__author__ = 'prs'


def remove_duplicate_from_list(some_list):
    # and some_list.contains(',')
    if len(some_list) > 0:
        # removes trailing whitespace in a list such as a,b ,c ,c
        list_values = [x.strip() for x in some_list.split(',')]
        # removes any duplicate values in a list such as a,a,b,c
        list_values_nodup = list(set(list_values))
        # removes any empty string supplied as is a,,c,d
        list_values_nodup = filter(bool, list_values_nodup)
    else:
        print "the list you have supplied is not valid, please enter a csv list"

    return list_values_nodup


def compute_study_groups(factor_and_levels):
    # todo: rename compute_study_groups to compute_treatment
    study_groups = [dict(izip(factor_and_levels, x)) for x in product(*factor_and_levels.itervalues())]
    # print study_groups
    return study_groups


def get_number_of_factors():
    number = raw_input("how many study factors are there? (provide an integer): ")
    return number


def intervention_or_observation():
    is_intervention = True
    inter_or_obs = raw_input("is the study an intervention or an observation? (intervention/observation)")
    if inter_or_obs == "intervention":
        is_intervention = True

    elif inter_or_obs == "observation":
        is_intervention = False

    else:
        print "answer should be either 'intervention' or 'observation'"
        print "answer not recognized, choose between 'intervention' or 'observation'"

    return is_intervention


def single_or_repeated_treatment():

    treatment_repeat_input = raw_input("are study subjects exposed to a single intervention or to multiple intervention"
                                 " (applied sequentially)? (choose either 'single' or 'multiple')")
    if treatment_repeat_input == 'single':
        treatment_repeat = False
    elif treatment_repeat_input == 'multiple':
        treatment_repeat = True
    else:
        print 'invalid input, please try again'
        single_or_repeated_treatment()

    return treatment_repeat


def get_repeat_number():

    nbr_of_repeats_input = raw_input("how many interventions each subject receives in total (enter an integer)? ")
    nbr_of_repeats = int(nbr_of_repeats_input)
    return nbr_of_repeats


def get_list_of_interventions():
    # IMPORTANT: we will first only support symmetric arms
    treatment_type_list = raw_input("list the different intervention types (comma-separated-values from the following"
                                    " options {chemical intervention, behavioral intervention, surgical intervention,"
                                    " biological intervention, radiological intervention }): ")
    treatment_type_list = remove_duplicate_from_list(treatment_type_list)

    treatment_types = {}
    for treatment_type in treatment_type_list:
        treatment_type.strip()
        if treatment_type == "chemical intervention":
            treatment_types["chemical intervention"] = {"agent": [], "dose": [], "duration of exposure": []}
            # set_factor_as_key("chemical agent", factor_dict)

        if treatment_type == "behavioral intervention":
            # set_factor_as_key("behavioral agent", factor_dict)
            treatment_types["behavioral intervention"] = {"agent": [], "dose": [], "duration of exposure": []}

        if treatment_type == "surgical intervention":
            # set_factor_as_key("surgery", factor_dict)
            treatment_types["surgical intervention"] = {"surgery procedure": [], "dose": [], "duration post surgery": []}

        if treatment_type == "biological intervention":
            # set_factor_as_key("biological agent", factor_dict)
            treatment_types["biological intervention"] = {"agent": [], "dose": [], "duration of exposure": []}

        if treatment_type == "radiological intervention":
            # set_factor_as_key("radiological agent", factor_dict)
            treatment_types["radiological intervention"] = {"agent": [], "dose": [],
                                                          "duration of exposure": []}

    return treatment_types


#
#     """if treatment_list != "" and treatment_list.isalnum():
#        return treatment_list
#     else:
#        print "the treatments supplied are not valid, please enter a string: "
#        """
#
#     """if treatment"""
#
#
# """def get_factors_from_treatment_type(treatment_type_list):"""


def compute_treatment_sequences(treatments, num_repeats):
    treatment_sequences = list(permutations(treatments, num_repeats))
    return treatment_sequences


def get_factor_name():
    factor_name = raw_input("provide factor name: ")
    if factor_name != "" and factor_name.isalnum():
        return factor_name
    else:
        print "the factor supplied is not valid, please enter a string: "


def set_factor_as_key(factor_name, factor_dict):
    this_factor_dict = factor_dict
    if factor_name not in factor_dict.keys():
        this_factor_dict[factor_name] = []
    else:
        print "factor already declared! define a new factor"
        get_factor_name()
    return this_factor_dict


def set_factorvalues(factor_name, factor_dict):

    factor_values = raw_input("provide the factor levels associated with '" + factor_name + "' as a list of comma separated values: ")
    factor_values = remove_duplicate_from_list(factor_values)
    for element in factor_values:
        factor_dict[factor_name].append(element)
    return factor_dict


def balanced_design():
    balanced_design_var = raw_input("Do all groups of the same size, the same number of subjects "
                                    "(in other words are the groups balanced)? (balanced/unbalanced)")
    if balanced_design_var == "balanced":
        is_balanced = True
        return is_balanced
    elif balanced_design_var == "unbalanced":
        is_balanced = False
        return is_balanced
    else:
        print "answer should be either 'balanced' or 'unbalanced'"
        print "answer not recognized, choose between 'balanced' or 'unbalanced'"


def full_or_fractional():
    full_or_fract = raw_input("did you use a all possible groups or only a subset? (full/fractional)")
    if full_or_fract == "full":
        full_or_fract = True
    elif full_or_fract == "fractional":
        full_or_fract = False
    else:
        print "answer not recognized, choose between 'full' or 'fractional'"

    return full_or_fract


def set_study_arms(nb_repeats):
    study_groups = {}
    # forf = full_or_fractional()
    bd = balanced_design()
    j = 0
    if bd is True and repeats is False:
        size = raw_input("provide the number of subject per study group (must be an integer): ")
        if size.isdigit():
            size = int(size)
            if int(size) > 0:
                study_group_size = size
                for j in range(len(study_factor_combo)):
                    study_groups["guid"] = uuid.uuid4()
                    study_groups["id"] = j
                    study_groups["factor_level_combo"] = study_factor_combo[j]
                    study_groups["size"] = study_group_size
                    print study_groups
        else:
            print "invalid input, please try again"

    elif bd is False and repeats is False:
        for j in range(len(study_factor_combo)):
            study_groups["guid"] = uuid.uuid4()
            study_groups["id"] = j
            study_groups["factor_level_combo"] = study_factor_combo[j]
            size = raw_input("provide the number of subject per study group (must be an integer): ")
            size = int(size)
            if int(size) > 0:
                study_group_size = size
                study_groups["size"] = study_group_size
            else:
                print "invalid input, please try again"

            print study_groups

    elif bd is False and repeats is True:

        # nb_repeats=raw_input("state the number of consecutive treatments (integer): ")
        # print study_factor_combo
        sequences = compute_treatment_sequences(study_factor_combo, int(nb_repeats))
        print "sequences"
        for j in range(len(sequences)):
            study_groups["guid"] = uuid.uuid4()
            study_groups["id"] = j
            study_groups["sequence"] = sequences[j]
            size = raw_input("provide the number of subject per study arm (must be an integer): ")
            size = int(size)
            if int(size) > 0:
                study_group_size = size
                study_groups["size"] = study_group_size
            else:
                print "invalid input, please try again"

    else:
        # nb_repeats=raw_input("state the number of consecutive treatments (integer): ")
        # print study_factor_combo
        sequences = compute_treatment_sequences(study_factor_combo, int(nb_repeats))
        print(sequences)
        for j in range(len(sequences)):
            study_groups["guid"] = uuid.uuid4()
            study_groups["id"] = j
            study_groups["sequence"] = sequences[j]
            size = raw_input("provide the number of subject per study arm (must be an integer): ")
            size = int(size)
            if int(size) > 0:
                study_group_size = size
                study_groups["size"] = study_group_size
            else:
                print "invalid input, please try again"

            print study_groups

def collection_sample_type():

    sample_types = raw_input("list the type of sample collected from each study group member as csv list: ")
    # for example: blood,urine,sweat,muscle
    sample_types = remove_duplicate_from_list(sample_types)
    return sample_types


def sample_collection_plan(sample_types):

    common2all = raw_input("is the sampling plan applicable to all samples? (yes/no)")

    if common2all == 'yes':
        sampling_events = raw_input("list all sampling points as csv list: ")
        sampling_events = remove_duplicate_from_list(sampling_events)
        return sampling_events

    elif common2all == 'no':
        samples_and_events = {}
        for s_type in sample_types:
            specific_sampling_events = raw_input("list sampling events for this sample type as csv:")
            specific_sampling_events = remove_duplicate_from_list(specific_sampling_events)
            samples_and_events[s_type] = specific_sampling_events

        return samples_and_events

    else:
        print "please say yes or no"



intervention_check = intervention_or_observation()

intervention_list = []

if intervention_check is True:

    repeats = single_or_repeated_treatment()

    if repeats is False:
        print("single exposure experiment")
        intervention_list = get_list_of_interventions()
        for intervention_type in intervention_list.keys():
            print("type of intervention: ", intervention_type)
            for factor in intervention_list[intervention_type].keys():
                print("factor :", factor)
                set_factorvalues(factor,intervention_list[intervention_type])
                print("associated factor values:", intervention_list[intervention_type][factor])

        # if nbf.isdigit():
        #     nbf = int(nbf)
        #     if nbf > 0:
        #         nbf
        #     else:
        #         print "try again, this is not a valid value"
        #         nbf = get_number_of_factors()
        # else:
        #     nbf = 0
        #     print "try again, this is not a valid value"
        #     nbf = get_number_of_factors()

        # my_factors = {}
        # i = 0
        # while i < nbf:
        #     my_factor_as_key = get_factor_name()
        #     my_factors = set_factor_as_key(my_factor_as_key, my_factors)
        #     my_factors = set_factorvalues(my_factor_as_key, my_factors)
        #     i+1
        #
        # study_factor_combo = compute_study_groups(my_factors)
        study_factor_combo = compute_study_groups(intervention_list[intervention_type])
        print("study groups:", study_factor_combo)
        set_study_arms()

    else:
        print("""we deal with a cross over design and repeated treatment case""")
        my_factors = {}
        study_factor_combo = []
        number_of_repeats = get_repeat_number()
        intervention_list = get_list_of_interventions()
        """factors_for_treatment = get_factors_from_treatment_type(intervention_list)"""
        for intervention_type in intervention_list.keys():
            print("type of intervention: ", intervention_type)
            for factor in intervention_list[intervention_type].keys():
                print("factor :", factor)
                set_factorvalues(factor, intervention_list[intervention_type])
                print("associated factor values:", intervention_list[intervention_type][factor])

            study_factor_combo.append(compute_study_groups(intervention_list[intervention_type]))
            print("study groups:", study_factor_combo)
            # set_study_arms()

        # for intervention in intervention_list:
        #         int_dict = dict
        #         set_factorvalues(intervention, int_dict)
        print compute_treatment_sequences(study_factor_combo, number_of_repeats)
        # treatment_arms = compute_treatment_sequences(intervention_list, number_of_repeats)
        set_study_arms(number_of_repeats)

        # for element in range(len(treatment_arms)):

