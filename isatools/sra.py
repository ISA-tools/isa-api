from ena.sra import submission, run, experiment, sample, study
import logging
import pyxb
import pyxb.binding.datatypes as xs
import iso8601

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def build_exported_assay_sample(assay):
    pass


def build_exported_assay(assay, xrun_set, xexperiment_set, xsample_set):

    def get_comment(assay, name):
        hits = [c for c in assay.comment if c.name.lower() == name.lower()]
        if len(hits) > 1:
            raise AttributeError("Multiple comments of label '{}' found".format(name))
        elif len(hits) < 1:
            return None
        else:
            return hits[0]

    assay_acc = assay.identifier
    do_export = True
    if get_comment(assay, 'export') is not None:
        logger.info("HAS EXPORT COMMENT IN ASSAY");
        export = get_comment(assay, 'export')
        logger.info("export is " + export)
        do_export = export.lower() != 'no'
    else:
        logger.info("NO EXPORT COMMENT FOUND")
    logger.info("Perform export? " + str(do_export))


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
    logger.info("isatools.sra.export()")
    for istudy in investigation.studies:
        is_sra = False
        for assay in istudy.assays:
            if (assay.measurement_type.name, assay.technology_type.name) in supported_sra_assays:
                is_sra = True
                break
        if not is_sra:
            logger.info("No SRA assay found, skipping processing")
            continue
        study_acc = istudy.identifier
        logger.info("sra exporter, working on " + study_acc)
        # Prepare the sumbission
        xsubmission = submission.SUBMISSION()
        xsubmission.center_name = sra_center_name
        xsubmission.accession = ''
        xsubmission.alias = study_acc
        xsubmission.broker_name = sra_broker_name
        xsubmission.lab_name = sra_lab_name
        xsubmission.submission_date = xs.date(iso8601.parse_date(istudy.submission_date, iso8601.UTC))
        build_exported_submission_contacts(xsubmission, istudy)
        build_study_actions(xsubmission, istudy)

        run_set = run.RUN_SET()
        exp_set = experiment.EXPERIMENT_SET()
        sample_set = sample.SAMPLE_SET()

        xstudy_doc = None
        is_assay_ok = True
        for assay in istudy.assays:
            if (assay.measurement_type.name, assay.technology_type.name) in supported_sra_assays:
                xstudy_doc = build_exported_study(istudy)
                logger.info("SraExporter, Working on assay " + assay.filename)
                print(xstudy_doc.toxml())
                # if !build_exported_assay(assay, run_set, exp_set, sample_set):
                #     is_assay_ok = False
                #     # Skip all the assay file if only a single assay is wrong, a partial export is too dangerous
                #     break



def build_exported_submission_contacts(xsub, study):
    xsub.CONTACTS = pyxb.BIND()
    for contact in study.contacts:
        full_name = "{} {}".format(contact.first_name, contact.last_name)
        is_sra_contact = False
        if "sra inform on status" in [r.name.lower() for r in contact.roles]:
            inform_on_status = contact.email
            is_sra_contact = True
        if "sra inform on status" in [r.name.lower() for r in contact.roles]:
            inform_on_error = contact.email
            is_sra_contact = True
        if is_sra_contact:
            xsub.CONTACTS.CONTACT.append(pyxb.BIND())
            xsub.CONTACTS.CONTACT[-1].name = full_name
            xsub.CONTACTS.CONTACT[-1].inform_on_status = inform_on_status
            xsub.CONTACTS.CONTACT[-1].inform_on_error = inform_on_error
    if len(xsub.CONTACTS.CONTACT) == 0:
        raise ValueError("The study ''{0}'' has either no SRA contact or no email specified for the contact. Please "
                         "ensure you have one contact with a 'Role' as 'SRA Inform On Status', otherwise we cannot "
                         "export to SRA.".format(study.identifier))


def build_study_actions(xsub, study):
    xsub.ACTIONS = pyxb.BIND()
    schemas = ['study', 'sample', 'experiment', 'run']
    sources = ['study', 'sample_set', 'experiment_set', 'run_set']
    if 'add' == sra_submission_action.lower():
        for i, schemas in enumerate(schemas):
            xsub.ACTIONS.ACTION.append(pyxb.BIND())
            xsub.ACTIONS.ACTION[i].ADD = pyxb.BIND()
            xsub.ACTIONS.ACTION[i].ADD.schema = schemas
            xsub.ACTIONS.ACTION[i].ADD.source = sources[i] + '.xml'

    if 'modify' == sra_submission_action.lower():
        for i, schemas in enumerate(schemas):
            xsub.ACTIONS.ACTION.append(pyxb.BIND())
            xsub.ACTIONS.ACTION[i].MODIFY = pyxb.BIND()
            xsub.ACTIONS.ACTION[i].MODIFY.schema = schemas
            xsub.ACTIONS.ACTION[i].MODIFY.source = sources[i] + '.xml'

    if 'validate' == sra_submission_action.lower():
        for i, schemas in enumerate(schemas):
            xsub.ACTIONS.ACTION.append(pyxb.BIND())
            xsub.ACTIONS.ACTION[i].VALIDATE = pyxb.BIND()
            xsub.ACTIONS.ACTION[i].VALIDATE.schema = schemas
            xsub.ACTIONS.ACTION[i].VALIDATE.source = sources[i] + '.xml'

    if 'suppress' == sra_submission_action.lower():
        xsub.ACTIONS.ACTION.append(pyxb.BIND())
        xsub.ACTIONS.ACTION[i].SUPPRESS = pyxb.BIND()
        xsub.ACTIONS.ACTION[i].SUPPRESS.target = study.identifier

    if len(xsub.ACTIONS.ACTION) == 0:
        raise ValueError("The study ''{0}'' has no SRA Submission Action, cannot export to SRA"
                         .format(study.identifier))


def build_exported_study(istudy):

    study_acc = istudy.identifier

    xstudy = study.STUDY_SET()
    xstudy.STUDY.append(pyxb.BIND())
    xstudy.STUDY[0].accession = study_acc
    xstudy.STUDY[0].DESCRIPTOR = pyxb.BIND()
    xstudy.STUDY[0].DESCRIPTOR.center_name = sra_center_name
    xstudy.STUDY[0].center_name = sra_center_name

    if sra_broker_name != '':
        xstudy.STUDY[0].broker_name = sra_broker_name

    if sra_center_prj_name is not None:
        xstudy.STUDY[0].DESCRIPTOR.CENTER_PROJECT_NAME = pyxb.BIND(sra_center_prj_name)

    if istudy.title is not None:
        xstudy.STUDY[0].DESCRIPTOR.STUDY_TITLE = pyxb.BIND(istudy.title)
    else:
        raise ValueError("The study ''{0}'' has no 'Study Title', cannot export to SRA format"
                         .format(istudy.identifier))

    if istudy.description is not None:
        xstudy.STUDY[0].DESCRIPTOR.STUDY_ABSTRACT = pyxb.BIND(istudy.description)

    xstudy.STUDY[0].STUDY_ATTRIBUTES = pyxb.BIND()
    xstudy.STUDY[0].STUDY_LINKS = pyxb.BIND()

    sub_date = istudy.submission_date
    if sub_date is not None:
        xstudy.STUDY[0].STUDY_ATTRIBUTES.STUDY_ATTRIBUTE.append(pyxb.BIND("Submission Date", istudy.submission_date))

    rel_date = istudy.public_release_date
    if rel_date is not None:
        xstudy.STUDY[0].STUDY_ATTRIBUTES.STUDY_ATTRIBUTE.append(pyxb.BIND("Release Date", rel_date))

    if rel_date is not None:
        xstudy.STUDY[0].STUDY_ATTRIBUTES.STUDY_ATTRIBUTE.append(pyxb.BIND("Release Date", rel_date))

    if istudy.identifier is not None:
        xstudy.STUDY[0].STUDY_ATTRIBUTES.STUDY_ATTRIBUTE.append(pyxb.BIND("Local Study Accession", istudy.identifier))

    if istudy.description is not None:
        xstudy.STUDY[0].DESCRIPTOR.STUDY_DESCRIPTION = pyxb.BIND(istudy.description)

    # Study type should be ignored. This field is contained in the legacy ERP study. SUB#921766
    xstudy.STUDY[0].DESCRIPTOR.STUDY_TYPE = pyxb.BIND(existing_study_type="Other")

    for contact in istudy.contacts:
        build_exported_contact(contact, xstudy.STUDY[0].STUDY_ATTRIBUTES.STUDY_ATTRIBUTE, False)

    for publication in istudy.publications:
        build_exported_publication(publication, xstudy.STUDY[0].STUDY_ATTRIBUTES.STUDY_ATTRIBUTE,
                                   xstudy.STUDY[0].STUDY_LINKS.STUDY_LINK, False)

    return xstudy


def build_exported_contact(icontact, xattrs, is_investigation):
    if is_investigation:
        prefix_label = 'Investigation '
    else:
        prefix_label = 'Study '

    contact_value_str = ""

    # get full name
    name = icontact.first_name
    if icontact.mid_initials is not None and icontact.mid_initials != '':
        name += ' '
        name += icontact.mid_initials
    name += ' '
    name += icontact.last_name
    if name is not None:
        contact_value_str += "Name: " + name + '\n'

    email = icontact.email
    if email is not None:
        contact_value_str += "e-mail: " + email + '\n'

    affiliation = icontact.affiliation
    if affiliation is not None:
        contact_value_str += "Affiliation: " + affiliation + '\n'

    addr = icontact.address
    if addr is not None:
        contact_value_str += "Address: " + addr + '\n'

    for role in icontact.roles:
        contact_value_str += "Role: " + role.name + '\n'

    xattrs.append(pyxb.BIND(prefix_label + "Contact", contact_value_str))


def build_exported_publication(ipub, xattrs, xlinks, is_investigation):
    if is_investigation:
        prefix_label = 'Investigation '
    else:
        prefix_label = 'Study '

    pub_str = ""

    # get full name
    title = ipub.title
    if title is not None:
        pub_str += "Title: " + title + '\n'

    authors = ipub.author_list
    if authors is not None:
        pub_str += "Authors: " + authors + '\n'

    status = ipub.status
    if status is not None:
        pub_str += "Status: " + status.name + '\n'

    pmid = ipub.pubmed_id
    if pmid is not None:
        pub_str += "PUBMED ID: " + pmid + '\n'
        xlinks.append(pyxb.BIND())
        xlinks[-1].ENTREZ_LINK = pyxb.BIND()
        xlinks[-1].ENTREZ_LINK.DB = pyxb.BIND('pubmed')
        try:
            xlinks[-1].ENTREZ_LINK.ID = pyxb.BIND(int(pmid))
        except ValueError:
            logger.warn("The PUBMED ID '" + pmid + "' for '" + title + "' is not valid, not exporting this publication")

    doi = ipub.doi
    if doi is not None:
        pub_str += "DOI: " + doi + '\n'
        xlinks.append(pyxb.BIND())
        xlinks[-1].URL_LINK = pyxb.BIND()
        xlinks[-1].URL_LINK.LABEL = pyxb.BIND(prefix_label + "Publication DOI")
        xlinks[-1].URL_LINK.URL = pyxb.BIND("http://dx.doi.org/" + doi)

    xattrs.append(pyxb.BIND(prefix_label + "Publication", pub_str))
