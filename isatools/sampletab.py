import io
import pandas as pd
import numpy as np
from isatools.model.v1 import *


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
        import numpy as np
        df = pd.read_csv(f, names=range(0, 64), sep='\t').dropna(axis=1, how='all') # load MSI section
        df = df.T  # transpose MSI section
        df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
        df.reset_index(inplace=True)  # Reset index so it is accessible as column
        df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
        df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
        return df

    # Read in investigation file into DataFrames first
    msi_df = _build_msi_df(_read_tab_section(
        f=fp,
        sec_key='[MSI]',
        next_sec_key='[SCD]'
    ))
    return msi_df


def get_value(object_column, column_group, object_series, ontology_source_map, unit_categories):

    cell_value = object_series[object_column]

    # if cell_value == '':
    #     return cell_value, None

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

    ontology_source_map = dict(map(lambda x: (x.name, x), ISA.ontology_source_references))

    row = msi_df[["Submission Title", "Submission Identifier", "Submission Description", "Submission Version",
                  "Submission Reference Layer", "Submission Release Date", "Submission Update Date"]].iloc[0]
    ISA.identifier = row["Submission Identifier"]
    ISA.title = row["Submission Title"]
    ISA.description = row["Submission Description"]
    ISA.submission_date = row["Submission Release Date"]
    ISA.comments = [
        Comment(name="Submission Version", value=row["Submission Version"]),
        Comment(name="Submission Reference Layer", value=row["Submission Reference Layer"]),
        Comment(name="Submission Update Date", value=row["Submission Update Date"]),
    ]

    for _, row in msi_df[
        ["Person Last Name", "Person First Name", "Person Initials", "Person Email", "Person Role"]]\
            .replace('', np.nan).dropna(axis=0, how='all').iterrows():
        person = Person(last_name=row['Person Last Name'],
                        first_name=row['Person First Name'],
                        mid_initials=row['Person Initials'],
                        email=row['Person Email'],
                        roles=[OntologyAnnotation(row['Person Role'])])
        ISA.contacts.append(person)

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
    scd_df = pd.read_csv(_read_tab_section(
        f=FP,
        sec_key='[SCD]'
    ), sep='\t').fillna('')

    study = Study(filename="s_{}.txt".format(ISA.identifier))
    study.protocols = [Protocol(name='sample collection', protocol_type=OntologyAnnotation(term='sample collection'))]
    protocol_map = {
        "sample collection": Protocol(name="sample collection",
                                      protocol_type=OntologyAnnotation(term="sample collection"))
    }
    study.protocols = list(protocol_map.values())
    sources, samples, processes, characteristic_categories, unit_categories = GenericSampleTabProcessSequenceFactory(
        ontology_sources=ISA.ontology_source_references, study_factors=study.factors).create_from_df(scd_df)
    study.materials['sources'] = list(sources.values())
    study.materials['samples'] = list(samples.values())
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
    ISA.studies =[study]
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
                print("{} project type".format(cproject.iloc[0]))
        except KeyError:
            print("Assuming default project type")

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

            if row["Derived From"] != "":
                try:
                    category = characteristic_categories["Derived From"]
                except KeyError:
                    category = OntologyAnnotation(term="Derived From")
                    characteristic_categories["Derived From"] = category
                sample.characteristics.append(Characteristic(category=category, value=row["Derived From"]))

            if row["Child Of"] != "":
                try:
                    category = characteristic_categories["Child Of"]
                except KeyError:
                    category = OntologyAnnotation(term="Child Of")
                    characteristic_categories["Child Of"] = category
                sample.characteristics.append(Characteristic(category=category, value=row["Child Of"]))

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
