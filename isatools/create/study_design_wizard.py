from itertools import product
from itertools import permutations
from isatools.model import *
from isatools import isatab
from isatools.isatab import dump
from isatools.isatab import write_study_table_files
# from random import sample
import uuid
import datetime
import json
import random

__author__ = 'proccaserra@gmail.com'


# def save_study_profile():
    # TODO: code the method
    # save study parameters using YAML or JSON file
    # -study_type: intervention or observation
    # -number_of_intervention: integer
    #   -agent
    #   -intensity
    #   -duration
    # -study_regularity: balanced_or_imbalanced
    #    -study group size: integer
    # -study_variable_blocking:
    # -study_hard_to_change_variable: yes_no
    #


# def load_study_profile():
    # TODO: do it


def get_parameters( some_json_file ):
    source = json.loads( some_json_file )
    return dict(
        study_type = source.get('study_type',1),
        treatment_multiplicity= source['treatment_multiplicity'],
        hard_to_change_factor = source['hard_to_change_factor'],
        intervention_type_list = source['intervention_type_list'],
        sg_size = source["sg_size"]["size"],
        sg_size_toall = source["sg_size"]["applied_to_all_flag"],
        sample_list = source["sample_collection_list"]["sample_type"],
        assay_plan = source["assay_type"][""][""]
    )



def use_default_inv():
    try:
        investigation = Investigation()
        investigation.identifier = ""
        investigation.title = ""
        investigation.description = ""
        investigation.submission_date = ""
        investigation.public_release_date = ""
        study = Study(filename="s_study.txt", comments=[])
        study.identifier = str(uuid.uuid4())
        study.title = "boilerplate title"
        study.description = "boilerplate study description (testing purpose)"
        study.submission_date = str(datetime.date.today())
        study.public_release_date = str(datetime.date.today() + datetime.timedelta(days=30))

        sample_collection_protocol = Protocol(name="sample collection",
                                              protocol_type=OntologyAnnotation(term="sample collection"))

        study.protocols.append(sample_collection_protocol)
        investigation.studies.append(study)

        contact = Person(first_name="Boiler", last_name="Plate", affiliation="boiler plate affiliation")
        # roles=[OntologyAnnotation(term="submitter")]
        study.contacts.append(contact)
        publication = Publication(title="boiler plate publication", author_list="A. Robertson, B. Robertson")
        publication.pubmed_id = "12345678"
        publication.status = OntologyAnnotation(term="published")
        study.publications.append(publication)

        return investigation

    except IOError:
        print("error in get_number_of_factors() method")


def remove_duplicate_from_list(some_list):
    # and some_list.contains(',')
    try:
        if len(some_list) > 0:
            # removes trailing whitespace in a list such as a,b ,c ,c
            list_values = [x.strip() for x in some_list.split(',')]
            # removes any duplicate values in a list such as a,a,b,c
            list_values_nodup = list(set(list_values))
            # removes any empty string supplied as is a,,c,d
            # list_values_nodup = filter(bool, list_values_nodup)
        else:
            print("the list you have supplied is not valid, please enter a csv list")

        return list_values_nodup

    except ValueError:
        print("error in value in remove_duplicate_from_list() method")


def compute_study_groups(factor_and_levels):
    # TODO: rename compute_study_groups to compute_treatment
    try:
        study_groups = [dict(zip(factor_and_levels, x)) for x in product(*factor_and_levels.values())]
        # print study_groups
        return study_groups
    except IOError:
        print("error in compute_study_groups() method")


def get_number_of_factors():
    try:
        number = input("how many study non-interventional factors (i.e variable intrinsic to the model organism such as gender or strain or ethnicity) are there? (provide an integer): ")
        return number
    except IOError:
        print("error in get_number_of_factors() method")


def intervention_or_observation():
    try:
        is_intervention = True
        inter_or_obs = input("is the study an intervention or an observation (please select key)?"
                             " (intervention [1]/observation [2])")
        # intervention
        if inter_or_obs == "1":
            is_intervention = True

        # observation
        elif inter_or_obs == "2":
            is_intervention = False

        else:
            print("answer should be either 'intervention' or 'observation'")
            print("answer not recognized, choose between 'intervention' or 'observation'")

        return is_intervention
    except IOError:
        print("input error in intervention_or_observation() method")


def single_or_repeated_treatment():
    treatment_repeat = False
    try:
        treatment_repeat_input = input("are study subjects exposed to a single intervention or to multiple intervention"
                                       " (applied sequentially)? (choose either 'single [1]' or 'multiple [2]')")
        if treatment_repeat_input == '1':
            treatment_repeat = False
        elif treatment_repeat_input == '2':
            treatment_repeat = True
        else:
            print('invalid input, please try again')
            single_or_repeated_treatment()

        return treatment_repeat
    except IOError:
        print("input error in single_or_repeated_treatment() method")


def get_repeat_number():
    try:
        nbr_of_repeats_input = input("how many interventions each subject receives in total (enter an integer)? ")
        nbr_of_repeats = int(nbr_of_repeats_input)
        return nbr_of_repeats
    except IOError:
        print("get_repeat_number() method error")


def get_processrun_random_token(number_of_elements):
    try:
        # number_of_elements = input("what is the size of the plate/list? ")
        run_order = []
        my_list = list(range(int(number_of_elements)))
        new_list = [x + 1 for x in my_list]
        # print("my list: ",new_list)
        run_order = random.sample(new_list, len(new_list))
        # print("run order: ", run_order)
        return run_order

    except NotImplemented:
        print('something went wrong in get_processrun_random_token() method')


def create_control_element(some_inv, control_type, quantity, frequency):

    try:
        if control_type == "1":
            for entity in 1..quantity:
                control_source = Source(name='solvent blank', id_=entity)
                some_inv.sources.append(control_source)
        if control_type == "2":
            for entity in 1..quantity:
                control_source = Source(name='sample preparation blank', id_=entity)
                some_inv.sources.append(control_source)
        if control_type == "3":
            for entity in 1..quantity:
                control_source = Source(name='study reference material', id_=entity)
                some_inv.sources.append(control_source)
        else:
            print('choice not,recognised,please try again')
            # create_control_element()

    except NotImplemented:
        print("something went wrong in create_control_element() method")


def get_list_of_interventions(some_investigation):

    try:
        # IMPORTANT: we will first only support symmetric arms
        treatment_type_list = input("list the different intervention types (comma-separated-values from the following"
                                    " options {chemical intervention [1], behavioral intervention [2], "
                                    "surgical intervention [3], "
                                    "biological intervention [4], radiological intervention [5]}): ")
        treatment_type_list = remove_duplicate_from_list(treatment_type_list)

        treatment_types = {}
        for treatment_type in treatment_type_list:
            treatment_type.strip()
            if treatment_type == "1":
                treatment_types["chemical intervention"] = {"agent": [], "dose": [], "duration of exposure": []}
                f1 = StudyFactor(name="agent", factor_type=OntologyAnnotation(term="perturbation agent"))
                some_investigation.studies[0].factors.append(f1)
                f2 = StudyFactor(name="dose", factor_type=OntologyAnnotation(term="intensity"))
                some_investigation.studies[0].factors.append(f2)
                f3 = StudyFactor(name="duration of exposure", factor_type=OntologyAnnotation(term="time"))
                some_investigation.studies[0].factors.append(f3)

                # set_factor_as_key("chemical agent", factor_dict)

            if treatment_type == "2":
                # set_factor_as_key("behavioral agent", factor_dict)
                treatment_types["behavioral intervention"] = {"agent": [],
                                                              "dose": [],
                                                              "duration of exposure": []}

            if treatment_type == "3":
                # set_factor_as_key("surgery", factor_dict)
                treatment_types["surgical intervention"] = {"surgery procedure": [],
                                                            "dose": [],
                                                            "duration post surgery": []}

            if treatment_type == "4":
                # set_factor_as_key("biological agent", factor_dict)
                treatment_types["biological intervention"] = {"agent": [],
                                                              "dose": [],
                                                              "duration of exposure": []}

            if treatment_type == "5":
                # set_factor_as_key("radiological agent", factor_dict)
                treatment_types["radiological intervention"] = {"agent": [],
                                                                "dose": [],
                                                                "duration of exposure": []}

        return treatment_types, some_investigation

    except IOError:
        print("error in get_list_of_interventions() method")
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
    try:
        treatment_sequences = list(permutations(treatments, num_repeats))
        return treatment_sequences
    except IOError:
        print("error in compute_treatment_sequences() method")


def get_factor_name():
    try:
        factor_name = input("provide factor name: ")
        if factor_name != "" and factor_name.isalnum():
            return factor_name
        else:
            print("the factor supplied is not valid, please enter a string: ")
    except IOError:
        print("error in get_factor_name() method")


def set_factor_as_key(factor_name, factor_dict):
    try:
        this_factor_dict = factor_dict
        if factor_name not in factor_dict.keys():
            this_factor_dict[factor_name] = []
        else:
            print("factor already declared! define a new factor")
            get_factor_name()
        return this_factor_dict
    except IOError:
        print("error in set_factor_as_key() method")


def set_factor_values(factor_name, factor_dict):
    try:
        factor_values = input("provide the factor levels associated with '" + factor_name +
                              "' as a list of comma separated values: ")
        factor_values = remove_duplicate_from_list(factor_values)
        for element in factor_values:
            factor_dict[factor_name].append(element)
        return factor_dict
    except IOError:
        print("error in set_factor_values() method")


def balanced_design():
    try:
        balanced_design_var = input("Are all study groups of the same size, i.e have the same number of subjects? "
                                    "(in other words, are the groups balanced)? (balanced [1]/unbalanced [2])")
        if balanced_design_var == "1":
            is_balanced = True
            return is_balanced
        elif balanced_design_var == "2":
            is_balanced = False
            return is_balanced
        else:
            print("answer should be either 'balanced' or 'unbalanced'")
            print("answer not recognized, choose between 'balanced' or 'unbalanced'")
    except IOError:
        print("Error in balanced_design() method")


def full_or_fractional():
    try:
        full_or_fract = input("did you use a all possible groups or only a subset? (full [1]/fractional [2])")
        if full_or_fract == "1":
            full_or_fract = True
        elif full_or_fract == "2":
            full_or_fract = False
        else:
            print("answer not recognized, choose between 'full' or 'fractional'")
            full_or_fractional()

        return full_or_fract

    except IOError:
        print("error in full_or_fractional() method")


def free_or_restricted_randomization():
    try:
        design = ""
        hardtochange = input("Are there 'hard to change' factors,"
                             " which restrict randomization of experimental unit? (no [1]/yes [2])")
        if hardtochange == "1":
            # free_randomization = True
            design = "factorial design"
        elif hardtochange == "2":
            # free_randomization = False
            splitplot = input("how many 'hard to change factors'? (1/2")
            if splitplot == "1":
                design = "split plot design"
            elif splitplot == "2":
                design = "split split plot design"
        else:
            print("answer not recognized, choose between 'yes' or 'no'")
            free_or_restricted_randomization()

        return design

    except IOError:
        print("error in complete_or_restricted_randomization() method")


def choose_fluid_or_solid_or_both():

    this_sample_type = input("are the samples 'solid'[1] or 'fluid'[2] or 'both'[3]? ")
    if this_sample_type == "1":
        return this_sample_type
        # collected_samples(sample_type)
    elif this_sample_type == "2":
        return this_sample_type
        # collected_samples(sample_type)
    elif this_sample_type == "3":
        return this_sample_type
        # collected_samples(sample_type)
    else:
        print("input not recognised")
        choose_fluid_or_solid_or_both()

# def sample_collection_plan(sample_types):
#
#         samples_and_events = {}
#         for s_type in sample_types:
#             specific_sampling_events = input("for sample type " + "'" + str(s_type) + "'," +
#                                              " how many times each of the samples have been collected (integer): ")
#             # specific_sampling_events = remove_duplicate_from_list(specific_sampling_events)
#             samples_and_events[str(s_type)] = specific_sampling_events
#
#         return samples_and_events


def sample_collection_events(some_sample_type):

    try:
        sample_types = []
        samples_and_events_plan = {}

        if some_sample_type == "1":
            sample_types = input("select from the following list (liver,kidney,muscle,brain,lung,flower):  ")
            sample_types = remove_duplicate_from_list(sample_types)
            # return solid_samples

        elif some_sample_type == "2":
            sample_types = input("select from the following list (urine,blood,csf,sweat,lavage):  ")
            # for example: blood,urine,sweat,muscle
            sample_types = remove_duplicate_from_list(sample_types)
            # return fluid_samples

        elif some_sample_type == "3":
            sample_types = input("select from the following list (urine,blood,csf,sweat,lavage): ")
            sample_types = remove_duplicate_from_list(sample_types)
            # print(sample_types)
            s_sample_types = input("select from the following list (liver,kidney,muscle,brain,lung,2): ")
            s_sample_types = remove_duplicate_from_list(s_sample_types)
            sample_types.append(s_sample_types)

        else:
            print("input not recognised")
            # choose_fluid_or_solid_both()
        print(sample_types)
        for s_type in sample_types:
            specific_sampling_events = input("for sample type " + "'" + str(s_type) + "'," +
                                             " how many times each of the samples have been collected (integer): ")
            # specific_sampling_events = remove_duplicate_from_list(specific_sampling_events)
            samples_and_events_plan[str(s_type)] = specific_sampling_events
        print(samples_and_events_plan)

        return samples_and_events_plan
    except IOError:
        print("error in sample_collection_events() method")


# def define_sample_collection_plan():
# def define_assay_data_plan():

def create_study_subjects(group_size, this_study, group_uuid, group_factor_combo, some_sampling_event_plan):
    try:

        if group_size > 0:

            # sample_type = choose_fluid_or_solid_or_both()
            # collected_materials = collected_sample_types(sample_type)
            # sampling_plan = sample_collection_plan(collected_materials)

            for individual in range(group_size):
                source_name = "studygroup_" + str(group_uuid) + "_subject#" + str(individual)
                ncbitaxon = OntologySource(name="NCBITaxon", description="NCBI Taxonomy")
                characteristic_organism = Characteristic(category=OntologyAnnotation(term="organism"),
                                                         value=OntologyAnnotation(term="Homo sapiens",
                                                                                  term_source=ncbitaxon,
                                                                                  term_accession="http://purl.bioontology.org/ontology/NCBITAXON/9606"))
                # TODO: request taxonomic information from users
                source = Source(name=source_name)
                source.characteristics.append(characteristic_organism)
                # print("source: ", source.name, source.characteristics[0].category.term,
                #       source.characteristics[0].value.term)
                this_study.studies[0].sources.append(source)

                for tissue, number_of_collections in some_sampling_event_plan.items():

                    for specimen_number in range(int(number_of_collections)):

                        sample_name = source_name + "_" + "sample#" + str(specimen_number) + "_" + tissue
                        sample_template = Sample(name=sample_name, derives_from=[source])
                        characteristic_op = Characteristic(category=OntologyAnnotation(term="organism part"),
                                                           value=OntologyAnnotation(term=tissue))
                        sample_template.characteristics.append(characteristic_op)
                        characteristic_rk = Characteristic(category=OntologyAnnotation(term="collection event rank"),
                                                           value=OntologyAnnotation(term=str(specimen_number+1)))
                        sample_template.characteristics.append(characteristic_rk)
                        # print("sample type: " + key, ", number of collection events: " + value + " times.")

                        # this_study.studies[0].samples = batch_create_materials(prototype_sample, n=2)
                        # for sam in this_study.studies[0].samples:
                        # sample_name = source_name + "_" + "sample#" + str(i)
                        # sample = Sample(name=sample_name, derives_from=[source])

                        combo = group_factor_combo
                        # print("this study group from create_study_subject: ", combo)
                        for key, value in combo.items():
                            # print("this key:", key)
                            for item in range(0, len(this_study.studies[0].factors)):
                                if key == this_study.studies[0].factors[item].name:
                                    # print("factor name: ", this_study.studies[0].factors[item].name)
                                    fv = FactorValue(factor_name=this_study.studies[0].factors[item],
                                                     value=OntologyAnnotation(term=combo[key]))
                                    sample_template.factor_values.append(fv)

                        # print("sample: ", sample_template.name)
                        this_study.studies[0].samples.append(sample_template)
                        process_name = "protocol_" + str(group_uuid)
                        sample_collection_process = Process(name=process_name,
                                                            executes_protocol=this_study.studies[0].protocols[0],
                                                            date_=datetime.date.today() + datetime.timedelta(days=-30),
                                                            performer="bob")
                        sample_collection_process.outputs.append(sample_template)
                        sample_collection_process.inputs.append(source)

                        this_study.studies[0].process_sequence.append(sample_collection_process)
                        # print("p: ", sample_collection_process.name, sample_collection_process.executes_protocol.name,
                        #       sample_collection_process.inputs[0].name, sample_collection_process.outputs[0].name,
                        #       sample_collection_process.date, sample_collection_process.performer)

        return this_study

    except NotImplemented:
        print("error in create_study_subject() method")


def set_study_arms(list_of_study_group_dictionaries, this_investigation, this_repeats):
    try:
        # print(this_repeats)
        study_groups = {}
        # forf = full_or_fractional()
        bd = balanced_design()

        if bd is True and this_repeats is False:

            size = input("provide the number of subject per study group (must be an integer): ")
            if size.isdigit():
                size = int(size)
                if size > 0:

                    study_group_size = size
                    stato = OntologySource(name="STATO", description="Ontology for Statistical Methods")
                    this_investigation.ontology_source_references.append(stato)
                    design_term = OntologyAnnotation(term_source=stato)
                    design_term.term = "balanced design"
                    design_term.term_accession = "http://purl.obolibrary.org/obo/STATO_0000003"
                    this_investigation.studies[0].design_descriptors.append(design_term)

                    comment1 = Comment(name="number of study groups", value=len(list_of_study_group_dictionaries))
                    comment2 = Comment(name="study group size", value=int(study_group_size))

                    this_investigation.studies[0].comments.append(comment1)
                    this_investigation.studies[0].comments.append(comment2)

                    sample_type = choose_fluid_or_solid_or_both()
                    current_sampling_plan = sample_collection_events(sample_type)

                    sg_index = 0
                    for sg_index in range(len(list_of_study_group_dictionaries)):
                        study_groups["guid"] = uuid.uuid4()
                        study_groups["id"] = sg_index
                        study_groups["factor_level_combo"] = list_of_study_group_dictionaries[sg_index]
                        # print("this study group: ", study_groups["factor_level_combo"])
                        study_groups["size"] = study_group_size
                        this_investigation = create_study_subjects(study_group_size,
                                                                   this_investigation,
                                                                   study_groups["guid"],
                                                                   study_groups["factor_level_combo"],
                                                                   current_sampling_plan)
            else:
                print("invalid input, please try again")

        elif bd is False and this_repeats is False:
            for sg_index in range(len(list_of_study_group_dictionaries)):
                study_groups["guid"] = uuid.uuid4()
                study_groups["id"] = sg_index
                study_groups["factor_level_combo"] = list_of_study_group_dictionaries[sg_index]
                size = input("provide the number of subject per study group (must be an integer): ")
                size = int(size)
                if int(size) > 0:
                    study_group_size = size
                    stato = OntologySource(name="STATO", description="Ontology for Statistical Methods")
                    this_investigation.ontology_source_references.append(stato)
                    design_term = OntologyAnnotation(term_source=stato)
                    design_term.term = "unbalanced design"
                    design_term.term_accession = "http://purl.obolibrary.org/obo/STATO_000000X"
                    this_investigation.studies[0].design_descriptors.append(design_term)

                    study_groups["size"] = study_group_size
                    sample_type = choose_fluid_or_solid_or_both()
                    current_sampling_plan = sample_collection_events(sample_type)

                    this_investigation = create_study_subjects(study_group_size,
                                                               this_investigation,
                                                               study_groups["guid"],
                                                               study_groups["factor_level_combo"],
                                                               current_sampling_plan)
                else:
                    print("invalid input, please try again")

                print(study_groups)

        elif bd is False and this_repeats is True:

            nb_repeats = input("state the number of consecutive treatments (integer): ")
            # print study_factor_combo
            sequences = compute_treatment_sequences(list_of_study_group_dictionaries, int(nb_repeats))
            print("sequences")
            for sg_index in range(len(sequences)):
                study_groups["guid"] = uuid.uuid4()
                study_groups["id"] = sg_index
                study_groups["sequence"] = sequences[sg_index]
                size = input("provide the number of subject per study arm (must be an integer): ")
                size = int(size)
                if int(size) > 0:
                    study_group_size = size
                    study_groups["size"] = study_group_size
                    sample_type = choose_fluid_or_solid_or_both()
                    current_sampling_plan = sample_collection_events(sample_type)
                    this_investigation = create_study_subjects(study_group_size,
                                                               this_investigation,
                                                               study_groups["guid"],
                                                               study_groups["factor_level_combo"],
                                                               current_sampling_plan)

                else:
                    print("invalid input, please try again")

        else:
            nb_repeats = input("state the number of consecutive treatments (integer): ")
            # print study_factor_combo
            sequences = compute_treatment_sequences(list_of_study_group_dictionaries, int(nb_repeats))
            print(sequences)
            for sg_index in range(len(sequences)):
                study_groups["guid"] = uuid.uuid4()
                study_groups["id"] = sg_index
                study_groups["sequence"] = sequences[sg_index]
                size = input("provide the number of subject per study arm (must be an integer): ")
                size = int(size)
                if int(size) > 0:
                    study_group_size = size
                    study_groups["size"] = study_group_size
                    sample_type = choose_fluid_or_solid_or_both()
                    current_sampling_plan = sample_collection_events(sample_type)
                    this_investigation = create_study_subjects(study_group_size,
                                                               this_investigation,
                                                               study_groups["guid"],
                                                               study_groups["factor_level_combo"],
                                                               current_sampling_plan)
                else:
                    print("invalid input, please try again")

                # print(study_groups)

        return this_investigation, current_sampling_plan

    except IOError:
        print("error in set_study_arms() method")

# def sample_collection_plan(sample_types):
#
#         samples_and_events = {}
#         for s_type in sample_types:
#             specific_sampling_events = input("for sample type " + "'" + str(s_type) + "'," +
#                                              " how many times each of the samples have been collected (integer): ")
#             # specific_sampling_events = remove_duplicate_from_list(specific_sampling_events)
#             samples_and_events[str(s_type)] = specific_sampling_events
#
#         return samples_and_events

# def collection_sample_type():
#     try:
#         sample_types = input("list the type of sample collected from each study group member as csv list: ")
#         # for example: blood,urine,sweat,muscle
#         sample_types = remove_duplicate_from_list(sample_types)
#         return sample_types
#     except IOError:
#         print("error in collection_sample_type() method")

# def collected_sample_types(some_sample_type):
#     # TODO implement pulling the list of allowed values from ISA configuration or another configuration files
#
#     if some_sample_type == "1":
#         sample_types = input("select from the following list (liver,kidney,muscle,brain,lung,flower):  ")
#         sample_types = remove_duplicate_from_list(sample_types)
#         # return solid_samples
#
#     elif some_sample_type == "2":
#         sample_types = input("select from the following list (urine,blood,csf,sweat,lavage):  ")
#         # for example: blood,urine,sweat,muscle
#         sample_types = remove_duplicate_from_list(sample_types)
#         # return fluid_samples
#
#     elif some_sample_type == "3":
#         sample_types = input("select from the following list (urine,blood,csf,sweat,lavage): ")
#         sample_types = remove_duplicate_from_list(sample_types)
#         # print(sample_types)
#
#         s_sample_types = input("select from the following list (liver,kidney,muscle,brain,lung,2): ")
#         s_sample_types = remove_duplicate_from_list(s_sample_types)
#
#         sample_types.append(s_sample_types)
#
#     else:
#         print("input not recognised")
#         choose_fluid_or_solid_both()
#
#     return sample_types


def define_assay_plan(some_investigation, some_sample_collection_events):

    try:
        study_assay_plan = []

        applies_to_all = input("will all samples be tested with the same set of assays? yes[1]/no[2]")

        if applies_to_all == "1":
            initial_sample_assay_plan = input("provide  assay types being used as a comma separated list:"
                                              " [1]:transcription profiling using ngs, "
                                              " [2]:transcription profiling using DNA microarray,"
                                              " [3]:targeted metabolite profiling using mass spectrometry,"
                                              " [4]:metabolite profiling using NMR spectroscopy? ")

            initial_sample_assay_plan = remove_duplicate_from_list(initial_sample_assay_plan)
            print("initial sample assay plan:", initial_sample_assay_plan)

            for bio_material, nb_sampling_event in some_sample_collection_events.items():
                # print("biomat:", bio_material, "how many? ", nb_sampling_event)
                for element in range(int(nb_sampling_event)):
                    for this_item in range(len(initial_sample_assay_plan)):
                        sample_assay_plan = {"sample_type": bio_material,
                                             "sample_number": element+1,
                                             "assay_type": initial_sample_assay_plan[this_item]}
                        study_assay_plan.append(sample_assay_plan)
            print("final number of assay plans:", len(study_assay_plan))

        elif applies_to_all == "2":

            # we need to iterate through each sample type and record the relevant assays for that sample type

            for bio_material, nb_sampling_event in some_sample_collection_events.items():
                # sample_assay_plan = {"sample_type": "", "sample_number": "", "assay_type": []}
                print("biomat:", bio_material, "how many? ", nb_sampling_event)
                initial_sample_assay_plan = input("select assay types being used for that sample type '" + bio_material
                                                  + "' as a comma separated list:"
                                                  " [1]:transcription profiling using ngs, "
                                                  " [2]:transcription profiling using DNA microarray,"
                                                  " [3]:targeted metabolite profiling using mass spectrometry,"
                                                  " [4]:metabolite profiling using NMR spectroscopy? ")

                initial_sample_assay_plan = remove_duplicate_from_list(initial_sample_assay_plan)

                to_all_of_these = input("will these assays be performed on all specimens"
                                        " of this sample type? yes[1]/no[2]")

                if to_all_of_these == "2":
                    for element in range(int(nb_sampling_event)):
                            this_sample_assay_plan = input("select assay types being used for that sample type"
                                                           " as a comma separated list:"
                                                           " [1]:transcription profiling using ngs, "
                                                           " [2]:transcription profiling using DNA microarray,"
                                                           " [3]:targeted metabolite profiling using mass spectrometry,"
                                                           " [4]:metabolite profiling using NMR spectroscopy? ")

                            study_assay_plan = remove_duplicate_from_list(this_sample_assay_plan)

                            for this_item in range(len(initial_sample_assay_plan)):
                                sample_assay_plan = {"sample_type": bio_material,
                                                     "sample_number": element+1,
                                                     "assay_type": initial_sample_assay_plan[this_item]}
                            study_assay_plan.append(sample_assay_plan)
                            # [{"sample_type":"liver", "sample_number":"1", "assay_types": ["1","2","3"]}]

                    print(this_sample_assay_plan[0]["sample_type"])

                elif to_all_of_these == "1":
                    for element in range(int(nb_sampling_event)):
                        for this_item in range(len(initial_sample_assay_plan)):
                            sample_assay_plan = {"sample_type": bio_material,
                                                 "sample_number": element+1,
                                                 "assay_type": initial_sample_assay_plan[this_item]}
                        study_assay_plan.append(sample_assay_plan)

                else:
                    print("input not recognized, please reiterate your selection.")

        else:
            print("input not recognized, please reiterate your selection.")
            define_assay_plan(some_investigation, some_sample_collection_events)
        print("number of assay plans from define_assay_plan(): ", len(study_assay_plan))

        return some_investigation, study_assay_plan

    except IOError:
        print("error in define_assay_plan() method")


def set_assay_type_topology_modifiers(this_sample_type, this_sampling_event, this_assay_type):
    # TODO: refactor in order to implement modular assay specific topologies, switching between cases depending on assay
    # TODO: types supplied by users with the define_assay_plan() method
    try:
        # this_assay_type = input(
        #                         "which assay types are being used: [1]:transcription profiling using ngs, "
        #                         " [2]:transcription profiling using DNA microarray,"
        #                         " [3]:targeted metabolite profiling using mass spectrometry,"
        #                         " [4]:metabolite profiling using NMR spectroscopy? ")
        sample_assay_plans = []

        # for this_assay_type in range(len(this_assay_type_array)):
        with_topology_params = {"sample type": "",
                           "collection event": "",
                           "assay type": 0,
                           "params": {
                               "distinct libraries": 0,
                               "distinct array designs": 0,
                               "number of injection modes": 0,
                               "number of acquisition modes": 0,
                               "number of channels": 0,
                               "pulse sequences": 0,
                               "number of technical replicates": 0}
                           }
        # print("this assay type:", this_assay_type_array[this_assay_type], "counter:", this_assay_type)
        if int(this_assay_type) == 1:

            nb_library = input(
                "how many distinct libraries per sample (provide an positive integer, default is 1)?")
            nb_multiplexing_channels = input("how many labels were used (provide an positive integer, default is 1)?")
            nb_technical_rep = input("how many technical replicate for each sample, default is 1?")
            with_topology_params["sample type"] = this_sample_type
            with_topology_params["collection event"] = this_sampling_event
            with_topology_params["assay type"] = 1
            with_topology_params["params"]["distinct libraries"] = nb_library
            with_topology_params["params"]["number of channels"] = nb_multiplexing_channels
            with_topology_params["params"]["number of technical replicates"] = nb_technical_rep

        elif int(this_assay_type) == 2:

            nb_chip_design = input(
                "how many distinct microarray designs (provide an positive integer, default is 1)?")
            nb_multiplexing_channels = input("how many labels were used (provide an positive integer, default is 1)?")
            nb_technical_rep = input("how many technical replicate for each sample, default is 1?")

            with_topology_params["sample type"] = this_sample_type
            with_topology_params["collection event"] = this_sampling_event
            with_topology_params["assay type"] = 2
            with_topology_params["params"]["distinct array designs"] = nb_chip_design
            print("typology:", with_topology_params["params"]["distinct array designs"])
            with_topology_params["params"]["number of channels"] = nb_multiplexing_channels
            with_topology_params["params"]["number of technical replicates"] = nb_technical_rep

        elif this_assay_type == "3":

            injection_modes = input(
                "how many distinct sample introduction modes (1:FIA,2:LC,3:GC)?")
            injection_modes = remove_duplicate_from_list(injection_modes)
            acquisition_modes = input(
                "how many distinct acquisition modes (1:negative mode, 2:positive mode) ?")
            acquisition_modes = remove_duplicate_from_list(acquisition_modes)
            # nb_channels = input("how many labels were used (provide an positive integer, default is 1)?")
            nb_technical_rep = input("how many technical replicate for each sample, default is 1?")

            with_topology_params["sample type"] = this_sample_type
            with_topology_params["collection event"] = this_sampling_event
            with_topology_params["assay type"] = 3
            with_topology_params["params"]["injection modes"] = injection_modes
            with_topology_params["params"]["number of channels"] = acquisition_modes
            with_topology_params["params"]["number of technical replicates"] = nb_technical_rep

        elif this_assay_type == "4":

            injection_modes = input(
                "how many distinct sample introduction modes (1:autoloader,2:LC,3:GC)?")
            injection_modes = remove_duplicate_from_list(injection_modes)
            acquisition_modes = input(
                "how many distinct acquisition modes (1:COSY, 2:NOESY, 3:TOSCY, 4:CPMG ,5: INEPT, 6:HMQC, 7:WATERGATE) ?")
            acquisition_modes = remove_duplicate_from_list(acquisition_modes)
            # nb_multiplexing_channels = input("how many labels were used (provide an positive integer, default is 1)?")
            nb_technical_rep = input("how many technical replicate for each sample, default is 1?")

            with_topology_params["sample type"] = this_sample_type
            with_topology_params["collection event"] = this_sampling_event
            with_topology_params["assay type"] = 4
            with_topology_params["params"]["injection modes"] = injection_modes
            with_topology_params["params"]["pulse sequences"] = acquisition_modes
            # typology_params["params"]["number of channels"] = acquisition_modes
            with_topology_params["params"]["number of technical replicates"] = nb_technical_rep

        # else:
        #     print("input not recognised in set_assay_type_topology_modifiers() method")
            # set_assay_type_topology_modifiers( this_sample_type, this_assay_type)

        # sample_assay_plans.append(typology_params)

        return with_topology_params
        # nb_chip_design, nb_multiplexing_channels, nb_technical_rep

    except IOError:
        print("error in set_assay_type_topology_modifiers() method")


# def create_assays(some_assay_plan,some_assay_object):
# #
#     for item in range(len(assay_plan)):
#         # print("assay definitions are: ", assay_definitions[item])
#         print("dealing with the first assay plan, for the specimen of sample type :", assay_plan[item]["sample type"],
#               "for collection event:", assay_plan[item]["collection event"])
#         # print("sample type:", assay_definitions[item]["sample type"],
#         #       "| assay type: ", assay_definitions[item]["assay type"],
#         #       "| assay params: ", assay_definitions[item]["params"])
#         # dealing with Mass Spectrometry Applications
#         if assay_plan[item]["assay type"] == 3:
#             # TODO: implement get_or_create method and refactor
#             ms = [a for a in new_inv.studies[0].assays if
#                    a.measurement_type.term == "metabolite profiling" and a.technology_type.term == "liquid chromatography mass spectrometry" and a.filename == "a_mp_lcms.txt"]
#             if len(ngs) > 0:
#                 print("yes, exists in 1", ms)
#                 # if such an assay table already exists, we retrieve it
#                 this_assay = ms[0]
#             else:
#                 # or print('nothing found, creating a new object)...')
#                 this_assay = Assay(measurement_type=OntologyAnnotation(term="metabolite profiling"),
#                                    technology_type=OntologyAnnotation(term="liquid chromatography mass spectrometry"),
#                                    filename="a_mp_lcms.txt")
#                 # the object is attached to the relevant study
#                 new_inv.studies[0].assays.append(this_assay)
#
#                 extraction_protocol = Protocol(name='metabolite extraction',
#                                                protocol_type=OntologyAnnotation(term="material separation"))
#                 new_inv.studies[0].protocols.append(extraction_protocol)
#
#                 # lc_protocol = Protocol(name="liquid chromatography",
#                 #                              protocol_type=OntologyAnnotation(term="material separation"))
#                 # new_inv.studies[0].protocols.append(labeling_protocol)
#
#                 ms_protocol = Protocol(name='liquid chromatography mass spectrometry',
#                                                protocol_type=OntologyAnnotation(term="data collection"))
#                 new_inv.studies[0].protocols.append(sequencing_protocol)
#
#             index_i = 0
#             index_j = 0
#             index_k = 0
#             # for index_i, sample in enumerate(new_inv.studies[0].samples):
#             some_sample_list = [sample for sample in new_inv.studies[0].samples if
#                           sample.characteristics[0].value.term == assay_plan[item]["sample type"] and
#                           sample.characteristics[1].value.term == assay_plan[item]["collection event"]]
#             print("number of samples: ", len(some_sample_list))
#             extractlist_before = [ext for ext in new_inv.studies[0].assays[0].other_material if
#                                   ext.type == "Extract Name"]
#             # print("number of extracts", len(extractlist_before))
#
#             for index_i, sample in enumerate([sample for sample in new_inv.studies[0].samples if
#                                         sample.characteristics[0].value.term == assay_plan[item][
#                                             "sample type"]]):
#                 # print("i: ", index_i, "sample: ", sample.characteristics[1].value.term)
#                 # print("current collection event", assay_plan[item]["collection event"])
#                 if str(sample.characteristics[1].value.term) == str(assay_plan[item]["collection event"]):
#                     # create an extraction process that executes the extraction protocol
#                     extraction_process = Process(executes_protocol=[prtcl for prtcl in new_inv.studies[0].protocols
#                                                                     if prtcl.name == "metabolite extraction"][0],
#                                                  performer="rick",
#                                                  date_=datetime.datetime.now())
#
#                     # extraction process takes as input a sample, and produces an extract material as output
#                     # we make sure only the right kind of samples get assayed so we check against the sample type
#                     # if sample.characteristics[0].value.term == assay_plan[item]["sample type"]:
#                     # print("sample characteristics: ", sample.characteristics[0].value.term)
#
#                     extraction_process.inputs.append(sample)
#                     extract = Material(name=sample.name + "extract-{}".format(index_i))
#                     extract.type = "Extract Name"
#                     extraction_process.outputs.append(extract)
#
#                     # this loop is meant to handle the case where several acquisition modes (e.g. Neg or positive) are used from a sample
#                     # TODO: include a function to obtain the relevant parameters used for data acquisition
#                     for index_j in range(int(assay_plan[item]["params"]["platforms"])):
#                         # this inner is for handling multiple runs of the same platform, i.e. tech replicates
#                         for index_k in range(
#                                 int(assay_plan[item]["params"]["number of technical replicates"])):
#                             prtcl_name = [prtcl for prtcl in new_inv.studie   s[0].protocols
#                                           if prtcl.name == "data collection"][0]
#
#                             data_acq_process = Process(executes_protocol=prtcl_name,
#                                                        performer="louis",
#                                                        date_=datetime.datetime.now())
#
#                             platform_name = "platform-{}".format(index_j)
#                             data_acq_process.name = "assay-name-{}".format(index_i) + "_" + platform_name + \
#                                                     "_run-{}".format(index_k)
#                             data_acq_process.inputs.append(labeling_process.outputs[0])
#
#                             # data acquisition process usually has an output data file
#                             datafile = DataFile(
#                                 filename="acquired-data-{}".format(index_i) + "_" + platform_name +
#                                          "_run-{}".format(index_k) + ".mzml.gz",
#                                 label="MS Raw Data File")
#                             data_acq_process.outputs.append(datafile)
#
#                             # ensure Processes are linked forward and backward
#                             extraction_process.next_process = data_acq_process
#                             # labeling_process.prev_process = extraction_process
#                             extraction_process.next_process = data_acq_process
#                             # data_acq_process.prev_process = labeling_process
#                             data_acq_process.prev_process = extraction_process
#
#                             # make sure extract(library), data file, and the processes are attached to the assay
#                             this_assay.data_files.append(datafile)
#                             this_assay.other_material.append(extract)
#                             # this_assay.other_material.append(le)
#                             this_assay.process_sequence.append(extraction_process)
#                             # this_assay.process_sequence.append(labeling_process)
#                             this_assay.process_sequence.append(data_acq_process)
#
#             # extractlist_after = [ext for ext in new_inv.studies[0].assays[0].other_material if
#             #                      ext.type == "Extract Name"]
#             # print("number of extracts", len(extractlist_after))


# MAIN METHOD:

def main():

    intervention_list = []

    intervention_check = intervention_or_observation()

    if intervention_check is True:

        try:
            new_inv = use_default_inv()
            repeats = single_or_repeated_treatment()
            free_or_restricted_design = free_or_restricted_randomization()
            assay_plan = []

            if repeats is False and "factorial" in free_or_restricted_design:

                obi = OntologySource(name="OBI", description="Ontology for Biomedical Investigations")
                new_inv.ontology_source_references.append(obi)
                stato = OntologySource(name="STATO", description="Ontology for Statistical Methods")
                new_inv.ontology_source_references.append(stato)
                design1 = OntologyAnnotation(term_source=obi)
                design1.term = "intervention design"
                design1.term_accession = "http://purl.obolibrary.org/obo/OBI_0000115"
                new_inv.studies[0].design_descriptors.append(design1)
                design2 = OntologyAnnotation(term_source=stato)
                design2.term = "full factorial design"
                design2.term_accession = "http://purl.obolibrary.org/obo/STATO_0000270"
                new_inv.studies[0].design_descriptors.append(design2)

                intervention_list, new_inv = get_list_of_interventions(new_inv)

                assay_plan = []
                for intervention_type in intervention_list.keys():
                    # print("type of intervention: ", intervention_type)
                    for factor in intervention_list[intervention_type].keys():
                        # print("factor :", factor)
                        set_factor_values(factor, intervention_list[intervention_type])
                        # print("associated factor values:", intervention_list[intervention_type][factor])

                # study_factor_combo = compute_study_groups(my_factors)
                study_group_dictionaries = compute_study_groups(intervention_list[intervention_type])
                # print("study groups:", study_group_dictionaries)
                new_inv, sampling_plan = set_study_arms(study_group_dictionaries, new_inv, repeats)
                # print("is this correct?" , new_inv.studies[0].sources[0].name)

                new_inv, assay_plan = define_assay_plan(new_inv, sampling_plan)

                print("number of assay plans in Main: ", len(assay_plan))

                for l in range(len(assay_plan)):
                    assay_plan[l] = set_assay_type_topology_modifiers(assay_plan[l]["sample_type"],
                                                                      assay_plan[l]["sample_number"],
                                                                      assay_plan[l]["assay_type"])

                    # applies_to_all_plan_of_that_assay_type = input("Apply this parameter selection to all plans using this assay type? [1]Yes/2[No]")

                    # if applies_to_all_plan_of_that_assay_type == 1:


                    print(assay_plan[l])

                    # assay_definitions.append(set_assay_type_topology_modifiers(assay_plan[l]["sample_type"],
                    #                                                             assay_plan[l]["assay_type"]))
                    # print("assay plan: ", assay_plan[l]["sample_type"], "|", assay_plan[l]["assay_type"])

                # for m in range(len(assay_plan[l]["assay_types"])):

                print("number of assay full definitions", len(assay_plan))
                # print(assay_definitions[0]["sample type"])

                for item in range(len(assay_plan)):
                    # print("assay definitions are: ", assay_definitions[item])
                    print("dealing with the first assay plan, for the specimen of sample type :", assay_plan[item]["sample type"], "for collection event:", assay_plan[item]["collection event"])
                    # print("sample type:", assay_definitions[item]["sample type"],
                    #       "| assay type: ", assay_definitions[item]["assay type"],
                    #       "| assay params: ", assay_definitions[item]["params"])

                    if assay_plan[item]["assay type"] == 1:
                        # TODO: implement get_or_create method and refactor
                        ngs = [a for a in new_inv.studies[0].assays if a.measurement_type.term == "transcription profiling" and a.technology_type.term == "nucleic acid sequencing" and a.filename == "a_tp_ngs.txt"]
                        if len(ngs) > 0:
                            print("yes, exists in 1", ngs)
                            # if such an assay table already exists, we retrieve it
                            this_assay = ngs[0]
                        else:
                            # or print('nothing found, creating a new object)...')
                            this_assay = Assay(measurement_type=OntologyAnnotation(term="transcription profiling"),
                                               technology_type=OntologyAnnotation(term="nucleic acid sequencing"),
                                               filename="a_tp_ngs.txt")
                            # the object is attached to the relevant study
                            new_inv.studies[0].assays.append(this_assay)

                            extraction_protocol = Protocol(name='RNA extraction',
                                                           protocol_type=OntologyAnnotation(term="material separation"))
                            new_inv.studies[0].protocols.append(extraction_protocol)

                            labeling_protocol = Protocol(name="nucleic acid library preparation",
                                                         protocol_type=OntologyAnnotation(term="material labeling"))
                            new_inv.studies[0].protocols.append(labeling_protocol)

                            sequencing_protocol = Protocol(name='nucleic acid sequencing',
                                                           protocol_type=OntologyAnnotation(term="data collection"))
                            new_inv.studies[0].protocols.append(sequencing_protocol)

                        i = 0
                        j = 0
                        k = 0
                        # for i, sample in enumerate(new_inv.studies[0].samples):
                        samplelist=[sample for sample in new_inv.studies[0].samples if
                         sample.characteristics[0].value.term == assay_plan[item]["sample type"] and sample.characteristics[1].value.term == assay_plan[item]["collection event"]]
                        # print("number of samples: ", len(samplelist))
                        extractlist_before = [ext for ext in new_inv.studies[0].assays[0].other_material if ext.type == "Extract Name"]
                        # print("number of extracts", len(extractlist_before))

                        for i, sample in enumerate([sample for sample in new_inv.studies[0].samples if
                                                    sample.characteristics[0].value.term == assay_plan[item][
                                                            "sample type"]]):
                            # print("i: ", i, "sample: ", sample.characteristics[1].value.term)
                            # print("current collection event", assay_plan[item]["collection event"])
                            if str(sample.characteristics[1].value.term) == str(assay_plan[item]["collection event"]):
                                # create an extraction process that executes the extraction protocol
                                extraction_process = Process(executes_protocol=[prtcl for prtcl in new_inv.studies[0].protocols
                                                                                if prtcl.name == "RNA extraction"][0],
                                                             performer="amy",
                                                             date_=datetime.datetime.now())

                                # extraction process takes as input a sample, and produces an extract material as output
                                # we make sure only the right kind of samples get assayed so we check against the sample type
                                # if sample.characteristics[0].value.term == assay_plan[item]["sample type"]:
                                # print("sample characteristics: ", sample.characteristics[0].value.term)

                                extraction_process.inputs.append(sample)
                                extract = Material(name=sample.name+"extract-{}".format(i))
                                extract.type = "Extract Name"
                                extraction_process.outputs.append(extract)

                                # TODO: support multiplex identifiers in a future release
                                labeling_process = Process(
                                    executes_protocol=[prtcl for prtcl in new_inv.studies[0].protocols
                                                       if prtcl.name == "nucleic acid library preparation"][0],
                                    performer="xua",
                                    date_=datetime.datetime.now()
                                    )
                                # extraction process takes as input a sample, and produces an extract material as output
                                labeling_process.inputs.append(extract)
                                le = Material(name= extract.name +"labeled-extract-{}".format(i))
                                le.type = "Labeled Extract Name"
                                dye = Characteristic(category=OntologyAnnotation(term="label"),
                                                     value=OntologyAnnotation(term="none"))
                                le.characteristics.append(dye)
                                labeling_process.outputs.append(le)

                                # this loop is meant to handle the case where several libraries are produced from a sample
                                # TODO: include a function to obtain the relevant parameters used for library creation
                                for j in range(int(assay_plan[item]["params"]["distinct libraries"])):
                                    # this inner is for handling multiple runs of the same library, ie tech replicates
                                    for k in range(
                                            int(assay_plan[item]["params"]["number of technical replicates"])):
                                        prtcl_name = [prtcl for prtcl in new_inv.studies[0].protocols
                                                      if prtcl.name == "nucleic acid sequencing"][0]

                                        data_acq_process = Process(executes_protocol=prtcl_name,
                                                                   performer="louis",
                                                                   date_=datetime.datetime.now())

                                        library_name = "library-{}".format(j)
                                        data_acq_process.name = "assay-name-{}".format(i) + "_" + library_name + \
                                                                "_run-{}".format(k)
                                        data_acq_process.inputs.append(labeling_process.outputs[0])

                                        # data acquisition process usually has an output data file
                                        datafile = DataFile(
                                            filename="sequence-data-{}".format(i) + "_" + library_name +
                                                     "_run-{}".format(k) + ".fastq.gz",
                                            label="Raw Data File")
                                        data_acq_process.outputs.append(datafile)

                                        # ensure Processes are linked forward and backward
                                        extraction_process.next_process = labeling_process
                                        labeling_process.prev_process = extraction_process
                                        labeling_process.next_process = data_acq_process
                                        data_acq_process.prev_process = labeling_process

                                        # make sure extract(library), data file, and the processes are attached to the assay
                                        this_assay.data_files.append(datafile)
                                        this_assay.other_material.append(extract)
                                        this_assay.other_material.append(le)
                                        this_assay.process_sequence.append(extraction_process)
                                        this_assay.process_sequence.append(labeling_process)
                                        this_assay.process_sequence.append(data_acq_process)

                        extractlist_after = [ext for ext in new_inv.studies[0].assays[0].other_material if
                                              ext.type == "Extract Name"]
                        print("number of extracts", len(extractlist_after))

                    elif assay_plan[item]["assay type"] == 2:
                        # TODO: refactor to rely on a specific function handling assay create (create_assays() method)
                        tx = [a for a in new_inv.studies[0].assays if a.measurement_type.term == "transcription profiling" and a.technology_type.term == "DNA microarray"]
                        if len(tx) > 0:
                            print("yes, exists in 2", tx)
                            this_assay = tx[0]
                        else:
                            this_assay = Assay(measurement_type=OntologyAnnotation(term="transcription profiling"),
                                               technology_type=OntologyAnnotation(term="DNA microarray"),
                                               filename="a_tp_microarray.txt")
                            # attach the assay to the study
                            new_inv.studies[0].assays.append(this_assay)

                            extraction_protocol = Protocol(name='RNA extraction',
                                                           protocol_type=OntologyAnnotation(term="material separation"))
                            new_inv.studies[0].protocols.append(extraction_protocol)

                            labeling_protocol = Protocol(name="nucleic acid labeling",
                                                         protocol_type=OntologyAnnotation(term="material labeling"))
                            new_inv.studies[0].protocols.append(labeling_protocol)

                            hyb_protocol = Protocol(name='nucleic acid hybridization',
                                                    protocol_type=OntologyAnnotation(term="nucleic acid hybridization"))

                            new_inv.studies[0].protocols.append(hyb_protocol)

                        i = 0
                        j = 0
                        k = 0
                        # for i, sample in enumerate(new_inv.studies[0].samples):
                        for i, sample in enumerate([sample for sample in new_inv.studies[0].samples if
                                                   sample.characteristics[0].value.term == assay_plan[item]["sample type"]]):

                            if str(sample.characteristics[1].value.term) == str(assay_plan[item]["collection event"]):
                                # print("i: ", i, "sample: ", sample.characteristics[0].value.term)

                                # create an extraction process that executes the extraction protocol
                                # [prtcl for prtcl in inv.studies[0].protocols if prtcl.name == "RNA extraction"][0]

                                extraction_process = Process(executes_protocol=[prtcl for prtcl in new_inv.studies[0].protocols
                                                                                if prtcl.name == "RNA extraction"][0],
                                                             performer="amy",
                                                             date_=datetime.datetime.now())

                                # extraction process takes as input a sample, and produces an extract material as output
                                # if sample.characteristics[0].value.term == assay_plan[item]["sample type"]:

                                extraction_process.inputs.append(sample)
                                extract = Material(name="extract-{}".format(i))
                                extract.type = "Extract Name"
                                extraction_process.outputs.append(extract)

                                labeling_process = Process(executes_protocol=[prtcl for prtcl in new_inv.studies[0].protocols
                                                                              if prtcl.name == "nucleic acid labeling"][0],
                                                           performer="xua",
                                                           date_=datetime.datetime.now()
                                                           )

                                # extraction process takes as input a sample, and produces an extract material as output
                                labeling_process.inputs.append(extract)
                                le = Material(name="labeled-extract-{}".format(i))
                                le.type = "Labeled Extract Name"
                                dye = Characteristic(category=OntologyAnnotation(term="label"),
                                                     value=OntologyAnnotation(term="biotin"))
                                le.characteristics.append(dye)
                                labeling_process.outputs.append(le)

                                # create a data acquisition process that executes a data acquisition protocol
                                # print('number of array-design: ',
                                #       assay_definitions[item][0]["params"]["distinct array designs"])
                                        #assay_modifier1)
                                # print('number of technical replicates:',
                                #       assay_definitions[item][0]["params"]["number of technical replicates"])
                                      # assay_modifier3)

                                for j in range(int(assay_plan[item]["params"]["distinct array designs"])):

                                    for k in range(int(assay_plan[item]["params"]["number of technical replicates"])):

                                        prtcl_name = [prtcl for prtcl in new_inv.studies[0].protocols
                                                      if prtcl.name == "nucleic acid hybridization"][0]

                                        data_acq_process = Process(executes_protocol=prtcl_name,
                                                                   performer="louis",
                                                                   date_=datetime.datetime.now())

                                        array_design_name = "arraydesign-{}".format(j)
                                        data_acq_process.array_design_ref = OntologyAnnotation(term=array_design_name)
                                        # print("with array_design: ", array_design_name)
                                        array_design_as_pv = ParameterValue(
                                                                       category=ProtocolParameter(parameter_name=OntologyAnnotation(term="array_design_ref")),
                                                                       value=OntologyAnnotation(term=array_design_name))
                                        data_acq_process.parameter_values.append(array_design_as_pv)

                                        # print("data acquisition protocol name:", prtcl_name.name)
                                        # print("replicate: ", k)
                                        data_acq_process.name = "assay-name-{}".format(i) + "_" + array_design_name +\
                                                                "_run-{}".format(k)
                                        data_acq_process.array_design_ref = array_design_name
                                        # print(data_acq_process.name)
                                        data_acq_process.inputs.append(labeling_process.outputs[0])

                                        # process usually has an output data file
                                        datafile = DataFile(filename="microarray-data-{}".format(i) + "_" + array_design_name +
                                                                     "_run-{}".format(k),
                                                            label="Array Data File")
                                        data_acq_process.outputs.append(datafile)

                                        # ensure Processes are linked forward and backward
                                        extraction_process.next_process = labeling_process
                                        labeling_process.prev_process = extraction_process
                                        labeling_process.next_process = data_acq_process
                                        data_acq_process.prev_process = labeling_process

                                        # make sure the extract, data file, and the processes are attached to the assay
                                        this_assay.data_files.append(datafile)
                                        this_assay.other_material.append(extract)
                                        this_assay.other_material.append(le)
                                        this_assay.process_sequence.append(extraction_process)
                                        this_assay.process_sequence.append(labeling_process)
                                        this_assay.process_sequence.append(data_acq_process)

                    elif assay_plan[item]["assay type"] == 3:
                        # TODO: implement get_or_create method and refactor

                        if len(assay_plan[item]["params"]["injection modes"]) > 0:
                            inj_mode = ""
                            acq_mode = ""
                            for inj_mode_code in range(len(assay_plan[item]["params"]["injection modes"])):
                                if inj_mode_code == 0:
                                    print("YAY, this is FIA")
                                    inj_mode = "FIA"
                                elif inj_mode_code == 1:
                                    inj_mode = "LC"
                                elif inj_mode_code == 2:
                                    inj_mode = "GC"
                                else:
                                    print("error, injection method not recognized)")

                                for acq_mode_code in range(len(assay_plan[item]["params"]["number of channels"])):
                                  if acq_mode_code == 0:
                                    acq_mode = "positive"
                                  elif acq_mode_code == 1:
                                    acq_mode = "negative"
                                  else:
                                        print("error, injection method not recognized)")

                                  techname = inj_mode + "-" + acq_mode + " mass spectrometry"

                                  ms_filename = "a_mp_" + inj_mode + "_" + acq_mode + "_ms.txt"

                                  ms = [a for a in new_inv.studies[0].assays if
                                        a.measurement_type.term == "metabolite profiling"
                                        and a.technology_type.term == techname and a.filename == ms_filename]
                                  if len(ms) > 0:
                                      print("yes, exists in :", ms)
                                      # if such an assay table already exists, we retrieve it
                                      this_assay = ms[0]
                                  else:
                                      # or print('nothing found, creating a new object)...')
                                      this_assay = Assay(measurement_type=OntologyAnnotation(term="metabolite profiling"),
                                                       technology_type=OntologyAnnotation(term=techname),
                                                       filename=ms_filename)

                                      new_inv.studies[0].assays.append(this_assay)

                                      extraction_protocol = Protocol(name='metabolite extraction',
                                                                   protocol_type=OntologyAnnotation(term="material separation"))
                                      new_inv.studies[0].protocols.append(extraction_protocol)

                                    # lc_protocol = Protocol(name="liquid chromatography",
                                    #                              protocol_type=OntologyAnnotation(term="material separation"))
                                    # new_inv.studies[0].protocols.append(labeling_protocol)

                                      ms_protocol = Protocol(name=inj_mode + "-" + acq_mode +' mass spectrometry',
                                                                   protocol_type=OntologyAnnotation(term="mass spectrometry"))

                                      randomized_run_order = ProtocolParameter(parameter_name=OntologyAnnotation(term="randomized run order"))
                                      inj_param = ProtocolParameter(parameter_name=OntologyAnnotation(term="injection mode"))

                                      if inj_mode == 1 or inj_mode == 2:
                                        ch_instr = ProtocolParameter(parameter_name=OntologyAnnotation(term="chromatography instrument"))
                                        ch_column = ProtocolParameter(parameter_name=OntologyAnnotation(term="chromatography column"))
                                        ch_elu_p = ProtocolParameter(parameter_name=OntologyAnnotation(term="elution program"))
                                        ms_protocol.parameters.append(ch_instr)
                                        ms_protocol.parameters.append(ch_column)
                                        ms_protocol.parameters.append(ch_elu_p)
                                      ms_instr = ProtocolParameter(parameter_name=OntologyAnnotation(term="mass spectrometry instrument"))
                                      acq_param = ProtocolParameter(parameter_name=OntologyAnnotation(term="scan polarity"))

                                      ms_protocol.parameters.append(randomized_run_order)
                                      ms_protocol.parameters.append(inj_param)
                                      ms_protocol.parameters.append(ms_instr)
                                      ms_protocol.parameters.append(acq_param)

                                      new_inv.studies[0].protocols.append(ms_protocol)

                                  index_i = 0
                                  index_j = 0
                                  index_k = 0
                                  randomized_order = []
                                  # for index_i, sample in enumerate(new_inv.studies[0].samples):
                                  #some_sample_list = [sample for sample in new_inv.studies[0].samples if
                                  #                sample.characteristics[0].value.term == assay_plan[item]["sample type"] and
                                  #                sample.characteristics[1].value.term == assay_plan[item]["collection event"]]
                                  #print("number of samples: ", len(some_sample_list))
                                  #extractlist_before = [ext for ext in new_inv.studies[0].assays[0].other_material if
                                  #                        ext.type == "Extract Name"]
                                  # print("number of extracts", len(extractlist_before))
                                  expected_total_number_run = len([sample for sample in new_inv.studies[0].samples if
                                                                sample.characteristics[0].value.term == assay_plan[item][
                                                                    "sample type"]]) \
                                                              * int(
                                      assay_plan[item]["params"]["number of technical replicates"])
                                                     # * len(assay_plan[item]["params"]["number of channels"]) \

                                  print(len([sample for sample in new_inv.studies[0].samples if
                                                                sample.characteristics[0].value.term == assay_plan[item][
                                                                    "sample type"]]))
                                  print("expected size:", expected_total_number_run)

                                  len(assay_plan) *  int(
                                      assay_plan[item]["params"]["number of technical replicates"])

                                  randomized_order = get_processrun_random_token(expected_total_number_run)
                                  counter = -1
                                  for index_i, sample in enumerate([sample for sample in new_inv.studies[0].samples if
                                                                sample.characteristics[0].value.term == assay_plan[item][
                                                                    "sample type"]]):
                                        # print("i: ", index_i, "sample: ", sample.characteristics[1].value.term)
                                        # print("current collection event", assay_plan[item]["collection event"])
                                        if str(sample.characteristics[1].value.term) == str(assay_plan[item]["collection event"]):
                                            # create an extraction process that executes the extraction protocol
                                            extraction_process = Process(executes_protocol=[prtcl for prtcl in new_inv.studies[0].protocols
                                                                                            if prtcl.name == "metabolite extraction"][0],
                                                                         performer="rick",
                                                                         date_=datetime.datetime.now())

                                            # extraction process takes as input a sample, and produces an extract material as output
                                            # we make sure only the right kind of samples get assayed so we check against the sample type
                                            # if sample.characteristics[0].value.term == assay_plan[item]["sample type"]:
                                            # print("sample characteristics: ", sample.characteristics[0].value.term)

                                            extraction_process.inputs.append(sample)
                                            extract = Material(name=sample.name + "extract-{}".format(index_i))
                                            extract.type = "Extract Name"
                                            extraction_process.outputs.append(extract)

                                            # this loop is meant to handle the case where several acquisition modes (e.g. Neg or positive) are used from a sample
                                            # TODO: include a function to obtain the relevant parameters used for data acquisition
                                            #for index_j in range(int(assay_plan[item]["params"]["injection modes"])):
                                                # this inner is for handling multiple runs of the same mode, i.e. tech replicates
                                            for index_k in range(
                                                    int(assay_plan[item]["params"]["number of technical replicates"])):
                                                prtcl_name = [prtcl for prtcl in new_inv.studies[0].protocols
                                                              if prtcl.name == inj_mode + "-" + acq_mode + ' mass spectrometry'][0]
                                                data_acq_process = Process(executes_protocol=prtcl_name,
                                                                           performer="louis",
                                                                           date_=datetime.datetime.now())
                                                counter = counter+1
                                                # print(counter, randomized_order[counter])
                                                run_order = randomized_order[counter]
                                                pv_run_order = ParameterValue(category=ProtocolParameter(
                                                    parameter_name=OntologyAnnotation(term="randomized run order")),
                                                                      value=OntologyAnnotation(term=str(run_order)))

                                                pv_1 = ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term="injection mode")),value=OntologyAnnotation(term=inj_mode))

                                                # if we are dealing with liquid or gas "C"hromatography
                                                if "C" in inj_mode:
                                                    pv_1a = ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term="chromatography instrument")),value=OntologyAnnotation(term="Agilent Q12324A"))
                                                    pv_1b = ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term="chromatography column")),value=OntologyAnnotation(term="AB Hydroxyapatite"))
                                                    pv_1c = ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term="elution program")),value=OntologyAnnotation(term="Acetonitrile 90%, water 10% for 30 min, flow rate: 1ml/min"))

                                                    data_acq_process.parameter_values.append(pv_1a)
                                                    data_acq_process.parameter_values.append(pv_1b)
                                                    data_acq_process.parameter_values.append(pv_1c)

                                                pv_2 = ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term="mass spectrometry instrument")),value=OntologyAnnotation(term="Agilent QTOF"))
                                                pv_3 = ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term="scan polarity")),value=OntologyAnnotation(term=acq_mode))

                                                data_acq_process.parameter_values.append(pv_1)
                                                data_acq_process.parameter_values.append(pv_2)
                                                data_acq_process.parameter_values.append(pv_3)
                                                data_acq_process.parameter_values.append(pv_run_order)


                                                # platform_name = "platform-{}".format(index_j)
                                                platform_name = "platform-" + inj_mode
                                                data_acq_process.name = "assay-name-{}".format(index_i) + "_" + platform_name + \
                                                                        "_run-{}".format(index_k)
                                                data_acq_process.inputs.append(extraction_process.outputs[0])

                                                # data acquisition process usually has an output data file
                                                datafile = DataFile(
                                                    filename="acquired-data-{}".format(index_i) + "_" + platform_name +
                                                             "_run-{}".format(index_k) + ".mzml.gz",
                                                    label="Raw Spectral Data File")
                                                data_acq_process.outputs.append(datafile)

                                                # ensure Processes are linked forward and backward
                                                extraction_process.next_process = data_acq_process
                                                # labeling_process.prev_process = extraction_process
                                                extraction_process.next_process = data_acq_process
                                                # data_acq_process.prev_process = labeling_process
                                                data_acq_process.prev_process = extraction_process

                                                # make sure extract(library), data file, and the processes are attached to the assay
                                                this_assay.data_files.append(datafile)
                                                this_assay.other_material.append(extract)
                                                # this_assay.other_material.append(le)
                                                this_assay.process_sequence.append(extraction_process)
                                                # this_assay.process_sequence.append(labeling_process)
                                                this_assay.process_sequence.append(data_acq_process)
                    # for NMR:
                    elif assay_plan[item]["assay type"] == 4:
                        #TODO: implement get_or_create method and refactor

                        if len(assay_plan[item]["params"]["injection modes"]) > 0:
                            inj_mode = ""
                            acq_mode = ""
                            for inj_mode_code in range(
                                    len(assay_plan[item]["params"]["injection modes"])):
                                if inj_mode_code == 0:
                                    print("YAY, this is autoloader")
                                    inj_mode = "autoloader"
                                elif inj_mode_code == 1:
                                    inj_mode = "LC"
                                elif inj_mode_code == 2:
                                    inj_mode = "GC"
                                else:
                                    print("error, injection method not recognized)")

                                for acq_mode_code in range(
                                        len(assay_plan[item]["params"]["pulse sequences"])):
                                    print("CODE:", assay_plan[item]["params"]["pulse sequences"])
                                    if assay_plan[item]["params"]["pulse sequences"][acq_mode_code] == "1":
                                        acq_mode = "COSY"
                                    elif assay_plan[item]["params"]["pulse sequences"][acq_mode_code] == "2":
                                        acq_mode = "NOESY"
                                    elif assay_plan[item]["params"]["pulse sequences"][acq_mode_code] == "3":
                                        acq_mode = "TOSCY"
                                    elif assay_plan[item]["params"]["pulse sequences"][acq_mode_code] == "3":
                                        acq_mode = "CPMG"
                                    elif assay_plan[item]["params"]["pulse sequences"][acq_mode_code] == "4":
                                        acq_mode = "INEPT"
                                    elif assay_plan[item]["params"]["pulse sequences"][acq_mode_code] == "5":
                                        acq_mode = "HMQC"
                                    elif assay_plan[item]["params"]["pulse sequences"][acq_mode_code] == "6":
                                        acq_mode = "WATERGATE"
                                    else:
                                        print("error, injection method not recognized)")

                                    techname = inj_mode + "-" + acq_mode + " nmr spectroscopy"

                                    nmr_filename = "a_mp_" + inj_mode + "_" + acq_mode + "_nmr.txt"

                                    nmr = [a for a in new_inv.studies[0].assays if
                                          a.measurement_type.term == "metabolite profiling"
                                          and a.technology_type.term == techname and a.filename == nmr_filename]
                                    if len(nmr) > 0:
                                        print("yes, exists in :", nmr)
                                        # if such an assay table already exists, we retrieve it
                                        this_assay = nmr[0]
                                    else:
                                        # or print('nothing found, creating a new object)...')
                                        this_assay = Assay(measurement_type=OntologyAnnotation(
                                            term="metabolite profiling"),
                                                           technology_type=OntologyAnnotation(
                                                               term=techname),
                                                           filename=nmr_filename)

                                        new_inv.studies[0].assays.append(this_assay)

                                        extraction_protocol = Protocol(name='metabolite extraction',
                                                                       protocol_type=OntologyAnnotation(
                                                                           term="material separation"))
                                        new_inv.studies[0].protocols.append(extraction_protocol)

                                        # lc_protocol = Protocol(name="liquid chromatography",
                                        #                              protocol_type=OntologyAnnotation(term="material separation"))
                                        # new_inv.studies[0].protocols.append(labeling_protocol)

                                        nmr_protocol = Protocol(
                                            name=inj_mode + "-" + acq_mode + ' nmr spectroscopy',
                                            protocol_type=OntologyAnnotation(
                                                term="nmr spectroscopy"))
                                        inj_param = ProtocolParameter(
                                            parameter_name=OntologyAnnotation(
                                                term="injection mode"))
                                        if inj_mode == 1 or inj_mode == 2:
                                            ch_instr = ProtocolParameter(
                                                parameter_name=OntologyAnnotation(
                                                    term="chromatography instrument"))
                                            ch_column = ProtocolParameter(
                                                parameter_name=OntologyAnnotation(
                                                    term="chromatography column"))
                                            ch_elu_p = ProtocolParameter(
                                                parameter_name=OntologyAnnotation(
                                                    term="elution program"))
                                            nmr_protocol.parameters.append(ch_instr)
                                            nmr_protocol.parameters.append(ch_column)
                                            nmr_protocol.parameters.append(ch_elu_p)
                                        nmr_instr = ProtocolParameter(
                                            parameter_name=OntologyAnnotation(
                                                term="nmr spectroscopy instrument"))
                                        nmr_probe = ProtocolParameter(parameter_name=(OntologyAnnotation(term="NMR probe")))
                                        acq_param = ProtocolParameter(
                                            parameter_name=OntologyAnnotation(term="pulse sequence"))

                                        nmr_protocol.parameters.append(inj_param)
                                        nmr_protocol.parameters.append(nmr_instr)
                                        nmr_protocol.parameters.append(nmr_probe)
                                        nmr_protocol.parameters.append(acq_param)

                                        new_inv.studies[0].protocols.append(nmr_protocol)

                                    index_i = 0
                                    index_j = 0
                                    index_k = 0
                                    # for index_i, sample in enumerate(new_inv.studies[0].samples):
                                    # some_sample_list = [sample for sample in new_inv.studies[0].samples if
                                    #                sample.characteristics[0].value.term == assay_plan[item]["sample type"] and
                                    #                sample.characteristics[1].value.term == assay_plan[item]["collection event"]]
                                    # print("number of samples: ", len(some_sample_list))
                                    # extractlist_before = [ext for ext in new_inv.studies[0].assays[0].other_material if
                                    #                        ext.type == "Extract Name"]
                                    # print("number of extracts", len(extractlist_before))

                                    for index_i, sample in enumerate([sample for sample in
                                                                      new_inv.studies[0].materials[
                                                                          'samples'] if
                                                                      sample.characteristics[
                                                                          0].value.term ==
                                                                              assay_plan[item][
                                                                                  "sample type"]]):
                                        # print("i: ", index_i, "sample: ", sample.characteristics[1].value.term)
                                        # print("current collection event", assay_plan[item]["collection event"])
                                        if str(sample.characteristics[1].value.term) == str(
                                                assay_plan[item]["collection event"]):
                                            # create an extraction process that executes the extraction protocol
                                            extraction_process = Process(executes_protocol=
                                                                         [prtcl for prtcl in
                                                                          new_inv.studies[
                                                                              0].protocols
                                                                          if
                                                                          prtcl.name == "metabolite extraction"][
                                                                             0],
                                                                         performer="rick",
                                                                         date_=datetime.datetime.now())

                                            # extraction process takes as input a sample, and produces an extract material as output
                                            # we make sure only the right kind of samples get assayed so we check against the sample type
                                            # if sample.characteristics[0].value.term == assay_plan[item]["sample type"]:
                                            # print("sample characteristics: ", sample.characteristics[0].value.term)

                                            extraction_process.inputs.append(sample)
                                            extract = Material(
                                                name=sample.name + "extract-{}".format(index_i))
                                            extract.type = "Extract Name"
                                            extraction_process.outputs.append(extract)

                                            # this loop is meant to handle the case where several acquisition modes (e.g. Neg or positive) are used from a sample
                                            # TODO: include a function to obtain the relevant parameters used for data acquisition
                                            # for index_j in range(int(assay_plan[item]["params"]["injection modes"])):
                                            # this inner is for handling multiple runs of the same mode, i.e. tech replicates
                                            for index_k in range(
                                                    int(assay_plan[item]["params"][
                                                            "number of technical replicates"])):
                                                prtcl_name = \
                                                [prtcl for prtcl in new_inv.studies[0].protocols
                                                 if
                                                 prtcl.name == inj_mode + "-" + acq_mode + ' nmr spectroscopy'][
                                                    0]
                                                data_acq_process = Process(
                                                    executes_protocol=prtcl_name,
                                                    performer="mitsuko",
                                                    date_=datetime.datetime.now())
                                                pv_1 = ParameterValue(category=ProtocolParameter(
                                                    parameter_name=OntologyAnnotation(
                                                        term="injection mode")),
                                                                      value=OntologyAnnotation(
                                                                          term=inj_mode))

                                                # if we are dealing with liquid or gas "C"hromatography
                                                if "C" in inj_mode:
                                                    pv_1a = ParameterValue(
                                                        category=ProtocolParameter(
                                                            parameter_name=OntologyAnnotation(
                                                                term="chromatography instrument")),
                                                        value=OntologyAnnotation(
                                                            term="Agilent Q12324A"))
                                                    pv_1b = ParameterValue(
                                                        category=ProtocolParameter(
                                                            parameter_name=OntologyAnnotation(
                                                                term="chromatography column")),
                                                        value=OntologyAnnotation(
                                                            term="AB Hydroxyapatite"))
                                                    pv_1c = ParameterValue(
                                                        category=ProtocolParameter(
                                                            parameter_name=OntologyAnnotation(
                                                                term="elution program")),
                                                        value=OntologyAnnotation(
                                                            term="acetonitrile 90%, water 10% for 30 min, flow rate: 1ml/min"))

                                                    pv_1d = ParameterValue(
                                                        category=ProtocolParameter(
                                                            parameter_name=OntologyAnnotation(
                                                                term="NMR probe")),
                                                        value=OntologyAnnotation(
                                                            term="flow probe"))

                                                    data_acq_process.parameter_values.append(pv_1a)
                                                    data_acq_process.parameter_values.append(pv_1b)
                                                    data_acq_process.parameter_values.append(pv_1c)
                                                    data_acq_process.parameter_values.append(pv_1d)

                                                else:
                                                    pv_1d = ParameterValue(
                                                        category=ProtocolParameter(
                                                            parameter_name=OntologyAnnotation(
                                                                term="NMR probe")),
                                                        value=OntologyAnnotation(
                                                            term="non-flow probe"))



                                                pv_2 = ParameterValue(category=ProtocolParameter(
                                                    parameter_name=OntologyAnnotation(
                                                        term="nmr spectroscopy instrument")),
                                                                      value=OntologyAnnotation(
                                                                          term="Bruker Avance III"))
                                                pv_3 = ParameterValue(category=ProtocolParameter(
                                                    parameter_name=OntologyAnnotation(
                                                        term="pulse sequence")),
                                                                      value=OntologyAnnotation(
                                                                          term=acq_mode))

                                                data_acq_process.parameter_values.append(pv_1)
                                                data_acq_process.parameter_values.append(pv_2)
                                                data_acq_process.parameter_values.append(pv_3)

                                                # platform_name = "platform-{}".format(index_j)
                                                platform_name = "platform-" + inj_mode
                                                data_acq_process.name = "assay-name-{}".format(
                                                    index_i) + "_" + platform_name + \
                                                                        "_run-{}".format(index_k)
                                                data_acq_process.inputs.append(
                                                    extraction_process.outputs[0])

                                                # data acquisition process usually has an output data file
                                                datafile = DataFile(
                                                    filename="acquired-data-{}".format(
                                                        index_i) + "_" + platform_name +
                                                             "_run-{}".format(index_k) + ".nmrml.gz",
                                                    label="Free Induction Decay Data File")
                                                data_acq_process.outputs.append(datafile)

                                                # ensure Processes are linked forward and backward
                                                extraction_process.next_process = data_acq_process
                                                # labeling_process.prev_process = extraction_process
                                                extraction_process.next_process = data_acq_process
                                                # data_acq_process.prev_process = labeling_process
                                                data_acq_process.prev_process = extraction_process

                                                # make sure extract(library), data file, and the processes are attached to the assay
                                                this_assay.data_files.append(datafile)
                                                this_assay.other_material.append(
                                                    extract)
                                                # this_assay.other_material.append(le)
                                                this_assay.process_sequence.append(
                                                    extraction_process)
                                                # this_assay.process_sequence.append(labeling_process)
                                                this_assay.process_sequence.append(data_acq_process)
                    # else:
                    #     print("no luck :(")

            elif repeats is True and "factorial" in free_or_restricted_design:

                obi = OntologySource(name="OBI", description="Ontology for Biomedical Investigations")
                new_inv.ontology_source_references.append(obi)
                stato = OntologySource(name="STATO", description="Ontology for Statistical Methods")
                new_inv.ontology_source_references.append(stato)
                design1 = OntologyAnnotation(term_source=obi)
                design1.term = "intervention design"
                design1.term_accession = "http://purl.obolibrary.org/obo/OBI_0000115"
                new_inv.studies[0].design_descriptors.append(design1)
                design2 = OntologyAnnotation(term_source=stato)
                design2.term = "full factorial design"
                design2.term_accession = "http://purl.obolibrary.org/obo/STATO_0000270"
                new_inv.studies[0].design_descriptors.append(design2)
                design3 = OntologyAnnotation(term_source=obi)
                design3.term = "repeated measures design"
                design3.term_accession = "http://purl.obolibrary.org/obo/OBI_0500002"
                new_inv.studies[0].design_descriptors.append(design3)

                intervention_list, new_inv = get_list_of_interventions(new_inv)

                assay_plan = []
                for intervention_type in intervention_list.keys():
                    # print("type of intervention: ", intervention_type)
                    for factor in intervention_list[intervention_type].keys():
                        # print("factor :", factor)
                        set_factor_values(factor, intervention_list[intervention_type])
                        # print("associated factor values:", intervention_list[intervention_type][factor])

            dump(isa_obj=new_inv, output_path='./')

        except NotImplemented:
                    print("we have recognized a cross over design & repeated treatment case, which is not yet fully implemented")
                    print("error in create_study_subject() method")

                # my_factors = {}
                # study_group_dictionaries = []
                # number_of_repeats = get_repeat_number()
                # intervention_list = get_list_of_interventions()
                # """factors_for_treatment = get_factors_from_treatment_type(intervention_list)"""
                # for intervention_type in intervention_list.keys():
                #     print("type of intervention: ", intervention_type)
                #     for factor in intervention_list[intervention_type].keys():
                #         print("factor :", factor)
                #         set_factor_values(factor, intervention_list[intervention_type])
                #         print("associated factor values:", intervention_list[intervention_type][factor])
                #
                #         study_group_dictionaries.append(compute_study_groups(intervention_list[intervention_type]))
                #     print("study groups:", list_of_study_group_dictionaries)
                #     # set_study_arms()
                #
                # # for intervention in intervention_list:
                # #         int_dict = dict
                # #         set_factor_values(intervention, int_dict)
                # print(compute_treatment_sequences(list_of_study_group_dictionaries, number_of_repeats))
                # # treatment_arms = compute_treatment_sequences(intervention_list, number_of_repeats)
                # new_inv = set_study_arms(number_of_repeats)
                #
                # # for element in range(len(treatment_arms)):

    else:
        try:
            new_inv = use_default_inv()

            obi = OntologySource(name="OBI", description="Ontology for Biomedical Investigations")
            new_inv.ontology_source_references.append(obi)
            stato = OntologySource(name="STATO", description="Ontology for Statistical Methods")
            new_inv.ontology_source_references.append(stato)
            omiabis = OntologySource(name="OMIABIS", description="an ontological version of MIABIS (Minimum Information About BIobank data Sharing)")
            new_inv.ontology_source_references.append(obi)

            design1 = OntologyAnnotation(term_source=obi)
            design1.term = "observation design"
            design1.term_accession = "http://purl.obolibrary.org/obo/OBI_0300311"
            new_inv.studies[0].design_descriptors.append(design1)
            design2 = OntologyAnnotation(term_source=omiabis)
            design2.term = "cohort study design"
            design2.term_accession = "http://purl.obolibrary.org/obo/OMIABIS_0001020"
            new_inv.studies[0].design_descriptors.append(design2)

            # get_study_group()
            # get_study_temporal_span()
            # get_sample_collection_plan()
            # get_assay_plan()

        except NotImplemented:
            print("we have recognized an observation study, which is not yet fully implemented")
            print("error in create_study_subject() method")

if __name__ == '__main__':
    main()
