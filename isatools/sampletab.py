import io
import pandas as pd
import numpy as np
from isatools.model.v1 import *


def read_sampletab_msi(fp):

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
        if normed_line[len(normed_line)-1] == '"':
            normed_line = normed_line[:len(normed_line)-1]
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

    return investigation