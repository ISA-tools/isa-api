import json
import os
import logging
from isatools import isatab

from isatools.model.v1 import *
from isatools.model.v1 import Investigation, Study, Protocol, OntologyAnnotation, Person

with open('./tests/data/nih-dcc/nih-dcc-metadata4.json', 'r') as f:
    array = json.load(f)

# print(array['protocol'])
# for element in array['protocol']:
#     array['protocol'][element]['id']
#     array['protocol'][element]['description']
#     array['protocol'][element]['type']
#     array['protocol'][element]['filename']

# for element in array['measurement']:
#     print(array['measurement'][element]['corrected_mz'])

# for element in array['subject']:
#     print(array['subject'][element]['species'])

outputdir = "./tests/data/tmp/"

# Building the Investigation Object and its elements:
if len(array['project']) > 0:
    print(next(iter(array['project'])))
    prj=next(iter(array['project']))
    investigation = Investigation(identifier=array['project'][prj]['id'])

    obi = OntologySourceReference(name='OBI', description="Ontology for Biomedical Investigations")
    investigation.ontology_source_references.append(obi)

    invPerson = Person(first_name=array['project'][prj]['PI_first_name'], last_name=array['project'][prj]['PI_last_name'],
                       email=array['project'][prj]['PI_email'],
                       address=array['project'][prj]['address'],
                       affiliation=(array['project'][prj]['department'] + ", " + array['project'][prj]['institution']),
                       roles=[OntologyAnnotation(name="principal investigator", term_source=obi)])
    investigation.contacts.append(invPerson)

else:
    print("no project")


if len(array['study']) > 0 :
    st = next(iter(array['study']))
    oat = array['study'][st]['type']

    oa_st_design = OntologyAnnotation(name=oat, term_source=obi)

    investigation.studies.append(Study(identifier=array['study'][st]['id'],
                                       title=array['study'][st]['title'],
                                       description=array['study'][st]['description'],
                                       design_descriptors=[oa_st_design],
                                       filename="s_"+array['study'][st]['id'] + ".txt"))

    studyid = array['study'][st]['id']
    studyPerson = Person(first_name=array['study'][st]['PI_first_name'],
                         last_name=array['study'][st]['PI_last_name'],
                         email=array['study'][st]['PI_email'],
                         address=array['study'][st]['address'],
                         affiliation=(array['study'][st]['department'] + ", " + array['study'][st]['institution']),
                         roles=[OntologyAnnotation(name="principal investigator",term_source=obi)])

    investigation.studies[0].contacts.append(studyPerson)

for element in array['factor']:
    factor = StudyFactor(name=array['factor'][element]['id'])
    investigation.studies[0].factors.append(factor)


for element in array['protocol']:
    oat_p = array['protocol'][element]['type']
    oa_protocol_type = OntologyAnnotation(name=oat_p, term_source=obi)
    investigation.studies[0].protocols.append(Protocol(name=array['protocol'][element]['id'],
                                                       protocol_type=oa_protocol_type,
                                                       description=array['protocol'][element]['description'],
                                                       uri=array['protocol'][element]['filename']))

    if 'MS' in array['protocol'][element]['type']:
        investigation.studies[0].assays.append(Assay(measurement_type=OntologyAnnotation(name="metabolite profiling",term_source=obi),
                                                     technology_type=OntologyAnnotation(name="mass spectrometry",term_source=obi),
                                                     filename="a_assay_ms.txt"))
    if 'NMR' in array['protocol'][element]['type']:
        investigation.studies[0].assays.append(Assay(measurement_type=OntologyAnnotation(name="metabolite profiling",term_source=obi),
                                                     technology_type=OntologyAnnotation(name="nmr spectroscopy",term_source=obi),
                                                     filename="a_assay_nmr.txt"))
    # investigation.studies[0].protocols.append(Protocol())

for element in array['subject']:

    # print(array['subject'][element])
    # if "organism" in array['subject'][element]['type']:
    #     source = Source(name=array['subject'][element]['id'])
    #
    #     ncbitaxon = OntologySourceReference(name='NCBITaxon', description="NCBI Taxonomy")
    #     characteristic_organism = Characteristic(category=OntologyAnnotation(term="Organism"),
    #                                              value=OntologyAnnotation(term=array['subject'][element]['species'], term_source=ncbitaxon,
    #                                                                       term_accession="http://purl.bioontology.org/ontology/NCBITAXON/9606"))
    #     source.characteristics.append(characteristic_organism)

    if "tissue_slice" in array['subject'][element]['type']:
        # print(array['subject'][element]['type'])
        source = Source(name=array['subject'][element]['id'])
        investigation.studies[0].materials['sources'].append(source)
        sample = Sample(name=array['subject'][element]['id'], derives_from=array['subject'][element]['parentID'])
        characteristic_organism = Characteristic(category=OntologyAnnotation(name="organism_part", term_source=obi),
                                                 value=OntologyAnnotation(name=array['subject'][element]['tissue_type'],
                                                                          term_source=obi))
        sample.characteristics.append(characteristic_organism)
        investigation.studies[0].materials['samples'].append(sample)
        print(investigation.studies[0].materials['samples'][0].name)

        sample_collection_process = Process(executes_protocol=array['subject'][element]['protocol.id'])
        sample_collection_process.inputs.append(source)
        sample_collection_process.outputs.append(sample)
        investigation.studies[0].process_sequence.append(sample_collection_process)



# for src in investigation.studies[0].materials:
#
# for sam in investigation.studies[0].materials:


for element in array['sample']:
    if 'polar' in array['sample'][element]['type']:
        data_acq_process = Process(executes_protocol=array['sample'][element]['protocol.id'])
        data_acq_process.name = array['sample'][element]['id']

        material_in = Material(name=array['sample'][element]['parentID'])
        material_type = Characteristic(category=OntologyAnnotation(name="material_type", term_source=obi),
                                       value=OntologyAnnotation(name=array['sample'][element]['type'],
                                                                term_source=obi))
        material_in.characteristics.append(material_type)
        investigation.studies[0].assays[0].materials['other_material'].append(material_in)

        data_acq_process.inputs.append(material_in)
        datafile = DataFile(filename="mass_isotopomer-data_" + studyid + "_" + array['sample'][element]['id'] + "_" +
                                     ".txt", label="Raw Data File")
        data_acq_process.outputs.append(datafile)
        print(investigation.studies[0].assays[0].technology_type.name)
        investigation.studies[0].assays[0].data_files.append(datafile)
        print(investigation.studies[0].assays[0].data_files[0].filename)

    else:
        material_in = Material(name=array['sample'][element]['parentID'])
        material_out = Material(name=array['sample'][element]['id'])
        material_type = Characteristic(category=OntologyAnnotation(name="material_type"),
                                       value=OntologyAnnotation(name=array['sample'][element]['type']))
        material_out.characteristics.append(material_type)
        process = Process(executes_protocol=array['sample'][element]['protocol.id'])
        process.name = array['sample'][element]['id']
        process.inputs.append(material_in)
        process.outputs.append(material_out)

        investigation.studies[0].assays[0].materials['other_material'].append(material_in)
        investigation.studies[0].assays[0].materials['other_material'].append(material_out)


data_rec_header = "\t".join(("metabolite name", "assignment", "signal intensity", "retention time",
                            "m/z", "formula", "adduct", "isotopologue", "sample identifier"))
records = []
for element in array['measurement']:
    # metabolite_name: -> compound
    # array['measurement'][element]['signal_intensity']
    record = '\t'.join((array['measurement'][element]['compound'],
                        array['measurement'][element]['assignment'],
                        array['measurement'][element]['raw_intensity'],
                        array['measurement'][element]['retention_time'],
                        array['measurement'][element]['corrected_mz'],
                        array['measurement'][element]['formula'],
                        array['measurement'][element]['adduct'],
                        array['measurement'][element]['isotopologue'],
                        array['measurement'][element]['sample.id']))
    records.append(record)

output_path = outputdir + "/" + "nih-dcc" + "/"
if not os.path.exists(output_path):
    os.makedirs(output_path)
    try:
        print("writing 'investigation information' to file...")
        print(isatab.dump(investigation, output_path=output_path))
        isatab.dump(investigation, output_path=output_path)

        fh = open(output_path + "/" + studyid + "-maf-data-nih-dcc-json.txt", "w")
        # print("writing 'maf file document' to file from 'generate_maf_file' method:...")
        fh.writelines(data_rec_header)
        fh.writelines("\n")
        for item in records:
            fh.writelines(item)
            fh.writelines("\n")

    except IOError:
        print("Error: in main() method can\'t open file or write data")




