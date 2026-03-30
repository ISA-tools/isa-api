# -*- coding: utf-8 -*-
"""Functions for reading and writing SRA-XML.

Functions for reading and writing SRA-XML. SRA-XML content is loaded into
an in-memory representation using the ISA Data Model implemented in the
isatools.model package.
"""

import datetime
import hashlib
import html
import logging
import os
import xml.dom.minidom
from dataclasses import dataclass
from functools import lru_cache, partial

import iso8601
import jinja2
from lxml import etree

from isatools.model import DataFile, OntologyAnnotation, Sample

log = logging.getLogger("isatools")

supported_sra_assays = [
    ("genome sequencing", "nucleotide sequencing"),
    ("environmental gene survey", "nucleotide sequencing"),
    ("metagenome sequencing", "nucleotide sequencing"),
    ("transcription profiling", "nucleotide sequencing"),
]

SRA_CENTER_NAME_DEFAULT = "OXFORD"
SRA_BROKER_NAME_DEFAULT = "ISAcreator"
sra_center_name = SRA_CENTER_NAME_DEFAULT
sra_broker_name = SRA_BROKER_NAME_DEFAULT
sra_lab_name = sra_center_name
sra_submission_action = "ADD"
sra_center_prj_name = None


@dataclass(frozen=True)
class SraExportSettings:
    center_name: str = SRA_CENTER_NAME_DEFAULT
    broker_name: str = SRA_BROKER_NAME_DEFAULT
    broker_inform_on_status: str | None = None
    broker_inform_on_error: str | None = None
    broker_contact_name: str | None = None

    @property
    def broker_contact(self):
        if self.broker_inform_on_status or self.broker_inform_on_error or self.broker_contact_name:
            return {
                "inform_on_status": self.broker_inform_on_status,
                "inform_on_error": self.broker_inform_on_error,
                "contact_name": self.broker_contact_name,
            }
        return None


def _resolve_settings(sra_settings):
    if sra_settings is None:
        return SraExportSettings()
    return SraExportSettings(
        center_name=sra_settings.get("sra_center", SRA_CENTER_NAME_DEFAULT),
        broker_name=sra_settings.get("sra_broker", SRA_BROKER_NAME_DEFAULT),
        broker_inform_on_status=sra_settings.get("sra_broker_inform_on_status"),
        broker_inform_on_error=sra_settings.get("sra_broker_inform_on_error"),
        broker_contact_name=sra_settings.get("sra_broker_contact_name"),
    )


def _get_comment(assay, name):
    hits = [c for c in assay.comments if c.name.lower() == name.lower()]
    if len(hits) > 1:
        raise AttributeError("Multiple comments of label '{}' found".format(name))
    if not hits:
        return None
    return hits[0]


def _get_sample(process):
    return next((material for material in process.inputs if isinstance(material, Sample)), None)


def _normalize_value(value):
    if value is None:
        return None
    if isinstance(value, OntologyAnnotation):
        value = value.term
    if isinstance(value, str):
        return value.replace("_", " ")
    return str(value)


def _get_pv(process, name):
    expected = name.lower().replace("_", " ")
    hits = [
        pv
        for pv in process.parameter_values
        if pv.category.parameter_name.term.lower().replace("_", " ") == expected
    ]
    if len(hits) > 1:
        raise AttributeError("Multiple parameter values of category '{}' found".format(name))
    if not hits:
        return None
    return _normalize_value(hits[0].value)


def _lower_or_default(value, default):
    return value.lower() if isinstance(value, str) else default


def _safe_upper(value):
    return value.upper() if isinstance(value, str) else ""


def _find_sample_in_ancestry(assay_seq_process):
    sample = None
    curr_process = assay_seq_process
    while curr_process is not None and sample is None:
        sample = _get_sample(curr_process)
        curr_process = curr_process.prev_process
    if sample is None:
        raise ValueError("Could not find a Sample in the process chain for assay process '{}'".format(assay_seq_process))
    return sample


def _source_from_study_processes(study, sample):
    matching_inputs = [p.inputs for p in study.process_sequence if sample in p.outputs]
    if not matching_inputs:
        raise ValueError("Could not resolve source for sample '{}'".format(sample.name))
    first_inputs = matching_inputs[0]
    if len(first_inputs) == 1:
        return first_inputs[0]
    source_candidate = next((material for material in first_inputs if hasattr(material, "characteristics")), None)
    if source_candidate is None:
        raise ValueError("Could not resolve source for sample '{}' from process inputs".format(sample.name))
    return source_candidate


def _extract_taxon_id(term_accession):
    if not term_accession:
        return ""
    if "_" in term_accession:
        return term_accession.split("_", 1)[1]
    return term_accession


def _get_organism_characteristic(source):
    organism_chars = [c for c in source.characteristics if c.category.term == "organism"]
    if not organism_chars:
        raise ValueError("Source '{}' is missing an 'organism' characteristic".format(source.name))
    return organism_chars[-1]


def _prettify(xmlstr):
    parser = etree.XMLParser(remove_blank_text=True)
    xml_doc = etree.XML(xmlstr, parser=parser)
    dom = xml.dom.minidom.parseString(etree.tostring(xml_doc))
    return dom.toprettyxml()


@lru_cache(maxsize=None)
def _load_schema(schemaname):
    schema_path = os.path.join(os.path.dirname(__file__), "resources", "sra_schemas", schemaname)
    with open(schema_path, "rb") as xsd:
        schema_doc = etree.parse(xsd)
    return etree.XMLSchema(schema_doc)


def _validate(docpath, schemaname):
    try:
        schema = _load_schema(schemaname)
        with open(docpath, "rb") as xsub_file:
            doc = etree.parse(xsub_file)
        schema.assertValid(doc)
    except etree.DocumentInvalid as e:
        log.error("Schema validation failed on {}".format("{0}:\n{1}".format(docpath, str(e))))
    except etree.XMLSchemaParseError as e:
        log.error(e)


def export(investigation, export_path, sra_settings=None, datafilehashes=None):
    """Exports ISA Data model objects to SRA-XML files

    The exporter uses the jinja2 templating engine. The SRA templates can be
    found in isatools/resources/sra_templates

    :param investigation: An Investigation object
    :param export_path: Path to write SRA-XML files to
    :param sra_settings: Some universal settings to apply to the SRA export
    :param datafilehashes: A list of data file hashes to apply to the exported
    files
    :return: None
    """

    settings = _resolve_settings(sra_settings)

    env = jinja2.Environment()
    env.loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "resources", "sra_templates"))

    log.info("isatools.sra.export()")
    for istudy in investigation.studies:
        is_sra = False
        for iassay in istudy.assays:
            if (iassay.measurement_type.term, iassay.technology_type.term) in supported_sra_assays:
                is_sra = True
                break
        if not is_sra:
            log.info("No SRA assay found, skipping processing")
            continue

        study_acc = istudy.identifier
        log.debug("sra exporter, working on " + study_acc)

        # Flag SRA contacts for template
        has_sra_contact = False
        for contact in istudy.contacts:
            if "sra inform on status" in [r.term.lower() for r in contact.roles]:
                contact.inform_on_status = True
                has_sra_contact = True
            if "sra inform on error" in [r.term.lower() for r in contact.roles]:
                contact.inform_on_error = True
                has_sra_contact = True
        if not has_sra_contact:
            raise ValueError(
                "The study '{0}' has either no SRA contact or no "
                "email specified for the contact. Please ensure you have one "
                "contact with a 'Role' as 'SRA Inform On Status', otherwise "
                "we cannot export to SRA.".format(istudy.identifier)
            )

        if istudy.submission_date is None or istudy.submission_date == "":
            istudy.submission_date = iso8601.parse_date(datetime.date.today().isoformat(), iso8601.UTC).isoformat()
        else:
            istudy.submission_date = iso8601.parse_date(istudy.submission_date, iso8601.UTC).isoformat()
        istudy.description = html.escape(istudy.description)
        # ideally make it a requirement in the model or JSON to have html
        # escaped content

        xsub_template = env.get_template("submission_add.xml")
        xsub = xsub_template.render(
            accession=study_acc,
            contacts=istudy.contacts,
            submission_date=istudy.submission_date,
            sra_center_name=settings.center_name,
            sra_broker_name=settings.broker_name,
            sra_contact=settings.broker_contact,
        )
        xproj_template = env.get_template("project_set.xml")
        xproj = xproj_template.render(study=istudy, sra_center_name=settings.center_name)

        assays_to_export = list()
        for iassay in istudy.assays:
            if (iassay.measurement_type.term, iassay.technology_type.term) in supported_sra_assays:
                assay_seq_processes = [
                    a
                    for a in iassay.process_sequence
                    if a.executes_protocol.protocol_type.term == "nucleic acid sequencing"
                ]
                for assay_seq_process in assay_seq_processes:
                    do_export = True
                    export_comment = _get_comment(assay_seq_process, "export")
                    if export_comment is not None:
                        log.debug("HAS EXPORT COMMENT IN ASSAY")
                        export = export_comment.value
                        log.debug("export is {}".format(export))
                        do_export = export.lower() != "no"
                    else:
                        log.debug("NO EXPORT COMMENT FOUND")
                    log.debug("Perform export? {}".format(str(do_export)))
                    if do_export:
                        sample = _find_sample_in_ancestry(assay_seq_process)
                        assay_to_export = {
                            "sample": sample,
                            "sample_alias": "{0}:sample:{1}".format(study_acc, sample.name),
                            "run_alias": "{0}:assay:{1}".format(study_acc, assay_seq_process.name),
                            "exp_alias": "{0}:generic_assay:{1}".format(
                                study_acc, "{0}:{1}".format(iassay.filename[:-4], assay_seq_process.name)
                            ),
                            "data_files": [],
                        }
                        datafiles = list(
                            filter(lambda datafile: isinstance(datafile, DataFile), assay_seq_process.outputs)
                        )
                        for datafile in datafiles:
                            checksum = "00000000000000000000000000000000"
                            if datafilehashes is not None:
                                checksum = datafilehashes[datafile.filename]
                                # raises AttributeError if file not found
                            dot_indicies = [i for i, x in enumerate(datafile.filename) if x == "."]
                            file_ext = datafile.filename[dot_indicies[-1] + 1 :]
                            if ".gz" in file_ext:
                                # if is compressed, look for the actual ftype
                                try:
                                    filetype = datafile.filename[dot_indicies[-2] + 1 : dot_indicies[-1]]
                                except IndexError:
                                    log.warning(
                                        "Could not infer SRA filetype for "
                                        "data file {filename}; defaulting to "
                                        "'other'".format(filename=datafile.filename)
                                    )
                                    filetype = "other"
                            else:
                                filetype = file_ext
                            assay_to_export["data_files"].append(
                                {"filename": datafile.filename, "filetype": filetype, "checksum": checksum}
                            )
                        source = _source_from_study_processes(istudy, sample)
                        assay_to_export["source"] = {
                            "name": source.name,
                            "characteristics": source.characteristics,
                        }
                        organism_charac = _get_organism_characteristic(source)
                        assay_to_export["source"]["taxon_id"] = _extract_taxon_id(organism_charac.value.term_accession)
                        assay_to_export["source"]["scientific_name"] = organism_charac.value.term
                        curr_process = assay_seq_process
                        while curr_process.prev_process is not None:
                            assay_to_export[curr_process.executes_protocol.protocol_type.term] = curr_process
                            try:
                                curr_process = curr_process.prev_process
                            except AttributeError:
                                pass
                        target_taxon = _get_pv(assay_to_export["library construction"], "target_taxon")
                        assay_to_export["target_taxon"] = target_taxon
                        assay_to_export["targeted_loci"] = False
                        assay_to_export["min_match"] = 0
                        # BEGIN genome seq library selection
                        if iassay.measurement_type.term in ["genome sequencing", "whole genome sequencing"]:
                            library_source = _get_pv(assay_to_export["library construction"], "library source")
                            if _safe_upper(library_source) not in ["GENOMIC", "GENOMIC SINGLE CELL", "METAGENOMIC", "OTHER"]:
                                log.warning(
                                    "ERROR:value supplied is not compatible with SRA1.5 schema {}".format(
                                        library_source
                                    )
                                )
                                library_source = "OTHER"

                            library_strategy = _get_pv(assay_to_export["library construction"], "library strategy")
                            if _safe_upper(library_strategy) not in ["WGS", "OTHER"]:
                                log.warning(
                                    "ERROR:value supplied is not compatible with SRA1.5 schema {}".format(
                                        library_strategy
                                    )
                                )
                                library_strategy = "OTHER"

                            library_selection = _get_pv(assay_to_export["library construction"], "library selection")
                            if library_selection not in ["RANDOM", "UNSPECIFIED"]:
                                log.warning(
                                    "ERROR:value supplied is not compatible with SRA1.5 schema {}".format(
                                        library_selection
                                    )
                                )
                                library_selection = "unspecified"

                            protocol = "\n protocol_description: {}".format(
                                assay_to_export["library construction"].executes_protocol.description
                            )
                            mid_pv = _get_pv(assay_to_export["library construction"], "mid")
                            if mid_pv is not None:
                                protocol += "\n mid: {}".format(mid_pv)

                            assay_to_export["library_source"] = library_source
                            assay_to_export["library_strategy"] = library_strategy
                            assay_to_export["library_selection"] = library_selection
                            assay_to_export["library_construction_protocol"] = protocol

                            library_layout = _get_pv(assay_to_export["library construction"], "library layout")
                            assay_to_export["library_layout"] = _lower_or_default(library_layout, "single")
                        # END genome seq library selection
                        # BEGIN environmental gene survey library selection
                        elif iassay.measurement_type.term in ["environmental gene survey"]:
                            assay_to_export["library_source"] = "METAGENOMIC"
                            assay_to_export["library_strategy"] = "AMPLICON"
                            assay_to_export["library_selection"] = "PCR"
                            library_layout = _get_pv(assay_to_export["library construction"], "library layout")
                            assay_to_export["library_layout"] = _lower_or_default(library_layout, "single")
                            nucl_acid_amp = _get_pv(
                                assay_to_export["library construction"], "nucleic acid amplification"
                            )
                            if nucl_acid_amp is None:
                                nucl_acid_amp = _get_pv(assay_to_export["library construction"], "nucl_acid_amp")

                            protocol = "\n protocol_description: {}".format(
                                assay_to_export["library construction"].executes_protocol.description
                            )
                            mid_pv = _get_pv(assay_to_export["library construction"], "mid")
                            if mid_pv is not None:
                                protocol += "\n mid: {}".format(mid_pv)
                                assay_to_export["barcode"] = mid_pv
                                assay_to_export["min_match"] = len(mid_pv)
                            if nucl_acid_amp is not None:
                                protocol += "\n nucl_acid_amp: {}".format(nucl_acid_amp)
                            url = _get_pv(assay_to_export["library construction"], "url")
                            if url is not None:
                                protocol += "\n url: {}".format(url)
                            target_taxon = assay_to_export["target_taxon"]
                            if target_taxon is not None:
                                protocol += "\n target_taxon: {}".format(target_taxon)
                            target_gene = _get_pv(assay_to_export["library construction"], "target_gene")
                            if target_gene is not None:
                                protocol += "\n target_gene: {}".format(target_gene)
                            target_subfragment = _get_pv(assay_to_export["library construction"], "target_subfragment")
                            if target_subfragment is not None:
                                protocol += "\n target_subfragment: {}".format(target_subfragment)
                            pcr_primers = _get_pv(assay_to_export["library construction"], "pcr_primers")
                            if pcr_primers is not None:
                                protocol += "\n pcr_primers: {}".format(pcr_primers)
                            pcr_cond = _get_pv(assay_to_export["library construction"], "pcr_cond")
                            if pcr_cond is not None:
                                protocol += "\n pcr_cond: {}".format(pcr_cond)
                            assay_to_export["library_construction_protocol"] = protocol

                            if target_gene is not None:
                                assay_to_export["targeted_loci"] = True
                                assay_to_export["locus_name"] = target_gene
                        # END environmental gene survey library selection
                        # BEGIN metagenome seq library selection
                        elif iassay.measurement_type.term in ["metagenome sequencing"]:
                            library_source = "METAGENOMIC"
                            library_strategy = _get_pv(assay_to_export["library construction"], "library strategy")
                            if _safe_upper(library_strategy) not in ["WGS", "OTHER"]:
                                log.warning(
                                    "ERROR:value supplied is not compatible with SRA1.5 schema {}".format(
                                        library_strategy
                                    )
                                )
                                library_strategy = "OTHER"

                            library_selection = _get_pv(assay_to_export["library construction"], "library selection")
                            if library_selection not in ["RANDOM", "UNSPECIFIED"]:
                                log.warning(
                                    "ERROR:value supplied is not compatible with SRA1.5 schema {}".format(
                                        library_selection
                                    )
                                )
                                library_selection = "unspecified"

                            protocol = "\n protocol_description: {}".format(
                                assay_to_export["library construction"].executes_protocol.description
                            )
                            mid_pv = _get_pv(assay_to_export["library construction"], "mid")
                            if mid_pv is not None:
                                protocol += "\n mid: {}".format(mid_pv)

                            assay_to_export["library_source"] = library_source
                            assay_to_export["library_strategy"] = library_strategy
                            assay_to_export["library_selection"] = library_selection
                            assay_to_export["library_construction_protocol"] = protocol

                            library_layout = _get_pv(assay_to_export["library construction"], "library layout")
                            assay_to_export["library_layout"] = _lower_or_default(library_layout, "single")
                        # END metagenome seq library selection
                        # BEGIN transciption profiling library selection
                        elif iassay.measurement_type.term in ["transcription profiling"]:
                            library_source = _get_pv(assay_to_export["library construction"], "library source")
                            if library_source is None:
                                # if not specified, select TRANSCRIPTOMIC by
                                # default
                                library_source = "TRANSCRIPTOMIC"

                            if library_source.upper() not in [
                                "TRANSCRIPTOMIC",
                                "TRANSCRIPTOMIC SINGLE CELL",
                                "METATRANSCRIPTOMIC",
                                "OTHER",
                            ]:
                                log.warning(
                                    "ERROR:value supplied is not compatible with SRA1.5 schema {}".format(
                                        library_source
                                    )
                                )
                                library_source = "OTHER"

                            library_strategy = _get_pv(assay_to_export["library construction"], "library strategy")
                            if library_strategy not in [
                                "RNA-Seq",
                                "ssRNA-Seq",
                                "miRNA-Seq",
                                "ncRNA-Seq",
                                "FL-cDNA",
                                "EST",
                                "OTHER",
                            ]:
                                log.warning(
                                    "ERROR:value supplied is not compatible with SRA1.5 schema {}".format(
                                        library_strategy
                                    )
                                )
                                library_strategy = "OTHER"

                            library_selection = _get_pv(assay_to_export["library construction"], "library selection")
                            if library_selection not in [
                                "RT-PCR",
                                "cDNA",
                                "cDNA_randomPriming",
                                "cDNA_oligo_dT",
                                "PolyA",
                                "Oligo-dT",
                                "Inverse rRNA",
                                "Inverse rRNA selection",
                                "CAGE",
                                "RACE",
                                "other",
                            ]:
                                log.warning(
                                    "ERROR:value supplied is not compatible with SRA1.5 schema {}".format(
                                        library_selection
                                    )
                                )
                                library_selection = "other"

                            protocol = "\n protocol_description: {}".format(
                                assay_to_export["library construction"].executes_protocol.description
                            )
                            assay_to_export["library_source"] = library_source
                            assay_to_export["library_strategy"] = library_strategy
                            assay_to_export["library_selection"] = library_selection
                            assay_to_export["library_construction_protocol"] = protocol

                            library_layout = _get_pv(assay_to_export["library construction"], "library layout")
                            assay_to_export["library_layout"] = _lower_or_default(library_layout, "single")
                        # END transciption profiling library selection
                        else:
                            log.error("ERROR:Unsupported measurement type: {}".format(iassay.measurement_type.term))
                        mid_pv = _get_pv(assay_to_export["library construction"], "mid")
                        assay_to_export["poolingstrategy"] = mid_pv
                        seq_instrument = _get_pv(assay_to_export["nucleic acid sequencing"], "sequencing instrument")
                        assay_to_export["platform"] = seq_instrument
                        assays_to_export.append(assay_to_export)
            else:
                log.error(
                    "ERROR:Unsupported measurement/technology type {0}/{1}, skipping assays".format(
                        iassay.measurement_type.term, iassay.technology_type.term
                    )
                )

        xexp_set_template = env.get_template("experiment_set.xml")
        xexp_set = xexp_set_template.render(
            assays_to_export=assays_to_export,
            study=istudy,
            sra_center_name=settings.center_name,
            sra_broker_name=settings.broker_name,
        )
        xrun_set_template = env.get_template("run_set.xml")
        xrun_set = xrun_set_template.render(
            assays_to_export=assays_to_export,
            study=istudy,
            sra_center_name=settings.center_name,
            sra_broker_name=settings.broker_name,
        )
        samples_to_export = list()
        for assay_to_export in assays_to_export:
            if len([s for s in samples_to_export if s["sample_alias"] == assay_to_export["sample_alias"]]) > 0:
                pass
            else:
                samples_to_export.append(assay_to_export)
        xsample_set_template = env.get_template("sample_set.xml")
        xsample_set = xsample_set_template.render(
            assays_to_export=samples_to_export,
            study=istudy,
            sra_center_name=settings.center_name,
            sra_broker_name=settings.broker_name,
        )
        log.debug("SRA exporter: writing SRA XML files for study " + study_acc)

        if os.path.exists(export_path):
            with open(os.path.join(export_path, "submission.xml"), "w", encoding="utf-8") as xsub_file:
                print(_prettify(xsub), file=xsub_file)
            _validate(os.path.join(export_path, "submission.xml"), "SRA.submission.xsd")
            with open(os.path.join(export_path, "project_set.xml"), "w", encoding="utf-8") as xproj_set_file:
                print(_prettify(xproj), file=xproj_set_file)
            _validate(os.path.join(export_path, "project_set.xml"), "ENA.project.xsd")
            with open(os.path.join(export_path, "experiment_set.xml"), "w", encoding="utf-8") as xexp_set_file:
                print(_prettify(xexp_set), file=xexp_set_file)
            _validate(os.path.join(export_path, "experiment_set.xml"), "SRA.experiment.xsd")
            with open(os.path.join(export_path, "run_set.xml"), "w", encoding="utf-8") as xrun_set_file:
                print(_prettify(xrun_set), file=xrun_set_file)
            _validate(os.path.join(export_path, "run_set.xml"), "SRA.run.xsd")
            with open(os.path.join(export_path, "sample_set.xml"), "w", encoding="utf-8") as xsample_set_file:
                print(_prettify(xsample_set), file=xsample_set_file)
            _validate(os.path.join(export_path, "sample_set.xml"), "SRA.sample.xsd")
        else:
            raise NotADirectoryError("export path '{}' is not a directory".format(export_path))


def create_datafile_hashes(fileroot, filenames):
    """
      Create md5 file dict for files in a directory with a particular extension

      :param fileroot: Root to directory containing files (assumes all in
      same dir)
      :param filenames: List of filenames of files to md5, assumed in fileroot
      :return: dict containing filenames and md5s

      Usage:
     / >>> filenames = [f for f in listdir('/path/') if f.endswith('.fastq.gz')]
    /  >>> create_datafile_hashes(fileroot='/path/s', filenames=filesnames)
      {
          'myfile1.gz': 'd41d8cd98f00b204e9800998ecf8427e',
          'myfile2.gz': 'd41d8cd98f00b204e9800998ecf8427e'
      }
    """

    def md5sum(filename):
        with open(filename, mode="rb") as f:
            d = hashlib.md5()
            for buf in iter(partial(f.read, 8192), b""):
                d.update(buf)
        return d.hexdigest()

    from os.path import isfile, join

    datafilehashes = dict()
    for file in filenames:
        if isfile(join(fileroot, file)):
            datafilehashes[file] = md5sum(filename=join(fileroot, file))
        else:
            raise FileNotFoundError("{} is not a file".format(join(fileroot, file)))
    return datafilehashes
