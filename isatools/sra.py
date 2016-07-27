import logging
from lxml import etree
from xml.sax.saxutils import escape
import isatools.model.v1 as model

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

sra_default_config = {
    "broker_name": "ISAcreator",
    "center_name": "OXFORD",
    "center_project_name": "OXFORD",
    "lab_name": "Oxford e-Research Centre",
    "submission_action": "ADD",
    "funding_agency": "None",
    "grant_number": "None",
    "inform_on_status_name": "None",
    "inform_on_status_email": "None",
    "inform_on_error_name:": "None",
    "inform_on_error_email": "None"
}


def _get_comment(comments, name):
    matches = [i for i in comments if i.name == name]
    if len(matches) == 1:
        return matches[0].value
    else:
        if len(matches) == 0:
            return None
        else:
            raise AttributeError("Could not resolve comment with name '{}'".format(name))


def _get_sra_contact(contacts):
    matches = [c for c in contacts if 'SRA Inform On Status' in [r.name for r in c.roles]
               or 'SRA Inform On Error' in [r.name for r in c.roles]]
    if len(matches) == 1:
        return matches[0]
    else:
        if len(matches) == 0:
            return None
        else:
            raise AttributeError("Could not resolve SRA contact")


def _get_study_type(assays):
    measurement_types = [a.measurement_type.name for a in assays]
    logger.info(measurement_types)
    if 'transcription profiling' in measurement_types:
        return 'Transcriptome Analysis'
    elif 'environmental gene survey' in measurement_types:
        return 'Metagenomics'
    elif 'DNA-protein binding site identification' in measurement_types \
            or 'transcription factor binding site identification' in measurement_types:
        return 'Gene Regulation Study'
    elif 'DNA methylation profiling' in measurement_types:
        return 'Epigenetics'
    elif 'genome sequencing' in measurement_types:
        return 'Whole Genome Sequencing'
    elif 'chromosome rearrangement' in measurement_types:
        return 'Population Genomics'
    else:
        return 'Other'


def _write_submission_xml(i, sc):
    if len(i.studies) > 1:
        raise AttributeError("Detected more than one study in investigation. For an SRA submission, only one study per "
                             "ISA submission can be handled.")
    s = i.studies[0]
    submission_xml = """
    <SUBMISSION xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.submission.xsd"
    center_name="{sra_center_name}" accession="" alias="{study_identifier}" broker_name="{sra_broker_name}"
    submission_date="{submission_date}">
      <CONTACTS>
        <CONTACT name="{contact_name}" inform_on_status="{inform_on_status_email}"
        inform_on_error="{inform_on_error_email}"/>
      </CONTACTS>
      <ACTIONS>
        <ACTION>
          <ADD schema="study" source="study.xml"/>
        </ACTION>
        <ACTION>
          <ADD schema="sample" source="sample_set.xml"/>
        </ACTION>
        <ACTION>
          <ADD schema="experiment" source="experiment_set.xml"/>
        </ACTION>
        <ACTION>
          <ADD schema="run" source="run_set.xml"/>
        </ACTION>
      </ACTIONS>
    </SUBMISSION>""".format(
        sra_center_name=sc['center_name'],
        sra_broker_name=sc['broker_name'],
        study_identifier=s.identifier,
        submission_date=s.submission_date,
        contact_name=sc['inform_on_status_name'],
        inform_on_status_email=sc['inform_on_status_email'],
        inform_on_error_email=sc['inform_on_error_email']
    )
    return submission_xml


def _write_study_xml(i, sc):
    if len(i.studies) > 1:
        raise AttributeError("Detected more than one study in investigation. For an SRA submission, only one study per "
                             "ISA submission can be handled.")
    s = i.studies[0]
    study_type = _get_study_type(s.assays)
    study_xml = """<STUDY
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.study.xsd"
    alias="{study_id}" center_name="{sra_center_name}">""".format(
        study_id=s.identifier,
        sra_center_name=sc['center_name'])
    # build STUDY DESCRIPTOR
    study_xml += """
        <DESCRIPTOR>
            <CENTER_NAME>{sra_center_name}</CENTER_NAME>
            <CENTER_PROJECT_NAME>{sra_center_project_name}</CENTER_PROJECT_NAME>
            <STUDY_TITLE>{study_title}</STUDY_TITLE>
            <STUDY_ABSTRACT>{study_description}</STUDY_ABSTRACT>
            <STUDY_DESCRIPTION>{study_description}</STUDY_DESCRIPTION>
            <STUDY_TYPE existing_study_type="{study_type}"/>
        </DESCRIPTOR>
    """.format(sra_center_name=sc['center_name'],
               sra_center_project_name=sc['center_project_name'],
               study_title=s.title,
               study_abstract=escape(s.description),
               study_description=escape(s.description),
               study_type=study_type)
    # build STUDY LINKS (to publications)
    link_xml = """<STUDY_LINKS>"""
    for publication in s.publications:
        if publication.pubmed_id is not None and publication.pubmed_id != '':
            link_xml += """
                <STUDY_LINK>
                    <ENTREZ_LINK>
                        <DB>pubmed</DB>
                        <ID>{pubmed_id}</ID>
                    </ENTREZ_LINK>
                </STUDY_LINK>
            """.format(pubmed_id=publication.pubmed_id)
        if publication.doi is not None and publication.doi != '':
            link_xml += """
                <STUDY_LINK>
                    <URL_LINK>
                        <LABEL>Study Publication DOI</LABEL>
                        <URL>{doi}</URL>
                    </URL_LINK>
                </STUDY_LINK>
            """.format(doi=publication.doi)
    link_xml += """</STUDY_LINKS>"""
    study_xml += link_xml
    # build STUDY ATTRIBUTES
    attr_xml = """<STUDY_ATTRIBUTES>"""
    if s.submission_date is not None and s.submission_date != '':
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>Submission Date</TAG>
            <VALUE>{submission_date}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(submission_date=s.submission_date)
    if s.public_release_date is not None and s.public_release_date != '':
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>Release Date</TAG>
            <VALUE>{public_release_date}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(public_release_date=s.public_release_date)
    if s.identifier is not None and s.identifier != '':
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>BII Study Accession</TAG>
            <VALUE>{study_id}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(study_id=s.identifier)
    if i.identifier is not None and i.identifier != '':
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>BII Investigation Accession</TAG>
            <VALUE>{inv_id}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(inv_id=i.identifier)
    for contact in s.contacts:
        contact_txt = """"""
        if contact.first_name is not None and contact.first_name != '' and contact.last_name is not None and contact.last_name != '':
            contact_txt += "Name: {first} {last}\n".format(first=contact.first_name, last=contact.last_name)
        if contact.email is not None and contact.email != '':
            contact_txt += "e-mail: {email}\n".format(email=contact.email)
        if contact.affiliation is not None and contact.affiliation != '':
            contact_txt += "Affiliation: {affiliation}\n".format(affiliation=contact.affiliation)
        if contact.address is not None and contact.address != '':
            contact_txt += "Address: {address}\n".format(address=contact.address)
        for role in contact.roles:
            contact_txt += "Role: {role}\n".format(role=role.name)
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>Study Contact</TAG>
            <VALUE>{contact_info}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(contact_info=contact_txt[:len(contact_txt)-1])  # drop trailing line break
    for publication in s.publications:
        pub_txt = """"""
        if publication.title is not None and publication.title != '':
            pub_txt += "Title: {title}\n".format(title=publication.title.strip())
        if publication.author_list is not None and publication.author_list != '':
            pub_txt += "Authors: {author_list}\n".format(author_list=publication.author_list.strip())
        if publication.status is not None and publication.status != '':
            pub_txt += "Status: {status}\n".format(status=publication.status.name.strip())
        if publication.pubmed_id is not None and publication.pubmed_id != '':
            pub_txt += "PUBMED ID: {pubmed_id}\n".format(pubmed_id=publication.pubmed_id.strip())
        if publication.doi is not None and publication.doi != '':
            pub_txt += "DOI: {doi}\n".format(doi=publication.doi.strip())
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>Study Publication</TAG>
            <VALUE>{pub_txt}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(pub_txt=pub_txt[:len(pub_txt)-1])  # drop trailing line break
    attr_xml += """</STUDY_ATTRIBUTES>"""
    study_xml += attr_xml
    study_xml += """</STUDY>"""
    return study_xml


def _get_characteristic(m, cname):
    matches = [c for c in m.characteristics if c.category.name == cname]
    if len(matches) == 1:
        return matches[0]
    else:
        raise AttributeError("Could not resolve characteristic with name '{}'".format(cname))


def _write_sample_set_xml(i, sc):
    sample_set_xml = """
    <SAMPLE_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.sample.xsd">
    """
    for s in i.studies:
        for src in s.materials['sources']:
            characteristic_organism = _get_characteristic(src, 'organism')
            organism_ncbi_taxon_id = characteristic_organism.value.term_accession[len("http://purl.obolibrary.org/obo/NCBITaxon_"):]
            # write sample header and name
            sample_set_xml += """
            <SAMPLE center_name="{center_name}" broker_name="{broker_name}" alias="{study_id}:source:{source_id}">
                <TITLE>{study_id}:source:{source_id}</TITLE>
                <SAMPLE_NAME>
                    <TAXON_ID>{organism_ncbi_taxon_id}</TAXON_ID>
                    <SCIENTIFIC_NAME>{organism}</SCIENTIFIC_NAME>
                </SAMPLE_NAME>
            """.format(center_name=sc['center_name'],
                       broker_name=sc['broker_name'],
                       study_id=s.identifier,
                       source_id=src.name,
                       organism=characteristic_organism.value.name,
                       organism_ncbi_taxon_id=organism_ncbi_taxon_id)
            # write sample attributes if there is more than just organism
            if len(src.characteristics) > 1:
                sample_set_xml += """<SAMPLE_ATTRIBUTES>"""
                for characteristic in src.characteristics:
                    if characteristic.category.name == 'organism':
                        pass
                    else:
                        if isinstance(characteristic.value, model.OntologyAnnotation):
                            if isinstance(characteristic.value.name, str):
                                cvalue = characteristic.value.name.strip()
                            else:
                                cvalue = characteristic.value.name
                        elif isinstance(characteristic.value, str):
                            cvalue = characteristic.value.strip()
                        else:
                            cvalue = characteristic.value
                        sample_set_xml += """
                        <SAMPLE_ATTRIBUTE>
                            <TAG>{cname}</TAG>
                            <VALUE>{cvalue}</VALUE>
                        """.format(cname=characteristic.category.name,
                                   cvalue=cvalue)
                        if isinstance(cvalue, float) or isinstance(cvalue, int):
                            if characteristic.unit is not None:
                                sample_set_xml += """<UNITS>{unit}</UNITS>""".format(unit=characteristic.unit.name)
                        sample_set_xml += """</SAMPLE_ATTRIBUTE>"""
                sample_set_xml += """</SAMPLE_ATTRIBUTES>"""
            sample_set_xml += """</SAMPLE>"""
    sample_set_xml += """</SAMPLE_SET>"""
    return sample_set_xml


def _get_parameter_value(p, pvname):
    matches = [pv for pv in p.parameter_values if pv.category.parameter_name.name == pvname]
    if len(matches) == 1:
        if isinstance(matches[0].value, model.OntologyAnnotation):
            return matches[0].value.name
        else:
            return matches[0].value
    else:
        raise AttributeError("Could not resolve parameter value with name '{}'".format(pvname))


def _write_experiment_set_xml(i, sc):
    exp_set_xml = """
    <EXPERIMENT_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.experiment.xsd">
    """
    for s in i.studies:
        for a in s.assays:
            seq_processes = [p for p in a.process_sequence if p.executes_protocol.protocol_type.name == 'nucleic acid sequencing']
            for seq_process in seq_processes:
                assay_name = seq_process.additional_properties['Assay Name']
                filename_no_ext = a.filename[:-4]
                study_id = s.identifier
                technology_platform = a.technology_platform

                lib_construction_process = seq_process.prev_process
                lib_strategy = _get_parameter_value(lib_construction_process, 'library strategy')
                lib_source = _get_parameter_value(lib_construction_process, 'library source')
                lib_selection = _get_parameter_value(lib_construction_process, 'library selection')
                lib_layout = _get_parameter_value(lib_construction_process, 'library layout').upper()
                target_gene = _get_parameter_value(lib_construction_process, 'target_gene')
                protocol_description = lib_construction_process.executes_protocol.description
                target_taxon = _get_parameter_value(lib_construction_process, 'target_taxon')
                target_subfragment = _get_parameter_value(lib_construction_process, 'target_subfragment')
                pcr_primers = _get_parameter_value(lib_construction_process, 'pcr_primers')
                pcr_cond = _get_parameter_value(lib_construction_process, 'pcr_cond')
                mid = _get_parameter_value(lib_construction_process, 'mid')
                source_name = seq_process.prev_process.prev_process.prev_process.inputs[0].name  # assume one input sample to the process sequence
                exp_set_xml += """
                <EXPERIMENT alias="{study_identifier}:generic_assay:{filename_no_ext}.{assay_name}" center_name="{center_name}" broker_name="{broker_name}">
                    <TITLE>Sequencing library derived from sample {assay_name}</TITLE>
                    <STUDY_REF refname="{study_identifier}"/>
                    <DESIGN>
                      <DESIGN_DESCRIPTION>See study and sample descriptions for details</DESIGN_DESCRIPTION>
                      <SAMPLE_DESCRIPTOR refname="{study_identifier}:source:{source_name}"/>
                      <LIBRARY_DESCRIPTOR>
                        <LIBRARY_NAME>{study_identifier}:assay:{assay_name}.{target_taxon}</LIBRARY_NAME>
                        <LIBRARY_STRATEGY>{lib_strategy}</LIBRARY_STRATEGY>
                        <LIBRARY_SOURCE>{lib_source}</LIBRARY_SOURCE>
                        <LIBRARY_SELECTION>{lib_selection}</LIBRARY_SELECTION>
                        <LIBRARY_LAYOUT>
                          <{lib_layout}/>
                        </LIBRARY_LAYOUT>
                        <TARGETED_LOCI>
                          <LOCUS locus_name="{target_gene}"/>
                        </TARGETED_LOCI>
                        <POOLING_STRATEGY/>
                        <LIBRARY_CONSTRUCTION_PROTOCOL>protocol_description: {protocol_description}
 target_taxon: {target_taxon}
 target_gene: {target_gene}
 target_subfragment: {target_subfragment}
 pcr_primers: {pcr_primers}
 pcr_cond: {pcr_cond}
 mid: {mid}</LIBRARY_CONSTRUCTION_PROTOCOL>
                      </LIBRARY_DESCRIPTOR>
                      <SPOT_DESCRIPTOR>
                        <SPOT_DECODE_SPEC>
                          <READ_SPEC>
                            <READ_INDEX>0</READ_INDEX>
                            <READ_CLASS>Technical Read</READ_CLASS>
                            <READ_TYPE>Adapter</READ_TYPE>
                            <BASE_COORD>1</BASE_COORD>
                          </READ_SPEC>
                          <READ_SPEC>
                            <READ_INDEX>1</READ_INDEX>
                            <READ_CLASS>Technical Read</READ_CLASS>
                            <READ_TYPE>BarCode</READ_TYPE>
                            <EXPECTED_BASECALL_TABLE>
                              <BASECALL min_match="9" max_mismatch="0" match_edge="full" read_group_tag="{mid}">{mid}</BASECALL>
                            </EXPECTED_BASECALL_TABLE>
                          </READ_SPEC>
                          <READ_SPEC>
                            <READ_INDEX>2</READ_INDEX>
                            <READ_CLASS>Application Read</READ_CLASS>
                            <READ_TYPE>Forward</READ_TYPE>
                            <RELATIVE_ORDER follows_read_index="1"/>
                          </READ_SPEC>
                        </SPOT_DECODE_SPEC>
                      </SPOT_DESCRIPTOR>
                    </DESIGN>
                    <PLATFORM>
                      <LS454>
                        <INSTRUMENT_MODEL>{technology_platform}</INSTRUMENT_MODEL>
                      </LS454>
                    </PLATFORM>
                  </EXPERIMENT>
                """.format(assay_name=assay_name,
                           filename_no_ext=filename_no_ext,
                           study_identifier=study_id,
                           technology_platform=technology_platform,
                           lib_strategy=lib_strategy,
                           lib_source=lib_source,
                           lib_selection=lib_selection,
                           lib_layout=lib_layout,
                           target_gene=target_gene,
                           protocol_description=protocol_description,
                           target_taxon=target_taxon,
                           target_subfragment=target_subfragment,
                           pcr_primers=pcr_primers,
                           pcr_cond=pcr_cond,
                           mid=mid,
                           center_name=sc['center_name'],
                           broker_name=sc['broker_name'],
                           source_name=source_name
                           )
    exp_set_xml += """</EXPERIMENT_SET>"""
    return exp_set_xml


def _get_output_filename(process):
    output_files = process.outputs
    if len(output_files) == 1:
        return output_files[0].filename
    else:
        raise AttributeError("Could not resolve output file - zero or > 1 files found")


def _write_run_set_xml(i, sc):
    run_set_xml = """
    <RUN_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.run.xsd">
    """
    for s in i.studies:
        for a in s.assays:
            seq_processes = [p for p in a.process_sequence if p.executes_protocol.protocol_type.name == 'nucleic acid sequencing']
            for seq_process in seq_processes:
                assay_name = seq_process.additional_properties['Assay Name']
                filename_no_ext = a.filename[:-4]
                study_id = s.identifier
                output_filename = _get_output_filename(seq_process)
                run_set_xml += """
                <RUN alias="{study_id}:assay:{assay_name}" center_name="{center_name}" broker_name="{broker_name}">
                    <EXPERIMENT_REF refname="{study_id}:generic_assay:{filename_no_ext}.{assay_name}"/>
                        <DATA_BLOCK>
                            <FILES>
                                <FILE filetype="{output_file_ext}" filename="{output_filename}" checksum_method="MD5" checksum="0000000000000000000000000"/>
                            </FILES>
                        </DATA_BLOCK>
                </RUN>
                """.format(study_id=study_id,
                           assay_name=assay_name,
                           filename_no_ext=filename_no_ext,
                           center_name=sc['center_name'],
                           broker_name=sc['broker_name'],
                           output_filename=output_filename,
                           output_file_ext=output_filename[-4:]
                           )
    run_set_xml += """</RUN_SET>"""
    return run_set_xml


def dump(isa_obj, sra_config=sra_default_config, output_path=None):
    """
        >>> from isatools import sra, isajson
        >>> i = isajson.load(open('.../BII-S-7.json'))
        >>> sra.dump(i, None)
    """
    logger.info("Using config: {}".format(sra_config))
    submission_xml = _write_submission_xml(isa_obj, sra_config)
    logger.info(submission_xml)
    etree.fromstring(submission_xml)

    study_xml = _write_study_xml(isa_obj, sra_config)
    logger.info(study_xml)
    etree.fromstring(study_xml)  # checks if validates against XSD
