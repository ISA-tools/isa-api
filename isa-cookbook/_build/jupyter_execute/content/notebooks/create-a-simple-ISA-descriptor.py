# Create a simple ISA descriptor

This example creates minimal metadata for a single study ISA descriptor with no assay declared. 

It shows how to serialize (write) the ISA Model content to ISA-Tab and ISA-JSON formats.

# If executing the notebooks on `Google Colab`,uncomment the following command 
# and run it to install the required python libraries. Also, make the test datasets available.

# !pip install -r requirements.txt

from isatools.model import (Investigation, Study, Assay, Person, Material,
                            DataFile, plink,
                            OntologySource, OntologyAnnotation, Sample,
                            Source, Characteristic, Protocol,ProtocolParameter, Process)
import datetime

## Study metadata

investigation = Investigation()
study = Study(filename="s_study.txt")
study.identifier = "S1"
study.title = "My Simple ISA Study"
study.description = "We could alternatively use the class constructor's parameters to set some default " \
          "values at the time of creation, however we want to demonstrate how to use the " \
          "object's instance variables to set values."
study.submission_date = str(datetime.datetime.today())
study.public_release_date = str(datetime.datetime.today())
study.sources = [Source(name="source1")]
study.samples = [Sample(name="sample1")]
study.protocols = [Protocol(name="sample collection"),
                   Protocol(name="data analysis with Galaxy",
                            uri="https://doi.org/10.5464/workflow.cwl",
                            protocol_type=OntologyAnnotation(term="data transformation"),
                            parameters=[ProtocolParameter(parameter_name=OntologyAnnotation(term="genome assembly")),
                                        ProtocolParameter(parameter_name=OntologyAnnotation(term="cut-off value"))]),
                    Protocol(name="data visualization with Intermine",
                             uri="https://intermine.org/10.5464/network.svg",
                             protocol_type=OntologyAnnotation(term="data visualization"),
                                                                )]
study.process_sequence = [Process(executes_protocol=study.protocols[-1], inputs=[study.sources[-1]], outputs=[study.samples[-1]])]
investigation.studies = [study]



# Let's see the object :
investigation

## Writing to ISA-Tab

from isatools.isatab import dumps
print(dumps(investigation))

## Writing to ISA-JSON

import json
from isatools.isajson import ISAJSONEncoder
print(json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')))

## About this notebook

- authors: philippe.rocca-serra@oerc.ox.ac.uk, massimiliano.izzo@oerc.ox.ac.uk
- license: CC-BY 4.0
- support: isatools@googlegroups.com
- issue tracker: https://github.com/ISA-tools/isa-api/issues