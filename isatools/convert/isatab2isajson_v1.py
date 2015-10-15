__author__ = 'agbeltran'

import json
import os
from uuid import uuid4
from os import listdir
from os.path import isdir, join
import warlock

from isatools.io.isatab_parser import parse


SCHEMAS_PATH = join(os.path.dirname(os.path.realpath(__file__)), "../schemas/isa_model_version_1_0_schemas")
INVESTIGATION_SCHEMA = "investigation_schema.json"
STUDY_SCHEMA = "study_schema.json"
PUBLICATION_SCHEMA = "publication_schema.json"
ISA_MODEL_V1_SCHEMA = "isa_schema_v1.json"

class ISATab2ISAjson_v1():

    def __init__(self):
        pass

    def convert(self, work_dir, json_dir):
        """Convert an ISA-Tab dataset (version 1) to JSON provided the ISA model v1.0 JSON Schemas

            :param work_dir: directory containing the ISA-tab dataset
            :param json_dir: output directory where the resulting json file will be saved
        """
        print "Converting ISAtab to ISAjson for ", work_dir

        print SCHEMAS_PATH

        #investigation_schema = json.load(open(join(SCHEMAS_PATH,INVESTIGATION_SCHEMA)))
        #Investigation = warlock.model_factory(investigation_schema)
        isa_schema = json.load(open(join(SCHEMAS_PATH,ISA_MODEL_V1_SCHEMA)))
        ISAobject = warlock.model_factory(isa_schema)

        print ISAobject

        isa_tab = parse(work_dir)

        if isa_tab is None:
            print "No ISAtab dataset found"
        else:
                if isa_tab.metadata != {}:

                    #isa_json = Investigation(
                    isa_json = ISAobject(
                       identifier = isa_tab.metadata['Investigation Identifier'],
                       title = isa_tab.metadata['Investigation Title'],
                       description = isa_tab.metadata['Investigation Description'],
                       submissionDate = isa_tab.metadata['Investigation Submission Date'],
                       publicReleaseDate = isa_tab.metadata['Investigation Public Release Date'],
                       commentCreatedWithConfiguration = isa_tab.metadata['Comment[Created With Configuration]'],
                       commentLastOpenedWithConfiguration = isa_tab.metadata['Comment[Last Opened With Configuration]'],
                       ontologySourceReferences = [],
                       publications = [],
                       people = [],
                       studies = self.createStudyArray(isa_tab.studies)
                       )

                    print isa_json

    def createStudyArray(self, studies):

        study_schema = json.load(open(join(SCHEMAS_PATH,STUDY_SCHEMA)))
        Study = warlock.model_factory(study_schema)
        study_array = []
        for study in studies:
            studyJson = Study(
                identifer = study.metadata['Study Identifier'],
                title = study.metadata['Study Title'],
                description = study.metadata['Study Description'],
                submissionDate = study.metadata['Study Submission Date'],
                publicReleaseDate = study.metadata['Study Public Release Date'],
                people = [],
                studyDesignDescriptors = [],
                publications = [],
                protocols = [],
                sources = [],
                samples = [],
                processSequence = [],
                assays = []
            )
            study_array.append(studyJson)
        return study_array



isatab2isajson = ISATab2ISAjson_v1()
isatab2isajson.convert("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS1","../../tests/datasets/metabolights")