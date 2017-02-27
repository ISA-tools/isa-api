__author__ = 'prs'

from itertools import product
from itertools import izip
from itertools import permutations
import uuid
import getopt
import sys


assay_types = list


#todo:
# read in ISAconfiguration and get list of assay_types
#
# if "mass spectrometry"
#         option: chromatographycolumtypes
#         option: acquisition_mode {positive,negative,both}
#         option: number_of_replicate_run/technical_replicates
#
# if "nmr spectroscopy"
#         option: acquisition_mode {1D,2D,both}
#         option: number_of_replicate_run/technical_replicates
#
# if "NGS"
#         option: library_layout {single,double}
#         option: gene_survey {gene list}
#         option: barcoding {yes,no}
#         option: number_of_replicate_run/technical_replicates
#
# if "DNA microarray"
#         option: label
#         option: how many distinct array design
#         option: applied to all (yes,no) -> (deal with no answer)
#         option: number_of_replicate_run/technical_replicates






