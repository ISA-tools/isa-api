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

    investigation = Investigation()

    for _, row in msi_df[["Term Source Name", "Term Source URI", "Term Source Version"]]\
            .replace('', np.nan).dropna(axis=0, how='all').iterrows():
        ontology_source = OntologySource(name=row["Term Source Name"],
                                         file=row["Term Source URI"],
                                         version=row["Term Source Version"],
                                         description=row["Term Source Name"])
        investigation.ontology_source_references.append(ontology_source)

    ontology_source_map = dict(map(lambda x: (x.name, x), investigation.ontology_source_references))

    row = msi_df[["Submission Title", "Submission Identifier", "Submission Description", "Submission Version",
                  "Submission Reference Layer", "Submission Release Date", "Submission Update Date"]].iloc[0]
    investigation.identifier = row["Submission Identifier"]
    investigation.title = row["Submission Title"]
    investigation.description = row["Submission Description"]
    investigation.submission_date = row["Submission Release Date"]
    investigation.comments = [
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
        investigation.contacts.append(person)

    for i, row in msi_df[
        ["Organization Name", "Organization Address", "Organization URI", "Organization Email",
         "Organization Role"]].replace('', np.nan).dropna(axis=0, how='all').iterrows():
        investigation.comments.extend([
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

    sources = {}
    samples = {}
    characteristic_categories = {}
    unit_categories = {}
    processes = {}

    try:
        samples = dict(map(lambda x: (x, Sample(comments=[Comment(name="Sample Accession", value=x)])),
                           scd_df["Sample Accession"].drop_duplicates()))
    except KeyError:
        pass

    study = Study(filename='s_{}.txt'.format(investigation.identifier), samples=list(samples.values()))
    study.protocols = [Protocol(name='sample collection', protocol_type=OntologyAnnotation(term='sample collection'))]
    investigation.studies = [study]

    for _, object_series in scd_df.drop_duplicates().iterrows():

        node_key = object_series["Sample Accession"]
        sample = samples[node_key]

        if sample is not None:

            sample.name = object_series["Sample Name"]
            sample.comments.append(Comment(name="Sample Description", value=object_series['Sample Description']))
            sample.comments.append(Comment(name="Child Of", value=object_series['Child Of']))

            # create Material to Characteristic Material Type
            if len(object_series["Material"]) > 0:
                category_key = "Material Type"
                try:
                    category = characteristic_categories[category_key]
                except KeyError:
                    category = OntologyAnnotation(term=category_key)
                    characteristic_categories[category_key] = category
                characteristic = Characteristic(category=category)
                v, u = get_value("Material", scd_df.columns, object_series, ontology_source_map,
                                 unit_categories)
                characteristic.value = v
                characteristic.unit = u
                sample.characteristics.append(characteristic)

            if len(object_series["Organism"]) > 0:
                category_key = "Organism"
                try:
                    category = characteristic_categories[category_key]
                except KeyError:
                    category = OntologyAnnotation(term=category_key)
                    characteristic_categories[category_key] = category
                characteristic = Characteristic(category=category)
                v, u = get_value("Organism", scd_df.columns, object_series, ontology_source_map,
                                 unit_categories)
                characteristic.value = v
                characteristic.unit = u
                sample.characteristics.append(characteristic)

            if len(object_series["Sex"]) > 0:
                category_key = "Sex"
                try:
                    category = characteristic_categories[category_key]
                except KeyError:
                    category = OntologyAnnotation(term=category_key)
                    characteristic_categories[category_key] = category
                characteristic = Characteristic(category=category)
                v, u = get_value("Sex", scd_df.columns, object_series, ontology_source_map,
                                 unit_categories)
                characteristic.value = v
                characteristic.unit = u
                sample.characteristics.append(characteristic)

            for charac_column in [c for c in scd_df.columns if c.startswith('Characteristic[')]:
                category_key = charac_column[15:-1]

                try:
                    category = characteristic_categories[category_key]
                except KeyError:
                    category = OntologyAnnotation(term=category_key)
                    characteristic_categories[category_key] = category

                characteristic = Characteristic(category=category)

                v, u = get_value(charac_column, scd_df.columns, object_series, ontology_source_map,
                                 unit_categories)

                characteristic.value = v
                characteristic.unit = u

                sample.characteristics.append(characteristic)

            if len(object_series["Derived From"]) > 0:
                try:
                    source = sources[object_series["Derived From"]]
                except KeyError:
                    source_sample = samples[object_series["Derived From"]]
                    source = Source(name=source_sample.name,
                                    characteristics=source_sample.characteristics,
                                    comments=source_sample.comments)
                    sources[source.name] = source
                sample.derives_from.append(source)
                process_key = ":".join([source.name, 'sample collection'])
                try:
                    process = processes[process_key]
                except KeyError:
                    process = Process(executes_protocol=study.protocols[0])
                    processes.update(dict([(process_key, process)]))
                if source.name not in [x.name for x in process.inputs]:
                    process.inputs.append(source)
                if sample.name not in [x.name for x in process.outputs]:
                    process.outputs.append(sample)

            samples[sample.name] = sample

    study.materials['sources'] = list(sources.values())
    study.materials['samples'] = [x for x in list(samples.values()) if x not in list(sources.values())]
    study.process_sequence = list(processes.values())

    return investigation
