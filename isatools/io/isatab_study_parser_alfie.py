__author__ = 'alfie'

import os, csv, json

class IsatabStudyParser():
    def __init__(self):
        self._col_isaMaterialAttribute = ("Characteristics", "Material Type", "Term Source REF", "Term Accession Number", "Unit")
        self._col_isaMaterialNode = ("Source Name", "Sample Name", "Extract Name", "Labeled Extract Name")
        self._col_isaProcessNode = ("Assay Name", "Normalization Name", "Data Transformation Name")
        self._col_isaProtocolExecutionNode = ("Protocol REF")
        self._col_isaFactorValue = ("Factor Value")
        self._col_isaUnit = ("Unit")
        self._col_isaDataNode = ("File")

        work_dir = "BII-I-1"
        self._study_file = "s_BII-S-2"
        # not a good way of going to the path that we want
        os.chdir('..')
        os.chdir('..')
        self._dir = "tests/data/" + work_dir + "/"
        self._studyfilepath = self._dir + self._study_file + ".txt"

        if not os.path.exists(os.path.join(os.getcwd(), 'json')):
            os.makedirs(os.path.join(os.getcwd(), 'json'))

        # create the folder where we want to put the json files
        if not os.path.exists(os.path.join(os.getcwd(), 'json', work_dir + '_json')):
            os.makedirs(os.path.join(os.getcwd(), 'json', work_dir + '_json'))
        self.json_dir = os.path.join(os.getcwd(), 'json', work_dir + '_json')

    def parsingIsatabStudyToJson(self):
        header, nodes = self.readIsatabStudy()
        self.makeStudyJson(header, nodes, os.path.join(self.json_dir, self._study_file + ".json"))

    def readIsatabStudy(self):
        if os.path.isfile(self._studyfilepath):
            nodes = []
            with open(self._studyfilepath, "rU") as in_handle:
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

    def makeStudyJson(self, header, nodes, filename):
        json_structures = {}
        studyTableHeaders = []
        headerIndex = 0
        attributes = []
        heading = {}
        for h in header:
            if not (self.checkIfMaterialAttribute(h)):
                if headerIndex > 0:
                    studyTableHeaders.append(heading)
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
        studyTableHeaders.append(heading)

        json_structures["studyTableHeaders"] = studyTableHeaders
        json_structures["studyTableData"] = nodes
        top = {}
        top["studySampleTable"] = json_structures
        with open(filename, "w") as outfile:
            json.dump(top, outfile, indent=4)
        outfile.close()

foo = IsatabStudyParser()
foo.parsingIsatabStudyToJson()