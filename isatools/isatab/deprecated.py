# -*- coding: utf-8 -*-
"""Functions for reading, writing and validating ISA-Tab.

Functions for reading and writing ISA-Tab. ISA content is loaded into an
in-memory representation using the ISA Data Model implemented in the
isatools.model package.
"""
from __future__ import absolute_import
import csv
import glob
import json
import logging
import os
import re
import shutil
from json import dump
from itertools import zip_longest
from os import path
from glob import iglob

import numpy as np
from pandas import DataFrame, Series

from isatools.model import (
    Comment,
    Investigation,
    OntologyAnnotation,
    OntologySource,
    Person,
    Publication,
    Study,
    StudyFactor
)
from isatools.utils import utf8_text_file_open
from isatools.isatab.defaults import _RX_COMMENT, log
from isatools.isatab.utils import find_lt, find_gt, get_squashed
from isatools.isatab.load import load, load_table


def get_multiple_index(file_index, key):
    return np.where(np.array(file_index) in key)[0]


def find_in_between(a, x, y):
    result = []
    while True:
        try:
            element_gt = find_gt(a, x)
        except ValueError:
            return result

        if (element_gt > x and y == -1) or (element_gt > x and element_gt < y):
            result.append(element_gt)
            x = element_gt
        else:
            break

    while True:
        try:
            element_lt = find_lt(a, y)
        except ValueError:
            return result
        if element_lt not in result:
            if (element_lt < y and element_lt > x):
                result.append(element_lt)
                y = element_lt
            else:
                break
        else:
            break

    return result


class IsaTabParser(object):
    """
        This replacement should be more robust than current
        i_*.txt file reader. Based on what I did for the
        MAGE-TAB IDF parser. INCOMPLETE - do not use!

        TODO: Work out how to add comments in correct contexts
        TODO: Parse Assay section
        TODO: Unit tests
    """

    def __init__(self):
        self.ISA = Investigation()
        self._ts_dict = {}

    def parse_investigation(self, in_filename):
        section_keys = ('ontologysourcereference',
                        'investigation',
                        'investigationpublications',
                        'investigationcontacts',
                        'study',
                        'studydesigndescriptors',
                        'studypublciations',
                        'studyfactors',
                        'studyassays',
                        'studyprotocols',
                        'studycontacts')
        isecdict = {}
        ssecdicts = []
        with utf8_text_file_open(in_filename) as in_file:
            tabreader = csv.reader(
                filter(lambda r: r[0] != '#', in_file), dialect='excel-tab')
            current_section = ''
            for row in tabreader:
                key = get_squashed(key=row[0])
                if key in section_keys:
                    current_section = key
                if key.startswith('comment'):
                    key = '.'.join((current_section, key))
                if key == 'study':
                    ssecdicts.append({})
                if key.startswith('study'):
                    ssecdicts[-1][key] = row[1:]
                else:
                    isecdict[key] = row[1:]

        self.parse_ontology_sources_section(
            isecdict.get('termsourcename', []),
            isecdict.get('termsourcefile', []),
            isecdict.get('termsourceversion', []),
            isecdict.get('termsourcedescription'),
            {k: isecdict[k] for k in isecdict.keys()
             if k.startswith('ontologysourcereference.')})
        self.parse_investigation_section(
            isecdict.get('investigationidentifier', []),
            isecdict.get('investigationtitle', []),
            isecdict.get('investigationdescription', []),
            isecdict.get('investigationsubmissiondate', []),
            isecdict.get('investigationpublicreleasedate'),
            {k: isecdict[k] for k in isecdict.keys()
             if k.startswith('investigation.')})
        self.parse_publications_section(
            self.ISA,
            isecdict.get('investigationpubmedid', []),
            isecdict.get('investigationpublicationdoi', []),
            isecdict.get('investigationpublicationauthorlist', []),
            isecdict.get('investigationpublicationtitle', []),
            isecdict.get('investigationpublicationstatus', []),
            isecdict.get('investigationpublicationstatustermsourceref', []),
            isecdict.get('investigationpublicationstatustermaccessionnumber'),
            {k: isecdict[k] for k in isecdict.keys()
             if k.startswith('investigationpublications.')})
        self.parse_people_section(
            self.ISA,
            isecdict.get('investigationpersonlastname', []),
            isecdict.get('investigationpersonfirstname', []),
            isecdict.get('investigationpersonmidinitials', []),
            isecdict.get('investigationpersonemail', []),
            isecdict.get('investigationpersonphone', []),
            isecdict.get('investigationpersonfax', []),
            isecdict.get('investigationpersonaddress', []),
            isecdict.get('investigationpersonaffiliation', []),
            isecdict.get('investigationpersonroles', []),
            isecdict.get('investigationpersonrolestermaccessionnumber', []),
            isecdict.get('investigationpersonrolestermsourceref'),
            {k: isecdict[k] for k in isecdict.keys()
             if k.startswith('investigationcontacts.')})

        for ssecdict in ssecdicts:
            self.parse_study_section(
                ssecdict.get('studyidentifier', []),
                ssecdict.get('studytitle', []),
                ssecdict.get('studydescription', []),
                ssecdict.get('studysubmissiondate', []),
                ssecdict.get('studypublicreleasedate', []),
                ssecdict.get('studyfilename'))
            self.parse_study_design_section(
                self.ISA.studies[-1],
                ssecdict.get('studydesigntype', []),
                ssecdict.get('studydesigntypetermaccessionnumber', []),
                ssecdict.get('studydesigntypetermsourceref'))
            self.parse_publications_section(
                self.ISA.studies[-1],
                ssecdict.get('studypubmedid', []),
                ssecdict.get('studypublicationdoi', []),
                ssecdict.get('studypublicationauthorlist', []),
                ssecdict.get('studypublicationtitle', []),
                ssecdict.get('studypublicationstatus', []),
                ssecdict.get('studypublicationstatustermsourceref', []),
                ssecdict.get('studypublicationstatustermaccessionnumber'),
                {k: ssecdict[k] for k in ssecdict.keys()
                 if k.startswith('studypublications.')})
            self.parse_people_section(
                self.ISA.studies[-1],
                ssecdict.get('studypersonlastname', []),
                ssecdict.get('studypersonfirstname', []),
                ssecdict.get('studypersonmidinitials', []),
                ssecdict.get('studypersonemail', []),
                ssecdict.get('studypersonphone', []),
                ssecdict.get('studypersonfax', []),
                ssecdict.get('studypersonaddress', []),
                ssecdict.get('studypersonaffiliation', []),
                ssecdict.get('studypersonroles', []),
                ssecdict.get('studypersonrolestermaccessionnumber', []),
                ssecdict.get('studypersonrolestermsourceref'),
                {k: ssecdict[k] for k in ssecdict.keys()
                 if k.startswith('studycontacts.')})
            self.parse_study_factors_section(
                self.ISA.studies[-1],
                ssecdict.get('studyfactorname', []),
                ssecdict.get('studyfactorntype', []),
                ssecdict.get('studyfactortypetermaccessionnumber', []),
                ssecdict.get('studyfactortypetermsourceref'))

    def parse_ontology_sources_section(self, names, files, versions,
                                       descriptions, comments_dict):
        i = 0
        for name, file, version, description in zip_longest(
                names, files, versions, descriptions):
            i += 1
            current_onto_source = OntologySource(
                name=name, file=file, version=version, description=description)
            for k, v in comments_dict.items():
                if i < len(v) > 0:
                    current_onto_source.comments.append(
                        Comment(name=next(iter(_RX_COMMENT.findall(k))),
                                value=v[i]))
            self.ISA.ontology_source_references.append(current_onto_source)
            self._ts_dict[name] = current_onto_source

    def parse_investigation_section(
            self, identifiers, titles, descriptions, submissiondates,
            publicreleasedates, comments_dict):
        for identifier, title, description, submissiondate, publicreleasedate in \
           zip_longest(identifiers, titles, descriptions, submissiondates, publicreleasedates):
            self.ISA.identifier = identifier
            self.ISA.title = title
            self.ISA.description = description
            self.ISA.submission_date = submissiondate
            self.ISA.public_release_date = publicreleasedate
            for k, v in comments_dict.items():
                if len(v) > 0:
                    self.ISA.comments.append(
                        Comment(name=next(iter(_RX_COMMENT.findall(k))),
                                value=';'.join(v) if len(v) > 1 else v[0]))
            break  # because there should only be one or zero rows

    def parse_study_section(self, identifiers, titles, descriptions,
                            submissiondates, publicreleasedates, filenames):
        for identifier, title, description, submissiondate, publicreleasedate, \
            filename in zip_longest(identifiers, titles, descriptions, submissiondates,
                                    publicreleasedates, filenames):
            study = Study(
                identifier=identifier, title=title, description=description,
                submission_date=submissiondate,
                public_release_date=publicreleasedate, filename=filename)
            self.ISA.studies.append(study)

    def parse_study_design_section(self, obj, dtypes, dtypetans, dtypetsrs):
        for dtype, dtypetan, dtypetsr in zip_longest(
                dtypes, dtypetans, dtypetsrs):
            dtypeoa = OntologyAnnotation(
                term=dtype, term_source=self._ts_dict.get(dtypetsr),
                term_accession=dtypetan)
            obj.design_type = dtypeoa
            break

    def parse_publications_section(
            self, obj, pubmedids, dois, authorlists, titles, statuses,
            statustans, statustsrs, comments_dict):
        i = 0
        for pubmedid, doi, authorlist, title, status, statustsr, statustan in \
                zip_longest(
                    pubmedids, dois, authorlists, titles, statuses, statustans,
                    statustsrs):
            i += 1
            statusoa = OntologyAnnotation(
                term=status, term_source=self._ts_dict.get(statustsr),
                term_accession=statustan)
            publication = Publication(
                pubmed_id=pubmedid, doi=doi, author_list=authorlist,
                title=title, status=statusoa)
            for k, v in comments_dict.items():
                if i < len(v) > 0:
                    publication.comments.append(
                        Comment(name=next(iter(_RX_COMMENT.findall(k))),
                                value=v[i]))
            obj.publications.append(publication)

    def parse_people_section(
            self, obj, lastnames, firstnames, midinitialss, emails, phones,
            faxes, addresses, affiliations, roles, roletans, roletrs,
            comments_dict):
        i = 0
        for lastname, firstname, midinitials, email, phone, fax, address, \
            affiliation, role, roletan, roletsr in \
                zip_longest(
                    lastnames, firstnames, midinitialss, emails, phones, faxes,
                    addresses, affiliations, roles, roletans, roletrs):
            i += 1
            rolesoa = OntologyAnnotation(
                term=role, term_source=self._ts_dict.get(roletsr),
                term_accession=roletan)
            person = Person(
                last_name=lastname, first_name=firstname,
                mid_initials=midinitials, email=email, phone=phone, fax=fax,
                address=address, affiliation=affiliation, roles=rolesoa)
            obj.contacts.append(person)
        for i, contact in enumerate(self.ISA.studies[-1].contacts):
            for k, v in comments_dict.items():
                if len(v) > 0:
                    contact.comments.append(
                        Comment(name=next(iter(_RX_COMMENT.findall(k))),
                                value=v[i]))

    def parse_study_factors_section(
            self, obj, fnames, ftypes, ftypetans, ftypetsrs):
        for fname, ftype, ftypetan, ftypetsr in zip_longest(
                fnames, ftypes, ftypetans, ftypetsrs):
            ftypeoa = OntologyAnnotation(
                term=ftype, term_source=self._ts_dict.get(ftypetsr),
                term_accession=ftypetan)
            factor = StudyFactor(name=fname, factor_type=ftypeoa)
            obj.factors.append(factor)


def parse_in(in_filename, in_format='isa-tab'):
    """ Parse the given input file using the in_format and return as ISA
    objects"""

    log.debug("parsing {0} in format {1}".format(in_filename, in_format))

    log.debug("starting to parse {0}".format(in_filename))

    parser = IsaTabParser()
    parser.parse_investigation(in_filename)


def isatab_get_data_files_list_command(input_path, output, json_query=None, galaxy_parameters_file=None):
    """Get a data files list  based on a slicer query

    :param input_path: Path to an ISA-Tab
    :param output: resulting structure
    :param json_query: JSON query to slice
    :param galaxy_parameters_file: Galaxy input parameters JSON if not
    json_query
    :return: None
    """
    log.info("Getting data files for study %s. Writing to %s.",
             input_path, output.name)
    if json_query:
        log.debug("This is the specified query:\n%s", json_query)
        json_struct = json.loads(json_query)
    elif galaxy_parameters_file:
        log.debug("Using input Galaxy JSON parameters from:\n%s",
                  galaxy_parameters_file)
        with open(galaxy_parameters_file) as json_fp:
            galaxy_json = json.load(json_fp)
            json_struct = {}
            for fv_item in galaxy_json['factor_value_series']:
                json_struct[fv_item['factor_name']] = fv_item['factor_value']
    else:
        log.debug("No query was specified")
        json_struct = None
    factor_selection = json_struct
    result = slice_data_files(input_path, factor_selection=factor_selection)
    data_files = result
    log.debug("Result data files list: %s", data_files)
    if data_files is None:
        raise RuntimeError("Error getting data files with isatools")

    log.debug("dumping data files to %s", output.name)
    json.dump(list(data_files), output, indent=4)
    log.info("Finished writing data files to {}".format(output))


def isatab_get_data_files_collection_command(input_path, output_path, json_query=None, galaxy_parameters_file=None):
    """Creates a data files collection at a target path based on a
    slicer query

    :param input_path: Path to an ISA-Tab
    :param output_path: Path to write out the sliced files
    :param json_query: JSON query to slice
    :param galaxy_parameters_file: Galaxy input parameters JSON if not
    json_query
    :return: None
    """
    log.info("Getting data files for study %s. Writing to %s.",
             input_path, output_path)
    if json_query:
        log.debug("This is the specified query:\n%s", json_query)
    else:
        log.debug("No query was specified")
    if json_query is not None:
        json_struct = json.loads(json_query)
    elif galaxy_parameters_file:
        log.debug("Using input Galaxy JSON parameters from:\n%s",
                  galaxy_parameters_file)
        with open(galaxy_parameters_file) as json_fp:
            galaxy_json = json.load(json_fp)
            json_struct = {}
            for fv_item in galaxy_json['factor_value_series']:
                json_struct[fv_item['factor_name']] = fv_item['factor_value']
    else:
        log.debug("No query was specified")
        json_struct = None
    factor_selection = json_struct
    result = slice_data_files(input_path, factor_selection=factor_selection)
    data_files = result
    log.debug("Result data files list: %s", data_files)
    if data_files is None:
        raise RuntimeError("Error getting data files with isatools")
    output_path = next(iter(output_path))
    log.debug("copying data files to %s", output_path)
    for result in data_files:
        for data_file_name in result['data_files']:
            logging.info("Copying {}".format(data_file_name))
            shutil.copy(os.path.join(input_path, data_file_name), output_path)
    log.info("Finished writing data files to {}".format(output_path))


def slice_data_files(dir, factor_selection=None):
    """Slices ISA-Tab tables based on a factor selection

    :param dir: Path to the ISA-Tab table files (study-sample and assay files)
    :param factor_selection: Factor selection as JSON, given by k:v as
    factor name as keys and factor values as values
    :return: Slice results as a JSON
    """
    results = []
    # first collect matching samples
    for table_file in glob.iglob(os.path.join(dir, '[a|s]_*')):
        log.info('Loading {table_file}'.format(table_file=table_file))

        with open(os.path.join(dir, table_file)) as fp:
            df = load_table(fp)

            if factor_selection is None:
                matches = df['Sample Name'].items()

                for indx, match in matches:
                    sample_name = match
                    if len([r for r in results if r['sample'] == sample_name]) == 1:
                        continue
                    else:
                        results.append(
                            {
                                'sample': sample_name,
                                'data_files': []
                            }
                        )

            else:
                for factor_name, factor_value in factor_selection.items():
                    if 'Factor Value[{}]'.format(factor_name) in list(
                            df.columns.values):
                        matches = df.loc[df['Factor Value[{factor}]'.format(
                            factor=factor_name)] == factor_value][
                            'Sample Name'].items()

                        for indx, match in matches:
                            sample_name = match
                            if len([r for r in results if r['sample'] == sample_name]) == 1:
                                continue
                            else:
                                results.append(
                                    {
                                        'sample': sample_name,
                                        'data_files': [],
                                        'query_used': factor_selection
                                    }
                                )

    # now collect the data files relating to the samples
    for result in results:
        sample_name = result['sample']

        for table_file in glob.iglob(os.path.join(dir, 'a_*')):
            with open(table_file) as fp:
                df = load_table(fp)

                data_files = []

                table_headers = list(df.columns.values)
                sample_rows = df.loc[df['Sample Name'] == sample_name]

                data_node_labels = ['Raw Data File', 'Raw Spectral Data File',
                                    'Derived Spectral Data File',
                                    'Derived Array Data File',
                                    'Array Data File',
                                    'Protein Assignment File',
                                    'Peptide Assignment File',
                                    'Post Translational Modification '
                                    'Assignment File',
                                    'Acquisition Parameter Data File',
                                    'Free Induction Decay Data File',
                                    'Derived Array Data Matrix File',
                                    'Image File',
                                    'Derived Data File',
                                    'Metabolite Assignment File']
                for node_label in data_node_labels:
                    if node_label in table_headers:
                        data_files.extend(list(sample_rows[node_label]))

                result['data_files'] = [i for i in list(data_files) if
                                        str(i) != 'nan']
    return results


def isatab_get_factor_names_command(input_path, output):
    """Get the list of factors for an ISA-Tab study

    :param input_path: Path to an ISA-Tab
    :param output: File-like buffer object to write JSON results to
    :return: None
    """
    log.info("Getting factors for study %s. Writing to %s.",
             input_path, output.name)
    _RX_FACTOR_VALUE = re.compile(r'Factor Value\[(.*?)\]')
    factors = set()
    for table_file in glob.iglob(os.path.join(input_path, '[a|s]_*')):
        with open(os.path.join(input_path, table_file)) as fp:
            df = load_table(fp)

            factors_headers = [header for header in list(df.columns.values)
                               if _RX_FACTOR_VALUE.match(header)]

            for header in factors_headers:
                factors.add(header[13:-1])
    if factors is not None:
        json.dump(list(factors), output, indent=4)
        log.debug("Factor names written")
    else:
        raise RuntimeError("Error reading factors.")


def isatab_get_factor_values_command(input_path, factor, output):
    """Get the list of factor values for a given factor in an ISA-Tab study

        :param input_path: Path to an ISA-Tab
        :param factor: A string of the factor of interest
        :param output: File-like buffer object to write JSON results to
        :return: None
        """
    log.info("Getting values for factor {factor} in study {input_path}. "
             "Writing to {output_file}."
             .format(factor=factor, input_path=input_path,
                     output_file=output.name))
    fvs = set()

    factor_name = factor

    for table_file in glob.iglob(os.path.join(input_path, '[a|s]_*')):
        with open(os.path.join(input_path, table_file)) as fp:
            df = load_table(fp)

            if 'Factor Value[{factor}]'.format(factor=factor_name) in \
                    list(df.columns.values):
                for _, match in df[
                    'Factor Value[{factor}]'.format(
                        factor=factor_name)].iteritems():
                    try:
                        match = match.item()
                    except AttributeError:
                        pass

                    if isinstance(match, (str, int, float)):
                        if str(match) != 'nan':
                            fvs.add(match)
    if fvs is not None:
        json.dump(list(fvs), output, indent=4)
        log.debug("Factor values written to {}".format(output))
    else:
        raise RuntimeError("Error getting factor values")


def filter_data(input_path, output_path, slice, filename_filter):
    """Filters and extracts the data files based on a slice query and
    filename filter

    :param input_path: Path to the ISA-Tab directory or investigation file
    file-like buffer object
    :param output_path: Path to an output directory in which to copy the files
    :param slice: Sliced list of data files to copy over
    :param filename_filter: A filename filter using file wildcards, e.g. *.mzml
    :return: None

    Note that this function also writes out a log of what files were copied
    etc. to the file cli.log
    """
    loglines = []
    source_dir = input_path
    if source_dir:
        if not os.path.exists(source_dir):
            raise IOError('Source path does not exist!')
    data_files = []
    slice_json = slice
    for result in json.load(slice_json)['results']:
        data_files.extend(result.get('data_files', []))
    reduced_data_files = list(set(data_files))
    filtered_files = glob.glob(os.path.join(source_dir, filename_filter))
    to_copy = []
    for filepath in filtered_files:
        if os.path.basename(filepath) in reduced_data_files:
            to_copy.append(filepath)
    loglines.append("Using slice results from {}\n".format(slice_json))
    for filepath in to_copy:
        loglines.append("Copying {}\n".format(os.path.basename(filepath)))
        # try:
        #     shutil.copyfile(
        #         filepath, os.path.join(output_path,
        #                                os.path.basename(filepath)))
        # except Exception as e:
        #     log.debug(e)
        #     exit(1)
        try:
            os.symlink(
                filepath, os.path.join(output_path,
                                       os.path.basename(filepath)))
        except Exception as e:
            log.debug(e)
            exit(1)
    with open('cli.log', 'w') as fp:
        fp.writelines(loglines)


def query_isatab(source_dir, output, galaxy_parameters_file=None):
    """Query over an ISA-Tab

    :param source_dir: Input path to ISA-Tab
    :param output: Output file-like buffer object to write output JSON results
    :param galaxy_parameters_file: ISA Slicer 2 inputs as Galaxy tool JSON
    :return: JSON containing the original query and the list of samples and
    data files
    """
    debug = True
    if galaxy_parameters_file:
        galaxy_parameters = json.load(galaxy_parameters_file)
        log.debug('Galaxy parameters:')
        log.debug(json.dumps(galaxy_parameters, indent=4))
    else:
        raise IOError('Could not load Galaxy parameters file!')
    if source_dir:
        if not os.path.exists(source_dir):
            raise IOError('Source path does not exist!')
    query = galaxy_parameters['query']
    if debug:
        log.debug('Query is:')
        log.debug(json.dumps(query, indent=4))  # for debugging only
    if source_dir:
        investigation = load(source_dir)
    else:
        raise IOError("No source dir supplied")
    # filter assays by mt/tt
    matching_assays = []
    mt = query.get('measurement_type').strip()
    tt = query.get('technology_type').strip()
    if mt and tt:
        for study in investigation.studies:
            matching_assays.extend(
                [x for x in study.assays if x.measurement_type.term == mt
                 and x.technology_type.term == tt])
    elif mt and not tt:
        for study in investigation.studies:
            matching_assays.extend(
                [x for x in study.assays if x.measurement_type.term == mt])
    elif not mt and tt:
        for study in investigation.studies:
            matching_assays.extend(
                [x for x in study.assays if x.technology_type.term == tt])
    else:
        for study in investigation.studies:
            matching_assays.extend(study.assays)
    assay_samples = []
    for assay in matching_assays:
        assay_samples.extend(assay.samples)
    if debug:
        log.debug('Total samples: {}'.format(len(assay_samples)))

    # filter samples by fv
    factor_selection = {
        x.get('factor_name').strip(): x.get('factor_value').strip() for x in
        query.get('factor_selection', [])}

    fv_samples = set()
    if factor_selection:
        samples_to_remove = set()
        for f, v in factor_selection.items():
            for sample in assay_samples:
                for fv in [x for x in sample.factor_values if
                           x.factor_name.name == f]:
                    if isinstance(fv.value, OntologyAnnotation):
                        if fv.value.term == v:
                            fv_samples.add(sample)
                    elif fv.value == v:
                        fv_samples.add(sample)
        for f, v in factor_selection.items():
            for sample in fv_samples:
                for fv in [x for x in sample.factor_values if
                           x.factor_name.name == f]:
                    if isinstance(fv.value, OntologyAnnotation):
                        if fv.value.term != v:
                            samples_to_remove.add(sample)
                    elif fv.value != v:
                        samples_to_remove.add(sample)
        final_fv_samples = fv_samples.difference(samples_to_remove)
    else:
        final_fv_samples = assay_samples

    # filter samples by characteristic
    characteristics_selection = {
        x.get('characteristic_name').strip():
            x.get('characteristic_value').strip() for x in
        query.get('characteristics_selection', [])}

    cv_samples = set()
    if characteristics_selection:
        first_pass = True
        samples_to_remove = set()
        for c, v in characteristics_selection.items():
            if first_pass:
                for sample in final_fv_samples:
                    for cv in [x for x in sample.characteristics if
                               x.category.term == c]:
                        if isinstance(cv.value, OntologyAnnotation):
                            if cv.value.term == v:
                                cv_samples.add(sample)
                        elif cv.value == v:
                            cv_samples.add(sample)
                    for source in sample.derives_from:
                        for cv in [x for x in source.characteristics if
                                   x.category.term == c]:
                            if isinstance(cv.value, OntologyAnnotation):
                                if cv.value.term == v:
                                    cv_samples.add(sample)
                            elif cv.value == v:
                                cv_samples.add(sample)
                first_pass = False
            else:
                for sample in cv_samples:
                    for cv in [x for x in sample.characteristics if
                               x.category.term == c]:
                        if isinstance(cv.value, OntologyAnnotation):
                            if cv.value.term != v:
                                samples_to_remove.add(sample)
                        elif cv.value != v:
                            samples_to_remove.add(sample)
                    for source in sample.derives_from:
                        for cv in [x for x in source.characteristics if
                                   x.category.term == c]:
                            if isinstance(cv.value, OntologyAnnotation):
                                if cv.value.term != v:
                                    samples_to_remove.add(sample)
                            elif cv.value != v:
                                samples_to_remove.add(sample)
        final_cv_samples = cv_samples.difference(samples_to_remove)
    else:
        final_cv_samples = final_fv_samples

    # filter samples by process parameter
    parameters_selection = {
        x.get('parameter_name').strip():
            x.get('parameter_value').strip() for x in
        query.get('parameter_selection', [])}

    final_samples = final_cv_samples

    if debug:
        log.debug('Final number of samples: {}'.format(len(final_samples)))
    results = []
    for sample in final_samples:
        results.append({
            'sample_name': sample.name,
            'data_files': []
        })
    for result in results:
        sample_name = result['sample_name']
        if source_dir:
            table_files = glob.iglob(os.path.join(source_dir, 'a_*'))
        else:
            raise IOError("No source dir supplied")
        for table_file in table_files:
            with open(table_file) as fp:
                df = load_table(fp)
                data_files = []
                table_headers = list(df.columns.values)
                sample_rows = df.loc[df['Sample Name'] == sample_name]
                data_node_labels = [
                    'Raw Data File', 'Raw Spectral Data File',
                    'Derived Spectral Data File',
                    'Derived Array Data File', 'Array Data File',
                    'Protein Assignment File', 'Peptide Assignment File',
                    'Post Translational Modification Assignment File',
                    'Acquisition Parameter Data File',
                    'Free Induction Decay Data File',
                    'Derived Array Data Matrix File', 'Image File',
                    'Derived Data File', 'Metabolite Assignment File']
                if parameters_selection:
                    for p, v in parameters_selection.items():
                        sample_pv_rows = sample_rows.loc[
                            sample_rows['Parameter Value[{}]'.format(p)] == v]
                        for node_label in data_node_labels:
                            if node_label in table_headers:
                                data_files.extend(
                                    list(sample_pv_rows[node_label]))
                    result['data_files'].extend(list(set(
                        i for i in list(data_files) if
                        str(i) not in ('nan', ''))))
                else:
                    for node_label in data_node_labels:
                        if node_label in table_headers:
                            data_files.extend(list(sample_rows[node_label]))
                    result['data_files'].extend(
                        list(set(i for i in list(data_files) if
                                 str(i) not in ('nan', ''))))
    results_json = {
        'query': query,
        'results': results
    }
    json.dump(results_json, output, indent=4)


def get_sources_for_sample(input_path, sample_name):
    """Get the sources for a given sample

    :param input_path: Input path to ISA-tab
    :param sample_name: A sample name
    :return: A list of source names
    """
    ISA = load(input_path)
    hits = []

    for study in ISA.studies:
        for sample in study.samples:
            if sample.name == sample_name:
                log.debug('found a hit: {sample_name}'.format(sample_name=sample.name))

                for source in sample.derives_from:
                    hits.append(source.name)
    return hits


def get_study_groups(input_path):
    """Gets the study groups

    :param input_path: Input path to ISA-tab
    :return: List of study groups
    """
    factors_summary = isatab_get_factors_summary_command(input_path=input_path)
    study_groups = {}

    for factors_item in factors_summary:
        fvs = tuple(factors_item[k]
                    for k in factors_item.keys() if k != 'name')

        if fvs in study_groups.keys():
            study_groups[fvs].append(factors_item['name'])
        else:
            study_groups[fvs] = [factors_item['name']]
    return study_groups


def get_study_groups_samples_sizes(input_path):
    """Computes the sizes of the study groups based on number of samples

    :param input_path: Input path to ISA-tab
    :return: List of tuples of study group and study group sizes
    """
    study_groups = get_study_groups(input_path=input_path)
    return list(map(lambda x: (x[0], len(x[1])), study_groups.items()))


def get_study_groups_data_sizes(input_path):
    """Computes the sizes of the study groups based on number of data files

    :param input_path: Input path to ISA-tab
    :return: List of tuples of study group and study group sizes
    """
    study_groups = get_study_groups(input_path=input_path)
    return list(map(lambda x: (x[0], len(x[1])), study_groups.items()))


def isatab_get_factors_summary_command(input_path, output):
    """Get the summary of factors for an ISA-Tab study

    :param input_path: Path to an ISA-Tab
    :param output: File-like buffer object to write JSON result table
    :return: None
    """
    log.info("Getting summary for study %s. Writing to %s.",
             input_path, output.name)
    ISA = load(input_path)

    all_samples = []
    for study in ISA.studies:
        all_samples.extend(study.samples)

    samples_and_fvs = []

    for sample in all_samples:
        sample_and_fvs = {
            'sample_name': sample.name,
        }

        for fv in sample.factor_values:
            if isinstance(fv.value, (str, int, float)):
                fv_value = fv.value
                sample_and_fvs[fv.factor_name.name] = fv_value
            elif isinstance(fv.value, OntologyAnnotation):
                fv_value = fv.value.term
                sample_and_fvs[fv.factor_name.name] = fv_value

        samples_and_fvs.append(sample_and_fvs)

    df = DataFrame(samples_and_fvs)
    nunique = df.apply(Series.nunique)
    cols_to_drop = nunique[nunique == 1].index

    df = df.drop(cols_to_drop, axis=1)
    summary = df.to_dict(orient='records')
    if summary is not None:
        dump(summary, output, indent=4)
        log.debug("Summary dumped to JSON")
    else:
        raise RuntimeError("Error getting study summary")


def get_data_for_sample(input_path, sample_name):
    """Get the data filenames for a given sample

    :param input_path: Input path to ISA-tab
    :param sample_name: A sample name
    :return: A list of data filenames
    """
    ISA = load(input_path)
    hits = []
    for study in ISA.studies:
        for assay in study.assays:
            for data in assay.data_files:
                if sample_name in [x.name for x in data.generated_from]:
                    log.info('found a hit: {filename}'.format(filename=data.filename))
                    hits.append(data)
    return hits


def get_characteristics_summary(input_path):
    """
        This function generates a characteristics summary for a MetaboLights
        study

        :param input_path: Input path to ISA-tab
        :return: A list of dicts summarising the set of characteristic names
        and values associated with each sample

        Note: it only returns a summary of characteristics with variable
        values.

        Example usage:
            characteristics_summary = \
                get_characteristics_summary('/path/to/my/study/')
            [
                {
                    "name": "6089if_9",
                    "Variant": "Synechocystis sp. PCC 6803.sll0171.ko"
                },
                {
                    "name": "6089if_43",
                    "Variant": "Synechocystis sp. PCC 6803.WT.none"
                },
            ]


        """
    ISA = load(input_path)

    all_samples = []
    for study in ISA.studies:
        all_samples.extend(study.samples)

    samples_and_characs = []
    for sample in all_samples:
        sample_and_characs = {
            'name': sample.name
        }

        for source in sample.derives_from:
            for c in source.characteristics:
                if isinstance(c.value, (str, int, float)):
                    c_value = c.value
                    sample_and_characs[c.category.term] = c_value
                elif isinstance(c.value, OntologyAnnotation):
                    c_value = c.value.term
                    sample_and_characs[c.category.term] = c_value

        samples_and_characs.append(sample_and_characs)

    df = DataFrame(samples_and_characs)
    nunique = df.apply(Series.nunique)
    cols_to_drop = nunique[nunique == 1].index

    df = df.drop(cols_to_drop, axis=1)
    return df.to_dict(orient='records')


def get_study_variable_summary(input_path):
    """Computes the list of variable factors and characteristics found in
    an ISA-Tab

    :param input_path: Path to the ISA-Tab directory or investigation file
    file-like buffer object
    :return: A dictionary representation of the table
    """
    ISA = load(input_path)

    all_samples = []
    for study in ISA.studies:
        all_samples.extend(study.samples)

    samples_and_variables = []
    for sample in all_samples:
        sample_and_vars = {
            'sample_name': sample.name
        }

        for fv in sample.factor_values:
            if isinstance(fv.value, (str, int, float)):
                fv_value = fv.value
                sample_and_vars[fv.factor_name.name] = fv_value
            elif isinstance(fv.value, OntologyAnnotation):
                fv_value = fv.value.term
                sample_and_vars[fv.factor_name.name] = fv_value

        for source in sample.derives_from:
            sample_and_vars['source_name'] = source.name
            for c in source.characteristics:
                if isinstance(c.value, (str, int, float)):
                    c_value = c.value
                    sample_and_vars[c.category.term] = c_value
                elif isinstance(c.value, OntologyAnnotation):
                    c_value = c.value.term
                    sample_and_vars[c.category.term] = c_value

        samples_and_variables.append(sample_and_vars)

    df = DataFrame(samples_and_variables)
    nunique = df.apply(Series.nunique)
    cols_to_drop = nunique[nunique == 1].index

    df = df.drop(cols_to_drop, axis=1)
    return df.to_dict(orient='records')


def get_study_group_factors(input_path):
    """Computes the study groups

    :param input_path: Path to the ISA-Tab directory or investigation file
    file-like buffer object
    :return: List of Factor Value combinations representing the study groups
    """
    factors_list = []

    for table_file in iglob(path.join(input_path, '[a|s]_*')):
        with open(path.join(input_path, table_file)) as fp:
            df = load_table(fp)

            factor_columns = [x for x in df.columns if x.startswith(
                'Factor Value')]
            if len(factor_columns) > 0:
                factors_list = df[factor_columns].drop_duplicates() \
                    .to_dict(orient='records')
    return factors_list


def get_filtered_df_on_factors_list(input_path):
    """Computes the study groups and then prints the groups and sample lists

    :param input_path: Path to the ISA-Tab directory or investigation file
    file-like buffer object
    :return: The queries used to generate the summary
    """

    factors_list = get_study_group_factors(input_path=input_path)
    queries = []

    for item in factors_list:
        query_str = []

        for k, v in item.items():
            k = k.replace(' ', '_').replace('[', '_').replace(']', '_')
            if isinstance(v, str):
                v = v.replace(' ', '_').replace('[', '_').replace(']', '_')
                query_str.append("{k} == '{v}' and ".format(k=k, v=v))

        query_str = ''.join(query_str)[:-4]
        queries.append(query_str)

    for table_file in iglob(path.join(input_path, '[a|s]_*')):
        with open(path.join(input_path, table_file)) as fp:
            df = load_table(fp)

            cols = df.columns
            cols = cols.map(
                lambda x: x.replace(' ', '_') if isinstance(x, str) else x)
            df.columns = cols

            cols = df.columns
            cols = cols.map(
                lambda x: x.replace('[', '_') if isinstance(x, str) else x)
            df.columns = cols

            cols = df.columns
            cols = cols.map(
                lambda x: x.replace(']', '_') if isinstance(x, str) else x)
            df.columns = cols

        for query in queries:
            df2 = df.query(query)  # query uses pandas.eval, which evaluates
            # queries like pure Python notation
            if 'Sample_Name' in df.columns:
                log.debug('Group: {query} / Sample_Name: {sample_name}'.format(
                    query=query, sample_name=list(df2['Sample_Name'])))

            if 'Source_Name' in df.columns:
                log.debug('Group: {} / Sources_Name: {}'.format(
                    query, list(df2['Source_Name'])))

            if 'Raw_Spectral_Data_File' in df.columns:
                log.debug('Group: {query} / Raw_Spectral_Data_File: {filename}'
                          .format(query=query[13:-2],
                                  filename=list(df2['Raw_Spectral_Data_File'])))
    return queries
