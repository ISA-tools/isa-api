"""Parse ISA-Tab structured metadata describing experimental data.
Works with ISA-Tab (http://isatab.sourceforge.net), which provides a structured
format for describing experimental metdata.
The entry point for the module is the parse function, which takes an ISA-Tab
directory (or investigator file) to parse. It returns a ISATabRecord object
which contains details about the investigation. This is top level information
like associated publications and contacts.
This record contains a list of associated studies (ISATabStudyRecord objects).
Each study contains a metadata attribute, which has the key/value pairs
associated with the study in the investigation file. It also contains other
high level data like publications, contacts, and details about the experimental
design.
The nodes attribute of each record captures the information from the Study file.
This is a dictionary, where the keys are sample names and the values are
NodeRecord objects. This collapses the study information on samples, and
contains the associated information of each sample as key/value pairs in the
metadata attribute.
Finally, each study contains a list of assays, as ISATabAssayRecord objects.
Similar to the study objects, these have a metadata attribute with key/value
information about the assay. They also have a dictionary of nodes with data from
the Assay file; in assays the keys are raw data files.
This is a biased representation of the Study and Assay files which focuses on
collapsing the data across the samples and raw data.
"""
from __future__ import with_statement

__author__ = 'brad chapman' #initial version
__author__ = 'agbeltran' #modifications/extensions

import os
import re
import csv
import glob
import collections
import pprint
import bisect
import six
import functools

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rbU')


def find_lt(a, x):
    """Find rightmost value less than x"""
    i = bisect.bisect_left(a, x)
    if i:
        return a[i-1]
    else:
        return -1


def find_gt(a, x):
    """Find leftmost value greater than x"""
    i = bisect.bisect_right(a, x)
    if i != len(a):
        return a[i]
    else:
        return -1

def find_in_between(a, x, y):
    result = []
    while True:
        try:
            element_gt = find_gt(a, x)
        except ValueError:
            return result

        if (element_gt > x and y==-1) or (element_gt > x and element_gt < y):
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


def find_between(a, x, y):
    """Find value a between x and y"""
    result = []
    i = bisect.bisect_right(a, x)
    if i!= len(a):
        while i < len(a):
            result.append(i)
            i+=1
            return result
    raise ValueError

def parse(isatab_ref):
    """Entry point to parse an ISA-Tab directory.
    isatab_ref can point to a directory of ISA-Tab data, in which case we
    search for the investigator file, or be a reference to the high level
    investigation file.
    """
    if os.path.isdir(isatab_ref):
        fnames = glob.glob(os.path.join(isatab_ref, "i_*.txt")) + \
                 glob.glob(os.path.join(isatab_ref, "*.idf.txt"))
        assert len(fnames) == 1
        isatab_ref = fnames[0]
    assert os.path.exists(isatab_ref), "Did not find investigation file: %s" % isatab_ref
    i_parser = InvestigationParser()
    with open(isatab_ref) as in_handle:
        rec = i_parser.parse(in_handle)
    s_parser = StudyAssayParser(isatab_ref)
    rec = s_parser.parse(rec)
    return rec


class InvestigationParser:
    """Parse top level investigation files into ISATabRecord objects.
    """
    def __init__(self):
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
        line_iter = self._line_iter(in_handle)
        # parse top level investigation details
        rec = ISATabRecord()
        rec, _ = self._parse_region(rec, line_iter)

        # parse study information
        while 1:
            study = ISATabStudyRecord()
            study, had_info = self._parse_region(study, line_iter)
            if had_info:
                rec.studies.append(study)
            else:
                break
        # handle SDRF files for MAGE compliant ISATab
        if "SDRF File" in rec.metadata:
            study = ISATabStudyRecord()
            study.metadata["Study File Name"] = rec.metadata["SDRF File"]
            rec.studies.append(study)
        return rec

    def _parse_region(self, rec, line_iter):
        """Parse a section of an ISA-Tab, assigning information to a supplied record.
        """
        had_info = False
        keyvals, section = self._parse_keyvals(line_iter)

        if keyvals:
            rec.metadata = keyvals[0]
        while section and section[0] != "STUDY":
            had_info = True
            keyvals, next_section = self._parse_keyvals(line_iter)
            attr_name = self._sections[section[0]]
            if attr_name in self._nolist:
                try:
                    keyvals = keyvals[0]
                except IndexError:
                    keyvals = {}

            setattr(rec, attr_name, keyvals)
            section = next_section
        return rec, had_info

    def _line_iter(self, in_handle):
        """Read tab delimited file, handling ISA-Tab special case headers.
        """
        reader = csv.reader(in_handle, dialect="excel-tab")
        for line in reader:
            if line and line[0]:
                # check for section headers; all uppercase and a single value
                if line[0].upper() == line[0] and not "".join(line[1:]):
                    line = [line[0]]
                yield line

    def _parse_keyvals(self, line_iter):
        """Generate dictionary from key/value pairs.
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
                for i in six.moves.range(len(out)):
                    out[i][line[0]] = line[i+1].strip()
                line = None
        return out, line


class StudyAssayParser:
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
                                         "Comment", "Label", "Material Type", "Factor Value"),
                           "node" : ("Sample Name", "Source Name", "Image File",
                                     "Raw Data File", "Derived Data File", "Acquisition Parameter Data File",
                                     "Extract Name", "Labeled Extract Name"),
                           "node_assay" : ("Assay Name", "Data Transformation Name",
                                           "Normalization Name"),
                           "processing": ("Protocol REF"),
                           "parameter": ("Parameter Value", "Array Design REF")
                           }
        self._synonyms = {"Array Data File" : "Raw Data File",
                          "Free Induction Decay Data File": "Raw Data File",
                          "Derived Array Data File" : "Derived Data File",
                          "Hybridization Assay Name": "Assay Name",
                          "Scan Name": "Assay Name",
                          "Array Data Matrix File": "Derived Data File",
                          "Derived Array Data Matrix File": "Derived Data File",
                          "Raw Spectral Data File": "Raw Data File",
                          "Derived Spectral Data File": "Derived Data File"}

    def parse(self, rec):
        """Retrieve row data from files associated with the ISATabRecord.
        """
        final_studies = []
        for study in rec.studies:
            source_data = self._parse_study(study.metadata["Study File Name"],
                                            self._col_types["node"])
                                            #["Source Name", "Sample Name", "Comment[ENA_SAMPLE]"])
            if source_data:
                study.nodes = source_data
                final_assays = []
                for assay in study.assays:
                    cur_assay = ISATabAssayRecord(assay)
                    assay_data = self._parse_study(assay["Study Assay File Name"],
                                                   self._col_types["node"])
                    cur_assay.nodes = assay_data
                    assay_process_nodes = self._get_process_nodes(assay["Study Assay File Name"], cur_assay)

                    cur_assay.process_nodes = assay_process_nodes
                    final_assays.append(cur_assay)
                study.assays = final_assays

                #get process nodes
                study_process_nodes = self._get_process_nodes(study.metadata["Study File Name"], study)
                study.process_nodes = study_process_nodes
                final_studies.append(study)
        rec.studies = final_studies
        return rec


    def _get_process_nodes(self, fname, study):
        """Building the process nodes"""
        if not os.path.exists(os.path.join(self._dir, fname)):
            return {}
        process_nodes = {}

        with open(os.path.join(self._dir, fname)) as in_handle:
            reader = csv.reader(in_handle, dialect="excel-tab")
            headers = self._swap_synonyms(next(reader))
            hgroups = self._collapse_header(headers)
            htypes = self._characterize_header(headers, hgroups)
            processing_indices = [i for i, x in enumerate(htypes) if x == "processing"]
            all_parameters_indices = [i for i, x in enumerate(htypes) if x == "parameter"]
            node_indices = [i for i, x in enumerate(htypes) if x == "node"]
            node_assay_indices =  [i for i, x in enumerate(htypes) if x == "node_assay"]
            line_number = 0
            max_number = 0
            process_counters = {}
            assay_name_map = {}
            input_process_map = {}
            output_process_map = {}

            for line in reader:
                    previous_processing_node = None
                    for processing_index in processing_indices:

                        processing_name = line[hgroups[processing_index][0]]
                        if not processing_name:
                            continue
                        next_processing_index = find_gt(processing_indices, processing_index)
                        previous_processing_index = find_lt(processing_indices, processing_index)

                        input_indices = find_in_between(node_indices, previous_processing_index, processing_index)
                        output_indices = find_in_between(node_indices, processing_index, next_processing_index)
                        parameters_indices = find_in_between(all_parameters_indices, processing_index, next_processing_index)
                        assay_name_indices = find_in_between(node_assay_indices, processing_index, next_processing_index)
                        qualifier_indices = hgroups[processing_index][1:]

                        input_headers = [ headers[hgroups[x][0]] for i, x in enumerate(input_indices) ]
                        output_headers = [  headers[hgroups[x][0]] for i, x in enumerate(output_indices) ]
                        processing_header = headers[hgroups[processing_index][0]]

                        qualifier_headers = [  headers[x] for i, x in enumerate(qualifier_indices) ]
                        qualifier_values = [ line[x] for i, x in enumerate(qualifier_indices) ]

                        input_values = [ line[hgroups[x][0]] for i, x in enumerate(input_indices) ]
                        input_node_indices = [ self._build_node_index(input_headers[i],input_values[i]) for i, x in enumerate(input_values) ]

                        output_values = [ line[hgroups[x][0]] for i, x in enumerate(output_indices) ]
                        output_node_indices = [ self._build_node_index(output_headers[i], output_values[i]) for i, x in enumerate(output_values)]

                        qualifier_indices_string = '-'.join(qualifier_values)
                        input_node_indices_string = "-".join(input_node_indices)
                        output_node_indices_string = "-".join(output_node_indices)

                        assay_name = ""
                        if assay_name_indices:
                            if len(assay_name_indices)==1:
                                assay_name = line[hgroups[assay_name_indices[0]][0]]

                        if (assay_name):
                           unique_process_name = assay_name
                        else:
                            try:
                                unique_process_name = input_process_map[qualifier_indices_string+input_node_indices_string]
                                if not (unique_process_name.startswith(processing_name)):
                                    raise KeyError
                            except KeyError:
                                try:
                                    unique_process_name = output_process_map[qualifier_indices_string+output_node_indices_string]
                                    if not (unique_process_name.startswith(processing_name)):
                                        raise KeyError
                                except KeyError:
                                    try:
                                        process_number = process_counters[processing_name]
                                    except KeyError:
                                        process_number = 0

                                    process_number +=1
                                    process_counters[processing_name] = process_number
                                    unique_process_name = processing_name+str(process_number)

                        try:
                            process_node = process_nodes[unique_process_name]
                        except KeyError:
                            #create process node
                            process_node = ProcessNodeRecord(unique_process_name, processing_header, study, processing_name)

                        if (previous_processing_node):
                            previous_processing_node.next_process = process_node
                            process_node.previous_process = previous_processing_node

                        previous_processing_node = process_node
                        #previous_protocol = line[hgroups[next_processing_index]]

                        if assay_name:
                            process_node.assay_name = assay_name
                            assay_name_map[assay_name] = process_node

                        #Add qualifiers (performer and date)
                        for qualifier_index in qualifier_indices:
                            qualifier_header = headers[qualifier_index]
                            if qualifier_header=="Date":
                                process_node.date = line[qualifier_index]
                            elif qualifier_header == "Performer":
                                process_node.performer = line[qualifier_index]


                        if not (input_node_indices in process_node.inputs):
                            in_first = set(process_node.inputs)
                            in_second = set(input_node_indices)
                            in_second_but_not_in_first = in_second - in_first
                            process_node.inputs = process_node.inputs + list(in_second_but_not_in_first)
                        if not (output_node_indices in process_node.outputs):
                            in_first = set(process_node.outputs)
                            in_second = set(output_node_indices)
                            in_second_but_not_in_first = in_second - in_first
                            process_node.outputs = process_node.outputs + list(in_second_but_not_in_first)

                        input_process_map[qualifier_indices_string+input_node_indices_string] = unique_process_name
                        output_process_map[qualifier_indices_string+output_node_indices_string] = unique_process_name

                        #Add parameters
                        parameter_headers = []
                        for parameter_index in parameters_indices:
                            parameter_header = headers[hgroups[parameter_index][0]]
                            parameter_headers.append(parameter_header)
                            process_node.parameters.append(parameter_header)
                            #creating the metadata object
                            process_node.metadata = collections.defaultdict(set)
                            attrs = self._line_keyvals(line, headers, hgroups, htypes, process_node.metadata)
                            process_node.metadata = attrs

                        # max_number = max(len(process_node.inputs), len(process_node.outputs))
                        line_number += 1
                        process_nodes[unique_process_name] = process_node
                    else:
                        line_number += 1
                #study.process_nodes = process_nodes
        return {k:self._finalize_metadata(v)for k,v in six.iteritems(process_nodes)}


    def _parse_study(self, fname, node_types):
        """Parse study or assay row oriented file around the supplied base node.
        """
        if not os.path.exists(os.path.join(self._dir, fname)):
            return None
        nodes = {}
        with open(os.path.join(self._dir, fname)) as in_handle:
            reader = csv.reader(in_handle, dialect="excel-tab")
            headers = self._swap_synonyms(next(reader))
            hgroups = self._collapse_header(headers)
            htypes = self._characterize_header(headers, hgroups)

            node_indices = [i for i, x in enumerate(htypes) if x == "node"]
            all_attribute_indices = [i for i, x in enumerate(htypes) if x == "attribute"]

            for node_index in node_indices:

                node_type = headers[hgroups[node_index][0]]
                if node_type not in node_types:
                    continue
                try:
                    header_index = hgroups[node_index][0]

                except ValueError:
                    header_index = None

                if header_index is None:
                    #print "Could not find standard header name: %s in %s" \
                    #                        % (node_type, header)
                    continue

                next_node_index = find_gt(node_indices, node_index)
                previous_node_index = find_lt(node_indices, node_index)
                attribute_indices = find_in_between(all_attribute_indices, node_index, next_node_index)

                in_handle.seek(0, 0)
                for line in reader:
                    if line[0].startswith("#"):
                        continue
                    name = self._swap_synonyms([line[header_index]])[0]
                    #skip the header line and empty lines
                    if not name or name in headers:
                        continue
                    #to deal with same name used for different node types (e.g. Source Name and Sample Name using the same string)
                    node_index_name = self._build_node_index(node_type,name)

                    try:
                        node = nodes[node_index_name]

                        for attribute_index in attribute_indices:
                            attribute_header = headers[hgroups[attribute_index][0]]
                            if attribute_header.startswith("Factor Value") and node_type != "Sample Name":
                                continue
                            if attribute_header not in node.attributes:
                                node.attributes.append(attribute_header)

                    except KeyError:
                        node = NodeRecord(name, node_type, node_index_name)
                        node.metadata = collections.defaultdict(set)
                        nodes[node_index_name] = node
                        attrs = self._line_keyvals(line, headers, hgroups, htypes, node.metadata)
                        nodes[node_index_name].metadata = attrs

                        for attribute_index in attribute_indices:
                            attribute_header = headers[hgroups[attribute_index][0]]
                            if attribute_header.startswith("Factor Value") and node_type != "Sample Name":
                                continue
                            if attribute_header not in node.attributes:
                                node.attributes.append(attribute_header)

                    if not (previous_node_index == -1):
                        node.derivesFrom.append(line[previous_node_index])

        return {k:self._finalize_metadata(v) for k,v in six.iteritems(nodes)}

    def _finalize_metadata(self, node):
        """Convert node metadata back into a standard dictionary and list.
        """
        final = {}
        for key, val in six.iteritems(node.metadata):
            #val = list(val)
            #if isinstance(val[0], tuple):
            #    val = [dict(v) for v in val]
            final[key] = list(val)
        node.metadata = final
        return node

    def _line_keyvals(self, line, header, hgroups, htypes, out):
        out = self._line_by_type(line, header, hgroups, htypes, out, "node")
        out = self._line_by_type(line, header, hgroups, htypes, out, "attribute",
                                 self._collapse_attributes)
        out = self._line_by_type(line, header, hgroups, htypes, out, "processing",
                                 self._collapse_attributes)
        out = self._line_by_type(line, header, hgroups, htypes, out, "parameter",
                                 self._collapse_attributes)
        return out

    def _line_by_type(self, line, header, hgroups, htypes, out, want_type,
                      collapse_quals_fn = None):
        """Parse out key value pairs for line information based on a group of values.
        """
        for index, htype in ((i, t) for i, t in enumerate(htypes) if t == want_type):
            col = hgroups[index][0]
            key = header[col]
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
            if header[i]:
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
        for h in (header[g[0]] for g in hgroups):
            this_ctype = None
            for ctype, names in six.iteritems(self._col_types):
                if (h in names) or ( h.startswith(names) and h.endswith("]")):
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

    #to ensure uniqueness of node indexes
    def _build_node_index(self, type, name):
        if type=="Source Name":
            return "source-"+name
        else:
            if type == "Sample Name":
                return "sample-"+name
            else:
                if type == "Extract Name":
                    return "extract-"+name
                else:
                    if type == "Labeled Extract Name":
                        return "labeledextract-"+name
                    else:
                        if type == "Raw Data File":
                            return "rawdatafile-"+name
                        else:
                            if type=="Derived Data File":
                                return "deriveddatafile-"+name
                            else:
                                if type=="Acquisiton Parameter Data File":
                                    return "acquisitionparameterfile-"+name
                                else:
                                     if type=="Image File":
                                        return "imagefile-"+name
                                     else:
                                        "ERROR - Type not being considered! ", type
                                        return name


_record_str = \
"""* ISATab Record
 metadata: {md}
 studies:
{studies}
"""

_study_str = \
"""  * Study
   metadata: {md}
   design_descriptors: {design_descriptors}
   publications : {publications}
   factors: {factors}
   protocols: {protocols}
   nodes:
    {nodes}
   process_nodes:
    {process_nodes}
   assays:
{assays}
"""

_assay_str = \
"""    * Assay
     metadata: {md}
     nodes:
        {nodes}
     process_nodes:
       {process_nodes}
"""

_node_str = \
"""       * Node -> {name} {type} {index}
         attributes: {attributes}
         derivesFrom: {derivesFrom}
         metadata: {md}"""

_process_node_str = \
"""       * Process Node ->  {name} {type}
         assay_name: {assay_name}
         protocol: {protocol}
         performer: {performer}
         date: {date}
         inputs: {inputs}
         outputs: {outputs}
         previous_process = {previous_process}
         next_process = {next_process}
         parameters: {parameters}
         metadata: {md}"""


class ISATabRecord:
    """Represent ISA-Tab metadata in structured format.
    High level key/value data.
      - metadata -- dictionary
      - ontology_refs -- list of dictionaries
      - contacts -- list of dictionaries
      - publications -- list of dictionaries
    Sub-elements:
      - studies: List of ISATabStudyRecord objects.
    """
    def __init__(self):
        self.metadata = {}
        self.ontology_refs = []
        self.publications = []
        self.contacts = []
        self.studies = []

    def __str__(self):
        return _record_str.format(md=pprint.pformat(self.metadata).replace("\n", "\n" + " " * 3),
                                  ont=self.ontology_refs,
                                  pub=self.publications,
                                  contact=self.contacts,
                                  studies="\n".join(str(x) for x in self.studies))

class ISATabStudyRecord:
    """Represent a study within an ISA-Tab record.
    """
    def __init__(self):
        self.metadata = {}
        self.design_descriptors = []
        self.publications = []
        self.factors = []
        self.assays = []
        self.protocols = []
        self.contacts = []
        self.nodes = {}
        self.process_nodes = {}

    def __str__(self):
        return _study_str.format(md=pprint.pformat(self.metadata).replace("\n", "\n" + " " * 5),
                                 design_descriptors=pprint.pformat(self.design_descriptors).replace("\n", "\n" + " " * 5),
                                 publications="\n".join(str(x) for x in self.publications),
                                 factors="\n".join(str(x) for x in self.factors),
                                 assays="\n".join(str(x) for x in self.assays),
                                 protocols="\n".join(str(x) for x in self.protocols),
                                 nodes="\n".join(str(x) for x in self.nodes.values()),
                                 process_nodes="\n".join(str(x) for x in self.process_nodes.values())
        )

class ISATabAssayRecord:
    """Represent an assay within an ISA-Tab record.
    """
    def __init__(self, metadata=None):
        #if metadata is None: metadata = {}
        self.metadata = metadata or {}
        self.nodes = {}
        self.process_nodes = {}

    def __str__(self):
        return _assay_str.format(md=pprint.pformat(self.metadata).replace("\n", "\n" + " " * 7),
                                 nodes="\n".join(str(x) for x in self.nodes.values()),
                                 process_nodes="\n".join(str(x) for x in self.process_nodes.values())
        )

class NodeRecord:
    """Represent a data or material node within an ISA-Tab Study/Assay file.
    """
    def __init__(self, name="", ntype="", nindex=""):
        self.ntype = ntype
        self.name = name
        self.index = nindex
        self.metadata = {}
        self.attributes = []
        self.derivesFrom = []

    def __str__(self):
        return _node_str.format(md=pprint.pformat(self.metadata).replace("\n", "\n" + " " * 9),
                                index=self.index,
                                name=self.name,
                                type=self.ntype,
                                attributes=pprint.pformat(self.attributes).replace("\n","\n"+" "*9),
                                derivesFrom=pprint.pformat(self.derivesFrom).replace("\n","\n"+" "*9))


class ProcessNodeRecord:
    """Represent a process node within an ISA-Tab Study/Assay file (corresponds to Protocol REF).
    """
    def __init__(self, name="", ntype="", study_assay="", protocol=""):
        self.ntype = ntype
        self.study_assay = study_assay
        self.name = name
        self.protocol = protocol
        self.previous_process = None
        self.next_process = None
        self.inputs = []
        self.outputs = []
        self.metadata = {}
        self.parameters = []
        self.assay_name = "" #used when there is an associated 'Assay Name' for a 'Protocol REF'
        self.performer = ""
        self.date = ""

    def __str__(self):
        return _process_node_str.format(md=pprint.pformat(self.metadata).replace("\n", "\n" + " " * 9),
                                        inputs=pprint.pformat(self.inputs).replace("\n", "\n" + " " * 9),
                                        outputs=pprint.pformat(self.outputs).replace("\n", "\n" + " " * 9),
                                        name=self.name,
                                        assay_name=self.assay_name,
                                        type=self.ntype,
                                        protocol=self.protocol,
                                        performer=self.performer,
                                        date=self.date,
                                        previous_process=self.previous_process.name if self.previous_process else "",
                                        next_process=self.next_process.name if self.next_process else "",
                                        parameters=pprint.pformat(self.parameters).replace("\n","\n"+" "*9))

