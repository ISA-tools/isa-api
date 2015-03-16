
import os;
import glob;

ISASyntax = {
    "ONTOLOGY SOURCE REFERENCE": "ontology_refs",
    "INVESTIGATION": "metadata",
    "INVESTIGATION PUBLICATIONS": "publications",
    "INVESTIGATION CONTACTS": "contacts",
    "STUDY DESIGN DESCRIPTORS": "design_descriptors",
    "STUDY PUBLICATIONS": "publications",
    "STUDY FACTORS": "factors",
    "STUDY ASSAYS" : "assays",
    "STUDY PROTOCOLS" : "protocols",
    "STUDY CONTACTS": "contacts"
}


investigation_file_pattern = "i_*.txt"

def isatab_parser(isatab_path):
    """
    Parser for ISA-Tab files, the parameter is the path to the ISA-Tab folder.
    """
    if os.path.isdir(isatab_path):
        i_filename = glob.glob(os.path.join(isatab_path, investigation_file_pattern))
        assert len(i_filename) == 1
        isatab_path = i_filename[0]
    assert os.path.exists(isatab_path), "Did not find investigation file: %s" % isatab_path
    i_parser = investigation_parser()
    #with open(isatab_path, "rU") as in_handle:
    #    rec = i_parser.parse(in_handle)
    #s_parser = assay_parser(isatab_path)
    #rec = s_parser.parse(rec)
    #return rec


def investigation_parser(isatab_path):



#def assay_parser(isatab_path):
