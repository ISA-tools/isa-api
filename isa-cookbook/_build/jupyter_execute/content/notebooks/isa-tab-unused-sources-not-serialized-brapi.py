# Known Issue: unused ISA Source aren't serialized to ISA-Tab

## Abtract:

This notebook documents a behavior of the ISA-Tab writer which results in declared but unused ISA Source objects not to be serialized in the ISA-Tab file.
The ISA objects are serialized fine if using the ISA-JSON write.
The future releases of the ISA-API will see to address the issue.


## Let's get the tools

# If executing the notebooks on `Google Colab`,uncomment the following command 
# and run it to install the required python libraries. Also, make the test datasets available.

# !pip install -r requirements.txt

import os
import json
import datetime
from isatools.model import (Investigation, Study, Assay, Person, Material,
                            DataFile, plink,
                            OntologySource, OntologyAnnotation, Sample,
                            Source, Characteristic, Protocol, Process)
from isatools import isatab
from isatools.isajson import ISAJSONEncoder

final_dir = os.path.abspath(os.path.join('notebook-output', 'issue-brapi'))

## Creating an ISA Study and boilerplate information

investigation = Investigation()
investigation.identifier = "BRAPI-test-unused-source"
investigation.title = "BRAPI-test-unused-source"
investigation.description = "this is test to understand the conditions under which ISA-API will serialize or not serialize a Source entity declared but not used in a workflow. Note: while the python ISA-API does not serialize in the Tab format, the information is available from ISA-JSON."

prs_test_study = Study(filename="s_prs_test.txt")

prs_test_study.identifier = "PRS"
prs_test_study.title = "Unused Sources"
prs_test_study.description = "testing if the python ISA-API supports unusued Sources in ISA-Tab serialization"


prs = Person(last_name="Rocca-Serra", first_name="Philippe", mid_initials="T", affiliation="OeRC", email="prs@hotmail.com" )
prs_test_study.contacts.append(prs)
print(prs.mid_initials)

ncbi_taxon = OntologySource(name='NCBITaxon', description="NCBI Taxonomy")
human_characteristic= Characteristic(category=OntologyAnnotation(term="Organism"),
                                     value=OntologyAnnotation(term="Homo Sapiens", term_source=ncbi_taxon,
                                                              term_accession="http://purl.bioontology.org/ontology/NCBITAXON/9606"))

## Creating ISA Sources

subject_0 = Source(name='human individual-0', characteristics=[human_characteristic]) 
subject_1 = Source(name='human individual-1', characteristics=[human_characteristic]) 
subject_2 = Source(name='human individual-2', characteristics=[human_characteristic]) 


## Creating ISA Samples

sample_0 = Sample(name='SBJ0_sample1')
# note that 2 samples are generated from subject_1
sample_1 = Sample(name='SBJ1_sample1')
sample_2 = Sample(name='SBJ1_sample2')
# note that no sample is generated from subject_
sample_3 = Sample(name='SBJ2')

## Associating Sources and Samples to the ISA.Study. object

prs_test_study.sources.append(subject_0)
prs_test_study.sources.append(subject_1)
prs_test_study.sources.append(subject_2)

prs_test_study.samples.append(sample_0)
prs_test_study.samples.append(sample_1)
prs_test_study.samples.append(sample_2)
#prs_test_study.samples.append(subject_2)
prs_test_study.samples.append(sample_3)

## Declaring Protocol objects

### Don't forget the protocol_type should be declared as an ISA Ontology Annotation

prs_protocol = Protocol(name="sample collection",
                             protocol_type=OntologyAnnotation(term="sample collection"))

### Adding the newly created protocol to the list of protocols associated with an ISA Study Object

prs_test_study.protocols.append(prs_protocol)

## Creating the ProtocolApplication events connecting Parent to Children Materials

### executing a protocol minimally or maximally by specifying date and performer of execution

prs_process0 = Process(executes_protocol=prs_protocol)
now = str(datetime.datetime.now().strftime("%Y-%m-%d"))
prs_process1 = Process(executes_protocol=prs_protocol, performer=prs.first_name, date_=now)
prs_process2 = Process(executes_protocol=prs_protocol, performer=prs.first_name, date_=now)
prs_process3 = Process(executes_protocol=prs_protocol, performer=prs.first_name, date_=now)

### Setting input and outputs of each sample collection protocol application

prs_process0.inputs.append(subject_0)
prs_process0.outputs.append(sample_0)
prs_process1.inputs.append(subject_1)
prs_process1.outputs.append(sample_1)
prs_process2.inputs.append(subject_1)
prs_process2.outputs.append(sample_2)

### Now the following tests if setting a protocol application with no output jinxes the ISA-API

prs_process3.inputs.append(subject_2)
prs_process3.outputs.append(sample_3)

### Here, the ISA Study object is updated by associating all the processes/protocol_applications to the process_sequence attribute.


prs_test_study.process_sequence.append(prs_process0)
prs_test_study.process_sequence.append(prs_process1)
prs_test_study.process_sequence.append(prs_process2)
prs_test_study.process_sequence.append(prs_process3)

## Creating an ISA Assay object - This is to test associating an ISA Source as input to an Assay

### Step1 - Create the ISA Assay Object

assay_on_source = Assay(measurement_type=OntologyAnnotation(term="phenotyping"),
                     technology_type=OntologyAnnotation(term=""),
                     filename="a_assay-test.txt")

### Step2 - Create a new ISA Protocol the type of which is `data acquisition`

assay_protocol = Protocol(name="assay-on-source",
                          protocol_type="data acquisition")


### Step3 - Remember to add the new protocol to the ISA.Study object

prs_test_study.protocols.append(assay_protocol)

### Step4 - Create the Protocol Application event which generates an ISA DataFile

assay_process = Process(executes_protocol=assay_protocol, performer=prs.first_name)

### Step5 - Create an ISA DataFile object

dummy_file= DataFile(filename="dummy.txt")

### Step6 - Set ProtocolApplication/Process inputs and outputs testing if an ISA.Source can be used in an ISA.Assay

assay_process.inputs.append(sample_0)
assay_process.outputs.append(dummy_file)

### Step7 - Associate the newly created ISA.DataFile with the ISA.Assay object

assay_on_source.data_files.append(dummy_file)

### Step8 - Link and Connect ISA.ProtocolApplications via the process_sequence attribute

assay_on_source.process_sequence.append(prs_process3)
assay_on_source.process_sequence.append(assay_process)

### Step9 - Update the ISA.Assay Object by listing all ISA.Materials used in the Assay associated ProtocolApplications

assay_on_source.samples.append(sample_3)
#assay_on_source.other_material.append(subject_2)
plink(prs_process3, assay_process)

prs_test_study.process_sequence.append(assay_process)

### Step10 - Update the ISA.Study Object by adding the ISA Assay object to the ISA.Study assays attribute

prs_test_study.assays.append(assay_on_source)

investigation.studies.append(prs_test_study)

dataframes = isatab.dump_tables_to_dataframes(investigation)

dataframes['s_prs_test.txt']

#dataframes['assay-test.txt']

isatab.dump(isa_obj=investigation, output_path=final_dir)

isa_j = json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
open("isa_as_json_from_dumps.json","w").write(isa_j) # this call write the string 'isa_j' to the file called 'isa_as_json_from_dumps.json'

my_json_report = isatab.validate(open(os.path.join(final_dir, 'i_investigation.txt')))

print(my_json_report)

## About this notebook

- authors: philippe.rocca-serra@oerc.ox.ac.uk, massimiliano.izzo@oerc.ox.ac.uk
- license: CC-BY 4.0
- support: isatools@googlegroups.com
- issue tracker: https://github.com/ISA-tools/isa-api/issues