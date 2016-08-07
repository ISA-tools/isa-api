from ena.sra import submission, run, experiment, sample, study
import logging
import pyxb
import pyxb.binding.datatypes as xs
import iso8601
from isatools.model.v1 import Sample

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
        logger.debug("sra exporter, working on " + study_acc)
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

        xrun_set = run.RUN_SET()
        xexp_set = experiment.EXPERIMENT_SET()
        xsample_set = sample.SAMPLE_SET()

        xstudy_doc = None
        is_assay_ok = True
        for iassay in istudy.assays:
            if (iassay.measurement_type.name, iassay.technology_type.name) in supported_sra_assays:
                assay_processes = [a for a in iassay.process_sequence if a.executes_protocol.protocol_type.name ==
                         'nucleic acid sequencing']
                xstudy_doc = build_exported_study(istudy)
                for assay_process in assay_processes:
                    logger.debug("SraExporter, Working on assay " + assay_process.name)
                    if not build_exported_assay(study_acc, assay_process, xrun_set, xexp_set, xsample_set):
                        is_assay_ok = False
                        # Skip all the assay file if only a single assay is wrong, a partial export is too dangerous
                        break

        if is_assay_ok and xstudy_doc is not None:
            logger.debug("SRA exporter: writing SRA XML files for study " + study_acc)
            print(xstudy_doc.toxml())
            print(xexp_set.toxml())


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


def build_exported_assay(study_acc, assay_process, xrun_set, xexperiment_set, xsample_set):

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

    assay_acc = assay_process.name
    do_export = True
    if get_comment(assay_process, 'export') is not None:
        logger.debug("HAS EXPORT COMMENT IN ASSAY")
        export = get_comment(assay_process, 'export').value
        logger.debug("export is " + export)
        do_export = export.lower() != 'no'
    else:
        logger.debug("NO EXPORT COMMENT FOUND")
    logger.debug("Perform export? " + str(do_export))

    if do_export:
        sample = None
        curr_process = assay_process
        while sample is None:
            sample = get_sample(curr_process)
            curr_process = curr_process.prev_process
        logger.debug("FOUND SAMPLE " + sample.name)
        xexperiment_set.EXPERIMENT.append(pyxb.BIND())
        xexperiment_set.EXPERIMENT[-1].alias = sample.name
        xexperiment_set.EXPERIMENT[-1].TITLE = pyxb.BIND("Sequencing library derived from sample " + sample.name)

        xexperiment_set.EXPERIMENT[-1].center_name = sra_center_name
        xexperiment_set.EXPERIMENT[-1].broker_name = sra_broker_name

        xplatform = build_exported_platform(study_acc, assay_process)
        if xplatform is None:
            return False

        xexperiment_set.EXPERIMENT[-1].PLATFORM = pyxb.BIND(xplatform)

        xexperiment_set.STUDY_REF = pyxb.BIND(study_acc)
        xrun_set.EXPERIMENT_REF = pyxb.BIND(sample.name)

        xexperiment_set.DESIGN = pyxb.BIND()
        xexperiment_set.DESIGN.DESIGN_DESCRIPTION = pyxb.BIND("See study and sample descriptions for details")

        xsampleref = build_exported_assay_sample(study_acc, assay_process, xsample_set)
        if xsampleref is None:
            return False
        xexperiment_set.DESIGN.SAMPLE_DESCRIPTOR = pyxb.BIND(xsampleref)

        xlib = build_exported_library_descriptor(assay_process)

        xexperiment_set.DESIGN.LIBRARY_DESCRIPTOR = pyxb.BIND(xlib)

        return True
    else:
        return False


def build_exported_platform(study_acc, assay_process):
    proto = assay_process.executes_protocol
    sequencinginst = [pv.value for pv in assay_process.parameter_values if pv.category.parameter_name.name ==
                      'sequencing instrument'][-1]

    xplatform = pyxb.BIND()

    if '454' in sequencinginst:
        if sequencinginst in ['454 GS', '454 GS FLX', '454 GS FLX+', '454 GS 20', '454 GS FLX Titanium',
                              '454 GS Junior']:
            xplatform.LS454 = pyxb.BIND(sequencinginst)
        else:
            xplatform.LS454 = pyxb.BIND('unspecified')

    elif 'illumina' in sequencinginst.lower() or 'hiseq' in sequencinginst.lower() or 'nextseq' in sequencinginst.lower():
        if sequencinginst in ['Illumina Genome Analyzer', 'Illumina Genome Analyzer II',
                              'Illumina Genome Analyzer IIx', 'Illumina HiScanSQ', 'Illumina HiSeq 4000',
                              'Illumina HiSeq 3000', 'Illumina HiSeq 2500', 'Illumina HiSeq 2000',
                              'Illumina HiSeq 1500', 'Illumina HiSeq 1000', 'Illumina HiScanSQ', 'Illumina MiSeq',
                              'HiSeq X Five', 'HiSeq X Ten', 'NextSeq 500', 'NextSeq 550']:
            xplatform.ILLUMINA = pyxb.BIND(sequencinginst)
        else:
            xplatform.ILLUMINA = pyxb.BIND('unspecified')

    elif 'helicos' in sequencinginst.lower():
        if sequencinginst in ['Helicos HeliScope']:
            xplatform.HELICOS = pyxb.BIND(sequencinginst)
        else:
            xplatform.HELICOS = pyxb.BIND('unspecified')

    elif 'ion torrent' in sequencinginst.lower():
        if sequencinginst in ['Ion Torrent PGM', 'Ion Torrent Proton']:
            xplatform.ION_TORRENT = pyxb.BIND(sequencinginst)
        else:
            xplatform.ION_TORRENT = pyxb.BIND('unspecified')

    elif 'minion' in sequencinginst.lower() or 'gridion' in sequencinginst.lower():
        xplatform.PLATFORM.OXFORD_NANOPORE = pyxb.BIND(sequencinginst)

    elif 'ab ' in sequencinginst.lower():
        if sequencinginst in ['AB SOLiD System', 'AB SOLiD System 2.0', 'AB SOLiD System 3.0', 'AB SOLiD 3 System Plus',
                              'AB SOLiD 4 System', 'AB SOLiD 4hq System', 'AB SOLiD PI System', 'AB SOLiD 5500',
                              'AB SOLiD 5500xl', 'AB 5500 Genetic Analyzer', 'AB 5500xl Genetic Analyzer',
                              'AB 5500xl-W Genetic Analysis System']:
            xplatform.ABI_SOLID = pyxb.BIND(sequencinginst)
        else:
            xplatform.ABI_SOLID = pyxb.BIND('unspecified')
    else:
        raise ValueError("The SRA platform ''{0}'' is invalid in the study {1}".format(sequencinginst, study_acc))
        # raise ValueError("The SRA platform ''{0}'' for the assay ''{1}''/''{2}'' in the study ''{3}'' is invalid. Please supply the Platform information for the Assay in the Investigation file".format(sequencinginst),)

    return xplatform


def build_exported_assay_sample(study_acc, assay_process, xsample_set):

    def get_sample(process):
        materials = process.inputs
        sample = None
        for material in materials:
            if isinstance(material, Sample):
                sample = material
                break
        return sample

    sample = None
    curr_process = assay_process
    while sample is None:
        sample = get_sample(curr_process)
        curr_process = curr_process.prev_process
    xsample_descriptor = pyxb.BIND(refname=sample.name)

    return xsample_descriptor


def build_exported_library_descriptor(assay_process, measurement, technology):

    def get_pv(process, name):
        hits = [pv for pv in process.parameter_values if p.parameter_values.category.parameter_name.name.lower() == name.lower()]
        if len(hits) > 1:
            raise AttributeError("Multiple parameter values of category '{}' found".format(name))
        elif len(hits) < 1:
            return None
        else:
            return hits[0]

    papp = [p for p in assay_process.executes_protocol if p.protocol_type.name.lower() == 'library construction']
    if len(papp) == 0:
        return None
    papp = papp[-1]
    xlib = pyxb.BIND()
    lname = get_pv(papp, 'library name')
    if lname is not None:
        xlib.LIBRARY_NAME = pyxb.BIND(lname)
    else:
        xlib.LIBRARY_NAME = pyxb.BIND(assay_process.name)

    protocol = str()
    pdescription = papp.executes_protocol.description
    if pdescription is not None:
        protocol += "\n protocol_description: " + pdescription

    if technology.lower() == 'nucleotide sequencing':
        if measurement.lower() in ['genome sequencing', 'whole genome sequencing']:
            source = get_pv(papp, 'library source')
            strategy = get_pv(papp, 'library strategy')
            selection = get_pv(papp, 'library selection')

            if source.upper() in ['GENOMIC', 'GENOMIC SINGLE CELL', 'METAGENOMIC', 'OTHER']:
                xlib.LIBRARY_SOURCE = pyxb.BIND(source.upper())
            else:
                xlib.LIBRARY_SOURCE = pyxb.BIND('OTHER')
                logger.warn("ERROR:value supplied is not compatible with SRA1.5 schema" + source)

            if strategy.upper() in ['WGS', 'OTHER']:
                xlib.LIBRARY_STRATEGY = pyxb.BIND(strategy.upper())
            else:
                xlib.LIBRARY_STRATEGY = pyxb.BIND('OTHER')
                logger.warn("ERROR:value supplied is not compatible with SRA1.5 schema" + strategy)

            if selection.upper() in ['RANDOM', 'UNSPECIFIED']:
                xlib.LIBRARY_STRATEGY = pyxb.BIND(selection.upper())
            else:
                xlib.LIBRARY_STRATEGY = pyxb.BIND('UNSPECIFIED')
                logger.warn("ERROR:value supplied is not compatible with SRA1.5 schema" + selection)
