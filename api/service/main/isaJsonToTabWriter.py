__author__ = 'alfie'

import os, glob, json, ntpath


from .common_functions import CommonFunctions


class IsajsonToIsatabWriter():
    commonFunctions = CommonFunctions()


    def __init__(self):
        self._investigation_file_pattern = "i_*.json"
        self._study_file_pattern = "s_*.json"
        self._assay_file_pattern = "a_*.json"

        self._isatab_i_ontology_source_ref_sec = ["Term Source Name", "Term Source File",
                                                "Term Source Version", "Term Source Description"]

        self._isatab_i_investigation_sec = ["Investigation Identifier", "Investigation Title",
                                            "Investigation Description", "Investigation Submission Date",
                                            "Investigation Public Release Date", "Comment[Created With Configuration]",
                                            "Comment[Last Opened With Configuration]"]

        self._isatab_i_investigation_publications_sec = ["Investigation PubMed ID", "Investigation Publication DOI",
                                                        "Investigation Publication Author List", "Investigation Publication Title",
                                                        "Investigation Publication Status", "Investigation Publication Status Term Accession Number",
                                                        "Investigation Publication Status Term Source REF"]

        self._isatab_i_investigation_contacts_sec = ["Investigation Person Last Name", "Investigation Person First Name",
                                                    "Investigation Person Mid Initials", "Investigation Person Email",
                                                    "Investigation Person Phone", "Investigation Person Fax",
                                                    "Investigation Person Address", "Investigation Person Affiliation",
                                                    "Investigation Person Roles", "Investigation Person Roles Term Accession Number",
                                                    "Investigation Person Roles Term Source REF", "Comment[Investigation Person REF]"]

        self._isatab_i_study_sec = ["Study Identifier", "Study Title",
                                    "Study Description", "Comment[Study Grant Number]",
                                    "Comment[Study Funding Agency]", "Study Submission Date",
                                    "Study Public Release Date", "Study File Name"]

        self._isatab_i_study_design_descriptors_sec = ["Study Design Type", "Study Design Type Term Accession Number",
                                                    "Study Design Type Term Source REF"]

        self._isatab_i_study_publications_sec = ["Study PubMed ID", "Study Publication DOI",
                                                "Study Publication Author List", "Study Publication Title",
                                                "Study Publication Status", "Study Publication Status Term Accession Number",
                                                "Study Publication Status Term Source REF"]

        self._isatab_i_study_factors_sec = ["Study Factor Name", "Study Factor Type",
                                            "Study Factor Type Term Accession Number", "Study Factor Type Term Source REF"]

        self._isatab_i_study_assays_sec = ["Study Assay Measurement Type", "Study Assay Measurement Type Term Accession Number",
                                        "Study Assay Measurement Type Term Source REF", "Study Assay Technology Type",
                                        "Study Assay Technology Type Term Accession Number", "Study Assay Technology Type Term Source REF",
                                        "Study Assay Technology Platform", "Study Assay File Name"]

        self._isatab_i_study_protocols_sec = ["Study Protocol Name", "Study Protocol Type",
                                            "Study Protocol Type Term Accession Number", "Study Protocol Type Term Source REF",
                                            "Study Protocol Description", "Study Protocol URI",
                                            "Study Protocol Version", "Study Protocol Parameters Name",
                                            "Study Protocol Parameters Name Term Accession Number", "Study Protocol Parameters Name Term Source REF",
                                            "Study Protocol Components Name", "Study Protocol Components Type",
                                            "Study Protocol Components Type Term Accession Number", "Study Protocol Components Type Term Source REF"]

        self._isatab_i_study_contacts_sec = ["Study Person Last Name", "Study Person First Name",
                                            "Study Person Mid Initials", "Study Person Email",
                                            "Study Person Phone", "Study Person Fax",
                                            "Study Person Address", "Study Person Affiliation",
                                            "Study Person Roles", "Study Person Roles Term Accession Number",
                                            "Study Person Roles Term Source REF", "Comment[Study Person REF]"]


    def parsingJson(self, json_dir, output_dir):
        if os.path.isdir(json_dir):
            i_filenames = glob.glob(os.path.join(json_dir, self._investigation_file_pattern))
            s_filenames = glob.glob(os.path.join(json_dir, self._study_file_pattern))
            a_filenames = glob.glob(os.path.join(json_dir, self._assay_file_pattern))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.writeJsonInvestigationToIsatab(i_filenames, output_dir)
            self.writeJsonStudyAssayToIsatab(s_filenames, output_dir, "studySampleTable", "studyTableHeaders", "studyTableData")
            self.writeJsonStudyAssayToIsatab(a_filenames, output_dir, "assaysTable", "assayTableHeaders", "assayTableData")
            self.writeJsonStudyAssayExpandedToIsatab(s_filenames, output_dir, "studySamples")
            self.writeJsonStudyAssayExpandedToIsatab(a_filenames, output_dir, "assaysTable")


    def parsingJsonCombinedFile(self, filepath, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if os.path.exists(filepath):
            self.writeJsonCombinedFileToIsatab(filepath, output_dir)


    def writeJsonInvestigationToIsatab(self, filenames, output_dir):
        assert len(filenames) == 1
        json_investigation = filenames[0]
        assert os.path.exists(json_investigation), "Did not find investigation file: %s" % json_investigation
        with open(json_investigation) as in_handle:
            jsonData = json.load(in_handle)
            investigation_str = self.processInvestigationJson(jsonData)
        # now we write out the investigation file
        with open(os.path.join(output_dir, ntpath.basename(str(json_investigation)).split(".")[0] + ".txt"), "w") as file_isatab:
            file_isatab.write(investigation_str)


    def writeJsonCombinedFileToIsatab(self, filepath, output_dir):
        with open(filepath) as in_handle:
            jsonData = json.load(in_handle)
            investigation_str = self.processInvestigationJson(jsonData)
            for study in jsonData["studies"]:
                study_str = self.processStudyAssay(study["study"], "studySamples")
                with open(os.path.join(output_dir, study["study"]["studyFileName"]), "w") as study_isatab:
                    study_isatab.write(study_str)
                for assay in study["study"]["assays"]:
                    assay_str = self.processStudyAssay(assay, "assaysTable")
                    with open(os.path.join(output_dir, assay["studyAssayFileName"]), "w") as assay_isatab:
                        assay_isatab.write(assay_str.encode('ascii', errors='ignore'))
        # write out the investigation file
        with open(os.path.join(output_dir, "i_investigation.txt"), "w") as investigation_isatab:
            investigation_isatab.write(investigation_str)


    def processInvestigationJson(self, jsonData):
        my_str = ""
        # ONTOLOGY SOURCE REFERENCE
        my_str = self.writeSectionInvestigation(my_str, "ONTOLOGY SOURCE REFERENCE", jsonData["ontologySourceReference"], self._isatab_i_ontology_source_ref_sec)
        # INVESTIGATION
        my_str = my_str + "INVESTIGATION" + "\n"
        for i in self._isatab_i_investigation_sec:
            if self.commonFunctions.makeAttributeName(i) in jsonData["investigation"]:
                my_str = my_str + i + "\t\"" + jsonData["investigation"][self.commonFunctions.makeAttributeName(i)] + "\"" + "\n"
        # INVESTIGATION PUBLICATIONS
        my_str = self.writeSectionInvestigation(my_str, "INVESTIGATION PUBLICATIONS", jsonData["investigation"]["investigationPublications"], self._isatab_i_investigation_publications_sec)
        # INVESTIGATION CONTACTS
        my_str = self.writeSectionInvestigation(my_str, "INVESTIGATION CONTACTS", jsonData["investigation"]["investigationContacts"], self._isatab_i_investigation_contacts_sec)
        for study in jsonData["studies"]:
            # STUDY
            my_str = my_str + "STUDY" + "\n"
            for i in self._isatab_i_study_sec:
                if self.commonFunctions.makeAttributeName(i) in study["study"]:
                    my_str = my_str + i + "\t\"" + study["study"][self.commonFunctions.makeAttributeName(i)] + "\"" + "\n"
            # STUDY DESIGN DESCRIPTORS
            my_str = self.writeSectionInvestigation(my_str, "STUDY DESIGN DESCRIPTORS", study["study"]["studyDesignDescriptors"], self._isatab_i_study_design_descriptors_sec)
            # STUDY PUBLICATIONS
            my_str = self.writeSectionInvestigation(my_str, "STUDY PUBLICATIONS", study["study"]["studyPublications"], self._isatab_i_study_publications_sec)
            # STUDY FACTORS
            my_str = self.writeSectionInvestigation(my_str, "STUDY FACTORS", study["study"]["studyFactors"], self._isatab_i_study_factors_sec)
            # STUDY ASSAYS
            my_str = self.writeSectionInvestigation(my_str, "STUDY ASSAYS", study["study"]["assays"], self._isatab_i_study_assays_sec)
            # STUDY PROTOCOLS
            my_str = self.writeSectionInvestigation(my_str, "STUDY PROTOCOLS", study["study"]["studyProtocols"], self._isatab_i_study_protocols_sec)
            # STUDY CONTACTS
            my_str = self.writeSectionInvestigation(my_str, "STUDY CONTACTS", study["study"]["studyContacts"], self._isatab_i_study_contacts_sec)
        return my_str


    def writeSectionInvestigation(self, my_str, sec_header, study, sec_header_group):
        my_str = my_str + sec_header + "\n"
        for i in sec_header_group:
            if self.commonFunctions.makeAttributeName(i) in study[0]:
                my_str = my_str + i + "\t"
                last = len(study) - 1
                for ib, b in enumerate(study):
                    if self.commonFunctions.makeAttributeName(i) in b:
                        if ib == last:
                            my_str = my_str + "\"" + b[self.commonFunctions.makeAttributeName(i)] + "\""
                        else:
                            my_str = my_str + "\"" + b[self.commonFunctions.makeAttributeName(i)] + "\"" + "\t"
                    else:
                        if ib == last:
                            my_str = my_str + "\"\""
                        else:
                            my_str = my_str + "\"\"" + "\t"
                my_str = my_str + "\n"
        return my_str


    def writeJsonStudyAssayToIsatab(self, filenames, output_dir, tableNameTitle, tableHeaderTitle, tableDataTitle):
        assert len(filenames) > 0
        for each_file in filenames:
            assert os.path.exists(each_file), "Did not find study / assay file: %s" % each_file
            if not "expanded" in each_file:
                my_str = ""
                with open(each_file) as in_handle:
                    json_each_s = json.load(in_handle)
                    # the study headers
                    hlast = len(json_each_s[tableNameTitle][tableHeaderTitle]) - 1
                    for hi, node_h in enumerate(json_each_s[tableNameTitle][tableHeaderTitle]):
                        if hi == hlast and "attributes" in node_h and len(node_h["attributes"]) == 0:
                            my_str = my_str + "\"" + node_h["name"] + "\""
                        elif hi == hlast and not("attributes" in node_h):
                                my_str = my_str + "\"" + node_h["name"] + "\""
                        else:
                            my_str = my_str + "\"" + node_h["name"] + "\"" + "\t"
                        if "attributes" in node_h:
                            last = len(node_h["attributes"]) - 1
                            for i, n_h in enumerate(node_h["attributes"]):
                                if i == last and hi == hlast:
                                    my_str = my_str + "\"" + n_h["name"] + "\""
                                else:
                                    my_str = my_str + "\"" + n_h["name"] + "\"" + "\t"
                    my_str = my_str + "\n"
                    # now for each of the rows
                    for node_r in json_each_s[tableNameTitle][tableDataTitle]:
                        last = len(node_r) - 1
                        for i, n_r in enumerate(node_r):
                            if i == last:
                                my_str = my_str + "\"" + n_r + "\""
                            else:
                                my_str = my_str + "\"" + n_r + "\"" + "\t"
                        my_str = my_str + "\n"
                    # now we write out each of the study or assay files
                    with open(os.path.join(output_dir, ntpath.basename(str(each_file)).split(".")[0] + ".txt"), "w") as file_isatab:
                        file_isatab.write(my_str.encode('ascii', errors='ignore'))


    def processStudyAssay(self, json_each_s, mainHeader):
        my_str = ""
        # first we create the header first
        hlast = len(json_each_s[mainHeader][0]) - 1
        for hi, item in enumerate(json_each_s[mainHeader][0]):
            nodeType = item["type"]
            if not nodeType in ("isaMaterialType", "isaMaterialAttribute", "isaMaterialLabel", "isaFactorValue", "isaParameterValue", "isaComment"):
                if hi == hlast:
                    my_str = my_str + "\"" + item["name"] + "\""
                else:
                    my_str = my_str + "\"" + item["name"] + "\"" + "\t"
            else:
                if nodeType in ("isaMaterialType", "isaMaterialAttribute", "isaMaterialLabel", "isaFactorValue", "isaParameterValue"):
                    assert len(item["items"]) > 0
                    hEItemLast = len(item["items"]) - 1
                    for hei, eItem in enumerate(item["items"]):
                        if nodeType in "isaMaterialType":
                            my_str = my_str + "\"" + "Material Type" + "\"" + "\t"
                        if nodeType in "isaMaterialAttribute":
                            my_str = my_str + "\"" + "Characteristics[" + eItem["categoryTerm"] + "]\"" + "\t"
                        if nodeType in "isaMaterialLabel":
                            my_str = my_str + "\"" + "Label" + "\"" + "\t"
                        if nodeType in "isaFactorValue":
                            my_str = my_str + "\"" + "Factor Value[" + eItem["factorName"] + "]\"" + "\t"
                        if nodeType in "isaParameterValue":
                            my_str = my_str + "\"" + "Parameter Value[" + eItem["parameterTerm"] + "]\"" + "\t"
                        if "unit" in eItem:
                            my_str = my_str + "\"" + "Unit" + "\"" + "\t"
                        my_str = my_str + "\"" + "Term Source REF" + "\"" + "\t"
                        my_str = my_str + "\"" + "Term Accession Number" + "\""
                        if hei != hEItemLast:
                            my_str = my_str + "\t"
                        else:
                            if hi != hlast:
                                my_str = my_str + "\t"
                else:
                    my_str = my_str + "\"" + "Comment[" + item["commentTerm"] + "]\"" + "\t"
        my_str = my_str + "\n"
        # then we create the rows below the header
        for items in json_each_s[mainHeader]:
            hlastRow = len(items) - 1
            for hiItem, item in enumerate(items):
                nodeType = item["type"]
                if not nodeType in ("isaMaterialType", "isaMaterialAttribute", "isaMaterialLabel", "isaFactorValue", "isaParameterValue"):
                    if hiItem == hlastRow:
                        my_str = my_str + "\"" + item["value"] + "\""
                    else:
                        my_str = my_str + "\"" + item["value"] + "\"" + "\t"
                else:
                    hEItemLastRow = len(item["items"]) - 1
                    for heirow, eItem in enumerate(item["items"]):
                        if nodeType in "isaMaterialType":
                            my_str = my_str + "\"" + eItem["characteristics"] + "\"" + "\t"
                        if nodeType in "isaMaterialAttribute":
                            my_str = my_str + "\"" + eItem["characteristics"] + "\"" + "\t"
                        if nodeType in "isaMaterialLabel":
                            my_str = my_str + "\"" + eItem["label"] + "\"" + "\t"
                        if nodeType in "isaFactorValue":
                            my_str = my_str + "\"" + eItem["factorValue"] + "\"" + "\t"
                        if nodeType in "isaParameterValue":
                            my_str = my_str + "\"" + eItem["parameterValue"] + "\"" + "\t"
                        if "unit" in eItem:
                            my_str = my_str + "\"" + eItem["unit"] + "\"" + "\t"
                        my_str = my_str + "\"" + eItem["termSourceREF"] + "\"" + "\t"
                        my_str = my_str + "\"" + eItem["termAccessionNumber"] + "\""
                        if heirow != hEItemLastRow:
                            my_str = my_str + "\t"
                        else:
                            if hiItem != hlastRow:
                                my_str = my_str + "\t"
            my_str = my_str + "\n"
        return my_str


    def writeJsonStudyAssayExpandedToIsatab(self, filenames, output_dir, mainHeader):
        assert len(filenames) > 0
        for each_file in filenames:
            assert os.path.exists(each_file), "Did not find study / assay file: %s" % each_file
            if "expanded" in each_file:
                with open(each_file) as in_handle:
                    json_each_s = json.load(in_handle)
                    my_str = self.processStudyAssay(json_each_s, mainHeader)
                    # now we write out each of the study or assay files
                    with open(os.path.join(output_dir, ntpath.basename(str(each_file)).split(".")[0] + ".txt"), "w") as file_isatab:
                        file_isatab.write(my_str.encode('ascii', errors='ignore'))
