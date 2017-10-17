from __future__ import absolute_import
from isatools import isatab
from isatools.model import *
from isatools.model import Investigation, OntologySource, Person, Sample, Source, Assay, OntologyAnnotation, Protocol, \
    Study, \
    StudyFactor, Characteristic, Material, Process, DataFile, plink
import json
import os


def convert(json_path, output_path):
    print(json_path)
    print(output_path)

    with open(json_path, 'r') as f:
        dcc_json = json.load(f)

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

    # Building the Investigation Object and its elements:

    project_set_json = dcc_json.get('project')

    if len(project_set_json) == 0:
        raise IOError('No project found in input JSON')

    # print(next(iter(project_set_json)))
    project_json = next(iter(project_set_json.values()))
    investigation = Investigation(identifier=project_json['id'])

    obi = OntologySource(name='OBI',
                         description='Ontology for Biomedical Investigations')
    investigation.ontology_source_references.append(obi)

    inv_person = Person(
        first_name=project_json['PI_first_name'],
        last_name=project_json['PI_last_name'],
        email=project_json['PI_email'],
        address=project_json['address'],
        affiliation=(', '.join(
            [project_json['department'], project_json['institution']]
        )),
        roles=[
            OntologyAnnotation(term="",
                               term_source=obi,
                               term_accession="http://purl.org/obo/OBI_1")
        ])
    investigation.contacts.append(inv_person)

    study_set_json = dcc_json.get('study')

    if len(study_set_json) > 0:
        study_json = next(iter(study_set_json.values()))

        study = Study(identifier=study_json['id'], title=study_json['title'],
                      description=study_json['description'],
                      design_descriptors=[OntologyAnnotation(
                          term=study_json['type'],
                          term_source=obi,
                          term_accession="http://purl.org/obo/OBI_1")],
                      filename='s_{study_id}.txt'.format(study_id=study_json['id']))

        investigation.studies = [study]

        studyid = study_json['id']
        print(studyid)
        study_person = Person(
            first_name=study_json['PI_first_name'],
            last_name=study_json['PI_last_name'],
            email=study_json['PI_email'],
            address=study_json['address'],
            affiliation=(', '.join(
                [study_json['department'], study_json['institution']])),
            roles=[
                OntologyAnnotation(
                    term='principal investigator',
                    term_source=obi,
                    term_accession="http://purl.org/obo/OBI_1")])

        study.contacts.append(study_person)

        for factor_json in dcc_json['factor'].values():
            factor = StudyFactor(name=factor_json['id'])
            study.factors.append(factor)

        for i, protocol_json in enumerate(dcc_json['protocol'].values()):
            oat_p = protocol_json['type']
            oa_protocol_type = OntologyAnnotation(term=oat_p,
                                                  term_source=obi,
                                                  term_accession="http://purl.org/obo/OBI_1")
            study.protocols.append(
                Protocol(name=protocol_json['id'],
                         protocol_type=oa_protocol_type,
                         description=protocol_json['description'],
                         uri=protocol_json['filename']))

            if 'MS' in protocol_json['type']:
                study.assays.append(
                    Assay(measurement_type=OntologyAnnotation(
                            term='mass isotopologue distribution analysis',
                            term_source=obi,
                            term_accession="http://purl.org/obo/OBI_112"),
                          technology_type=OntologyAnnotation(
                            term='mass spectrometry',
                            term_source=obi,
                            term_accession="http://purl.org/obo/OBI_1"),
                          filename='a_assay_ms_{count}.txt'.format(count=i)))

            if 'NMR' in protocol_json['type']:
                study.assays.append(
                    Assay(measurement_type=OntologyAnnotation(
                            term='isotopomer analysis',
                            term_source=obi,
                            term_accession="http://purl.org/obo/OBI_111"),
                          technology_type=OntologyAnnotation(
                            term='nmr spectroscopy',
                            term_source=obi,
                            term_accession="http://purl.org/obo/OBI_1"),
                          filename='a_assay_nmr.txt'))

        for subject_json in dcc_json['subject'].values():

            # print(array['subject'][element])
            if "organism" in subject_json['type']:


                source = Source(name=subject_json['id'])

                ncbitaxon = OntologySource(name='NCBITaxon', description="NCBI Taxonomy")
                characteristic_organism = Characteristic(
                               category=OntologyAnnotation(term="Organism"),
                               value=OntologyAnnotation(term=subject_json['species'],
                                                        term_source=ncbitaxon,
                                                        term_accession='http://purl.bioontology.org/ontology/NCBITAXON/9606'))
                source.characteristics.append(characteristic_organism)
                study.sources.append(source)

            elif 'tissue_slice' in subject_json['type']:
                # print(array['subject'][element]['type'])
                source = Source(name=subject_json['id'])
                study.sources.append(source)
                ncbitaxon = OntologySource(name='NCBITaxon', description="NCBI Taxonomy")
                characteristic_organism = Characteristic(
                    category=OntologyAnnotation(term="Organism"),
                    value=OntologyAnnotation(term=subject_json['species'],
                                             term_source=ncbitaxon,
                                             term_accession='http://purl.bioontology.org/ontology/NCBITAXON/9606'))
                source.characteristics.append(characteristic_organism)

                sample = Sample(
                    name=subject_json['id'],
                    derives_from=subject_json['parentID'])
                characteristic_organismpart = Characteristic(
                    category=OntologyAnnotation(term='organism_part'),
                    value=OntologyAnnotation(
                        term=subject_json['tissue_type'],
                        term_source=obi,
                        term_accession="http://purl.org/obo/OBI_1"))

                sample.characteristics.append(characteristic_organismpart)
                study.samples.append(sample)
                # print(study.samples[0].name)

                sample_collection_process = Process(
                    executes_protocol=study.get_prot(
                        subject_json['protocol.id']))
                sample_collection_process.inputs.append(source)
                sample_collection_process.outputs.append(sample)
                study.process_sequence.append(sample_collection_process)

            else:
                source = Source(name=subject_json['id'])

                ncbitaxon = OntologySource(name='NCBITaxon', description="NCBI Taxonomy")
                characteristic_organism = Characteristic(
                    category=OntologyAnnotation(term="Organism"),
                    value=OntologyAnnotation(term=subject_json['species'],
                                             term_source=ncbitaxon,
                                             term_accession='http://purl.bioontology.org/ontology/NCBITAXON/9606'))
                source.characteristics.append(characteristic_organism)
                study.sources.append(source)
                print(subject_json['id'])
                print(subject_json['species'])
                print(subject_json['type'])
        # for src in investigation.studies[0].materials:
        #
        # for sam in investigation.studies[0].materials:

        for sample_json in dcc_json['sample'].values():

            if 'cells' in sample_json['type']:
                material_separation_process = Process(executes_protocol=study.get_prot(sample_json['protocol.id']))
                material_separation_process.name = sample_json['id']
                # dealing with input material, check that the parent material is already among known samples or sources

                if len([x for x in study.samples if x.name == sample_json['parentID']]) == 0:
                    material_in = Sample(name=sample_json['parentID'])
                    material_separation_process.inputs.append(material_in)
                    study.assays[0].samples.append(material_in)
                else:
                    print([x for x in study.samples if x.name == sample_json['parentID']])
                    material_separation_process.inputs.append([x for x in study.samples if x.name == sample_json['parentID']][0])

                material_out = Sample(name=sample_json['id'])
                material_type = Characteristic(
                    category=OntologyAnnotation(
                        term='material_type'),
                    value=OntologyAnnotation(term=sample_json['type'],
                                             term_source=obi,
                                             term_accession="http://purl.org/obo/OBI_xxxxxxx"))
                material_out.characteristics.append(material_type)
                material_separation_process.outputs.append(material_out)
                study.assays[0].samples.append(material_out)
                try:
                    sample_collection_process
                except NameError:
                    sample_collection_process = None
                if sample_collection_process is None:
                    sample_collection_process = Process(executes_protocol="")
                else:
                 # plink(protein_extraction_process, data_acq_process)
                 # plink(material_separation_process, protein_extraction_process)

                 plink(sample_collection_process, protein_extraction_process)

            if 'protein_extract' in sample_json['type']:
                protein_extraction_process = Process(executes_protocol=study.get_prot(sample_json['protocol.id']))
                protein_extraction_process.name = sample_json['id']

                if len([x for x in study.samples if x.name == sample_json['parentID']]) == 0:
                    material_in = Sample(name=sample_json['parentID'])
                    protein_extraction_process.inputs.append(material_in)
                    study.assays[0].samples.append(material_in)
                else:
                    # print([x for x in study.samples if x.name == sample_json['parentID']])
                    protein_extraction_process.inputs.append(material_in)

                # for material_in in study.samples:
                #     # print("OHO:", material_in.name)
                #     if material_in.name == sample_json['parentID']:
                #         # print("C:",sample_json['parentID'])
                #         #no need to create, just link to process
                #         protein_extraction_process.inputs.append(x)
                #     else:
                #         # print("D:", sample_json['parentID'])
                #         #create new material and link
                #         material_in = Sample(name=sample_json['parentID'])
                #         protein_extraction_process.inputs.append(material_in)

                material_out = Material(name=sample_json['id'])
                material_out.type = "Extract Name"
                material_type = Characteristic(
                    category=OntologyAnnotation(
                        term='material_type'),
                    value=OntologyAnnotation(term=sample_json['type'],
                                             term_source=obi,
                                             term_accession="http://purl.org/obo/OBI_1"))
                material_out.characteristics.append(material_type)

                study.assays[0].samples.append(material_in)
                study.assays[0].materials['other_material'].append(material_in)
                try:
                    material_separation_process
                except NameError:
                    material_separation_process = None
                if material_separation_process is None:
                    material_separation_process = Process(executes_protocol="")
                else:
                 # plink(protein_extraction_process, data_acq_process)
                 plink(material_separation_process, protein_extraction_process)

            if 'polar' in sample_json['type']:

                material_in = Material(name=sample_json['parentID'])
                material_type = Characteristic(
                    category=OntologyAnnotation(
                        term='material_type', term_source=obi),
                    value=OntologyAnnotation(term=sample_json['type'],
                                             term_source=obi))
                material_in.characteristics.append(material_type)
                study.assays[0].materials['other_material'].append(material_in)

                data_acq_process = Process(
                    executes_protocol=study.get_prot(
                        sample_json['protocol.id']))
                data_acq_process.name = sample_json['id']
                datafile = DataFile(
                    filename='{filename}.txt'.format(
                        filename='_'.join(['mass_isotopomer-data', studyid,
                                           sample_json['id']])),
                    label='Raw Data File')
                data_acq_process.outputs.append(datafile)
                # print(study.assays[0].technology_type.term)

                study.assays[0].data_files.append(datafile)
                try:
                    protein_extraction_process
                except NameError:
                    protein_extraction_process = None
                if protein_extraction_process is None:
                   protein_extraction_process = Process(executes_protocol="")
                else:
                 plink(protein_extraction_process, data_acq_process)

            # else:
            #     material_in = Material(name=sample_json['parentID'])
            #     material_out = Material(name=sample_json['id'])
            #     material_type = Characteristic(
            #         category=OntologyAnnotation(term="material_type"),
            #         value=OntologyAnnotation(term=sample_json['type'],
            #                                  term_source=obi,
            #                                  term_accession="http://purl.org/obo/OBI_1"))
            #     material_out.characteristics.append(material_type)
            #     process = Process(executes_protocol=sample_json['protocol.id'])
            #     process.name = sample_json['id']
            #     process.inputs.append(material_in)
            #     process.outputs.append(material_out)
            #
            #     study.assays[0].materials['other_material'].append(material_in)
            #     study.assays[0].materials['other_material'].append(material_out)

            if 'bulk_tissue' in sample_json['type']:
                bulk_process = Process(executes_protocol=study.get_prot(sample_json['protocol.id']))
                bulk_process.name = sample_json['id']

                if len([x for x in study.samples if x.name == sample_json['parentID']]) == 0:
                    material_in = Sample(name=sample_json['parentID'])
                    bulk_process.inputs.append(material_in)
                    study.assays[0].samples.append(material_in)
                else:
                    # print([x for x in study.samples if x.name == sample_json['parentID']])
                    bulk_process.inputs.append(material_in)

                    plink(sample_collection_process, bulk_process)

    data_rec_header = '\t'.join(
        ('metabolite name', 'assignment', 'signal intensity', 'retention time',
         'm/z', 'formula', 'adduct', 'isotopologue', 'sample identifier'))
    records = []
    for element in dcc_json['measurement']:
        # metabolite_name: -> compound
        # array['measurement'][element]['signal_intensity']
        record = '\t'.join((dcc_json['measurement'][element]['compound'],
                            dcc_json['measurement'][element]['assignment'],
                            dcc_json['measurement'][element]['raw_intensity'],
                            dcc_json['measurement'][element]['retention_time'],
                            dcc_json['measurement'][element]['corrected_mz'],
                            dcc_json['measurement'][element]['formula'],
                            dcc_json['measurement'][element]['adduct'],
                            dcc_json['measurement'][element]['isotopologue'],
                            dcc_json['measurement'][element]['sample.id']))
        # print(record)
        records.append(record)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        try:
            with open('{output_path}/{study_id}-maf-data-nih-dcc-json.txt'.
                    format(output_path=output_path, study_id=studyid), 'w') as fh:
                print("'writing 'maf file document' to file from 'generate_maf_file' method:...")
                fh.writelines(data_rec_header)
                fh.writelines('\n')
                for item in records:
                    fh.writelines(item)
                    fh.writelines('\n')

            print("writing 'investigation information' to file...")
            print(isatab.dumps(investigation))

            isatab.dump(investigation, output_path=output_path)
        except IOError:
            print("Error: in main() method can't open file or write data")


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description='Converting NIH DCC Fluxomics JSON to ISA-Tab.')
    parser.add_argument('-i', help='Input path to file to convert.',
                        dest='json_path', required=True)
    parser.add_argument('-o', help='Output path to write ISA-Tabs.',
                        dest='output_path', required=True)

    # args = parser.parse_args()
    # args = vars(args)
    # convert(args['json_path'], args['output_path'])
    convert(
        json_path='/Users/Philippe/Documents/git/isa-api/tests/nih-dcc-metadata4.json',
        output_path='/Users/Philippe/Documents/tmp/'
    )
