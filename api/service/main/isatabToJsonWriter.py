__author__ = 'alfie'

import json, glob, os, ntpath, csv


from . import parser
from .common_functions import CommonFunctions


class IsatabToJsonWriter():
    commonFunctions = CommonFunctions()


    def __init__(self):
        self._col_isaMaterialType = ("Material Type", "Term Source REF", "Term Accession Number")
        self._col_isaMaterialAttribute = ("Characteristics", "Term Source REF", "Term Accession Number", "Unit")
        self._col_isaMaterialLabel = ("Label", "Term Source REF", "Term Accession Number")
        self._col_isaMaterialNode = ("Source Name", "Sample Name", "Extract Name", "Labeled Extract Name")
        self._col_isaProcessNode = ("Assay Name", "Normalization Name", "Data Transformation Name", "Array Design REF", "Scan Name")
        self._col_isaProtocolExecutionNode = ("Protocol REF")
        self._col_isaFactorValue = ("Factor Value")
        self._col_isaParameterValue = ("Parameter Value")
        self._col_isaDataNode = ("File")


    def parsingIsatab(self, work_dir, json_dir, chunked):
        rec = parser.parse(work_dir)
        # process the investigation files
        fnames = glob.glob(os.path.join(work_dir, "i_*.txt")) + \
                 glob.glob(os.path.join(work_dir, "*.idf.txt"))
        investigationFilename = ntpath.basename(str(fnames[0])).split(".")
        self.parseInvestigationToJson(rec, os.path.join(json_dir, investigationFilename[0] + ".json"), os.path.join(json_dir, os.path.basename(work_dir) + ".json"), work_dir, json_dir, chunked)


    def parseInvestigationToJson(self, rec, i_File, single_file, work_dir, json_dir, chunked):
        json_structures = {}
        self.createListOfAttributes(json_structures, rec.ontology_refs, "ontologySourceReference")
        self.createInvestigationNode(json_structures, rec)
        if (chunked):
            #  multiple json structure
            self.studies(json_structures, rec.studies, work_dir, json_dir, False)
            with open(i_File, "w") as outfile:
                json.dump(json_structures, outfile, indent=4, sort_keys=True)
            outfile.close()
        else:
            # single json structure
            single_json_structures = json_structures.copy()
            self.studies(single_json_structures, rec.studies, work_dir, json_dir, True)
            with open(single_file, "w") as outfile:
                json.dump(single_json_structures, outfile, indent=4, sort_keys=True)
            outfile.close()


    def createInvestigationNode(self, json_structures, rec):
        json_inner_struct = {}
        for meta in rec.metadata:
            json_inner_struct[self.commonFunctions.makeAttributeName(meta, '')] = rec.metadata[meta]
        json_inner_struct["investigationPublications"] = self.createListOfAttributesArray(rec.publications)
        json_inner_struct["investigationContacts"] = self.createListOfAttributesArray(rec.contacts)
        json_structures["investigation"] = json_inner_struct
        return json_structures


    def createAttributes(self, json_structures, metadata, tagName):
        json_inner_struct = {}
        for meta in metadata:
            json_inner_struct[self.commonFunctions.makeAttributeName(meta, '')] = metadata[meta]
        json_structures[tagName] = json_inner_struct
        return json_structures


    def createListOfAttributesArray(self, properties):
        json_list_struct = []
        for onto in properties:
            json_item_struct = {}
            for item in onto:
                json_item_struct[self.commonFunctions.makeAttributeName(item, '')] = onto[item]
            json_list_struct.append(json_item_struct)
        return json_list_struct


    def createListOfAttributes(self, json_structures, properties, tagName):
        json_list_struct = []
        for onto in properties:
            json_item_struct = {}
            for item in onto:
                json_item_struct[self.commonFunctions.makeAttributeName(item, '')] = onto[item]
            json_list_struct.append(json_item_struct)
        json_structures[tagName] = json_list_struct
        return json_structures


    def createStudyNode(self, json_structures, rec, work_dir, json_dir, isSingleStructure):
        json_inner_struct = {}
        for meta in rec.metadata:
            json_inner_struct[self.commonFunctions.makeAttributeName(meta, '')] = rec.metadata[meta]
        json_inner_struct["studyDesignDescriptors"] = self.createListOfAttributesArray(rec.design_descriptors)
        json_inner_struct["studyPublications"] = self.createListOfAttributesArray(rec.publications)
        json_inner_struct["studyFactors"] = self.createListOfAttributesArray(rec.factors)
        # this is a very silly way of doing extracting the study protocol but needed because of the error in encoding
        # need to think of a better way
        json_study_protocol = []
        for sp in rec.protocols:
            json_sp = {}
            for i_sp in sp:
                json_sp[self.commonFunctions.makeAttributeName(i_sp, '')] = sp[i_sp].decode('ascii', errors='ignore')
            json_study_protocol.append(json_sp)
        json_inner_struct["studyProtocols"] = json_study_protocol
        json_inner_struct["studyContacts"] = self.createListOfAttributesArray(rec.contacts)
        filename = (rec.metadata["Study File Name"]).split(".")[0]
        studySamples = self.readIsatabStudyAssayExtend(os.path.join(work_dir, filename + ".txt"))
        if (isSingleStructure):
            json_inner_struct["studySamples"] = studySamples
        else:
            header, nodes = self.readIsatabStudyAssay(os.path.join(work_dir, filename + ".txt"))
            self.makeStudyAssayJson(header, nodes, os.path.join(json_dir, filename + ".json"), "studySampleTable", "studyTableHeaders", "studyTableData")
            outputJson = {}
            outputJson["studySamples"] = studySamples
            with open(os.path.join(json_dir, filename + "_expanded.json"), "w") as outfile:
                json.dump(outputJson, outfile, indent=4, sort_keys=True)
            outfile.close()
        myassay = []
        for assay in rec.assays:
            json_assay_structure = {}
            for i_assay in assay:
                json_assay_structure[self.commonFunctions.makeAttributeName(i_assay, '')] = assay[i_assay]
                filename = (assay["Study Assay File Name"]).split(".")[0]
                assaysTable = self.readIsatabStudyAssayExtend(os.path.join(work_dir, filename + ".txt"))
                if (isSingleStructure):
                    json_assay_structure["assaysTable"] = assaysTable
                else:
                    header, nodes = self.readIsatabStudyAssay(os.path.join(work_dir, filename + ".txt"))
                    self.makeStudyAssayJson(header, nodes, os.path.join(json_dir, filename + ".json"), "assaysTable", "assayTableHeaders", "assayTableData")
                    outputJson = {}
                    outputJson["assaysTable"] = assaysTable
                    with open(os.path.join(json_dir, filename + "_expanded.json"), "w") as outfile:
                        json.dump(outputJson, outfile, indent=4, sort_keys=True)
                    outfile.close()
            myassay.append(json_assay_structure)
        json_inner_struct["assays"] = myassay
        json_structures["study"] = json_inner_struct


    def studies(self, json_structures, studies, work_dir, json_dir, isSingleStructure):
        mystudies = []
        for _study in studies:
            json_study_structure = {}
            self.createStudyNode(json_study_structure, _study, work_dir, json_dir, isSingleStructure)
            mystudies.append(json_study_structure)
            json_structures["studies"] = mystudies


    def parseStudyAssayToJson(self, rec, work_dir, json_dir):
        for study in rec.studies:
            filename = (study.metadata["Study File Name"]).split(".")[0]
            header, nodes = self.readIsatabStudyAssay(os.path.join(work_dir, filename + ".txt"))
            self.makeStudyAssayJson(header, nodes, os.path.join(json_dir, filename + ".json"), "studySampleTable", "studyTableHeaders", "studyTableData")
            for assay in study.assays:
                filename = (assay["Study Assay File Name"]).split(".")[0]
                header, nodes = self.readIsatabStudyAssay(os.path.join(work_dir, filename + ".txt"))
                self.makeStudyAssayJson(header, nodes, os.path.join(json_dir, filename + ".json"), "assaysTable", "assayTableHeaders", "assayTableData")


    def readIsatabStudyAssayExtend(self, studyfilepath):
        if os.path.isfile(studyfilepath):
            studySamples = []
            with open(studyfilepath, "rU") as in_handle:
                reader = csv.reader(in_handle, dialect="excel-tab")
                header = reader.next()
                hGroupings = self.createHeaderGrouping(header)
                for line in reader:
                    studySample = []
                    characteristicsArray = []
                    factorsArray = []
                    parametersArray = []
                    labelsArray = []
                    for i in hGroupings:
                        obj = {}
                        for p in i:
                            attrDict = {}
                            if not (isinstance(p, list)):
                                obj["type"] = self.typeValue(header[p])
                                obj["value"] = line[p]
                                if "Comment" in header[p]:
                                    obj["name"] = header[p].split("[")[0]
                                    obj["commentTerm"] = header[p][header[p].index("[") + 1:header[p].rindex("]")]
                                else:
                                    obj["name"] = header[p]
                            else:
                                for b, t in enumerate(p):
                                    str = header[t]
                                    if "Characteristics" in header[t]:
                                        attrDict["characteristics"] = line[t]
                                        attrDict["categoryTerm"] = str[str.index("[") + 1:str.rindex("]")]
                                    else:
                                        if "Factor" in header[t]:
                                            attrDict["factorValue"] = line[t]
                                            attrDict["factorName"] = str[str.index("[") + 1:str.rindex("]")]
                                        else:
                                            if "Parameter" in header[t]:
                                                attrDict["parameterValue"] = line[t]
                                                attrDict["parameterTerm"] = str[str.index("[") + 1:str.rindex("]")]
                                            else:
                                                if "Material" in header[t]:
                                                    attrDict["characteristics"] = line[t]
                                                    attrDict["categoryTerm"] = "Material Type"
                                                else:
                                                    attrDict[self.commonFunctions.makeAttributeName(header[t], '')] = line[t]
                                    obj["type"] = self.typeValue(header[p[0]])
                                if "Characteristics" in header[p[0]] or "Material" in header[p[0]]:
                                    characteristicsArray.append(attrDict)
                                if "Factor" in header[p[0]]:
                                    factorsArray.append(attrDict)
                                if "Parameter" in header[p[0]]:
                                    parametersArray.append(attrDict)
                                if "Label" in header[p[0]]:
                                    labelsArray.append(attrDict)
                        if (isinstance(p, list)):
                            if len(characteristicsArray) > 0:
                                obj["items"] = characteristicsArray
                                characteristicsArray = []
                            if len(factorsArray) > 0:
                                obj["items"] = factorsArray
                                factorsArray = []
                            if len(parametersArray) > 0:
                                obj["items"] = parametersArray
                                parametersArray = []
                            if len(labelsArray) > 0:
                                obj["items"] = labelsArray
                                labelsArray = []
                        studySample.append(obj)
                    studySamples.append(studySample)
            return studySamples


    def createHeaderGrouping(self, header):
        out = []
        attributes = []
        miniAttr = []
        for i, h in enumerate(header):
            if (self.checkIfMaterialNode(h)) or (h in self._col_isaProtocolExecutionNode) or (self.checkIfProcessNode(h)) or ("file" in h.lower()) or ("comment" in h.lower()):
                if (i > 0):
                    if len(attributes) > 0:
                        out.append(attributes)
                    attributes = []
                out.append([i])
            else:
                if ("Characteristics" in h) or ("Factor" in h) or ("Parameter" in h) or ("Label" in h):
                    miniAttr = []
                miniAttr.append(i)
                if ("Term Accession Number" in h):
                    attributes.append(miniAttr)
        if len(attributes) > 0:
            out.append(attributes)
        return out


    def typeValue(self, type):
        if (self.checkIfMaterialType(type)):
            return "isaMaterialType"
        if (self.checkIfMaterialAttribute(type)):
            return "isaMaterialAttribute"
        if (self.checkIfMaterialLabel(type)):
            return "isaMaterialLabel"
        if (self.checkIfMaterialNode(type)):
            return "isaMaterialNode"
        if (self.checkIfProcessNode(type)):
            return "isaProcessNode"
        if self._col_isaProtocolExecutionNode in type:
            return "isaProtocolExecutionNode"
        if self._col_isaFactorValue in type:
            return "isaFactorValue"
        if self._col_isaParameterValue in type:
            return "isaParameterValue"
        if self._col_isaDataNode in type:
            return "isaDataNode"
        if "Comment" in type:
            return "isaComment"
        return ""


    def readIsatabStudyAssay(self, studyfilepath):
        if os.path.isfile(studyfilepath):
            nodes = []
            with open(studyfilepath, "rU") as in_handle:
                reader = csv.reader(in_handle, dialect="excel-tab")
                header = reader.next()
                for line in reader:
                    nodes.append(line)
            return header, nodes


    def checkIfMaterialNode(self, header):
        for isaMN in self._col_isaMaterialNode:
            if isaMN in header:
                return True
        return False


    def checkIfProcessNode(self, header):
        for isaPN in self._col_isaProcessNode:
            if isaPN in header:
                return True
        return False


    def checkIfMaterialAttribute(self, header):
        for isaMA in self._col_isaMaterialAttribute:
            if isaMA in header:
                return True
        return False


    def checkIfMaterialType(self, header):
        for isaMT in self._col_isaMaterialType:
            if isaMT in header:
                return True
        return False


    def checkIfMaterialLabel(self, header):
        for isaML in self._col_isaMaterialLabel:
            if header in isaML:
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
            json.dump(top, outfile, indent=4, sort_keys=True)
        outfile.close()
