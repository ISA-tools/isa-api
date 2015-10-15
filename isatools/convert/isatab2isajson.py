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

class ISATab2ISAjson():

    def convert(self, work_dir, json_dir):
        print "Converting ISAtab to ISAjson for ", work_dir
        investigation_schema = json.load(open(join(SCHEMAS_PATH,INVESTIGATION_SCHEMA)))
        Investigation = warlock.model_factory(investigation_schema)

        isa_tab = parse(work_dir)

        if isa_tab is None:
            print "No ISAtab dataset found"
        else:
                if isa_tab.metadata != {}:

                    isa_json = Investigation(
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
                       studies = []
                       )

                    print isa_json




isatab2isajson = ISATab2ISAjson()
isatab2isajson.convert("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS1","../../tests/datasets/metabolights")