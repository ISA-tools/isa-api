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
ONTOLOGY_REF_SCHEMA = "ontology_source_reference_schema.json"
ISA_MODEL_V1_SCHEMA = "isa_schema_v1.json"

class ISATab2ISAjson_v1():

    def __init__(self):
        pass

    def convert(self, work_dir, json_dir, inv_identifier):
        """Convert an ISA-Tab dataset (version 1) to JSON provided the ISA model v1.0 JSON Schemas

            :param work_dir: directory containing the ISA-tab dataset
            :param json_dir: output directory where the resulting json file will be saved
        """
        print "Converting ISAtab to ISAjson for ", work_dir

        print SCHEMAS_PATH

        #warlock related
        #investigation_schema = json.load(open(join(SCHEMAS_PATH,INVESTIGATION_SCHEMA)))
        #Investigation = warlock.model_factory(investigation_schema)
        # isa_schema = json.load(open(join(SCHEMAS_PATH,ISA_MODEL_V1_SCHEMA)))
        # ISAobject = warlock.model_factory(isa_schema)

        isa_tab = parse(work_dir)

        if isa_tab is None:
            print "No ISAtab dataset found"
        else:
                if isa_tab.metadata != {}:
                    isa_json = dict([
                        ("identifier",isa_tab.metadata['Investigation Identifier']),
                        ("title", isa_tab.metadata['Investigation Title']),
                        ("description",isa_tab.metadata['Investigation Description']),
                        ("submissionDate", isa_tab.metadata['Investigation Submission Date']),
                        ("publicReleaseDate", isa_tab.metadata['Investigation Public Release Date']),
                        ("commentCreatedWithConfiguration", isa_tab.metadata['Comment[Created With Configuration]']),
                        ("commentLastOpenedWithConfiguration", isa_tab.metadata['Comment[Last Opened With Configuration]']),
                        ("ontologySourceReferences", self.createOntologySourceReferences(isa_tab.ontology_refs)),
                        ("publications", self.createPublications(isa_tab.publications, "Investigation")),
                        ("people", self.createContacts(isa_tab.contacts, "Investigation")),
                        ("studies", self.createStudies(isa_tab.studies))
                    ])
                    #isa_json = Investigation(
                    # isa_json = ISAobject(
                    #    identifier = isa_tab.metadata['Investigation Identifier'],
                    #    title = isa_tab.metadata['Investigation Title'],
                    #    description = isa_tab.metadata['Investigation Description'],
                    #    submissionDate = isa_tab.metadata['Investigation Submission Date'],
                    #    publicReleaseDate = isa_tab.metadata['Investigation Public Release Date'],
                    #    commentCreatedWithConfiguration = isa_tab.metadata['Comment[Created With Configuration]'],
                    #    commentLastOpenedWithConfiguration = isa_tab.metadata['Comment[Last Opened With Configuration]'],
                    #    ontologySourceReferences = self.createOntologySourceReferences(isa_tab.ontology_refs),
                    #    publications = self.createInvestigationPublications(isa_tab.publications),
                    #    people = [],
                    #    studies = self.createStudies(isa_tab.studies)
                    #    )

                if (inv_identifier):
                    file_name = os.path.join(json_dir,isa_tab.metadata['Investigation Identifier']+".json")
                else:
                    file_name = os.path.join(json_dir,isa_tab.studies[0].metadata['Study Identifier']+".json")

                #validate json

                with open(file_name, "w") as outfile:
                    json.dump(isa_json, outfile, indent=4, sort_keys=True)
                    outfile.close()
                print "... conversion finished."


    def createContacts(self, contacts, inv_or_study):
        people_json = []
        for contact in contacts:
            person_json = dict([
                ("lastName", contact[inv_or_study+" Person Last Name"]),
                ("firstName", contact[inv_or_study+" Person First Name"]),
                ("midInitials", contact[inv_or_study+" Person Mid Initials"]),
                ("email", contact[inv_or_study+" Person Email"]),
                ("phone", contact[inv_or_study+" Person Phone"]),
                ("fax", contact[inv_or_study+" Person Fax"]),
                ("address", contact[inv_or_study+" Person Address"]),
                ("affiliations", contact[inv_or_study+" Person Affiliation"]),
               #TODO
                ("roles", [])
            ])
            people_json.append(person_json)
        return people_json


    def createPublications(self, publications, inv_or_study):
        # publication_schema = json.load(open(join(SCHEMAS_PATH, PUBLICATION_SCHEMA)))
        # Publication = warlock.model_factory(publication_schema)
        # publications_json = []
        # for pub in publications:
        #     publication_json = Publication(
        #          pubMedID = pub[inv_or_study+' PubMed ID'],
        #          doi = pub[inv_or_study+' Publication DOI'],
        #          authorList = pub[inv_or_study+' Publication Author List'],
        #          title = pub[inv_or_study+' Publication Title'],
        #         #status = self.createStatusOntologyAnnotation(pub)
        #     )
        #     publications_json.append(publication_json)
        # return publications_json

        publications_json = []
        for pub in publications:
            publication_json = dict([
                ("pubMedID", pub[inv_or_study+' PubMed ID']),
                ("doi", pub[inv_or_study+' Publication DOI']),
                ("authorList", pub[inv_or_study+' Publication Author List']),
                ("title", pub[inv_or_study+' Publication Title']),
                ("status", self.createOntologyAnnotation(pub, inv_or_study, " Publication Status"))
            ]
            )
            publications_json.append(publication_json)
        return publications_json

    def createProtocols(self, protocols):
        protocols_json = []
        for protocol in protocols:
            protocol_json = dict([
                ("name", protocol['Study Protocol Name']),
                ("type", self.createOntologyAnnotation(protocol,"Study", " Protocol Type")),
                ("description", protocol['Study Protocol Description']),
                ("uri", protocol['Study Protocol URI']),
                ("version", protocol['Study Protocol Version']),
                ("parameters", self.createOntologyAnnotationsFromStringList(protocol,"Study", " Protocol Parameters Name")),
            ]
            )
            protocols_json.append(protocol_json)
        return protocols_json

    def createOntologyAnnotation(self, object, inv_or_study, type):
        onto_ann = dict([
            ("name", object[inv_or_study+type]),
            ("termSource", object[inv_or_study+type+" Term Source REF"]),
            ("termAccession", object[inv_or_study+type+" Term Accession Number"])
        ])
        return onto_ann


    def createOntologyAnnotationsFromStringList(self, object, inv_or_study, type):
        name_array = object[inv_or_study+type].split(";")
        term_source_array = object[inv_or_study+type+" Term Source REF"].split(";")
        term_accession_array = object[inv_or_study+type+" Term Accession Number"].split(";")
        onto_annotations = []

        for i in xrange(0,len(name_array)):
             onto_ann = dict([
                 ("name", name_array[i]),
                 ("termSource", term_source_array[i]),
                 ("termAccession", term_accession_array[i])
             ])
             onto_annotations.append(onto_ann)
        return onto_annotations


    def createOntologyAnnotationsFromObject(self, array, inv_or_study, type):
        onto_annotations = []
        for object in array:
            onto_ann = dict([
                ("name", object[inv_or_study+type]),
                ("termSource", object[inv_or_study+type+" Term Source REF"]),
                ("termAccession", object[inv_or_study+type+" Term Accession Number"])
            ])
            onto_annotations.append(onto_ann)
        return onto_annotations


    def createOntologySourceReferences(self, ontology_refs):
        ontology_reference_schema = json.load(open(join(SCHEMAS_PATH, ONTOLOGY_REF_SCHEMA)))
        OntologyRef = warlock.model_factory(ontology_reference_schema)
        ontologies = []
        for ontology_ref in ontology_refs:
            ontology = OntologyRef(
                 description = ontology_ref["Term Source Description"],
                 file = ontology_ref["Term Source File"],
                 name = ontology_ref["Term Source Name"],
                 version = ontology_ref["Term Source Version"]
            )
            ontologies.append(ontology)
        return ontologies

    def createStudies(self, studies):
        study_array = []
        for study in studies:
            studyJson = dict([
                ("identifier",study.metadata['Study Identifier']),
                ("title", study.metadata['Study Title']),
                ("description", study.metadata['Study Description']),
                ("submissionDate", study.metadata['Study Submission Date']),
                ("publicReleaseDate", study.metadata['Study Public Release Date']),
                ("people", self.createContacts(study.contacts, "Study")),
                ("studyDesignDescriptors",self.createOntologyAnnotationsFromObject(study.design_descriptors,"Study", " Design Type")),
                ("publications", self.createPublications(study.publications, "Study")),
                ("protocols", self.createProtocols(study.protocols)),
                ("sources", self.createSources(study.nodes)),
                ("samples",[]),
                ("processSequence", []),
                ("assays", [])
            ])
            study_array.append(studyJson)

        return study_array

        # study_schema = json.load(open(join(SCHEMAS_PATH,STUDY_SCHEMA)))
        # Study = warlock.model_factory(study_schema)
        # study_array = []
        # for study in studies:
        #     studyJson = Study(
        #         identifier = study.metadata['Study Identifier'],
        #         title = study.metadata['Study Title'],
        #         description = study.metadata['Study Description'],
        #         submissionDate = study.metadata['Study Submission Date'],
        #         publicReleaseDate = study.metadata['Study Public Release Date'],
        #         people = self.createContacts(study.contacts, "Study"),
        #         studyDesignDescriptors = [],
        #         publications = [],#self.createInvestigationPublications(study.publications),
        #         protocols = [],
        #         sources = [],
        #         samples = [],
        #         processSequence = [],
        #         assays = []
        #     )
        #     study_array.append(studyJson)
        # return study_array



    def createSources(self, nodes):
        json_dict = dict([])
        for node_name in nodes:
            if nodes[node_name].ntype == "Source Name":
                json_item = dict([
                    ("name", dict([("value", node_name)])),
                    ("characteristics", self.createCharacteristicList(node_name, nodes[node_name])),
                ])
                json_dict.update({node_name: json_item})
        return json_dict


    def createCharacteristicList(self, node_name, node):
        json_list = []
        for header in node.metadata:
            if header.startswith("Characteristics"):
                 characteristic = header.replace("]", "").split("[")[-1]
                 json_item = dict([
                    ("name", dict([("value", characteristic)])),
                    ("termSource", dict([("value", "")])),
                    ("termAccession", self.createCharacteristicValueList(node.metadata[header]))
                    ])
                 json_list.append(json_item)
        return json_list



isatab2isajson = ISATab2ISAjson_v1()
#isatab2isajson.convert("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS1","../../tests/datasets/metabolights", False)
isatab2isajson.convert("../../tests/data/BII-I-1","../../tests/data", True)