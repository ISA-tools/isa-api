__author__ = 'Alfie Abdul-Rahman'

import json, glob, os, ntpath, csv, string

from api.io import parser

class IsatabToJsonWriter():
    def __init__(self):
        self._col_isaMaterialAttribute = ("Characteristics", "Material Type", "Term Source REF", "Term Accession Number", "Unit")
        self._col_isaMaterialNode = ("Source Name", "Sample Name", "Extract Name", "Labeled Extract Name")
        self._col_isaProcessNode = ("Assay Name", "Normalization Name", "Data Transformation Name")
        self._col_isaProtocolExecutionNode = ("Protocol REF")
        self._col_isaFactorValue = ("Factor Value")
        self._col_isaUnit = ("Unit")
        self._col_isaDataNode = ("File")

        work_dir = "BII-I-1"
        # not a good way of going to the path that we want
        os.chdir('..')
        os.chdir('..')
        self._dir = "tests/data/" + work_dir
        if not os.path.exists(os.path.join(os.getcwd(), 'json')):
            os.makedirs(os.path.join(os.getcwd(), 'json'))

        # create the folder where we want to put the json files
        if not os.path.exists(os.path.join(os.getcwd(), 'json', work_dir + '_json')):
            os.makedirs(os.path.join(os.getcwd(), 'json', work_dir + '_json'))
        self.json_dir = os.path.join(os.getcwd(), 'json', work_dir + '_json')

    def parsingIsatab(self):
        rec = parser.parse(self._dir)
        # process the investigation files
        fnames = glob.glob(os.path.join(self._dir, "i_*.txt")) + \
                 glob.glob(os.path.join(self._dir, "*.idf.txt"))
        investigationFilename = ntpath.basename(str(fnames[0])).split(".")
        self.parseInvestigationToJson(rec, os.path.join(self.json_dir, investigationFilename[0] + ".json"))
        # process the study files
        self.parseStudyToJson(rec)

    def parseInvestigationToJson(self, rec, filename):
        json_structures = {}
        self.createAttributes(json_structures, rec.metadata, "investigation")
        self.createListOfAttributes(json_structures, rec.ontology_refs, "ontologySourceReference")
        self.createListOfAttributes(json_structures, rec.publications, "investigationPublications")
        self.createListOfAttributes(json_structures, rec.contacts, "investigationContacts")
        self.studies(json_structures, rec.studies)
        with open(filename, "w") as outfile:
            json.dump(json_structures, outfile, indent=4)
        outfile.close()

    def makeLowercaseFirstChar(self, s):
        if len(s) == 0:
            return s
        else:
            return s[0].lower() + s[1:]

    def makeUppercaseFirstCharInStringArray(self, s):
        myStr = ""
        for i in s.split(' '):
            if len(i) == 0:
                myStr = myStr + i
            else:
                myStr = myStr + i[0].upper() + i[1:]
        return myStr

    def makeAttributeName(self, tag):
        table = string.maketrans("","")
        stripTag = tag.translate(table, string.punctuation)
        return self.makeLowercaseFirstChar(stripTag.split(' ',1)[0]) + self.makeUppercaseFirstCharInStringArray(stripTag.split(' ',1)[1])

    def createAttributes(self, json_structures, metadata, tagName):
        json_inner_struct = {}
        for meta in metadata:
            json_inner_struct[self.makeAttributeName(meta)] = metadata[meta]
        json_structures[tagName] = json_inner_struct
        return json_structures

    def createListOfAttributes(self, json_structures, properties, tagName):
        json_list_struct = []
        for onto in properties:
            json_item_struct = {}
            for item in onto:
                json_item_struct[self.makeAttributeName(item)] = onto[item]
            json_list_struct.append(json_item_struct)
        json_structures[tagName] = json_list_struct
        return json_structures

    def studies(self, json_structures, studies):
        mystudies = []
        for _study in studies:
            json_study_structure = {}
            # write out the metadata information
            self.createAttributes(json_study_structure, _study.metadata, "study")
            # write out the "Study Design Descriptors"
            self.createListOfAttributes(json_study_structure, _study.design_descriptors, "studyDesignDescriptors")
            # write out the "Study Publications"
            self.createListOfAttributes(json_study_structure, _study.publications, "studyPublications")
            # write out the "Study Factors"
            self.createListOfAttributes(json_study_structure, _study.factors, "studyFactors")
            # this is a very silly way of doing extracting the study protocol but needed because of the error in encoding
            # need to think of a better way
            json_study_protocol = []
            for sp in _study.protocols:
                json_sp = {}
                for i_sp in sp:
                    json_sp[self.makeAttributeName(i_sp)] = sp[i_sp].decode('ascii', errors='ignore')
                json_study_protocol.append(json_sp)
            json_study_structure["studyProtocols"] = json_study_protocol
            # write out the "Study Contacts"
            self.createListOfAttributes(json_study_structure, _study.contacts, "studyContacts")
            myassay = []
            for assay in _study.assays:
                json_assay_structure = {}
                for i_assay in assay:
                    json_assay_structure[self.makeAttributeName(i_assay)] = assay[i_assay]
                myassay.append(json_assay_structure)
            json_study_structure["assays"] = myassay
            mystudies.append(json_study_structure)
            json_structures["studies"] = mystudies

    def parseStudyToJson(self, rec):
        for study in rec.studies:
            filename = (study.metadata["Study File Name"]).split(".")[0]
            header, nodes = self.readIsatabStudy(os.path.join(self._dir, filename + ".txt"))
            self.makeStudyAssayJson(header, nodes, os.path.join(self.json_dir, filename + ".json"), "studySampleTable", "studyTableHeaders", "studyTableData")

            for assay in study.assays:
                filename = (assay["Study Assay File Name"]).split(".")[0]
                header, nodes = self.readIsatabStudy(os.path.join(self._dir, filename + ".txt"))
                self.makeStudyAssayJson(header, nodes, os.path.join(self.json_dir, filename + ".json"), "assayTable", "assayTableHeaders", "assayTableData")

    def readIsatabStudy(self, studyfilepath):
        if os.path.isfile(studyfilepath):
            nodes = []
            with open(studyfilepath, "rU") as in_handle:
                reader = csv.reader(in_handle, dialect="excel-tab")
                header = reader.next()
                for line in reader:
                    nodes.append(line)
            return header, nodes

    def checkIfMaterialAttribute(self, header):
        for isaMA in self._col_isaMaterialAttribute:
            if isaMA in header:
                return True
        return False

    def makeStudyAssayJson(self, header, nodes, filename, tableNameTitle, tableHeaderTitle, tableDataTitle):
        json_structures = {}
        tableHeaders = []
        headerIndex = 0
        attributes = []
        heading = {}
        for h in header:
            if not (self.checkIfMaterialAttribute(h)):
                if headerIndex > 0:
                    tableHeaders.append(heading)
                    attributes = []
                heading = {}
                heading.clear()
                heading["name"] = h
                heading["index"] = headerIndex
            else:
                attr = {}
                attr["name"] = h
                attr["index"] = headerIndex
                attributes.append(attr)
                heading["attributes"] = attributes
            headerIndex = headerIndex + 1

        # to add the last item
        tableHeaders.append(heading)

        json_structures[tableHeaderTitle] = tableHeaders
        json_structures[tableDataTitle] = nodes
        top = {}
        top[tableNameTitle] = json_structures
        with open(filename, "w") as outfile:
            json.dump(top, outfile, indent=4)
        outfile.close()

my_foo = IsatabToJsonWriter()
my_foo.parsingIsatab()