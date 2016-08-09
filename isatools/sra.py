import logging
import iso8601
import jinja2
from isatools.model.v1 import Sample, OntologyAnnotation, DataFile

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

supported_sra_assays = [
    ('genome sequencing', 'nucleotide sequencing'),
    ('environmental gene survey', 'nucleotide sequencing')
]

sra_center_name = 'OXFORD'
sra_broker_name = 'ISAcreator'
sra_lab_name = sra_center_name
sra_submission_action = 'ADD'
sra_center_prj_name = None


def export(investigation, export_path):

    def get_comment(assay, name):
        hits = [c for c in assay.comments if c.name.lower() == name.lower()]
        if len(hits) > 1:
            raise AttributeError("Multiple comments of label '{}' found".format(name))
        elif len(hits) < 1:
            return None
        else:
            return hits[0]

    def get_sample(process):
        materials = process.inputs
        sample = None
        for material in materials:
            if isinstance(material, Sample):
                sample = material
                break
        return sample

    def get_pv(process, name):
        hits = [pv for pv in process.parameter_values if
                pv.category.parameter_name.name.lower().replace('_', ' ') == name.lower().replace('_', ' ')]
        if len(hits) > 1:
            raise AttributeError("Multiple parameter values of category '{}' found".format(name))
        elif len(hits) < 1:
            return None
        else:
            if isinstance(hits[0].value, OntologyAnnotation):
                value = hits[0].value.name
            else:
                value = hits[0].value
            return value.replace('_', ' ')

    logger.info("isatools.sra.export()")
    for istudy in investigation.studies:
        is_sra = False
        for iassay in istudy.assays:
            if (iassay.measurement_type.name, iassay.technology_type.name) in supported_sra_assays:
                is_sra = True
                break
        if not is_sra:
            logger.info("No SRA assay found, skipping processing")
            continue

        study_acc = istudy.identifier
        logger.debug("sra exporter, working on " + study_acc)

        # Flag SRA contacts for template
        has_sra_contact = False
        for contact in istudy.contacts:
            if "sra inform on status" in [r.name.lower() for r in contact.roles]:
                contact.inform_on_status = True
                has_sra_contact = True
            if "sra inform on error" in [r.name.lower() for r in contact.roles]:
                contact.inform_on_error = True
                has_sra_contact = True
        if not has_sra_contact:
            raise ValueError(
                "The study ''{0}'' has either no SRA contact or no email specified for the contact. Please "
                "ensure you have one contact with a 'Role' as 'SRA Inform On Status', otherwise we cannot "
                "export to SRA.".format(istudy.identifier))

        submission_date = iso8601.parse_date(istudy.submission_date, iso8601.UTC)
        import os
        env = jinja2.Environment()
        env.loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'resources', 'sra_templates'))
        xsub_template = env.get_template('submission_add.xml')
        xsub = xsub_template.render(accession=study_acc, contacts=istudy.contacts, submission_date=submission_date,
                                    sra_center_name=sra_center_name, sra_broker_name=sra_broker_name)
        xproj_template = env.get_template('project_set.xml')
        xproj = xproj_template.render(study=istudy, sra_center_name=sra_center_name)

        assays_to_export = list()
        for iassay in istudy.assays:
            if (iassay.measurement_type.name, iassay.technology_type.name) in supported_sra_assays:
                assay_seq_processes = [a for a in iassay.process_sequence if a.executes_protocol.protocol_type.name ==
                                       'nucleic acid sequencing']
                for assay_seq_process in assay_seq_processes:
                    do_export = True
                    if get_comment(assay_seq_process, 'export') is not None:
                        logger.debug("HAS EXPORT COMMENT IN ASSAY")
                        export = get_comment(assay_seq_process, 'export').value
                        logger.debug("export is " + export)
                        do_export = export.lower() != 'no'
                    else:
                        logger.debug("NO EXPORT COMMENT FOUND")
                    logger.debug("Perform export? " + str(do_export))
                    if do_export:
                        sample = None
                        curr_process = assay_seq_process
                        while sample is None:
                            sample = get_sample(curr_process)
                            curr_process = curr_process.prev_process
                        for charac in sample.characteristics:
                            if isinstance(charac.value, OntologyAnnotation):
                                charac.value = charac.value.name
                        assay_to_export = \
                            {
                                "sample": sample,
                                "sample_alias": study_acc + ':sample:' + sample.name,
                                "run_alias": study_acc + ':assay:' + assay_seq_process.name,
                                "exp_alias": study_acc + ':generic_assay:' + iassay.filename[:-4] + ':' + assay_seq_process.name
                            }
                        datafiles = [d for d in assay_seq_process.outputs if isinstance(d, DataFile)]
                        assay_to_export['data_file'] = {
                            "filename": datafiles[0].filename,
                            "filetype": datafiles[0].filename[-3:]
                        }
                        source = None
                        matching_sources = [p.inputs for p in istudy.process_sequence if sample in p.outputs]
                        if len(matching_sources[0]) == 1:
                            source = matching_sources[0][0]
                        assay_to_export['source'] = {
                            "characteristics": source.characteristics,
                        }
                        organism_taxon_id = [c.value.term_accession for c in source.characteristics if c.category.name == 'organism']
                        for charac in source.characteristics:
                            if isinstance(charac.value, OntologyAnnotation):
                                charac.value = charac.value.name
                        orgnism_name = [c.value for c in source.characteristics if c.category.name == 'organism']
                        assay_to_export['source']['taxon_id'] = organism_taxon_id[-1][-6:]
                        assay_to_export['source']['scientific_name'] = orgnism_name[-1]
                        curr_process = assay_seq_process
                        while curr_process.prev_process is not None:
                            assay_to_export[curr_process.executes_protocol.protocol_type.name] = curr_process
                            try:
                                curr_process = curr_process.prev_process
                            except AttributeError:
                                pass
                        target_taxon = get_pv(assay_to_export['library construction'], 'target_taxon')
                        assay_to_export['target_taxon'] = target_taxon
                        assay_to_export['targeted_loci'] = False
                        # BEGIN genome seq library selection
                        if iassay.measurement_type.name in ['genome sequencing', 'whole genome sequencing']:
                            library_source = get_pv(assay_to_export['library construction'],
                                                      'library source')
                            if library_source.upper() not in ['GENOMIC', 'GENOMIC SINGLE CELL', 'METAGENOMIC', 'OTHER']:
                                logger.warn("ERROR:value supplied is not compatible with SRA1.5 schema " + library_source)
                                library_source = 'OTHER'

                            library_strategy = get_pv(assay_to_export['library construction'],
                                                      'library strategy').value.name
                            if library_strategy.upper() not in ['WGS', 'OTHER']:
                                logger.warn("ERROR:value supplied is not compatible with SRA1.5 schema " + library_strategy)
                                library_strategy = 'OTHER'

                            library_selection = get_pv(assay_to_export['library construction'],
                                                       'library selection').value.name
                            if library_selection not in ['RANDOM', 'UNSPECIFIED']:
                                logger.warn("ERROR:value supplied is not compatible with SRA1.5 schema " + library_selection)
                                library_selection = 'UNSPECIFIED'

                            protocol = "\n protocol_description: " \
                                       + assay_to_export['library construction'].executes_protocol.description
                            mid_pv = get_pv(assay_to_export['library construction'], 'mid')
                            if mid_pv is not None:
                                protocol += "\n mid: " + mid_pv.value

                            assay_to_export['library_source'] = library_source
                            assay_to_export['library_strategy'] = library_strategy
                            assay_to_export['library_selection'] = library_selection
                            assay_to_export['library_construction_protocol'] = protocol

                            library_layout = get_pv(assay_to_export['library construction'], 'library layout').value
                            assay_to_export['library_layout'] = library_layout

                            assays_to_export.append(assay_to_export)
                        # END genome seq library selection
                        # BEGIN environmental gene survey library selection
                        elif iassay.measurement_type.name in ['environmental gene survey']:
                            assay_to_export['library_source'] = 'METAGENOMIC'
                            assay_to_export['library_strategy'] = 'AMPLICON'
                            assay_to_export['library_selection'] = 'PCR'
                            library_layout = get_pv(assay_to_export['library construction'], 'library layout')
                            assay_to_export['library_layout'] = library_layout

                            nucl_acid_amp = get_pv(assay_to_export['library construction'], 'nucleic acid amplification')
                            if nucl_acid_amp is None:
                                nucl_acid_amp = get_pv(assay_to_export['library construction'], 'nucl_acid_amp')

                            protocol = "\n protocol_description: " \
                                       + assay_to_export['library construction'].executes_protocol.description
                            if nucl_acid_amp is not None:
                                protocol += "\n nucl_acid_amp: " + nucl_acid_amp.value
                            url = get_pv(assay_to_export['library construction'], 'url')
                            if url is not None:
                                protocol += "\n url: " + nucl_acid_amp.value
                            target_taxon = assay_to_export['target_taxon']
                            if target_taxon is not None:
                                protocol += "\n target_taxon: " + target_taxon
                            target_gene = get_pv(assay_to_export['library construction'], 'target_gene')
                            if target_gene is not None:
                                protocol += "\n target_gene: " + target_gene
                            target_subfragment = get_pv(assay_to_export['library construction'], 'target_subfragment')
                            if target_subfragment is not None:
                                protocol += "\n target_subfragment: " + target_subfragment
                            pcr_primers = get_pv(assay_to_export['library construction'], 'pcr_primers')
                            if pcr_primers is not None:
                                protocol += "\n pcr_primers: " + pcr_primers
                            pcr_cond = get_pv(assay_to_export['library construction'], 'pcr_cond')
                            if pcr_cond is not None:
                                protocol += "\n pcr_cond: " + pcr_cond
                            assay_to_export['library_construction_protocol'] = protocol

                            if target_gene is not None:
                                assay_to_export['targeted_loci'] = True
                                assay_to_export['locus_name'] = target_gene

                            assay_to_export['platform'] = iassay.technology_platform

                        # END environmental gene survey library selection
                        else:
                            logger.error("ERROR:Unsupported measurement type: " + iassay.measurement_type.name)
                        assays_to_export.append(assay_to_export)

        xexp_set_template = env.get_template('experiment_set.xml')
        xexp_set = xexp_set_template.render(assays_to_export=assays_to_export, study=istudy,
                                            sra_center_name=sra_center_name, sra_broker_name=sra_broker_name)
        xrun_set_template = env.get_template('run_set.xml')
        xrun_set = xrun_set_template.render(assays_to_export=assays_to_export, study=istudy,
                                            sra_center_name=sra_center_name, sra_broker_name=sra_broker_name)

        xsample_set_template = env.get_template('sample_set.xml')
        xsample_set = xsample_set_template.render(assays_to_export=assays_to_export, study=istudy,
                                            sra_center_name=sra_center_name, sra_broker_name=sra_broker_name)
        logger.debug("SRA exporter: writing SRA XML files for study " + study_acc)
        # TODO Check outputs against xsds
        # TODO Write outputs to files
        print(xsub)
        print(xproj)
        print(xexp_set)
        print(xrun_set)
        print(xsample_set)
