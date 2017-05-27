import csv
from isatools.model.v1 import *

idf_map = {
    "MAGE-TAB Version": "magetab_version",
    "Investigation Title": "investigation_title",
    "Investigation Accession": "investigation_accession",
    "Investigation Accession Term Source REF": "investigation_accession_term_source_ref",
    "Experimental Design": "experimental_design",
    "Experimental Design Term Source REF": "experimental_design_term_source_ref",
    "Experimental Design Term Accession Number": "experimental_design_term_accession_number",
    "Experimental Factor Name": "experimental_factor",
    "Experimental Factor Term Source REF": "experimental_factor_term_source_ref",
    "Experimental Factor Term Accession Number": "experimental_factor_term_accession_number",
    
    "Person Last Name": "person_last_name",
    "Person First Name": "person_first_name",
    "Person Mid Initials": "person_mid_initials",
    "Person Email": "person_email",
    "Person Phone": "person_phone",
    "Person Fax": "person_fax",
    "Person Address": "person_address",
    "Person Affiliation": "person_affiliation",
    "Person Roles": "person_roles",
    "Person Roles Term Source REF": "person_roles_term_source_ref",
    "Person Roles Term Accession Number": "person_roles_term_accession_number",

    "Quality Control Type": "quality_control_type",
    "Quality Control Term Source REF": "quality_control_term_source_ref",
    "Quality Control Term Accession Number": "quality_control_term_accession_number",
    "Replicate Type": "replicate_type",
    "Replicate Term Source REF": "replicate_term_source_ref",
    "Replicate Term Accession Number": "replicate_term_accession_number",
    "Normalization Type": "normalization_type",
    "Normalization Term Source REF": "normalization_term_source_ref",
    "Normalization Term Accession Number": "normalization_term_accession_number",
    
    "Date of Experiment": "date_of_experiment",
    "Public Release Date": "public_release_date",

    "PubMed ID": "publication_pubmed_id",
    "Publication DOI": "publication_doi",
    "Publication Author List": "publication_author_list",
    "Publication Title": "publication_title",
    "Publication Status": "publication_status",
    "Publication Status Term Source REF": "publication_status_term_source_ref",
    "Publication Status Term Accession Number": "publication_status_term_accession_number",

    "Experimental Description": "experimental_description",
    
    "Protocol Name": "protocol_name",
    "Protocol Type": "protocol_type",
    "Protocol Term Source REF": "protocol_term_source_ref",
    "Protocol Term Accession Number": "protocol_term_accession_number",
    "Protocol Description": "protocol_description",
    "Protocol Parameters": "protocol_parameters",
    "Protocol Hardware": "protocol_hardware",
    "Protocol Software": "protocol_software",
    "Protocol Contact": "protocol_contact",

    "SDRF File": "sdrf_file",

    "Term Source Name": "term_source_name",
    "Term Source File": "term_source_file",
    "Term Source Version": "term_source_version",

}


def parse(magetab_idf_path):

    idf_dict = {}

    with open(magetab_idf_path, "r", encoding="utf-8") as magetab_idf_file:
        magetab_idf_reader = csv.reader(filter(lambda r: r[0] != '#', magetab_idf_file), dialect='excel-tab')

        for row in magetab_idf_reader:
            if not row[0].startswith("Comment["):
                try:
                    idf_dict[idf_map[row[0]]] = row[1:]
                except KeyError:
                    pass

    ISA = Investigation(identifier="Investigation")

    ontology_source_dict = {}

    v = idf_dict['term_source_name']
    for i in range(0, len(v)):
        ontology_source = OntologySource(name=v[i])
        ontology_source.file = idf_dict['term_source_file'][i]
        ontology_source.version = idf_dict['term_source_version'][i]
        ISA.ontology_source_references.append(ontology_source)
        ontology_source_dict[ontology_source.name] = ontology_source

    S = Study(identifier="Study")

    for k, v in idf_dict.items():
        if k == 'investigation_title' and len([x for x in v if x != '']) == 1:
            ISA.title = v[0]
            S.title = v[0]
        if k == 'experimental_description' and len([x for x in v if x != '']) == 1:
            ISA.description = v[0]
        elif k in ('investigation_accession',
                   'investigation_accession_term_source_ref',
                   'date_of_experiment',
                   'magetab_version') and len([x for x in v if x != '']) == 1:
            S.comments.append(Comment(name=k, value=v[0]))
        elif k == 'experimental_design':
            experimental_design_comment = Comment(name="Experimental Design")
            experimental_design_term_source_ref_comment = Comment(name="Experimental Design Term Source REF")
            experimental_factor_term_accession_number_comment = Comment(name="Experimental Design Term Accession Number")
            experimental_design_comment.value += ';'.join(idf_dict['experimental_design'])
            experimental_design_term_source_ref_comment.value = ';'.join(idf_dict['experimental_design_term_source_ref'])
            if 'experimental_design_term_accession_number' in idf_dict.keys():
                experimental_factor_term_accession_number_comment.value = ';'.join(idf_dict['experimental_design_term_accession_number'])
            S.comments.append(experimental_design_comment)
            S.comments.append(experimental_design_term_source_ref_comment)
            S.comments.append(experimental_factor_term_accession_number_comment)

        elif k == 'public_release_date':
            ISA.public_release_date = v[0]
            S.public_release_date = v[0]
        elif k == 'person_last_name' and len(v) > 0:
            for i in range(0, len(v)):
                p = Person()
                p.last_name = v[i]
                p.first_name = idf_dict['person_first_name'][i]
                p.last_name = idf_dict['person_last_name'][i]
                p.mid_initials = idf_dict['person_mid_initials'][i]
                p.email = idf_dict['person_email'][i]
                p.phone = idf_dict['person_phone'][i]
                p.fax = idf_dict['person_fax'][i]
                p.address = idf_dict['person_address'][i]
                p.affiliation = idf_dict['person_affiliation'][i]
                roles_list = idf_dict['person_roles'][i].split(';')
                roles_term_source_ref_list = idf_dict['person_roles_term_source_ref'][i].split(';')
                if 'person_roles_term_accession_number' in idf_dict.keys():
                    roles_term_accession_number_list = idf_dict['person_roles_term_accession_number'][i].split(';')
                for j, term in enumerate(roles_list):
                    role = OntologyAnnotation(term=term)
                    role_term_source_ref = roles_term_source_ref_list[j]
                    if role_term_source_ref != '':
                        role.term_source = ontology_source_dict[role_term_source_ref]
                    if 'person_roles_term_accession_number' in idf_dict.keys():
                        role.term_accession = roles_term_accession_number_list[j]
                    p.roles.append(role)
                S.contacts.append(p)
        elif k == 'publication_pubmed_id' and len(v) > 0:
            for i in range(0, len(v)):
                p = Publication()
                p.pubmed_id = v[i]
                p.doi = idf_dict['publication_doi'][i]
                p.author_list = idf_dict['publication_author_list'][i]
                p.title = idf_dict['publication_title'][i]
                p.doi = idf_dict['publication_doi'][i]
                status = OntologyAnnotation(term=idf_dict['publication_status'][i])
                if 'publication_status_term_source_ref' in idf_dict.keys():
                    try:
                        status.term_source = ontology_source_dict[idf_dict['publication_status_term_source_ref'][i]]
                    except IndexError:
                        pass
                    except KeyError:
                        pass
                if 'publication_status_term_accession_number' in idf_dict.keys():
                    status.term_accession = idf_dict['publication_status_term_accession_number'][i]
                p.status = status
                S.publications.append(p)
        elif k == 'protocol_name' and len(v) > 0:
            for i in range(0, len(v)):
                p = Protocol()
                p.name = v[i]
                protocol_type = OntologyAnnotation(term=idf_dict['protocol_type'][i])
                if 'publication_status_term_source_ref' in idf_dict.keys():
                    try:
                        protocol_type.term_source = ontology_source_dict[idf_dict['protocol_term_source_ref'][i]]
                    except IndexError:
                        pass
                    except KeyError:
                        pass
                if 'publication_status_term_accession_number' in idf_dict.keys():
                    protocol_type.term_accession = idf_dict['protocol_term_accession_number'][i]
                p.protocol_type = protocol_type
                p.description = idf_dict['protocol_description'][i]
                # TODO: parse Protocol Parameters
                S.protocols.append(p)
        elif k == 'sdrf_file':
            S.filename = 's_{}'.format(v[0])
            S.assays = [
                Assay(filename='a_{}'.format(v[0]),
                      technology_type=OntologyAnnotation(term='DNA microarray'),
                      measurement_type=OntologyAnnotation(term='protein expression profiling'))
            ]
        ISA.studies = [S]
    return ISA