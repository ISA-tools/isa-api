"""Functions for reading and writing MAGE-TAB."""
from __future__ import absolute_import
import copy
import csv
import logging
import tempfile
import numpy as np
import os
import pandas as pd
import re
from io import StringIO
from itertools import zip_longest


from isatools import isatab
from isatools.model import *


log = logging.getLogger('isatools')


def _get_sdrf_filenames(ISA):
    sdrf_filenames = []
    for study in ISA.studies:
        for assay in [x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]:
            sdrf_filenames.append(study.filename[2:-3] + assay.filename[2:-3] + "sdrf.txt")
    return sdrf_filenames


def _build_metadata_df(ISA):
    metadata_df = pd.DataFrame(columns=(
        "MAGE-TAB Version",
        "Investigation Title",
        "Public Release Date",
        "SDRF File"
    ))
    sdrf_filenames = _get_sdrf_filenames(ISA)
    metadata_df.loc[0] = [
        "1.1",
        ISA.title,
        ISA.public_release_date,
        sdrf_filenames[0]
    ]
    for i, sdrf_filename in enumerate(sdrf_filenames):
        if i == 0:
            pass
        else:
            metadata_df.loc[i] = [
                "",
                "",
                "",
                sdrf_filename
            ]
    return metadata_df


def _build_exp_designs_df(ISA):
    exp_designs_df = pd.DataFrame(columns=(
        "Experimental Design",
        "Experimental Design Term Source REF",
        "Experimental Design Term Accession Number"))
    microarray_study_design = []
    for study in ISA.studies:
        if len([x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]) > 0:
            microarray_study_design.extend(study.design_descriptors)
    for i, design_descriptor in enumerate(microarray_study_design):
        exp_designs_df.loc[i] = [
            design_descriptor.term,
            design_descriptor.term_source.name,
            design_descriptor.term_accession
        ]
    return exp_designs_df


def _build_exp_factors_df(ISA):
    exp_factors_df = pd.DataFrame(columns=(
        "Experimental Factor Name",
        "Experimental Factor Type",
        "Experimental Factor Term Source REF",
        "Experimental Factor Term Accession Number"))
    microarray_study_factors = []
    for study in ISA.studies:
        if len([x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]) > 0:
            microarray_study_factors.extend(study.factors)
    for i, factor in enumerate(microarray_study_factors):
        exp_factors_df.loc[i] = [
            factor.name,
            factor.factor_type.term,
            factor.factor_type.term_source.name if factor.factor_type.term_source else "",
            factor.factor_type.term_accession if factor.factor_type.term_source else ""
        ]
    return exp_factors_df


def _build_roles_str(roles):
    if roles is None:
        roles = list()
    roles_names = ''
    roles_accession_numbers = ''
    roles_source_refs = ''
    for role in roles:
        roles_names += (role.term if role.term else '') + ';'
        roles_accession_numbers += (role.term_accession if role.term_accession else '') + ';'
        roles_source_refs += (role.term_source.name if role.term_source else '') + ';'
    if len(roles) > 0:
        roles_names = roles_names[:-1]
        roles_accession_numbers = roles_accession_numbers[:-1]
        roles_source_refs = roles_source_refs[:-1]
    return roles_names, roles_accession_numbers, roles_source_refs


def _build_people_df(ISA):
    people_df = pd.DataFrame(columns=("Person Last Name",
                                      "Person Mid Initials",
                                      "Person First Name",
                                      "Person Email",
                                      "Person Phone",
                                      "Person Fax",
                                      "Person Address",
                                      "Person Affiliation",
                                      "Person Roles",
                                      "Person Roles Term Source REF",
                                      "Person Roles Term Accession Number"))
    for i, contact in enumerate(ISA.contacts):
        roles_names, roles_accessions, roles_sources = _build_roles_str(contact.roles)
        people_df.loc[i] = [
            contact.last_name,
            contact.mid_initials,
            contact.first_name,
            contact.email,
            contact.phone,
            contact.fax,
            contact.address,
            contact.affiliation,
            roles_names,
            roles_sources,
            roles_accessions
        ]
    return people_df


def _build_protocols_df(ISA):
    protocols_df = pd.DataFrame(columns=('Protocol Name',
                                         'Protocol Type',
                                         'Protocol Term Accession Number',
                                         'Protocol Term Source REF',
                                         'Protocol Description',
                                         'Protocol Parameters',
                                         'Protocol Hardware',
                                         'Protocol Software',
                                         'Protocol Contact'
                                         )
                                )
    microarray_study_protocols = []
    for study in ISA.studies:
        if len([x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]) > 0:
            microarray_study_protocols.extend(study.protocols)
    for i, protocol in enumerate(microarray_study_protocols):
        parameters_names = ''
        parameters_accession_numbers = ''
        parameters_source_refs = ''
        for parameter in protocol.parameters:
            parameters_names += parameter.parameter_name.term + ';'
            parameters_accession_numbers += (
                                            parameter.parameter_name.term_accession if parameter.parameter_name.term_accession is not None else '') + ';'
            parameters_source_refs += (
                                      parameter.parameter_name.term_source.name if parameter.parameter_name.term_source else '') + ';'
        if len(protocol.parameters) > 0:
            parameters_names = parameters_names[:-1]
        if protocol.protocol_type:
            protocol_type_term = protocol.protocol_type.term
            protocol_type_term_accession = protocol.protocol_type.term_accession
            if protocol.protocol_type.term_source:
                protocol_type_term_source_name = protocol.protocol_type.term_source.name
                protocols_df.loc[i] = [
                    protocol.name,
                    protocol_type_term,
                    protocol_type_term_accession,
                    protocol_type_term_source_name,
                    protocol.description,
                    parameters_names,
                    "",
                    "",
                    ""
                ]
    return protocols_df


def _build_term_sources_df(ISA):
    term_sources_df = pd.DataFrame(columns=("Term Source Name", "Term Source File", "Term Source Version"))
    for i, term_source in enumerate(ISA.ontology_source_references):
        term_sources_df.loc[i] = [
            term_source.name,
            term_source.file,
            term_source.version
        ]
    return term_sources_df


def _build_publications_df(ISA):
    publications = ISA.studies[0].publications
    publications_df_cols = ['PubMed ID',
                            'Publication DOI',
                            'Publication Author List',
                            'Publication Title',
                            'Publication Status',
                            'Publication Status Term Accession Number',
                            'Publication Status Term Source REF']
    if len(publications) > 0:
        try:
            for comment in publications[0].comments:
                publications_df_cols.append('Comment[' + comment.name + ']')
        except TypeError:
            pass
    publications_df = pd.DataFrame(columns=tuple(publications_df_cols))
    for i, publication in enumerate(publications):
        if publication.status is not None:
            status_term = publication.status.term
            status_term_accession = publication.status.term_accession
            if publication.status.term_source is not None:
                status_term_source_name = publication.status.term_source.name
            else:
                status_term_source_name = ''
        else:
            status_term = ''
            status_term_accession = ''
            status_term_source_name = ''
        publications_df_row = [
            publication.pubmed_id,
            publication.doi,
            publication.author_list,
            publication.title,
            status_term,
            status_term_accession,
            status_term_source_name,
        ]
        try:
            for comment in publication.comments:
                publications_df_row.append(comment.value)
        except TypeError:
            pass
        publications_df.loc[i] = publications_df_row
    return publications_df


def _build_qc_df(ISA):
    qc_df = pd.DataFrame(columns=(
        "Quality Control Type",
        "Quality Control Term Accession Number",
        "Quality Control Term Source REF"))
    for i, qc_comment in enumerate([x for x in ISA.studies[0].comments if x.name == "Quality Control Type"]):
        qc_df.loc[i] = [
            qc_comment.value,
            "",
            ""
        ]
    return qc_df


def _build_replicates_df(ISA):
    replicates_df = pd.DataFrame(columns=(
        "Replicate Type",
        "Replicate Term Accession Number",
        "Replicate Term Source REF"))
    for i, replicate_comment in enumerate([x for x in ISA.studies[0].comments if x.name == "Replicate Type"]):
        replicates_df.loc[i] = [
            replicate_comment.value,
            "",
            ""
        ]
    return replicates_df


def _build_normalizations_df(ISA):
    normalizations_df = pd.DataFrame(columns=(
        "Normalization Type",
        "Normalization Term Accession Number",
        "Normalization Term Source REF"))
    for i, normalization_comment in enumerate([x for x in ISA.studies[0].comments if x.name == "Normalization Type"]):
        normalizations_df.loc[i] = [
            normalization_comment.value,
            "",
            ""
        ]
    return normalizations_df


def write_idf_file(inv_obj, output_path):
    investigation = inv_obj
    metadata_df = _build_metadata_df(investigation)
    exp_designs_df = _build_exp_designs_df(investigation)
    exp_factors_df = _build_exp_factors_df(investigation)

    qc_df = _build_qc_df(investigation)
    replicates_df = _build_replicates_df(investigation)
    normalizations_df = _build_normalizations_df(investigation)

    people_df = _build_people_df(investigation)
    publications_df = _build_publications_df(investigation)
    protocols_df = _build_protocols_df(investigation)
    term_sources_df = _build_term_sources_df(investigation)

    idf_df = pd.concat([
        metadata_df,
        exp_designs_df,
        exp_factors_df,
        qc_df,
        replicates_df,
        normalizations_df,
        people_df,
        publications_df,
        protocols_df,
        term_sources_df
    ], axis=1)
    idf_df = idf_df.set_index("MAGE-TAB Version").T
    idf_df = idf_df.replace('', np.nan)
    with open(os.path.join(output_path, "{}.idf.txt".format(investigation.identifier if investigation.identifier != "" else investigation.filename[2:-3])), "w", encoding='utf-8') as idf_fp:
        idf_df.to_csv(path_or_buf=idf_fp, index=True, sep='\t', encoding='utf-8', index_label="MAGE-TAB Version")


def write_sdrf_table_files(i, output_path):
    tmp = tempfile.mkdtemp()
    isatab.write_study_table_files(inv_obj=i, output_dir=tmp)
    isatab.write_assay_table_files(inv_obj=i, output_dir=tmp)
    for study in i.studies:
        for assay in [x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]:
            sdrf_filename = study.filename[2:-3] + assay.filename[2:-3] + "sdrf.txt"
            log.debug("Writing {}".format(sdrf_filename))
            try:
                isatab.merge_study_with_assay_tables(os.path.join(tmp, study.filename),
                                                     os.path.join(tmp, assay.filename),
                                                     os.path.join(output_path, sdrf_filename))
            except FileNotFoundError:
                raise IOError("There was a problem merging intermediate ISA-Tab files into SDRF")


def dump(inv_obj, output_path):
    num_microarray_assays = 0
    for study in inv_obj.studies:
        num_microarray_assays += len([x for x in study.assays if x.technology_type.term.lower() == "dna microarray"])

    if num_microarray_assays > 0:
        write_idf_file(inv_obj, output_path=output_path)
        write_sdrf_table_files(i=inv_obj, output_path=output_path)
    else:
        raise IOError("Input must contain at least one assay of type DNA microarray, halt writing MAGE-TAB")
    return inv_obj


inv_to_idf_map = {
            "Study File Name": "SDRF File",
            "Study Title": "Investigation Title",
            "Study Description": "Experiment Description",
            "Study Public Release Date": "Public Release Date",
            "Comment[MAGETAB TimeStamp_Version]": "MAGETAB TimeStamp_Version",
            "Comment[ArrayExpressReleaseDate]": "ArrayExpressReleaseDate",
            "Comment[Date of Experiment]": "Date of Experiment",
            "Comment[AEMIAMESCORE]": "AEMIAMESCORE",
            "Comment[Submitted Name]": "Submitted Name",
            "Comment[ArrayExpressAccession]": "ArrayExpressAccession",
            "Study Design Type": "Experimental Design",
            "Study Design Type Term Accession Number": "Experimental Design Term Accession Number",
            "Study Design Type Ter Source REF": "Experimental Design Term Source REF",
            "Study Factor Name": "Experimental Factor Name",
            "Study Factor Type": "Experimental Factor Type",
            "Study Factor Type Term Accession Number": "Experimental Factor Type Term Accession Number",
            "Study Factor Type Ter Source REF": "Experimental Factor Type Term Source REF",
            "Study PubMed ID": "PubMed ID",
            "Study Publication DOI": "Publication DOI",
            "Study Publication Author List": "Publication Author List",
            "Study Publication Title": "Publication Title",
            "Study Publication Status": "Publication Status",
            "Study Publication Status Term Accession Number": "Publication Status Term Accession Number",
            "Study Publication Status Term Source REF": "Publication Status Term Source REF",
            "Study Person Last Name": "Person Last Name",
            "Study Person First Name": "Person First Name",
            "Study Person Mid Initials": "Person Mid Initials",
            "Study Person Email": "Person Email",
            "Study Person Phone": "Person Phone",
            "Study Person Fax": "Person Fax",
            "Study Person Address": "Person Address",
            "Study Person Affiliation": "Person Affiliation",
            "Study Person Roles": "Person Role",
            "Study Person Roles Term Accession Number": "Person Role Term Accession Number",
            "Study Person Roles Term Source REF": "Person Role Term Source REF",
            "Study Protocol Name": "Protocol Name",
            "Study Protocol Description": "Protocol Description",
            "Study Protocol Parameters": "Protocol Parameters",
            "Study Protocol Type": "Protocol Type",
            "Study Protocol Type Accession Number": "Protocol Term Accession Number",
            "Study Protocol Type Source REF": "Protocol Term Source REF",
            "Comment[Protocol Software]": "Protocol Software",
            "Comment[Protocol Hardware]": "Protocol Hardware",
            "Comment[Protocol Contact]": "Protocol Contact",
            "Term Source Name": "Term Source Name",
            "Term Source File": "Term Source File",
            "Term Source Version": "Term Source Version",
            "Term Source Description": "Term Source Description"
        }  # Relabel these, ignore all other lines


def cast_inv_to_idf(FP):
    # Cut out relevant Study sections from Investigation file
    idf_FP = StringIO()
    for line in FP:
        if line.startswith(tuple(inv_to_idf_map.keys())) or line.startswith("Comment["):
            for k, v in inv_to_idf_map.items():
                line = line.replace(k, v)
            idf_FP.write(line)
    idf_FP.seek(0)
    idf_FP.name = FP.name
    return idf_FP


class MageTabParserException(Exception):
    pass


def squashstr(string):
    nospaces = "".join(string.split())
    return nospaces.lower()


def get_squashed(key):  # for MAGE-TAB spec 2.1.7, deal with variants on labels
    if key is None:
        return ''
    try:
        if squashstr(key[:key.index('[')]) == 'comment':
            return 'comment' + key[key.index('['):]
        else:
            return squashstr(key)
    except ValueError:
        return squashstr(key)


class MageTabParser(object):
    """ The MAGE-TAB parser
    This parses MAGE-TAB IDF and SDRF files into the Python ISA model. It does some best-effort inferences on missing
    metadata required by ISA, but note that outputs may still be incomplete and flag warnings and errors in the ISA
    validators. """

    def __init__(self):
        self.ISA = Investigation(studies=[Study()])
        self._idfdict = {}
        self._ts_dict = {}

    def parse_idf(self, in_filename):
        self.load_into_idfdict(in_filename=in_filename)
        # Parse the ontology sources first, as we need to reference these later
        self.parse_ontology_sources(self._idfdict.get('termsourcename', []),
                                    self._idfdict.get('termsourcefile', []),
                                    self._idfdict.get('termsourceversion', []))
        # Then parse the rest of the sections in blocks; follows order of MAGE-TAB v1.1 2011-07-28 specification
        self.parse_investigation(self._idfdict.get('investigationtitle', []),
                                 self._idfdict.get('investigationaccession', []),
                                 self._idfdict.get('investigationaccessiontermsourceref', []))
        self.parse_experimental_designs(self._idfdict.get('experimentaldesign', []),
                                        self._idfdict.get('experimentaldesigntermsourceref', []),
                                        self._idfdict.get('experimentaldesigntermaccessionnumber', []))
        self.parse_experimental_factors(self._idfdict.get('experimentalfactorname', []),
                                        self._idfdict.get('experimentalfactortype', []),
                                        self._idfdict.get('experimentalfactortypetermsourceref', []),
                                        self._idfdict.get('experimentalfactortypetermaccessionnumber', []))
        self.parse_people(self._idfdict.get('personlastname', []),
                          self._idfdict.get('personfirstname', []),
                          self._idfdict.get('personmidinitials', []),
                          self._idfdict.get('personemail', []),
                          self._idfdict.get('personphone', []),
                          self._idfdict.get('personfax', []),
                          self._idfdict.get('personaddress', []),
                          self._idfdict.get('personaffiliation', []),
                          self._idfdict.get('personroles', []),
                          self._idfdict.get('personrolestermsourceref', []),
                          self._idfdict.get('personrolestermaccessionnumber', []))
        self.parse_dates(self._idfdict.get('dateofexperiment', []), self._idfdict.get('publicreleasedate', []))
        self.parse_publications(self._idfdict.get('pubmedid', []),
                                self._idfdict.get('publicationdoi', []),
                                self._idfdict.get('publicationauthorlist', []),
                                self._idfdict.get('publicationtitle', []),
                                self._idfdict.get('publicationstatus', []),
                                self._idfdict.get('publicationstatustermsourceref', []),
                                self._idfdict.get('publicationstatustermaccessionnumber', []))
        self.parse_experiment_description(self._idfdict.get('experimentdescription'))
        self.parse_protocols(self._idfdict.get('protocolname', []),
                             self._idfdict.get('protocoltype', []),
                             self._idfdict.get('protocoltermsourceref', []),
                             self._idfdict.get('protocoltermaccessionnumber', []),
                             self._idfdict.get('protocoldescription', []),
                             self._idfdict.get('protocolparameters', []),
                             self._idfdict.get('protocolhardware', []),
                             self._idfdict.get('protocolsoftware', []),
                             self._idfdict.get('protocolcontact', []))
        self.parse_sdrf_file(self._idfdict.get('sdrffile', []))
        self.parse_comments({key: self._idfdict[key] for key in [x for x in self._idfdict.keys() if x.startswith('comment[')]})
        self.infer_missing_metadata()
        return self.ISA
    
    def load_into_idfdict(self, in_filename):
        try:
            with open(in_filename, encoding='utf-8') as unicode_file:
                tabreader = csv.reader(filter(lambda r: r[0] != '#', unicode_file), dialect='excel-tab')
                for row in tabreader:
                    key = get_squashed(key=row[0])
                    self._idfdict[key] = row[1:]
        except UnicodeDecodeError:
            with open(in_filename, encoding='ISO8859-2') as latin2_file:
                tabreader = csv.reader(filter(lambda r: r[0] != '#', latin2_file), dialect='excel-tab')
                for row in tabreader:
                    key = get_squashed(key=row[0])
                    self._idfdict[key] = row[1:]

    def parse_ontology_sources(self, names, files, versions):
        for name, file, version in zip_longest(names, files, versions, fillvalue=''):
            if name != '':  # only add if the OS has a name and therefore can be referenced
                os = OntologySource(name=name, file=file, version=version)
                self.ISA.ontology_source_references.append(os)
                self._ts_dict[name] = os

    def parse_investigation(self, titles, accessions, accessiontsrs):
        for title, accession, accessiontsr in zip_longest(titles, accessions, accessiontsrs, fillvalue=''):
            self.ISA.identifier = accession
            self.ISA.title = title
            self.ISA.studies[-1].title = title
            self.ISA.studies[-1].identifier = accession
            if accessiontsr is not None:
                self.ISA.comments.append(Comment(name="Investigation Accession Term Source REF", value=accessiontsr))
            break  # because there should only be one or zero rows

    def parse_experimental_designs(self, designs, tsrs, tans):
        for design, tsr, tan in zip_longest(designs, tsrs, tans, fillvalue=''):
            design_descriptor = OntologyAnnotation(term=design, term_source=self._ts_dict.get(tsr), term_accession=tan)
            if design_descriptor.term != '':  # only add if the DD has a term
                self.ISA.studies[-1].design_descriptors.append(design_descriptor)

    def parse_experimental_factors(self, factors, factortypes, tsrs, tans):
        for factor, factortype, tsr, tan in zip_longest(factors, factortypes, tsrs, tans, fillvalue=''):
            if factor != '':  # only add if there's a factor name
                factortype_oa = OntologyAnnotation(term=factortype, term_source=self._ts_dict.get(tsr), term_accession=tan)
                study_factor = StudyFactor(name=factor, factor_type=factortype_oa)
                self.ISA.studies[-1].factors.append(study_factor)

    def parse_people(self, lastnames, firstnames, midinitialss, emails, phones, faxes, addresses, affiliations, roles,
                     roletans, roletrs):
        for lastname, firstname, midinitials, email, phone, fax, address, affiliation, role, roletan, roletsr in \
                zip_longest(lastnames, firstnames, midinitialss, emails, phones, faxes, addresses, affiliations, roles,
                            roletans, roletrs, fillvalue=''):
            rolesoa = OntologyAnnotation(term=role, term_source=self._ts_dict.get(roletsr), term_accession=roletan)
            person = Person(last_name=lastname, first_name=firstname, mid_initials=midinitials, email=email,
                            phone=phone, fax=fax, address=address, affiliation=affiliation, roles=[rolesoa])
            self.ISA.studies[-1].contacts.append(person)

    def parse_dates(self, dateofexperiments, publicreleasedates):
        for dateofexperiment, publicreleasedate in zip_longest(dateofexperiments, publicreleasedates, fillvalue=''):
            self.ISA.public_release_date = publicreleasedate
            self.ISA.studies[-1].public_release_date = publicreleasedate
            self.ISA.studies[-1].comments.append(Comment(name="Date of Experiment", value=dateofexperiment))
            break  # because there should only be one or zero rows

    def parse_publications(self, pubmedids, dois, authorlists, titles, statuses, statustans, statustsrs):
        for pubmedid, doi, authorlist, title, status, statustsr, statustan in \
                zip_longest(pubmedids, dois, authorlists, titles, statuses, statustans, statustsrs, fillvalue=''):
            if pubmedid != '' or doi != '' or title != '':  # only add if there's a pubmed ID, DOI or title
                statusoa = OntologyAnnotation(term=status, term_source=self._ts_dict.get(statustsr),
                                              term_accession=statustan)
                publication = Publication(pubmed_id=pubmedid, doi=doi, author_list=authorlist, title=title, status=statusoa)
                self.ISA.studies[-1].publications.append(publication)

    def parse_experiment_description(self, descriptions):
        for description in zip_longest(descriptions, fillvalue=''):
            self.ISA.studies[-1].description = description[-1]
            break  # because there should only be one or zero rows

    def parse_protocols(self, names, ptypes, tsrs, tans, descriptions, parameterslists, hardwares, softwares, contacts):
        for name, ptype, tsr, tan, description, parameterslist, hardware, software, contact in \
                zip_longest(names, ptypes, tsrs, tans, descriptions, parameterslists, hardwares, softwares, contacts,
                            fillvalue=''):
            if name != '':  # only add if there's a name
                protocoltype_oa = OntologyAnnotation(term=ptype, term_source=self._ts_dict.get(tsr), term_accession=tan)
                protocol = Protocol(name=name, protocol_type=protocoltype_oa, description=description,
                                    parameters=list(map(lambda x: ProtocolParameter(
                                        parameter_name=OntologyAnnotation(term=x)),
                                                        parameterslist.split(';')
                                                        if parameterslist is not None else '')))
                protocol.comments = [Comment(name="Protocol Hardware", value=hardware),
                                     Comment(name="Protocol Software", value=software),
                                     Comment(name="Protocol Contact", value=contact)]
                self.ISA.studies[-1].protocols.append(protocol)

    def parse_sdrf_file(self, sdrffiles):
        sdrffiles_no_empty = [x for x in sdrffiles if x != '']
        if len(sdrffiles_no_empty) > 0:
            if len(sdrffiles_no_empty) > 1:
                self.ISA.studies[-1].comments.append(Comment(name="SDRF File", value=';'.join(sdrffiles_no_empty)))
            else:
                self.ISA.studies[-1].comments.append(Comment(name="SDRF File", value=sdrffiles_no_empty[0]))

    def parse_comments(self, commentsdict):
        for k, v in commentsdict.items():
            v_no_empty = [x for x in v if x != '']
            if len(v_no_empty) > 0:
                if len(v_no_empty) > 1:
                    v = ';'.join(v_no_empty)
                else:
                    v = v_no_empty[0]
                self.ISA.studies[-1].comments.append(Comment(name=k[8:-1], value=v))

    def infer_missing_metadata(self):
        I = self.ISA
        S = I.studies[-1]

        defaultassay = None
        # first let's try and infer the MT/TT from the study design descriptors, only checks first one
        if len(S.design_descriptors) > 0:
            defaultassay = self._get_measurement_and_tech(S.design_descriptors[0].term)

        # next, go through the loaded comments to see what we can find
        for comment in S.comments:
            commentkey = get_squashed(comment.name)
            # ArrayExpress specific comments
            # (1) if there is no default assay yet, try use AEExperimentType
            if commentkey == 'aeexperimenttype' and defaultassay is None:
                defaultassay = self._get_measurement_and_tech(comment.value)
            # (2) if there is no identifier set, try use ArrayExpressAccession
            if commentkey == 'arrayexpressaccession':
                if I.identifier == '':
                    I.identifier = comment.value
                if S.identifier == '':
                    S.identifier = comment.value
            # (3) if there is no submission date set, try use ArrayExpressSubmissionDate
            if commentkey == 'arrayexpresssubmissiondate':
                if I.submission_date == '':
                    I.submission_date = comment.value
                if S.submission_date == '':
                    S.submission_date = comment.value

        # if there is STILL no defaultassay set, try infer from study title
        if defaultassay is None \
                and ('transcriptionprof' in get_squashed(S.title) or 'geneexpressionprof' in get_squashed(S.title)):
            defaultassay = Assay(measurement_type=OntologyAnnotation(term='transcription profiling'),
                                 technology_type=OntologyAnnotation(term='DNA microarray'),
                                 technology_platform='GeneChip')

        if defaultassay is None:
            defaultassay = Assay()

        # set file names if identifiers are available
        I.filename = 'i_{0}investigation.txt'.format(I.identifier + '_' if I.identifier != '' else I.identifier)
        S.filename = 's_{0}study.txt'.format(S.identifier + '_' if S.identifier != '' else S.identifier)
        defaultassay.filename = 'a_{0}assay.txt'.format(S.identifier + '_' if S.identifier != '' else S.identifier)

        S.assays = [defaultassay]

    @staticmethod
    def _get_measurement_and_tech(design_type):
        assay = None
        if re.match('(?i).*ChIP-Chip.*', design_type):
            assay = Assay(measurement_type=OntologyAnnotation(term='protein-DNA binding site identification'),
                          technology_type=OntologyAnnotation(term='DNA microarray'),
                          technology_platform='ChIP-Chip')
        if re.match('(?i).*RNA-seq.*', design_type) or re.match('(?i).*RNA-Seq.*', design_type) or re.match(
                '(?i).*transcription profiling by high throughput sequencing.*', design_type):
            assay = Assay(measurement_type=OntologyAnnotation(term='transcription profiling'),
                          technology_type=OntologyAnnotation(term='nucleotide sequencing'),
                          technology_platform='RNA-Seq')
        if re.match('.*transcription profiling by array.*', design_type) or re.match('dye_swap_design',
                                                                                     design_type):
            assay = Assay(measurement_type=OntologyAnnotation(term='transcription profiling'),
                          technology_type=OntologyAnnotation(term= 'DNA microarray'),
                          technology_platform='GeneChip')
        if re.match('(?i).*methylation profiling by array.*', design_type):
            assay = Assay(measurement_type=OntologyAnnotation(term='DNA methylation profiling'),
                          technology_type=OntologyAnnotation(term='DNA microarray'),
                          technology_platform='Me-Chip')
        if re.match('(?i).*comparative genomic hybridization by array.*', design_type):
            assay = Assay(measurement_type=OntologyAnnotation(term='comparative genomic hybridization'),
                          technology_type=OntologyAnnotation(term='DNA microarray'),
                          technology_platform='CGH-Chip')
        if re.match('.*genotyping by array.*', design_type):
            assay = Assay(measurement_type=OntologyAnnotation(term='SNP analysis'),
                          technology_type=OntologyAnnotation(term='DNA microarray'),
                          technology_platform='SNPChip')
        if re.match('(?i).*ChIP-Seq.*', design_type) or re.match('(?i).*chip-seq.*', design_type):
            assay = Assay(measurement_type=OntologyAnnotation(term='protein-DNA binding site identification'),
                          technology_type=OntologyAnnotation(term='nucleotide sequencing'),
                          technology_platform='ChIP-Seq')
        if assay is not None:
            assay._design_type = design_type
        return assay

    def parse_sdrf_to_isa_table_files(self, in_filename):
        """ Parses MAGE-TAB SDRF file into ISA-Tab study and assay tables as pandas dataframes"""
        with open(in_filename, encoding='utf-8') as in_fp:
            with strip_comments(in_fp) as fp:
                df = pd.read_csv(fp, dtype=str, sep='\t', encoding='utf-8').fillna('')
            # do some preliminary cleanup of the table
            columns_to_keep = []
            for i, col in enumerate(df.columns):
                if col.lower().startswith('term source ref') and df.columns[i-1].lower().startswith('protocol ref'):
                    pass  # drop term source ref column that appears after protocol ref
                elif col.lower().startswith('term source ref') and df.columns[i-1].lower().startswith('array design ref'):
                    pass  # drop term source ref column that appears after array design ref
                elif col.lower().startswith('technology type'):
                    pass  # drop technology type column / in java code it moves it 1 to the right of assay name column
                elif col.lower().startswith('provider'):
                    pass  # drop provider column
                else:
                    columns_to_keep.append(col)
            df = df[columns_to_keep]  # reset dataframe with only columns we are interested in
            #  TODO: Do we need to replicate what CleanupRunner.java does?

            # now find the first index to split the SDRF into sfile and afile(s)
            cols = [x.lower() for x in list(df.columns)]  # columns all lowered
            if 'sample name' not in cols:  # if we can't find the sample name, we need to insert it somewhere
                first_node_index = -1
                if 'extract name' in cols:
                    first_node_index = cols.index('extract name')
                elif 'labeled extract name' in cols:
                    first_node_index = cols.index('labeled extract name')
                elif 'labeled extract name' in cols:
                    first_node_index = cols.index('hybridization name')
                if first_node_index > 0:  # do Sample Name insertion here
                    cols_ = list(df.columns)
                    df["Sample Name"] = df[cols_[first_node_index]]  # add Sample Name column where first indexed col is
                    cols_.insert(first_node_index, "Sample Name")  # insert to the column index where Sample Name should occur
                    df = df[cols_]  # reset the dataframe with the new order of columns

            # before splitting, let's rename columns where necessary

            df = df.rename(columns={
                "Material Type": "Characteristic[material]",
                "Technology Type": "Comment[technology type]",
                "Hybridization Name": "Hybridization Assay Name"
            })

            # now do the slice
            cols = list(df.columns)
            sample_name_index = cols.index("Sample Name")
            study_df = df[df.columns[0:sample_name_index + 1]].drop_duplicates()
            assay_df = df[df.columns[sample_name_index:]]

            table_files = []
            with StringIO() as assay_fp:
                columns = [x[:x.rindex('.')] if '.' in x else x for x in list(assay_df.columns)]
                assay_df.columns = columns
                assay_df.to_csv(path_or_buf=assay_fp, mode='a', sep='\t', encoding='utf-8', index=False)
                log.info("Trying to split assay file extracted from %s", in_filename)
                assay_fp.seek(0)
                assay_files = self.split_assay(assay_fp)
                log.info("We have %s assays", len(assay_files))

            study_fp = StringIO()
            study_fp.name = self.ISA.studies[-1].filename
            columns = [x[:x.rindex('.')] if '.' in x else x for x in list(study_df.columns)]
            study_df.columns = columns
            study_df.to_csv(path_or_buf=study_fp, mode='a', sep='\t', encoding='utf-8', index=False)
            study_fp.seek(0)
            table_files.append(study_fp)
            table_files.extend(assay_files)
            return table_files

    def split_assay(self, fp):
        assay_files = []
        header = fp.readline()
        chip_seq_records = [header]
        rna_seq_records = [header]
        me_seq_records = [header]
        tf_seq_records = [header]
        genechip_records = [header]
        chipchip_records = [header]

        default_records = [header]

        assay_types = set()

        is_hybridization_assay = 'hybridization' in get_squashed(header)
        contains_antibody_in_header = 'antibody' in get_squashed(header)

        A = self.ISA.studies[-1].assays[-1]

        log.info("Reading assay memory file; mt=%s, tt=%s", A.measurement_type.term, A.technology_type.term)
        for line in fp.readlines():
            sqline = get_squashed(line)
            if A.measurement_type and A.technology_type:
                if 'sequencing' in get_squashed(A.technology_type.term) \
                        and 'protein-dnabindingsiteidentification' == get_squashed(A.measurement_type.term):
                    if not is_hybridization_assay and 'chip-seq' in sqline or 'chipseq' in sqline:
                        assay_types.add('ChIP-Seq')
                        chip_seq_records.append(line)
                    if 'bisulfite-seq' in sqline or 'mre-seq' in sqline or 'mbd-seq' in sqline or 'medip-seq' in sqline:
                        assay_types.add('ME-Seq')
                        me_seq_records.append(line)
                    if 'dnase-hypersensitivity' in sqline or 'mnase-seq' in sqline:
                        assay_types.add('Chromatin-Seq')
                        tf_seq_records.append(line)

            if is_hybridization_assay and ('genomicdna' in sqline or 'genomic_dna' in sqline) and 'mnase-seq' not in sqline:
                assay_types.add('ChIP-Seq')
                chip_seq_records.append(line)

            if hasattr(A, '_design_type'):
                if 'dye_swap_design' == get_squashed(A._design_type):
                    assay_types.add('Hybridization')
                    genechip_records.append(line)

                if 'chip-chipbytilingarray' in get_squashed(A._design_type):
                    assay_types.add('ChIP-chip by tiling array')
                    chipchip_records.append(line)

            if (is_hybridization_assay and not contains_antibody_in_header) and 'rna' in sqline \
                    or 'genomicdna' in sqline:
                assay_types.add('transcription profiling by array')
                genechip_records.append(line)

            if (not is_hybridization_assay and ('genomicdna' in sqline or 'genomic_dna' in sqline)) \
                    and 'mnase-seq' in sqline:
                assay_types.add('ChIP-Seq')
                chip_seq_records.append(line)

            if not is_hybridization_assay and ('rna-seq' in sqline or 'totalrna' in sqline):
                assay_types.add('RNA-Seq')
                rna_seq_records.append(line)

            if is_hybridization_assay and contains_antibody_in_header and ('genomicdna' in sqline or 'chip' in sqline):
                assay_types.add('ChIP-chip')
                chipchip_records.append(line)
            else:
                default_records.append(line)

        log.info("assay_types found: %s", assay_types)

        if len(assay_types) > 0:
            self.ISA.studies[-1].assays = []  # reset the assays list to load new split ones
            for assay_type in assay_types:
                new_A = copy.copy(A)
                if 'transcription profiling by array' in assay_type:
                    new_A.filename = '{0}-{1}.txt'.format(A.filename[:A.filename.rindex('.')], assay_type)
                    new_A.technology_platform = assay_type
                    a_fp = StringIO()
                    a_fp.writelines(genechip_records)
                    a_fp.name = new_A.filename
                    a_fp.seek(0)
                    self.ISA.studies[-1].assays.append(new_A)
                    assay_files.append(a_fp)
                if 'ChIP-chip' in assay_type:
                    new_A.filename = '{0}-{1}.txt'.format(A.filename[:A.filename.rindex('.')], assay_type)
                    new_A.technology_platform = assay_type
                    a_fp = StringIO()
                    a_fp.writelines(chipchip_records)
                    a_fp.name = new_A.filename
                    a_fp.seek(0)
                    self.ISA.studies[-1].assays.append(new_A)
                    assay_files.append(a_fp)
                if 'ChIP-Seq' in assay_type:
                    new_A.filename = '{0}-{1}.txt'.format(A.filename[:A.filename.rindex('.')], assay_type)
                    new_A.technology_platform = assay_type
                    a_fp = StringIO()
                    a_fp.writelines(chip_seq_records)
                    a_fp.name = new_A.filename
                    a_fp.seek(0)
                    self.ISA.studies[-1].assays.append(new_A)
                    assay_files.append(a_fp)
                if 'RNA-Seq' in assay_type:
                    new_A.filename = '{0}-{1}.txt'.format(A.filename[:A.filename.rindex('.')], assay_type)
                    new_A.technology_platform = assay_type
                    a_fp = StringIO()
                    a_fp.writelines(rna_seq_records)
                    a_fp.name = new_A.filename
                    a_fp.seek(0)
                    self.ISA.studies[-1].assays.append(new_A)
                    assay_files.append(a_fp)
                if 'ME-Seq' in assay_type:
                    new_A.filename = '{0}-{1}.txt'.format(A.filename[:A.filename.rindex('.')], assay_type)
                    new_A.technology_platform = assay_type
                    a_fp = StringIO()
                    a_fp.writelines(me_seq_records)
                    a_fp.name = new_A.filename
                    a_fp.seek(0)
                    self.ISA.studies[-1].assays.append(new_A)
                    assay_files.append(a_fp)
                if 'Chromatin-Seq' in assay_type:
                    new_A.filename = '{0}-{1}.txt'.format(A.filename[:A.filename.rindex('.')], assay_type)
                    new_A.technology_platform = assay_type
                    a_fp = StringIO()
                    a_fp.writelines(tf_seq_records)
                    a_fp.name = new_A.filename
                    a_fp.seek(0)
                    self.ISA.studies[-1].assays.append(new_A)
                    assay_files.append(a_fp)
        else:
            a_fp = StringIO()
            a_fp.writelines(default_records)
            a_fp.name = A.filename
            a_fp.seek(0)
            assay_files.append(a_fp)
        return assay_files


def strip_comments(in_fp):
    out_fp = StringIO()
    if not isinstance(in_fp, StringIO):
        out_fp.name = in_fp.name
    for line in in_fp.readlines():
        if line.lstrip().startswith('#'):
            pass
        else:
            out_fp.write(line)
    out_fp.seek(0)
    return out_fp
