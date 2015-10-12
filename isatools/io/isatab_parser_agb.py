__author__ = 'agbeltran'

import os;
import glob;
import csv;
import collections;

#regular expressions
import re;

from isatools.io.isa_model import InvestigationClass;
from isatools.io.isa_model import AssayTabClass;
from isatools.io.isa_model import StudyAssayTabClass;
from isatools.io.isa_model import NodeRecord;


def ISATabParser(path):
    """
    Parser for ISA-Tab files, the parameter is the path to the ISA-Tab folder.
    """
    if os.path.isdir(path):
        i_filename = glob.glob(os.path.join(path, InvestigationClass.investigation_file_pattern))
        assert len(i_filename) == 1
        path = i_filename[0]
    assert os.path.exists(path), "Did not find investigation file: %s" % path
    investigation_parser = InvestigationParser()
    with open(path, "rU") as in_handle:
        rec = investigation_parser.parse(in_handle)
    #s_parser = AssayParser(isatab_path)
    #rec = s_parser.parse(rec)
    return rec


class InvestigationParser:
    """
    Parse top level investigation files into ISATabClass objects.
    """

    def __init__(self):
        """section headers"""
        self._sections = {
            "ONTOLOGY SOURCE REFERENCE": "ontology_refs",
            "INVESTIGATION": "metadata",
            "INVESTIGATION PUBLICATIONS": "publications",
            "INVESTIGATION CONTACTS": "contacts",
            "STUDY DESIGN DESCRIPTORS": "design_descriptors",
            "STUDY PUBLICATIONS": "publications",
            "STUDY FACTORS": "factors",
            "STUDY ASSAYS" : "assays",
            "STUDY PROTOCOLS" : "protocols",
            "STUDY CONTACTS": "contacts"}
        self._nolist = ["metadata"]

    def parse(self, in_handle):
        line_iterator = self._line_iterator(in_handle)
        # parse top level investigation details
        rec = ISATabClass()
        rec, _ = self._parse_section(rec, line_iterator)
        # parse study information
        while 1:
            study = StudyAssayTabClass()
            study, had_info = self._parse_section(study, line_iterator)
            if had_info:
                rec.studies.append(study)
            else:
                break
        return rec

    def _parse_section(self, rec, line_iterator):
        """
        Parse a section of an ISA-Tab, assigning information to a supplied record.
        """
        had_info = False
        keyvals, section = self._parse_keyvals(line_iterator)
        if keyvals:
            rec.metadata = keyvals[0]
        while section and section[0] != "STUDY":
            had_info = True
            keyvals, next_section = self._parse_keyvals(line_iterator)
            attr_name = self._sections[section[0]]
            if attr_name in self._nolist:
                try:
                    keyvals = keyvals[0]
                except IndexError:
                    keyvals = {}
            setattr(rec, attr_name, keyvals)
            section = next_section
        return rec, had_info

    def _line_iterator(self, in_handle):
        """
        Read tab delimited file, handling ISA-Tab special case headers.
        """
        reader = csv.reader(in_handle, dialect="excel-tab")
        for line in reader:
            if len(line) > 0 and line[0]:
                # check for section headers; all uppercase and a single value
                if line[0].upper() == line[0] and "".join(line[1:]) == "":
                    line = [line[0]]
                yield line

    def _parse_keyvals(self, line_iter):
        """
        Generates a dictionary of key/value pairs from a line with key and values.
        """
        out = None
        line = None
        for line in line_iter:
            if len(line) == 1 and line[0].upper() == line[0]:
                break
            else:
                # setup output dictionaries, trimming off blank columns
                if out is None:
                    while not line[-1]:
                        line = line[:-1]
                    out = [{} for _ in line[1:]]
                # add blank values if the line is stripped
                while len(line) < len(out) + 1:
                    line.append("")
                for i in range(len(out)):
                    out[i][line[0]] = line[i+1].strip()
                line = None
        return out, line




class AssayParser:
    """Parse row oriented metadata associated with study and assay samples.

    This currently does not attempt to be complete, but rather to extract the
    most useful information (in my biased opinion) and represent it simply
    in the record objects.

    This is coded generally, so can be expanded to more cases. It is biased
    towards microarray and next-gen sequencing data.
    """
    def __init__(self, base_file):
        self._dir = os.path.dirname(base_file)
        self._col_quals = ("Performer", "Date", "Unit",
                           "Term Accession Number", "Term Source REF")
        self._col_types = {"attribute": ("Characteristics", "Factor Type",
                                         "Comment", "Label", "Material Type"),
                           "node" : ("Sample Name", "Source Name", "Image File",
                                     "Raw Data File", "Derived Data File"),
                           "node_assay" : ("Extract Name", "Labeled Extract Name",
                                           "Assay Name", "Data Transformation Name",
                                           "Normalization Name"),
                           "processing": ("Protocol REF",)}
        self._synonyms = {"Array Data File" : "Raw Data File",
                          "Derived Array Data File" : "Derived Data File",
                          "Hybridization Assay Name": "Assay Name",
                          "Derived Array Data Matrix File": "Derived Data File",
                          "Raw Spectral Data File": "Raw Data File",
                          "Derived Spectral Data File": "Derived Data File"}

    def parse(self, rec):
        """Retrieve row data from files associated with the ISATabRecord.
        """
        final_studies = []
        for study in rec.studies:
            source_data = self._parse_study(study.metadata["Study File Name"],
                                            ["Sample Name", "Comment[ENA_SAMPLE]"])
            if source_data:
                study.nodes = source_data
                final_assays = []
                for assay in study.assays:
                    cur_assay = AssayTabClass(assay)
                    assay_data = self._parse_study(assay["Study Assay File Name"],
                                                   ["Raw Data File", "Derived Data File",
                                                    "Image File"])
                    cur_assay.nodes = assay_data
                    final_assays.append(cur_assay)
                study.assays = final_assays
                final_studies.append(study)
        rec.studies = final_studies
        return rec

    def _parse_study(self, fname, node_types):
        """Parse study or assay row oriented file around the supplied base node.
        """
        if not os.path.exists(os.path.join(self._dir, fname)):
            return None
        nodes = {}
        with open(os.path.join(self._dir, fname), "rU") as in_handle:
            reader = csv.reader(in_handle, dialect="excel-tab")
            header = self._swap_synonyms(reader.next())
            hgroups = self._collapse_header(header)
            htypes = self._characterize_header(header, hgroups)
            for node_type in node_types:
                try:
                    name_index = header.index(node_type)
                    break
                except ValueError:
                    name_index = None
            assert name_index is not None, "Could not find standard header name: %s in %s" \
                   % (node_types, header)
            for line in reader:
                name = line[name_index]
                try:
                    node = nodes[name]
                except KeyError:
                    node = NodeRecord(name, node_type)
                    node.metadata = collections.defaultdict(set)
                    nodes[name] = node
                attrs = self._line_keyvals(line, header, hgroups, htypes,
                                           node.metadata)
                nodes[name].metadata = attrs
        return dict([(k, self._finalize_metadata(v)) for k, v in nodes.items()])

    def _finalize_metadata(self, node):
        """Convert node metadata back into a standard dictionary and list.
        """
        final = {}
        for key, val in node.metadata.iteritems():
            #val = list(val)
            #if isinstance(val[0], tuple):
            #    val = [dict(v) for v in val]
            final[key] = list(val)
        node.metadata = final
        return node

    def _line_keyvals(self, line, header, hgroups, htypes, out):
        out = self._line_by_type(line, header, hgroups, htypes, out, "attribute",
                                 self._collapse_attributes)
        out = self._line_by_type(line, header, hgroups, htypes, out, "processing",
                                 self._collapse_attributes)
        out = self._line_by_type(line, header, hgroups, htypes, out, "node")
        return out

    def _line_by_type(self, line, header, hgroups, htypes, out, want_type,
                      collapse_quals_fn = None):
        """Parse out key value pairs for line information based on a group of values.
        """
        for index, htype in ((i, t) for i, t in enumerate(htypes) if t == want_type):
            col = hgroups[index][0]
            key = self._clean_header(header[col])
            if collapse_quals_fn:
                val = collapse_quals_fn(line, header, hgroups[index])
            else:
                val = line[col]
            out[key].add(val)
        return out

    def _collapse_attributes(self, line, header, indexes):
        """Combine attributes in multiple columns into single named tuple.
        """
        names = []
        vals = []
        pat = re.compile("[\W]+")
        for i in indexes:
            names.append(pat.sub("_", self._clean_header(header[i])))
            vals.append(line[i])
        Attrs = collections.namedtuple('Attrs', names)
        return Attrs(*vals)

    def _clean_header(self, header):
        """Remove ISA-Tab specific information from Header[real name] headers.
        """
        if header.find("[") >= 0:
            header = header.replace("]", "").split("[")[-1]
        # ISATab can start with numbers but this is not supported in
        # the python datastructure, so prefix with isa_ to make legal
        try:
            int(header[0])
            header = "isa_" + header
        except ValueError:
            pass
        return header

    def _characterize_header(self, header, hgroups):
        """Characterize header groups into different data types.
        """
        out = []
        for h in [header[g[0]] for g in hgroups]:
            this_ctype = None
            for ctype, names in self._col_types.iteritems():
                if h.startswith(names):
                    this_ctype = ctype
                    break
            out.append(this_ctype)
        return out

    def _collapse_header(self, header):
        """Combine header columns into related groups.
        """
        out = []
        for i, h in enumerate(header):
            if h.startswith(self._col_quals):
                out[-1].append(i)
            else:
                out.append([i])
        return out

    def _swap_synonyms(self, header):
        return [self._synonyms.get(h, h) for h in header]

