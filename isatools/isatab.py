from .model.v1 import Investigation, OntologySourceReference, Publication, Contact, Study, StudyDesignDescriptor, \
    StudyFactor, Assay
from datetime import date
from isatools.io import isatab_parser


def load(isatab_dir):
    # build ISA objects from ISA-Tab ISArchive (zipped or not zipped?)
    print("Reading " + isatab_dir)
    # There is always everything in the Investigation file (for a valid ISATab), but portions can be empty
    isa_tab = isatab_parser.parse(isatab_dir)
    if isa_tab is None:
        raise IOError("There was problem parsing the ISA Tab")
    else:
        investigation = Investigation(
            title=isa_tab.metadata['Investigation Title'],
            description=isa_tab.metadata['Investigation Description'],
            identifier=isa_tab.metadata['Investigation Identifier'],
            submission_date=isa_tab.metadata['Investigation Submission Date'],
            public_release_date=isa_tab.metadata['Investigation Public Release Date'],
        )

    return investigation


def dump(isa_obj, fp):
    s = isa_obj.to_json()
    return s


def loads(s):
    isa_obj = Investigation()
    return isa_obj


def dumps(isa_obj):
    s = isa_obj.to_json()
    return s
