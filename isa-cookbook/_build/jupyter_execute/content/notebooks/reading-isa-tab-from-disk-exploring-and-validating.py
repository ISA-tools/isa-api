# Reading ISA-Tab from files and Validating ISA-Tab files 

## Abstract:

The aim of this notebook is to:
    - show essential function to read and load an ISA-tab file in memory.
    - navigate key objects and pull essential attributes.
    - learn how to invoke the ISA-tab validation function.
    - interpret the output of the validation report.


## 1. Getting the tools

import isatools
import os
import sys
from isatools import isatab

## 2. Reading and loading an ISA Investigation in memory from an ISA-Tab instance

with open(os.path.join('./BII-S-3', 'i_gilbert.txt')) as fp:
            ISA = isatab.load(fp)

### Let's check the description of the first study object present in an ISA Investigation object

ISA.studies[0].description

### Let's check the protocols declared in ISA the study (using a python list comprehension):


[ISA.studies[0].protocols[n].description for n in range(len(ISA.studies[0].protocols))]


### Let's now checks the ISA Assay Measurement and Technology Types  are used in this ISA Study object

[ISA.studies[0].assays[n].measurement_type.term + " using " + ISA.studies[0].assays[n].technology_type.term  for n in range(len(ISA.studies[0].assays))]

### Let's now check the `ISA Study Source` Material:

[ISA.studies[0].sources[n].name   for n in range(len(ISA.studies[0].sources))]

#### Let's check what is the first `ISA Study Source property`:

ISA.studies[0].sources[0].characteristics[0].category.term

#### Let's now check what is the `value` associated with that first `ISA Study Source property`:

ISA.studies[0].sources[0].characteristics[0].value.term

#### Let's now check what are all the properties associated with this first `ISA Study Source`

[ISA.studies[0].sources[0].characteristics[n].category.term for n in range(len(ISA.studies[0].sources[0].characteristics))]

#### And the corresponding values are:

[ISA.studies[0].sources[0].characteristics[n].value for n in range(len(ISA.studies[0].sources[0].characteristics))]

## 3. Invoking the python ISA-Tab Validator

my_json_report_bii_i_1 = isatab.validate(open(os.path.join('./BII-I-1/', 'i_investigation.txt')))

my_json_report_bii_s_3 = isatab.validate(open(os.path.join('./BII-S-3/', 'i_gilbert.txt')))

my_json_report_bii_s_4 = isatab.validate(open(os.path.join('./BII-S-4/', 'i_investigation.txt')))

my_json_report_bii_s_7 = isatab.validate(open(os.path.join('./BII-S-7/', 'i_matteo.txt')))

my_json_report_bii_s_7

- This Validation Report shows that No Error has been logged
- The rest of the report consists in warnings meant to draw the attention of the curator to elements which may be provided but which do not break the ISA syntax.
- Notice the `study group` information reported on both study and assay files. If ISA `Factor Value[]` fields are found present in the `ISA Study` or ` ISA Assay` tables, the validator will try to identify the set of unique `Factor Value` combination defining a `Study Group`.
    - When no `Factor Value` are found in a ISA `Study` or `Assay` table, the value is left to its default value: -1, which means that `No Study Group` have been found.
    - ISA **strongly** encourages to declare Study Group using ISA Factor Value to unambiguously identify the Independent Variables of an experiment.
    

## 4. How does a validation failure looks like ?

### BII-S-5 contains an error located in the `i_investigation.txt` file of the submission

my_json_report_bii_s_5 = isatab.validate(open(os.path.join('./BII-S-5/', 'i_investigation.txt')))

my_json_report_bii_s_5

- The Validator report the Error Array is not empty and shows the root cause of the syntactic validator error.
- There is a typo in the Investigation file which affects 2 positions on the file for both Investigation and Study Object: 
<span style="color:red">Publication **l**ist</span>. vs <span style="color:green">Publication **L**ist</span>

## About this notebook

- authors: philippe.rocca-serra@oerc.ox.ac.uk, massimiliano.izzo@oerc.ox.ac.uk
- license: CC-BY 4.0
- support: isatools@googlegroups.com
- issue tracker: https://github.com/ISA-tools/isa-api/issues