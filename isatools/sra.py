import logging
from lxml import etree
from xml.sax.saxutils import escape

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


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


def _write_submission_xml(s):
    sra_center_name = _get_comment(s.comments, 'SRA Center Name')
    sra_broker_name = _get_comment(s.comments, 'SRA Broker Name')
    sra_contact = _get_sra_contact(s.contacts)
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
        sra_center_name=sra_center_name,
        sra_broker_name=sra_broker_name,
        study_identifier=s.identifier,
        submission_date=s.submission_date,
        contact_name=sra_contact.first_name + ' ' + sra_contact.last_name,
        inform_on_status_email=sra_contact.email,
        inform_on_error_email=sra_contact.email
    )
    return submission_xml


def _write_study_xml(s):
    sra_center_name = _get_comment(s.comments, 'SRA Center Name')
    sra_center_project_name = _get_comment(s.comments, 'SRA Center Project Name')
    study_type = _get_study_type(s.assays)
    study_xml = """<STUDY
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.study.xsd"
    alias="{study_id}" center_name="{sra_center_name}">""".format(
        study_id=s.identifier,
        sra_center_name=sra_center_name)
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
    """.format(sra_center_name=sra_center_name,
               sra_center_project_name=sra_center_project_name,
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
    if s.submission_date is not None:
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>Submission Date</TAG>
            <VALUE>{submission_date}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(submission_date=s.submission_date)
    if s.public_release_date is not None:
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>Release Date</TAG>
            <VALUE>{public_release_date}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(public_release_date=s.public_release_date)
    for contact in s.contacts:
        contact_info = """
Name: {contact_name}
e-mail: {contact_email}
Affiliation: {contact_affiliation}
Address: {contact_address}
        """.format(contact_name=contact.first_name + ' ' + contact.last_name,
                   contact_email=contact.email,
                   contact_affiliation=contact.affiliation,
                   contact_address=contact.address)
        for role in contact.roles:
            contact_info += """Role: {role}""".format(role=role.name)
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>Study Contact</TAG>
            <VALUE>{contact_info}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(contact_info=contact_info)
    for publication in s.publications:
        attr_xml += """
        <STUDY_ATTRIBUTE>
            <TAG>Study Publication</TAG>
            <VALUE>
Title: {title}
Authors: {author_list}
Status: {status}
PUBMED ID: {pubmed_id}
DOI: {doi}</VALUE>
        </STUDY_ATTRIBUTE>
        """.format(
            title=publication.title,
            author_list=publication.author_list,
            status=publication.status.name,
            pubmed_id=publication.pubmed_id,
            doi=publication.doi
        )
    attr_xml += """</STUDY_ATTRIBUTES>"""
    study_xml += attr_xml
    study_xml += """</STUDY>"""
    return study_xml


def _write_run_set_xml():
    run_set_xml = """
    <RUN_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.run.xsd">"""


def _write_experiment_set_xml():
    pass


def _write_sample_set_xml():
    pass


def dump(isa_obj, output_path):
    """
        >>> from isatools import sra, isajson
        >>> i = isajson.load(open('.../BII-S-7.json'))
        >>> sra.dump(i, None)
    """
    for study in isa_obj.studies:

        submission_xml = _write_submission_xml(study)
        logger.info(submission_xml)
        etree.fromstring(submission_xml)

        study_xml = _write_study_xml(study)
        logger.info(study_xml)
        etree.fromstring(study_xml)  # checks if validates against XSD
