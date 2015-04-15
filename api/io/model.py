__author__ = 'agbeltran'

import pprint

investigation = {
    "ONTOLOGY SOURCE REFERENCE": {},
    "INVESTIGATION": {},
    "INVESTIGATION CONTACTS": {},
    "INVESTIGATION PUBLICATIONS": {},
    "STUDY": []
};



class InvestigationClass:
    """
    Represents all the ISA-Tab metadata.
        - metadata -- dictionary
        - ontology_refs -- list of dictionaries
    """

    investigation_file_pattern = "i_*.txt"

    def __init__(self):
        self.ontology_refs = []
        self.investigation = []
        self.studies = []
        self.assays = []

        # def __str__(self):
        #    return _record_str.format(md=pprint.pformat(self.metadata).replace("\n", "\n" + " " * 3),
        #                              ont=self.ontology_refs,
        #                              pub=self.publications,
        #                              contact=self.contacts,
        #                              studies="\n".join(str(x) for x in self.studies))


class DescriptiveMetadataClass:
    """Common metadata for investigation and studies"""

    def __init__(self):
        self.filename = []
        self.publications = []
        self.contacts = []


class StudyAssayTabClass:
    """
   Represent a study within an ISA-Tab record.
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

    def __str__(self):
        return _study_str.format(md=pprint.pformat(self.metadata).replace("\n", "\n" + " " * 5),
                                 assays="\n".join(str(x) for x in self.assays),
                                 nodes="\n".join(str(x) for x in self.nodes.values()))


class AssayTabClass:
    """Represents the metadata in an assay table"""


class NodeRecord:
    """Represent a data node within an ISA-Tab Study/Assay file.
    """

    def __init__(self, name="", ntype=""):
        self.ntype = ntype
        self.name = name
        self.metadata = {}

    def __str__(self):
        """return _node_str.format(md=pprint.pformat(self.metadata).replace("\n", "\n" + " " * 9),
                                name=self.name,
                                type=self.ntype)"""

_record_str = \
"""* ISATab Record
 metadata: {md}
 studies:
{studies}
"""

_study_str = \
"""  * Study
   metadata: {md}
   nodes:
{nodes}
   assays:
{assays}
"""

_assay_str = \
"""    * Assay
     metadata: {md}
     nodes:
{nodes}
"""

_node_str = \
"""       * Node {name} {type}
         metadata: {md}"""
