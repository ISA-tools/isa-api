__author__ = 'prs'

from itertools import product
from itertools import izip
from itertools import permutations
import uuid
import getopt
import sys




def remove_duplicate_from_list(some_list):
    if len(some_list)>0 : # and some_list.contains(',')
        listvalues = [x.strip() for x in some_list.split(',')] #removes trailing whitespace in a list such as a,b ,c ,c
        listvaluesnodup = list(set(listvalues)) #removes any duplicate values in a list such as a,a,b,c
        listvaluesnodup = filter(bool, listvaluesnodup) #removes any empty string supplied as is a,,c,d
    else:
        print "the list you have supplied is not valid, please enter a csv list"

    return listvaluesnodup


"""def select_sample_type()
    longopts, shortopts = getopt.getopt(sys.argv[1:], shortopts=['s','f'], longopts=['solid tissue','biological fluid'])
    argDict = dict(longopts)"""



def choose_fluid_or_solid_both():

    sample_type=raw_input("are the samples 'solid' or 'biofluid' or 'both'? ")
    if sample_type == "solid":
        return sample_type
        #collected_samples(sample_type)
    elif sample_type == "biofluid":
        return sample_type
        #collected_samples(sample_type)
    elif sample_type == "both":
        return sample_type
       # collected_samples(sample_type)
    else:
        print "input not recognised"
        choose_fluid_or_solid_both()




def collected_samples(sample_type):

    if sample_type == "biofluid":
        fluid_samples=raw_input("select from the following list (urine,blood,cerebrospinal fluid,sweat,lavage):  ")
        #for example: blood,urine,sweat,muscle
        fluid_samples = remove_duplicate_from_list(fluid_samples)
        return fluid_samples

    elif sample_type == "solid":
        solid_samples=raw_input("select from the following list (liver,kidney,muscle,brain,lung,flower):  ")
        solid_samples = remove_duplicate_from_list(solid_samples)
        return solid_samples

    elif sample_type == "both":
        fluid_samples=raw_input("select from the following list (urine,blood,cerebrospinal fluid,sweat,lavage): ")
        fluid_samples = remove_duplicate_from_list(fluid_samples)

        solid_samples=raw_input("select from the following list (liver,kidney,muscle,brain,lung,2): ")
        solid_samples = remove_duplicate_from_list(solid_samples)

        return solid_samples,fluid_samples
    else:
        print "input not recognised"
        choose_fluid_or_solid_both()


def sample_collection_plan(sample_types):

    common2all = raw_input("is the sampling plan applicable to all samples? (yes/no)")

    if common2all == 'yes':
        #relying on providing a number of samples fails to place the sampling events in context of treatment (maybe solve it via UI)
       sampling_events=raw_input("how many times each of the samples have been collected (integer):  ")
       sampling_events=remove_duplicate_from_list(sampling_events)
       return sampling_events

    elif common2all == 'no':
        samples_and_events={}
        for s_type in sample_types:
            specific_sampling_events=raw_input("for sample " + "'" + s_type  + "'" + " how many times each of the samples have been collected (integer): ")
            specific_sampling_events=remove_duplicate_from_list(specific_sampling_events)
            samples_and_events[s_type]=specific_sampling_events

        return samples_and_events

    else:
        print "please say yes or no"


sample_type = choose_fluid_or_solid_both()

samples = collected_samples(sample_type)

sample_collection_plan(samples)


