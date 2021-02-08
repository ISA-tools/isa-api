# Create ISA-API Investigation from Datascriptor Study Design configuration

In this notebook I will show you how you can use a study design configuration is JSON format as produce by datascriptor (https://gitlab.com/datascriptor/datascriptor) to generate a single-study ISA investigation and how you can then serialise it in JSON and tabular (i.e. CSV) format.

Or study design configuration consists of:
- a 6-arm study design. Each arm has 10 subjects
- there is an observational factor with 3 values, which is age_group (young, middle-aged, elderly)
- a crossover of two treatments, a drug treatment and a biological treatment
- three non-treatment phases: screen, washout and follow-up
- two sample types colllected: blood and saliva
- two assay types: 
    - metabolite profiling through mass spectrometry on the saliva sample. The mass spec will be run on a "Agilent QTQF 6510" instrument, testing both "FIA" and "LC" injection modes, and "positive" acquisition mode.
    - metabolite profiling through  NMR spectroscopy on the blood samples.  The NMR will be run on a "Bruker Avance II 1 GHz" instrument, on "1D 1H NMR" acquisition mode, testing both "CPGM" amd "TOCSY" pulse sequences.

## 1. Setup

Let's import all the required libraries

# If executing the notebooks on `Google Colab`,uncomment the following command 
# and run it to install the required python libraries. Also, make the test datasets available.

# !pip install -r requirements.txt

from time import time
import os
import json

## ISA-API related imports
from isatools.model import Investigation, Study

## ISA-API create mode related imports
from isatools.create.model import StudyDesign
from isatools.create.connectors import generate_study_design

# serializer from ISA Investigation to JSON
from isatools.isajson import ISAJSONEncoder

# ISA-Tab serialisation
from isatools import isatab

## ISA-API create mode related imports
from isatools.create import model
from isatools import isajson

## 2. Load the Study Design JSON configuration

First of all we load the study design configurator with all the specs defined above

with open(os.path.abspath(os.path.join(
    "isa-study-design-as-json/datascriptor", "crossover-study-design-4-arms-blood-derma-nmr-ms-chipseq.json")), "r") as config_file:
    study_design_config = json.load(config_file)
    
study_design_config

## 3. Generate the ISA Study Design from the JSON configuration
To perform the conversion we just need to use the function `generate_isa_study_design_from_config` (name possibly subject to change, should we drop the "isa" and "datascriptor" qualifiers?)

study_design = generate_study_design(study_design_config)
assert isinstance(study_design, StudyDesign)

## 4. Generate the ISA Study from the StudyDesign and embed it into an ISA Investigation

The `StudyDesign.generate_isa_study()` method returns the complete ISA-API `Study` object.

start = time()
study = study_design.generate_isa_study()
end = time()
print('The generation of the study design took {:.2f} s.'.format(end - start))
assert isinstance(study, Study)
investigation = Investigation(studies=[study])

## 5. Serialize and save the JSON representation of the generated ISA Investigation

start = time()
inv_json = json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
end = time()
print('The JSON serialisation of the ISA investigation took {:.2f} s.'.format(end - start))

directory = os.path.abspath(os.path.join('output'))
if not os.path.exists(directory):
    os.makedirs(directory)
with open(os.path.abspath(os.path.join('output','isa-investigation-2-arms-nmr-ms.json')), 'w') as out_fp:
    json.dump(json.loads(inv_json), out_fp)

## 6. Dump the ISA Investigation to ISA-Tab

start = time()
isatab.dump(investigation, os.path.abspath(os.path.join('notebook-output/isa-study-from-design-config')))
end = time()
print('The Tab serialisation of the ISA investigation took {:.2f} s.'.format(end - start))

To use them on the notebook we can also dump the tables to pandas DataFrames, using the `dump_tables_to_dataframes` function rather than dump

dataframes = isatab.dump_tables_to_dataframes(investigation)

len(dataframes)

## 7. Check the correctness of the ISA-Tab DataFrames 

We have 1 study file and 2 assay files (one for MS and one for NMR). Let's check the names:

for key in dataframes.keys():
    display(key)

### 7.1 Count of subjects and samples

We have 10 subjects in the each of the six arms for a total of 60 subjects. 5 blood samples per subject are collected (1 in treatment 1 phase, 1 in treatment, and 3 in the follow-up phase) for a total of 300 blood samples. These will undergo the NMR assay. We have 4 saliva samples per subject (1 during screen and 3 during follow-up) for a total of 240 saliva samples. These will undergo the "mass spcetrometry" assay.

study_frame = dataframes['s_study_01.txt']
count_arm0_samples = len(study_frame[study_frame['Source Name'].apply(lambda el: 'GRP0' in el)])
count_arm2_samples = len(study_frame[study_frame['Source Name'].apply(lambda el: 'GRP1' in el)])
count_arm3_samples = len(study_frame[study_frame['Source Name'].apply(lambda el: 'GRP2' in el)])
count_arm4_samples = len(study_frame[study_frame['Source Name'].apply(lambda el: 'GRP3' in el)])
count_arm3_samples = len(study_frame[study_frame['Source Name'].apply(lambda el: 'GRP4' in el)])
count_arm4_samples = len(study_frame[study_frame['Source Name'].apply(lambda el: 'GRP5' in el)])
print("There are {} samples in the GRP0 arm (i.e. group)".format(count_arm0_samples))
print("There are {} samples in the GRP2 arm (i.e. group)".format(count_arm2_samples))
print("There are {} samples in the GRP3 arm (i.e. group)".format(count_arm3_samples))
print("There are {} samples in the GRP4 arm (i.e. group)".format(count_arm4_samples))

### 7.1 Overview of the Mass Spec assay table

For the mass. spec. assay table, we have 240 (saliva) samples, 480 extracts (2 per  sample, "lipids" and "polar" fractions), 960 labeled extracts (2 per extract, as "#replicates" is  2) and 3840 mass spec protocols + 3840 output files (4 per labeled extract as we do 2 technical replicates with 2 protocol parameter combinations `["Agilent QTQF 6510", "FIA", "positive mode"]` and `["Agilent QTQF 6510", "LC", "positive mode"]`).

dataframes['a_AT0_metabolite-profiling_mass-spectrometry.txt']

### Overview of the NMR assay table

For the NMR assay table, we have 300 (blood) samples, 1200 extracts (4 per  sample, 2 extraction replicates of the "supernatant" and "pellet" fractions) and 4800 NMR protocols + 4800 output files (4 per extract as we do 2 technical replicates with 2 protocol parameter combinations `["Bruker Avance II 1 GHz", "1D 1H NMR", "CPGM"]` and `["Bruker Avance II 1 GHz", "1D 1H NMR", "TOCSY"]`).

dataframes['a_AT2_metabolite-profiling_NMR-spectroscopy.txt']

### Overview of the Chip-Seq assay table

For the Chip-Seq assay table, we have 300 (blood) samples, 1200 extracts (4 per  sample, 2 extraction replicates of the "supernatant" and "pellet" fractions).

dataframes['a_AT16_protein-DNA-binding-site-identification_nucleic-acid-sequencing.txt']

dataframes['a_AT0_metabolite-profiling_mass-spectrometry.txt'].nunique(axis=0, dropna=True)

dataframes['a_AT2_metabolite-profiling_NMR-spectroscopy.txt'].nunique(axis=0, dropna=True)

## About this notebook

- authors: philippe.rocca-serra@oerc.ox.ac.uk, massimiliano.izzo@oerc.ox.ac.uk
- license: CC-BY 4.0
- support: isatools@googlegroups.com
- issue tracker: https://github.com/ISA-tools/isa-api/issues