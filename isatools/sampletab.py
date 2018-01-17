"""Functions for reading and writing SampleTab."""
import io
import logging
import numpy as np
import pandas as pd
from io import StringIO
from progressbar import Bar
from progressbar import ETA
from progressbar import ProgressBar
from progressbar import SimpleProgress

from isatools import logging as isa_logging
from isatools.model import *


log = logging.getLogger('isatools')


def _peek(f):
    position = f.tell()
    l = f.readline()
    f.seek(position)
    return l


def _read_tab_section(f, sec_key, next_sec_key=None):
    line = f.readline()
    normed_line = line.rstrip()
    if normed_line[0] == '"':
        normed_line = normed_line[1:]
    if normed_line[len(normed_line) - 1] == '"':
        normed_line = normed_line[:len(normed_line) - 1]
    if not normed_line == sec_key:
        raise IOError("Expected: " + sec_key + " section, but got: " + normed_line)
    memf = io.StringIO()
    while not _peek(f=f).rstrip() == next_sec_key:
        line = f.readline()
        if not line:
            break
        memf.write(line.rstrip() + '\n')
    memf.seek(0)
    return memf


def read_sampletab_msi(fp):

    def _build_msi_df(f):
        f = strip_comments(f)
        df = pd.read_csv(f, names=range(0, 128), sep='\t', engine='python',
                         encoding='utf-8').dropna(axis=1, how='all')  # load MSI section
        df = df.T  # transpose MSI section
        df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
        df.reset_index(inplace=True)  # Reset index so it is accessible as column
        df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
        df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
        return df

    # Read in MSI section into DataFrames first
    msi_df = _build_msi_df(_read_tab_section(
        f=fp,
        sec_key='[MSI]',
        next_sec_key='[SCD]'
    ))
    return msi_df


def get_value(object_column, column_group, object_series, ontology_source_map, unit_categories):

    cell_value = object_series[object_column]

    column_index = list(column_group).index(object_column)

    try:
        offset_1r_col = column_group[column_index + 1]
        offset_2r_col = column_group[column_index + 2]
    except IndexError:
        return cell_value, None

    if offset_1r_col.startswith('Term Source REF') and offset_2r_col.startswith('Term Source ID'):

        value = OntologyAnnotation(term=str(cell_value))

        term_source_value = object_series[offset_1r_col]

        if term_source_value is not '':

            try:
                value.term_source = ontology_source_map[term_source_value]
            except KeyError:
                print('term source: ', term_source_value, ' not found')

        term_accession_value = str(object_series[offset_2r_col])

        if term_accession_value is not '':
            value.term_accession = term_accession_value

        return value, None

    try:
        offset_3r_col = column_group[column_index + 3]
    except IndexError:
        return cell_value, None

    if offset_1r_col.startswith('Unit') and offset_2r_col.startswith('Term Source REF') \
            and offset_3r_col.startswith('Term Source ID'):

        category_key = object_series[offset_1r_col]

        try:
            unit_term_value = unit_categories[category_key]
        except KeyError:
            unit_term_value = OntologyAnnotation(term=category_key)
            unit_categories[category_key] = unit_term_value

            unit_term_source_value = object_series[offset_2r_col]

            if unit_term_source_value is not '':

                try:
                    unit_term_value.term_source = ontology_source_map[unit_term_source_value]
                except KeyError:
                    print('term source: ', unit_term_source_value, ' not found')

            term_accession_value = object_series[offset_3r_col]

            if term_accession_value is not '':
                unit_term_value.term_accession = term_accession_value

        return cell_value, unit_term_value

    else:
        return cell_value, None


def load(FP):

    msi_df = read_sampletab_msi(FP)

    ISA = Investigation()

    for _, row in msi_df[["Term Source Name", "Term Source URI", "Term Source Version"]]\
            .replace('', np.nan).dropna(axis=0, how='all').iterrows():
        ontology_source = OntologySource(name=row["Term Source Name"],
                                         file=row["Term Source URI"],
                                         version=row["Term Source Version"],
                                         description=row["Term Source Name"])
        ISA.ontology_source_references.append(ontology_source)

    row = msi_df[["Submission Title", "Submission Identifier", "Submission Description", "Submission Version",
                  "Submission Reference Layer", "Submission Release Date", "Submission Update Date"]].iloc[0]
    ISA.identifier = row["Submission Identifier"]
    ISA.title = row["Submission Title"]
    ISA.descriptiondescription = row["Submission Description"]
    ISA.submission_date = row["Submission Release Date"]
    ISA.comments = [
        Comment(name="Submission Version", value=row["Submission Version"]),
        Comment(name="Submission Reference Layer", value=row["Submission Reference Layer"]),
        Comment(name="Submission Update Date", value=row["Submission Update Date"]),
    ]

    try:
        for _, row in msi_df[["Person Last Name", "Person First Name", "Person Initials", "Person Email", "Person Role"]].replace('', np.nan).dropna(axis=0, how='all').iterrows():
            person = Person(last_name=row['Person Last Name'],
                            first_name=row['Person First Name'],
                            mid_initials=row['Person Initials'],
                            email=row['Person Email'],
                            roles=[OntologyAnnotation(row['Person Role'])])
            ISA.contacts.append(person)
    except KeyError:
        pass  # skip if no person part of MSI section is present, as in GSB-3.txt

    for i, row in msi_df[
        ["Organization Name", "Organization Address", "Organization URI", "Organization Email",
         "Organization Role"]].replace('', np.nan).dropna(axis=0, how='all').iterrows():
        ISA.comments.extend([
            Comment(name="Organization Name.{}".format(i), value=row["Organization Name"]),
            Comment(name="Organization Address.{}".format(i), value=row["Organization Address"]),
            Comment(name="Organization URI.{}".format(i), value=row["Organization URI"]),
            Comment(name="Organization Email.{}".format(i), value=row["Organization Email"]),
            Comment(name="Organization Role.{}".format(i), value=row["Organization Role"])
        ])

    # Read in SCD section into DataFrame first
    FP = strip_comments(FP)
    scd_df = pd.read_csv(_read_tab_section(f=FP, sec_key='[SCD]'), sep='\t', encoding='utf-8').fillna('')

    study = Study(filename="s_{}.txt".format(ISA.identifier))
    study.protocols = [Protocol(name='sample collection', protocol_type=OntologyAnnotation(term='sample collection'))]
    protocol_map = {
        "sample collection": Protocol(name="sample collection",
                                      protocol_type=OntologyAnnotation(term="sample collection"))
    }
    study.protocols = list(protocol_map.values())
    study.factors = [
        StudyFactor(name="Group Name"),
        StudyFactor(name="Group Accession")
    ]
    sources, samples, processes, characteristic_categories, unit_categories = GenericSampleTabProcessSequenceFactory(
        ontology_sources=ISA.ontology_source_references, study_factors=study.factors).create_from_df(scd_df)
    study.sources = list(sources.values())
    study.samples = list(samples.values())
    study.process_sequence = list(processes.values())
    study.characteristic_categories = list(characteristic_categories.values())
    study.units = list(unit_categories.values())
    for process in study.process_sequence:
        try:
            process.executes_protocol = protocol_map[process.executes_protocol]
        except KeyError:
            try:
                unknown_protocol = protocol_map['unknown']
            except KeyError:
                protocol_map['unknown'] = Protocol(
                    name="unknown protocol",
                    description="This protocol was auto-generated where a protocol could not be determined.")
                unknown_protocol = protocol_map['unknown']
                study.protocols.append(unknown_protocol)
            process.executes_protocol = unknown_protocol
    ISA.studies = [study]
    return ISA


class GenericSampleTabProcessSequenceFactory:

    def __init__(self, ontology_sources=None, study_factors=None):
        self.ontology_sources = ontology_sources
        self.factors = study_factors

    def create_from_df(self, DF):

        if self.ontology_sources is not None:
            ontology_source_map = dict(map(lambda x: (x.name, x), self.ontology_sources))
        else:
            ontology_source_map = {}

        samples = {}
        characteristic_categories = {}
        unit_categories = {}
        processes = {}

        try:
            cproject = DF["Characteristic[project]"].drop_duplicates()
            if len(cproject.index) == 1:
                log.info("{} project type".format(cproject.iloc[0]))
        except KeyError:
            log.info("Assuming default project type")

        try:
            samples.update(dict(map(lambda x: (x, Source(comments=[Comment(name="Sample Accession", value=x)])),
                                    DF["Sample Accession"].loc[DF["Derived From"] == ""].drop_duplicates())))
        except KeyError:
            pass

        try:
            samples.update(dict(map(lambda x: (x, Sample(comments=[Comment(name="Sample Accession", value=x)])),
                                    DF["Sample Accession"].loc[DF["Derived From"] != ""].drop_duplicates())))
        except KeyError:
            pass

        for sample_key in samples.keys():
            sample = samples[sample_key]

            row = DF[DF["Sample Accession"] == sample_key].iloc[0] # there should only be one row with accession
            sample.name = row["Sample Name"]

            if row["Sample Accession"] != "":

                try:
                    category = characteristic_categories["Sample Accession"]
                except KeyError:
                    category = OntologyAnnotation(term="Sample Accession")
                    characteristic_categories["Sample Accession"] = category
                sample.characteristics.append(Characteristic(category=category, value=row["Sample Accession"]))

            if row["Sample Description"] != "":
                try:
                    category = characteristic_categories["Sample Description"]
                except KeyError:
                    category = OntologyAnnotation(term="Sample Description")
                    characteristic_categories["Sample Description"] = category
                sample.characteristics.append(Characteristic(category=category, value=row["Sample Description"]))

            if row["Derived From"] != "":
                try:
                    category = characteristic_categories["Derived From"]
                except KeyError:
                    category = OntologyAnnotation(term="Derived From")
                    characteristic_categories["Derived From"] = category
                sample.characteristics.append(Characteristic(category=category, value=row["Derived From"]))

            try:
                if row["Child Of"] != "":
                    try:
                        category = characteristic_categories["Child Of"]
                    except KeyError:
                        category = OntologyAnnotation(term="Child Of")
                        characteristic_categories["Child Of"] = category
                    sample.characteristics.append(Characteristic(category=category, value=row["Child Of"]))
            except KeyError:
                pass  # skip if Child Of is not present in sample table

            if row["Group Name"] != "":
                if isinstance(sample, Sample):
                    factor_hits = [f for f in self.factors if f.name == "Group Name"]
                    if len(factor_hits) == 1:
                        factor = factor_hits[0]
                    else:
                        raise ValueError("Could not resolve Study Factor from Group Name")
                    fv = FactorValue(factor_name=factor)
                    v = row["Group Name"]
                    fv.value = v
                    sample.factor_values.append(fv)
                else:
                    category_key = "Group Name"
                    try:
                        category = characteristic_categories[category_key]
                    except KeyError:
                        category = OntologyAnnotation(term=category_key)
                        characteristic_categories[category_key] = category
                    characteristic = Characteristic(category=category)
                    v = row["Group Name"]
                    characteristic.value = v

            if row["Group Accession"] != "":
                if isinstance(sample, Sample):
                    factor_hits = [f for f in self.factors if f.name == "Group Accession"]
                    if len(factor_hits) == 1:
                        factor = factor_hits[0]
                    else:
                        raise ValueError("Could not resolve Study Factor from Group Accession")
                    fv = FactorValue(factor_name=factor)
                    v = row["Group Accession"]
                    fv.value = v
                    sample.factor_values.append(fv)
                else:
                    category_key = "Group Accession"
                    try:
                        category = characteristic_categories[category_key]
                    except KeyError:
                        category = OntologyAnnotation(term=category_key)
                        characteristic_categories[category_key] = category
                    characteristic = Characteristic(category=category)
                    v = row["Group Accession"]
                    characteristic.value = v

            for col in [x for x in DF.columns if x.startswith("Characteristic[")]:  # build object map
                category_key = col[15:col.rfind("]")]
                try:
                    category = characteristic_categories[category_key]
                except KeyError:
                    category = OntologyAnnotation(term=category_key)
                    characteristic_categories[category_key] = category

                characteristic = Characteristic(category=category)

                v, u = get_value(col, DF.columns, row, ontology_source_map, unit_categories)

                characteristic.value = v
                characteristic.unit = u

                sample.characteristics.append(characteristic)

            sample_accession = row["Derived From"]

            try:
                source = samples[sample_accession]
                sample.derives_from.append(source)
            except KeyError:
                pass

        sample_collection_protocol = "sample collection"

        for _, row in DF[["Sample Accession", "Derived From"]].iterrows():
            sample_accession = row["Sample Accession"]
            sample = samples[sample_accession]
            derived_from_accession = row["Derived From"]
            if derived_from_accession == "":
                continue
            derived_from_sample = samples[derived_from_accession]
            sample.derived_from = derived_from_sample
            process_key = ":".join([derived_from_accession, sample_collection_protocol])
            try:
                process = processes[process_key]
            except KeyError:
                process = Process(executes_protocol=sample_collection_protocol)
                processes[process_key] = process
            if derived_from_sample not in process.inputs:
                process.inputs.append(derived_from_sample)
            if sample not in process.outputs:
                process.outputs.append(sample)

        sources = dict([x for x in samples.items() if isinstance(x[1], Source)])
        study_samples = dict([x for x in samples.items() if isinstance(x[1], Sample)])
        return sources, study_samples, processes, characteristic_categories, unit_categories


def dumps(investigation):

    # build MSI section

    metadata_DF = pd.DataFrame(columns=("Submission Title", "Submission Identifier", "Submission Description",
                               "Submission Version", "Submission Reference Layer", "Submission Release Date",
                                        "Submission Update Date"))
    iversion_hits = [x for x in investigation.comments if x.name == "Submission Version"]
    if len(iversion_hits) == 1:
        investigation_version = iversion_hits[0].value
    else:
        investigation_version = ""
    ireference_layer_hits = [x for x in investigation.comments if x.name == "Submission Reference Layer"]
    if len(ireference_layer_hits) == 1:
        investigation_reference_layer = ireference_layer_hits[0].value
    else:
        investigation_reference_layer = ""
    iversion_update_date = [x for x in investigation.comments if x.name == "Submission Update Date"]
    if len(iversion_update_date) == 1:
        investigation_update_date = iversion_update_date[0].value
    else:
        investigation_update_date = ""
    metadata_DF.loc[0] = [
        investigation.title,
        investigation.identifier,
        investigation.description,
        investigation_version,
        investigation_reference_layer,
        investigation.submission_date,
        investigation_update_date
    ]

    org_DF = pd.DataFrame(columns=("Organization Name", "Organization Address", "Organization URI",
                                   "Organization Email", "Organization Role"))
    org_name_hits = [x for x in investigation.comments if x.name.startswith("Organization Name")]
    org_address_hits = [x for x in investigation.comments if x.name.startswith("Organization Address")]
    org_uri_hits = [x for x in investigation.comments if x.name.startswith("Organization URI")]
    org_email_hits = [x for x in investigation.comments if x.name.startswith("Organization Email")]
    org_role_hits = [x for x in investigation.comments if x.name.startswith("Organization Role")]
    for i, org_name in enumerate(org_name_hits):
        try:
            org_name = org_name_hits[i].value
        except IndexError:
            org_name = ""
        try:
            org_address = org_address_hits[i].value
        except IndexError:
            org_address = ""
        try:
            org_uri = org_uri_hits[i].value
        except IndexError:
            org_uri = ""
        try:
            org_email = org_email_hits[i].value
        except IndexError:
            org_email = ""
        try:
            org_role = org_role_hits[i].value
        except IndexError:
            org_role = ""
        org_DF.loc[i] = [
            org_name,
            org_address,
            org_uri,
            org_email,
            org_role
        ]

    people_DF = pd.DataFrame(columns=("Person Last Name", "Person Initials", "Person First Name", "Person Email",
                                      "Person Role"))
    for i, contact in enumerate(investigation.contacts):
        if len(contact.roles) == 1:
            role = contact.roles[0].term
        else:
            role = ""
        people_DF.loc[i] = [
            contact.last_name,
            contact.mid_initials,
            contact.first_name,
            contact.email,
            role
        ]

    term_sources_DF = pd.DataFrame(columns=("Term Source Name", "Term Source URI", "Term Source Version"))
    for i, term_source in enumerate(investigation.ontology_source_references):
        term_sources_DF.loc[i] = [
            term_source.name,
            term_source.file,
            term_source.version
        ]
    msi_DF = pd.concat([metadata_DF, org_DF, people_DF, term_sources_DF], axis=1)
    msi_DF = msi_DF.set_index("Submission Title").T
    msi_DF = msi_DF.replace('', np.nan)
    msi_memf = StringIO()
    msi_DF.to_csv(path_or_buf=msi_memf, index=True, sep='\t', encoding='utf-8', index_label="Submission Title")
    msi_memf.seek(0)

    scd_DF = pd.DataFrame(columns=("Sample Name", "Sample Accession", "Sample Description", "Derived From",
                                   "Group Name", "Group Accession"))

    all_samples = []
    for study in investigation.studies:
        all_samples += study.sources
        all_samples += study.samples

    all_samples = list(set(all_samples))
    if isa_logging.show_pbars:
        pbar = ProgressBar(min_value=0, max_value=len(all_samples),
                           widgets=['Writing {} samples: '.format(len(all_samples)), SimpleProgress(),
                                    Bar(left=" |", right="| "), ETA()]).start()
    else:
        pbar = lambda x: x
    for i, s in pbar(enumerate(all_samples)):
        derived_from = ""
        if isinstance(s, Sample) and s.derives_from is not None:
            if len(s.derives_from) == 1:
                derived_from_obj = s.derives_from[0]
                derives_from_accession_hits = [x for x in derived_from_obj.characteristics
                                               if x.category.term == "Sample Accession"]
                if len(derives_from_accession_hits) == 1:
                    derived_from = derives_from_accession_hits[0].value
                else:
                    log.warning("WARNING! No Sample Accession available so referencing Derived From relation using "
                             "Sample Name \"{}\" instead".format(derived_from_obj.name))
                    derived_from = derived_from_obj.name
        sample_accession_hits = [x for x in s.characteristics if x.category.term == "Sample Accession"]
        if len(sample_accession_hits) == 1:
            sample_accession = sample_accession_hits[0].value
        else:
            sample_accession = ""
        sample_description_hits = [x for x in s.characteristics if x.category.term == "Sample Description"]
        if len(sample_description_hits) == 1:
            sample_description = sample_description_hits[0].value
        else:
            sample_description = ""

        if isinstance(s, Sample):
            group_name_hits = [x for x in s.factor_values if x.factor_name.name == "Group Name"]
            if len(group_name_hits) == 1:
                group_name = group_name_hits[0].value
            else:
                group_name = ""
            group_accession_hits = [x for x in s.factor_values if x.factor_name.name == "Group Accession"]
            if len(group_accession_hits) == 1:
                group_accession = group_accession_hits[0].value
            else:
                group_accession = ""
        else:
            group_name_hits = [x for x in s.characteristics if x.category.term == "Group Name"]
            if len(group_name_hits) == 1:
                group_name = group_name_hits[0].value
            else:
                group_name = ""
            group_accession_hits = [x for x in s.characteristics if x.category.term == "Group Accession"]
            if len(group_accession_hits) == 1:
                group_accession = group_accession_hits[0].value
            else:
                group_accession = ""

        scd_DF.loc[i, "Sample Name"] = s.name
        scd_DF.loc[i, "Sample Accession"] = sample_accession
        scd_DF.loc[i, "Sample Description"] = sample_description
        scd_DF.loc[i, "Derived From"] = derived_from
        scd_DF.loc[i, "Group Name"] = group_name
        scd_DF.loc[i, "Group Accession"] = group_accession

        characteristics = [x for x in s.characteristics if x.category.term not in ["Sample Description",
                                                                                   "Derived From",
                                                                                   "Sample Accession"]]
        for characteristic in characteristics:
            characteristic_label = "Characteristic[{}]".format(characteristic.category.term)
            if characteristic_label not in scd_DF.columns:
                scd_DF[characteristic_label] = ""
                for val_col in get_value_columns(characteristic_label, characteristic):
                    scd_DF[val_col] = ""
            if isinstance(characteristic.value, (int, float)) and characteristic.unit:
                if isinstance(characteristic.unit, OntologyAnnotation):
                    scd_DF.loc[i, characteristic_label] = characteristic.value
                    scd_DF.loc[i, characteristic_label + ".Unit"] = characteristic.unit.term
                    scd_DF.loc[i, characteristic_label + ".Unit.Term Source REF"]\
                        = characteristic.unit.term_source.name if characteristic.unit.term_source else ""
                    scd_DF.loc[i, characteristic_label + ".Unit.Term Accession Number"] = \
                        characteristic.unit.term_accession
                else:
                    scd_DF.loc[i, characteristic_label] = characteristic.value
                    scd_DF.loc[i, characteristic_label + ".Unit"] = characteristic.unit
            elif isinstance(characteristic.value, OntologyAnnotation):
                scd_DF.loc[i, characteristic_label] = characteristic.value.term
                scd_DF.loc[i, characteristic_label + ".Term Source REF"] = \
                    characteristic.value.term_source.name if characteristic.value.term_source else ""
                scd_DF.loc[i, characteristic_label + ".Term Accession Number"] = \
                    characteristic.value.term_accession
            else:
                scd_DF.loc[i, characteristic_label] = characteristic.value

    scd_DF = scd_DF.replace('', np.nan)
    columns = list(scd_DF.columns)
    for i, col in enumerate(columns):
        if col.endswith("Term Source REF"):
            columns[i] = "Term Source REF"
        elif col.endswith("Term Accession Number"):
            columns[i] = "Term Source ID"
        elif col.endswith("Unit"):
            columns[i] = "Unit"
    scd_DF.columns = columns
    scd_memf = StringIO()
    scd_DF.to_csv(path_or_buf=scd_memf, index=False, sep='\t', encoding='utf-8')
    scd_memf.seek(0)

    sampletab_memf = StringIO()
    sampletab_memf.write("[MSI]\n")
    for line in msi_memf:
        sampletab_memf.write(line.rstrip() + '\n')
    sampletab_memf.write("[SCD]\n")
    for line in scd_memf:
        sampletab_memf.write(line.rstrip() + '\n')
    sampletab_memf.seek(0)

    return sampletab_memf.read()


def dump(investigation, out_fp):
    sampletab_str = dumps(investigation)
    out_fp.write(sampletab_str)


def get_value_columns(label, x):
    if isinstance(x.value, (int, float)) and x.unit:
        if isinstance(x.unit, OntologyAnnotation):
            return map(lambda x: "{0}.{1}".format(label, x),
                       ["Unit", "Unit.Term Source REF", "Unit.Term Accession Number"])
        else:
            return ["{0}.Unit".format(label)]
    elif isinstance(x.value, OntologyAnnotation):
        return map(lambda x: "{0}.{1}".format(label, x), ["Term Source REF", "Term Accession Number"])
    else:
        return []


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
