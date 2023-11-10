from isatools import isajson
from isatools.model import (
    Investigation, Study, Comment, OntologySource, OntologyAnnotation, Person, Publication, Source, Characteristic,
    Sample, batch_create_materials, Protocol, Process, StudyFactor, Assay, Material, DataFile, plink,

)
from isatools.tests import utils
import unittest
import json
import os


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


def create_descriptor(use_strings_for_characteristic_categories=False):
    """
    Returns a simple but complete ISA-JSON 1.0 descriptor for illustration.
    """

    # Create an empty Investigation object and set some values to the
    # instance variables.

    investigation = Investigation()
    investigation.identifier = "1"
    investigation.title = "My Simple ISA Investigation"
    investigation.description = \
        "We could alternatively use the class constructor's parameters to " \
        "set some default values at the time of creation, however we " \
        "want to demonstrate how to use the object's instance variables " \
        "to set values."
    investigation.submission_date = "2016-11-03"
    investigation.public_release_date = "2016-11-03"

    # Create an empty Study object and set some values. The Study must have a
    # filename, otherwise when we serialize it to ISA-Tab we would not know
    # where to write it. We must also attach the study to the investigation
    # by adding it to the 'investigation' object's list of studies.

    study = Study(filename="s_study.txt")
    study.identifier = "2"
    study.title = "My ISA Study"
    study.description = \
        "Like with the Investigation, we could use the class constructor " \
        "to set some default values, but have chosen to demonstrate in this " \
        "example the use of instance variables to set initial values."
    study.submission_date = "2016-11-03"
    study.public_release_date = "2016-11-03"
    investigation.studies.append(study)

    # this is to test if Comments are properly generated)
    study.comments.append(Comment(name="Study Start Date", value="Sun"))

    # Some instance variables are typed with different objects and lists of
    # objects. For example, a Study can have a list of design descriptors.
    # A design descriptor is an Ontology Annotation describing the kind of
    # study at hand. Ontology Annotations should typically reference an
    # Ontology Source. We demonstrate a mix of using the class constructors
    # and setting values with instance variables. Note that the
    # OntologyAnnotation object 'intervention_design' links its 'term_source'
    # directly to the 'obi' object instance. To ensure the OntologySource
    # is encapsulated in the descriptor, it is added to a list of
    # 'ontology_source_references' in the Investigation object. The
    # 'intervention_design' object is then added to the list of
    # 'design_descriptors' held by the Study object.

    obi = OntologySource(name='OBI',
                         description="Ontology for Biomedical Investigations")
    investigation.ontology_source_references.append(obi)
    intervention_design = OntologyAnnotation(term_source=obi)
    intervention_design.term = "intervention design"
    intervention_design.term_accession = \
        "http://purl.obolibrary.org/obo/OBI_0000115"
    study.design_descriptors.append(intervention_design)

    # Other instance variables common to both Investigation and Study objects
    # include 'contacts' and 'publications', each with lists of corresponding
    # Person and Publication objects.

    contact = Person(first_name="Alice", last_name="Robertson",
                     affiliation="University of Life",
                     roles=[OntologyAnnotation(term='submitter')])
    study.contacts.append(contact)
    publication = Publication(title="Experiments with Elephants",
                              author_list="A. Robertson, B. Robertson")
    publication.pubmed_id = "12345678"
    publication.status = OntologyAnnotation(term="published")
    study.publications.append(publication)

    # To create the study graph that corresponds to the contents of the study
    # table file (the s_*.txt file), we need to create a process sequence.
    # To do this we use the Process class and attach it to the Study object's
    # 'process_sequence' list instance variable. Each process must be linked
    # with a Protocol object that is attached to a Study object's 'protocols'
    # list instance variable. The sample collection Process object usually has
    # as input a Source material and as output a Sample material.

    # Here we create one Source material object and attach it to our study.

    source = Source(name='source_material')
    study.sources.append(source)

    # Then we create three Sample objects, with organism as Homo Sapiens, and
    # attach them to the study. We use the utility function
    # batch_create_material() to clone a prototype material object. The
    # function automatically appends an index to the material name. In this
    # case, three samples will be created, with the names 'sample_material-0',
    # 'sample_material-1' and 'sample_material-2'.

    ncbitaxon = OntologySource(name='NCBITaxon', description="NCBI Taxonomy")
    investigation.ontology_source_references.append(ncbitaxon)

    characteristic_organism = Characteristic(
        category=OntologyAnnotation(term="Organism") if not use_strings_for_characteristic_categories else "Organism",
        value=OntologyAnnotation(
            term="Homo Sapiens",
            term_source=ncbitaxon,
            term_accession="http://purl.bioontology.org/ontology/NCBITAXON/"
                           "9606"))

    # Adding the description to the ISA Source Material:
    source.characteristics.append(characteristic_organism)

    # declaring a new ontology and adding it to the list of resources used
    uberon = OntologySource(name='UBERON', description='Uber Anatomy Ontology')
    investigation.ontology_source_references.append(uberon)

    # preparing an ISA Characteristic object (~Material Property ) to annotate sample materials
    characteristic_organ = Characteristic(
        category=OntologyAnnotation(
            term="OrganismPart"
        ) if not use_strings_for_characteristic_categories else "OrganismPart",
        value=OntologyAnnotation(
            term="liver",
            term_source=uberon,
            term_accession="http://purl.bioontology.org/ontology/UBERON/"
                           "123245"))

    prototype_sample = Sample(name='sample_material', derives_from=[source])

    prototype_sample.characteristics.append(characteristic_organ)
    study.samples = batch_create_materials(prototype_sample, n=3)
    # creates a batch of 3 samples

    # IMPORTANT: remember to populate the list of ontology categories used to annotation ISA Material in a Study:
    study.characteristic_categories.append(characteristic_organism.category)
    study.characteristic_categories.append(characteristic_organ.category)

    # Now we create a single Protocol object that represents our sample
    # collection protocol, and attach it to the study object. Protocols must be
    # declared before we describe Processes, as a processing event of some sort
    # must execute some defined protocol. In the case of the class model,
    # Protocols should therefore be declared before Processes in order for the
    # Process to be linked to one.

    sample_collection_protocol = Protocol(
        name="sample collection",
        protocol_type=OntologyAnnotation(term="sample collection"))
    study.protocols.append(sample_collection_protocol)
    sample_collection_process = Process(
        executes_protocol=sample_collection_protocol)

    # adding a dummy Comment[] to ISA.protocol object
    study.protocols[0].comments.append(Comment(name="Study Start Date", value="Uranus"))
    study.protocols[0].comments.append(Comment(name="Study End Date", value="2017-08-11"))
    # checking that the ISA Protocol object has been modified
    # print(study.protocols[0])

    # Creation of an ISA Study Factor object
    f = StudyFactor(name="treatment['modality']", factor_type=OntologyAnnotation(term="treatment['modality']"))
    # testing serialization to ISA-TAB of Comments attached to ISA objects.
    f.comments.append(Comment(name="Study Start Date", value="Saturn"))
    f.comments.append(Comment(name="Study End Date", value="2039-12-12"))
    # print(f.comments[0].name, "|", f.comments[0].value)

    # checking that the ISA Factor object has been modified
    study.factors.append(f)

    # Next, we link our materials to the Process. In this particular case, we
    # are describing a sample collection process that takes one source
    # material, and produces three different samples.
    #
    # (source_material)->(sample collection)->
    # [(sample_material-0), (sample_material-1), (sample_material-2)]

    for src in study.sources:
        sample_collection_process.inputs.append(src)
    for sam in study.samples:
        sample_collection_process.outputs.append(sam)

    # Finally, attach the finished Process object to the study
    # process_sequence. This can be done many times to describe multiple
    # sample collection events.

    study.process_sequence.append(sample_collection_process)

    # Next, we build n Assay object and attach two protocols,
    # extraction and sequencing.

    assay = Assay(filename="a_assay.txt")
    extraction_protocol = Protocol(
        name='extraction',
        protocol_type=OntologyAnnotation(term="material extraction"))
    study.protocols.append(extraction_protocol)
    sequencing_protocol = Protocol(
        name='sequencing',
        protocol_type=OntologyAnnotation(term="material sequencing"))
    study.protocols.append(sequencing_protocol)

    # To build out assay graphs, we enumerate the samples from the
    # study-level, and for each sample we create an extraction process and
    # a sequencing process. The extraction process takes as input a sample
    # material, and produces an extract material. The sequencing process
    # takes the extract material and produces a data file. This will
    # produce three graphs, from sample material through to data, as follows:
    #
    # (sample_material-0)->(extraction)->(extract-0)->(sequencing)->
    # (sequenced-data-0)
    # (sample_material-1)->(extraction)->(extract-1)->(sequencing)->
    # (sequenced-data-1)
    # (sample_material-2)->(extraction)->(extract-2)->(sequencing)->
    # (sequenced-data-2)
    #
    # Note that the extraction processes and sequencing processes are
    # distinctly separate instances, where the three
    # graphs are NOT interconnected.

    for i, sample in enumerate(study.samples):
        # create an extraction process that executes the extraction protocol

        extraction_process = Process(executes_protocol=extraction_protocol)

        # extraction process takes as input a sample, and produces an extract
        # material as output

        extraction_process.inputs.append(sample)
        material = Material(name="extract-{}".format(i))
        material.type = "Extract Name"
        extraction_process.outputs.append(material)

        # create a sequencing process that executes the sequencing protocol

        sequencing_process = Process(executes_protocol=sequencing_protocol)
        sequencing_process.name = "assay-name-{}".format(i)
        sequencing_process.inputs.append(extraction_process.outputs[0])

        # Sequencing process usually has an output data file

        datafile = DataFile(filename="sequenced-data-{}".format(i),
                            label="Raw Data File", generated_from=[sample])
        sequencing_process.outputs.append(datafile)

        # ensure Processes are linked
        plink(sequencing_process, extraction_process)

        # make sure the extract, data file, and the processes are attached to
        # the assay

        assay.samples.append(sample)
        assay.data_files.append(datafile)
        assay.other_material.append(material)
        assay.process_sequence.append(extraction_process)
        assay.process_sequence.append(sequencing_process)
        assay.measurement_type = OntologyAnnotation(term="gene sequencing")
        assay.technology_type = OntologyAnnotation(
            term="nucleotide sequencing")

    # attach the assay to the study
    study.assays.append(assay)

    return investigation

    # import json
    # from isatools.isajson import ISAJSONEncoder
    #
    # # To write JSON out, use the ISAJSONEncoder class with the json package
    # # and use dump() or dumps(). Note that the extra parameters sort_keys,
    # # indent and separators are to make the output more human-readable.
    #
    # return json.dumps(investigation, cls=ISAJSONEncoder,
    #                   sort_keys=True, indent=4, separators=(',', ': '))


class TestIsaJson(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR

    def test_json_load_and_dump_bii_i_1(self):
        # Load into ISA objects
        with open(os.path.join(utils.JSON_DATA_DIR, 'BII-I-1', 'BII-I-1.json')) as isajson_fp:
            ISA = isajson.load(isajson_fp)

            # Dump into ISA JSON from ISA objects
            ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))

            self.assertListEqual([s['filename'] for s in ISA_J['studies']],
                                 ['s_BII-S-1.txt', 's_BII-S-2.txt'])  # 2 studies in i_investigation.txt

            study_bii_s_1 = [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-1.txt'][0]

            self.assertEqual(len(study_bii_s_1['materials']['sources']), 18)  # 18 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_1['materials']['samples']), 164)  # 164 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_1['processSequence']), 18)  # 18 study processes in s_BII-S-1.txt

            self.assertListEqual([a['filename'] for a in study_bii_s_1['assays']],
                                 ['a_proteome.txt', 'a_metabolome.txt',
                                  'a_transcriptome.txt'])  # 2 assays in s_BII-S-1.txt

            assay_proteome = [a for a in study_bii_s_1['assays'] if a['filename'] == 'a_proteome.txt'][0]

            self.assertEqual(len(assay_proteome['materials']['samples']), 8)  # 8 assay samples in a_proteome.txt
            self.assertEqual(len(assay_proteome['materials']['otherMaterials']),
                             19)  # 19 other materials in a_proteome.txt
            self.assertEqual(len(assay_proteome['dataFiles']), 7)  # 7 data files  in a_proteome.txt
            self.assertEqual(len(assay_proteome['processSequence']), 25)  # 25 processes in in a_proteome.txt

            assay_metabolome = [a for a in study_bii_s_1['assays'] if a['filename'] == 'a_metabolome.txt'][0]

            self.assertEqual(len(assay_metabolome['materials']['samples']), 92)  # 92 assay samples in a_metabolome.txt
            self.assertEqual(len(assay_metabolome['materials']['otherMaterials']),
                             92)  # 92 other materials in a_metabolome.txt
            self.assertEqual(len(assay_metabolome['dataFiles']), 111)  # 111 data files  in a_metabolome.txt
            self.assertEqual(len(assay_metabolome['processSequence']), 203)  # 203 processes in in a_metabolome.txt

            assay_transcriptome = [a for a in study_bii_s_1['assays'] if a['filename'] == 'a_transcriptome.txt'][0]

            self.assertEqual(len(assay_transcriptome['materials']['samples']),
                             48)  # 48 assay samples in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome['materials']['otherMaterials']),
                             96)  # 96 other materials in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome['dataFiles']), 49)  # 49 data files  in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome['processSequence']),
                             193)  # 203 processes in in a_transcriptome.txt

            study_bii_s_2 = [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-2.txt'][0]

            self.assertEqual(len(study_bii_s_2['materials']['sources']), 1)  # 1 sources in s_BII-S-2.txt
            self.assertEqual(len(study_bii_s_2['materials']['samples']), 2)  # 2 study samples in s_BII-S-2.txt
            self.assertEqual(len(study_bii_s_2['processSequence']), 1)  # 1 study processes in s_BII-S-2.txt

            self.assertEqual(len(study_bii_s_2['assays']), 1)  # 1 assays in s_BII-S-2.txt
            self.assertListEqual([a['filename'] for a in study_bii_s_2['assays']],
                                 ['a_microarray.txt'])  # 1 assays in s_BII-S-2.txt

            assay_microarray = [a for a in study_bii_s_2['assays'] if a['filename'] == 'a_microarray.txt'][0]

            self.assertEqual(len(assay_microarray['materials']['samples']), 2)  # 2 assay samples in a_microarray.txt
            self.assertEqual(len(assay_microarray['materials']['otherMaterials']),
                             28)  # 28 other materials in a_microarray.txt
            self.assertEqual(len(assay_microarray['dataFiles']), 15)  # 15 data files  in a_microarray.txt
            self.assertEqual(len(assay_microarray['processSequence']), 45)  # 45 processes in in a_microarray.txt

    def test_json_load_and_dump_bii_s_3(self):
        # Load into ISA objects
        with open(os.path.join(utils.JSON_DATA_DIR, 'BII-S-3', 'BII-S-3.json')) as isajson_fp:
            ISA = isajson.load(isajson_fp)

            # Dump into ISA JSON from ISA objects
            ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))

            self.assertListEqual([s['filename'] for s in ISA_J['studies']],
                                 ['s_BII-S-3.txt'])  # 1 studies in i_gilbert.txt

            study_bii_s_3 = [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-3.txt'][0]

            self.assertEqual(len(study_bii_s_3['materials']['sources']), 4)  # 4 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_3['materials']['samples']), 4)  # 4 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_3['processSequence']), 4)  # 4 study processes in s_BII-S-1.txt

            self.assertListEqual([a['filename'] for a in study_bii_s_3['assays']],
                                 ['a_gilbert-assay-Gx.txt', 'a_gilbert-assay-Tx.txt'])  # 2 assays in s_BII-S-1.txt

            assay_gx = [a for a in study_bii_s_3['assays'] if a['filename'] == 'a_gilbert-assay-Gx.txt'][0]

            self.assertEqual(len(assay_gx['materials']['samples']), 4)  # 4 assay samples in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx['materials']['otherMaterials']),
                             4)  # 4 other materials in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx['dataFiles']), 6)  # 6 data files  in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx['processSequence']), 18)  # 18 processes in in a_gilbert-assay-Gx.txt

            assay_tx = [a for a in study_bii_s_3['assays'] if a['filename'] == 'a_gilbert-assay-Tx.txt'][0]

            self.assertEqual(len(assay_tx['materials']['samples']), 4)  # 4 assay samples in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx['materials']['otherMaterials']),
                             4)  # 4 other materials in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx['dataFiles']), 24)  # 24 data files  in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx['processSequence']), 36)  # 36 processes in in a_gilbert-assay-Tx.txt

    def test_json_load_and_dump_bii_s_7(self):
        # Load into ISA objects
        with open(os.path.join(utils.JSON_DATA_DIR, 'BII-S-7', 'BII-S-7.json')) as isajson_fp:
            ISA = isajson.load(isajson_fp)

            # Dump into ISA JSON from ISA objects
            ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))

            self.assertListEqual([s['filename'] for s in ISA_J['studies']],
                                 ['s_BII-S-7.txt'])  # 1 studies in i_gilbert.txt

            study_bii_s_7 = [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-7.txt'][0]

            self.assertEqual(len(study_bii_s_7['materials']['sources']), 29)  # 29 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_7['materials']['samples']), 29)  # 29 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_7['processSequence']), 29)  # 29 study processes in s_BII-S-1.txt

            self.assertListEqual([a['filename'] for a in study_bii_s_7['assays']],
                                 ['a_matteo-assay-Gx.txt'])  # 1 assays in s_BII-S-1.txt

            assay_gx = [a for a in study_bii_s_7['assays'] if a['filename'] == 'a_matteo-assay-Gx.txt'][0]

            self.assertEqual(len(assay_gx['materials']['samples']), 29)  # 29 assay samples in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx['materials']['otherMaterials']),
                             29)  # 29 other materials in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx['dataFiles']), 29)  # 29 data files  in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx['processSequence']), 116)  # 116 processes in in a_matteo-assay-Gx.txt

    def test_json_load_and_dump_bii_s_test(self):
        # Load into ISA objects
        with open(os.path.join(utils.JSON_DATA_DIR, 'ISA-1', 'isa-test1.json')) as isajson_fp:
            ISA = isajson.load(isajson_fp)

            # Dump into ISA JSON from ISA objects
            ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))
            study_bii_s_test = [s for s in ISA_J['studies'] if s['filename'] == 's_study.txt'][0]
            assay_gx = [a for a in study_bii_s_test['assays'] if a['filename'] == 'a_assay.txt'][0]

    def test_json_load_and_dump_isa_le_test(self):
        # Load into ISA objects
        with open(os.path.join(utils.JSON_DATA_DIR, 'TEST-ISA-LabeledExtract1', 'isa-test-le1.json')) as isajson_fp:
            ISA = isajson.load(isajson_fp)

            # Dump into ISA JSON from ISA objects
            ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))
            study_bii_s_test = [s for s in ISA_J['studies'] if s['filename'] == 's_study.txt'][0]
            assay_gx = [a for a in study_bii_s_test['assays'] if a['filename'] == 'a_assay.txt'][0]
            self.assertEqual(assay_gx['materials']['otherMaterials'][3]["type"], "Labeled Extract Name")

    def test_json_load_from_file_and_create_isa_objects(self):
        # reading from file
        with open(os.path.join(utils.JSON_DATA_DIR, 'ISA-1', 'isa-test1.json')) as isajson_fp:
            inv = isajson.load(isajson_fp)

            # Dump into ISA JSON from ISA objects
            ISA_J = json.loads(json.dumps(inv, cls=isajson.ISAJSONEncoder))

            self.assertListEqual([s['filename'] for s in ISA_J['studies']], ['s_study.txt'])

            study_isa_1 = [s for s in ISA_J['studies'] if s['filename'] == 's_study.txt'][0]
            self.assertEqual(len(study_isa_1['materials']['sources']), 1)  # 1 sources in s_study.txt
            self.assertEqual(len(study_isa_1['materials']['samples']), 3)  # 3 sources in s_study.txt

    def test_create_isajson_and_write_to_file(self):
        test_isainvestigation = create_descriptor()

        isa_j = json.dumps(
            test_isainvestigation, cls=isajson.ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')
        )

        with open(os.path.join(utils.JSON_DATA_DIR, 'ISA-1', 'isa-test1.json'), 'w') as out_fp:
            out_fp.write(isa_j)

        out_fp.close()

    def test_isajson_with_strings_as_characteristic_category(self):
        test_isa_investigation = create_descriptor(use_strings_for_characteristic_categories=True)
        isa_j = json.dumps(
            test_isa_investigation, cls=isajson.ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')
        )
        self.assertIsInstance(isa_j, str)
        with open(os.path.join(utils.JSON_DATA_DIR, 'ISA-1', 'isa-test2.json'), 'w') as out_fp:
            out_fp.write(isa_j)
        with open(os.path.join(utils.JSON_DATA_DIR, 'ISA-1', 'isa-test2.json')) as in_fp:
            reverse_test_isa_investigation = isajson.load(in_fp)
            self.assertIsInstance(reverse_test_isa_investigation, Investigation)
