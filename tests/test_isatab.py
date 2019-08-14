"""Tests on isatab.py package"""
from __future__ import absolute_import
import unittest
import os
import pandas as pd
import shutil
import tempfile
from io import StringIO

from isatools import isatab
from isatools.io import isatab_parser
from isatools.isatab import ProcessSequenceFactory
from isatools.model import *
from isatools.tests.utils import assert_tab_content_equal
from isatools.tests import utils
from isatools.isatab import IsaTabDataFrame


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaMerge(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_merge_bii_s_1_with_a_proteome(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_proteome.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        # num rows expected is max of input DFs
        self.assertEqual(merged_DF.shape[0], 18)
        # num columns expected is sum of input DFs, minus index column
        self.assertEqual(merged_DF.shape[1], 43)

    def test_merge_bii_s_1_with_a_metabolome(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_metabolome.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        self.assertEqual(merged_DF.shape[0], 111)
        self.assertEqual(merged_DF.shape[1], 41)

    def test_merge_bii_s_1_with_a_transcriptome(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_transcriptome.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        self.assertEqual(merged_DF.shape[0], 48)
        self.assertEqual(merged_DF.shape[1], 40)

    def test_merge_bii_s_2_with_a_microarray(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-2.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_microarray.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        self.assertEqual(merged_DF.shape[0], 14)
        self.assertEqual(merged_DF.shape[1], 43)

    def test_merge_bii_s_1_with_a_microarray(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_microarray.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        self.assertEqual(merged_DF.shape[0], 0)  # tests no matching samples
        self.assertEqual(merged_DF.shape[1], 47)  # still prints out joined header though


class TestIsaTabDump(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab_bad_i_file_name(self):
        with self.assertRaises(NameError):
            isatab.dump(Investigation(), self._tmp_dir, i_file_name='investigation.txt')

    def test_isatab_dump_source_sample_split(self):
        i = Investigation()
        uberon = OntologySource(name='UBERON',
                                description="Uber Anatomy Ontology",
                                version='216',
                                file='http://data.bioontology.org/ontologies/UBERON')
        ncbitaxon = OntologySource(name='NCBITAXON',
                                   description="National Center for Biotechnology Information (NCBI) Organismal Classification",
                                   version='2',
                                   file='http://data.bioontology.org/ontologies/NCBITAXON')
        i.ontology_source_references.append(uberon)
        i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_pool.txt')

        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(term='sample collection')
        )

        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = OntologyAnnotation(term='reference descriptor')
        material_type_category = OntologyAnnotation(term='material type')
        organism_category = OntologyAnnotation(term='organism')

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = OntologyAnnotation(term='organism part')
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample2 = Sample(name='sample2')
        sample2.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='heart',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000948',
        )))

        sample3 = Sample(name='sample3')
        sample3.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample4 = Sample(name='sample4')
        sample4.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample_collection_process = Process(executes_protocol=sample_collection_protocol)

        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1, sample2, sample3, sample4]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_pool.txt')) as actual_file, \
                open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split',
                                  's_TEST-Template1-Splitting.txt')) as expected_file:
            self.assertTrue(assert_tab_content_equal(actual_file, expected_file))

    def test_isatab_dump_source_sample_pool(self):
        i = Investigation()
        uberon = OntologySource(name='UBERON')
        ncbitaxon = OntologySource(name='NCBITAXON')
        i.ontology_source_references.append(uberon)
        i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_pool.txt')
        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(term='sample collection')
        )

        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = OntologyAnnotation(term='reference descriptor')
        material_type_category = OntologyAnnotation(term='material type')
        organism_category = OntologyAnnotation(term='organism')

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source2 = Source(name='source2')
        source2.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source3 = Source(name='source3')
        source3.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source4 = Source(name='source4')
        source4.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = OntologyAnnotation(term='organism part')
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample_collection_process = Process(executes_protocol=sample_collection_protocol)

        sample_collection_process.inputs = [source1, source2, source3, source4]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_pool.txt')) as actual_file, \
                open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool',
                                  's_TEST-Template3-Splitting.txt')) as expected_file:
            self.assertTrue(assert_tab_content_equal(actual_file, expected_file))
            self.assertIsInstance(isatab.dumps(i), str)

    def test_isatab_dump_source_sample_sample(self):
        # Validates issue fix for #191
        i = Investigation()
        uberon = OntologySource(name='UBERON')
        ncbitaxon = OntologySource(name='NCBITAXON')
        i.ontology_source_references.append(uberon)
        i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_pool.txt')
        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(term='sample collection')
        )
        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = OntologyAnnotation(term='reference descriptor')
        material_type_category = OntologyAnnotation(term='material type')
        organism_category = OntologyAnnotation(term='organism')

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source2 = Source(name='source2')
        source2.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source3 = Source(name='source3')
        source3.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source4 = Source(name='source4')
        source4.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = OntologyAnnotation(term='organism part')
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample_collection_process = Process(executes_protocol=sample_collection_protocol)

        sample_collection_process2 = Process(executes_protocol=sample_collection_protocol)
        sample2 = Sample(name='sample2')

        sample_collection_process.inputs = [source1, source2, source3, source4]
        sample_collection_process.outputs = [sample1]
        sample_collection_process2.inputs = [sample1]
        sample_collection_process2.outputs = [sample2]
        s.process_sequence = [sample_collection_process, sample_collection_process2]
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_pool.txt')) as actual_file, \
                open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool-sample-chain',
                                  's_TEST-Template3-Splitting.txt')) as expected_file:
            self.assertTrue(assert_tab_content_equal(actual_file, expected_file))
            self.assertIsInstance(isatab.dumps(i), str)

    def test_isatab_dump_investigation_multiple_comments(self):
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
        investigation.comments.append(Comment(name="Investigation Start Date", value="Venus"))
        # Create an empty Study object and set some values. The Study must have a
        # filename, otherwise when we serialize it to ISA-Tab we would not know
        # where to write it. We must also attach the study to the investigation
        # by adding it to the 'investigation' object's list of studies.

        study = Study(filename="s_study.txt")
        study.identifier = "1"
        study.title = "My ISA Study"
        study.description = \
            "Like with the Investigation, we could use the class constructor " \
            "to set some default values, but have chosen to demonstrate in this " \
            "example the use of instance variables to set initial values."
        study.submission_date = "2016-11-03"
        study.public_release_date = "2016-11-03"

        # This is to show that ISA Comments can be used to annotate ISA objects, here ISA Study
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
                             description="Ontology for Biomedical Investigations", file="", version="1.0")

        # NOTE: The following call is not allowed by the model. This means that Comments can not be set programmatically
        # to annotation ONTOLOGY SOURCE REFERENCE SECTION
        # i.ontology_source_references.comments.append(Comment(name="test", value="test-value"))
        # instead you should do the following:
        # testing additon of comment and handling by ISA serializer
        obi.comments.append(Comment(name="reasoning type", value="using the reasoned version"))
        obi.comments.append(Comment(name="Ontology rating", value="sweet"))

        investigation.ontology_source_references.append(obi)

        intervention_design = OntologyAnnotation(term_source=obi)
        intervention_design.term = "intervention design"
        intervention_design.term_accession = \
            "http://purl.obolibrary.org/obo/OBI_0000115"
        # NOTE: to add a comment to the ISA-Tab STUDY DESIGN DESCRIPTOR Section in the ISA investigation file,
        # add a comment to the OntologyAnnotations accumulated in the ISA design_descriptors object.
        intervention_design.comments.append(Comment(name="Study Design Descriptor", value="Intelligent Study Design"))
        intervention_design.comments.append(Comment(name="design rating", value="rating 2"))
        intervention_design.comments.append(Comment(name="critics", value="terrible"))
        study.design_descriptors.append(intervention_design)

        other_design = OntologyAnnotation(term_source=obi)
        other_design.term="italian design"
        other_design.comments.append(Comment(name="Study Design Descriptor", value="smart design"))
        other_design.comments.append(Comment(name="design rating", value="rating 4"))
        other_design.comments.append(Comment(name="award", value="London award"))
        other_design.comments.append(Comment(name="critics", value="awful"))
        study.design_descriptors.append(other_design)

        another_design = OntologyAnnotation(term_source=obi)
        another_design.term = "scandinavian design"
        another_design.comments.append(Comment(name="Study Design Descriptor", value="minimalist design"))
        another_design.comments.append(Comment(name="design rating", value="rating 3"))
        another_design.comments.append(Comment(name="award", value="London award"))
        another_design.comments.append(Comment(name="critics", value="dreadful"))
        study.design_descriptors.append(another_design)
        # Other instance variables common to both Investigation and Study objects
        # include 'contacts' and 'publications', each with lists of corresponding
        # Person and Publication objects.

        contact1 = Person(first_name="Alice", last_name="Robertson",
                         affiliation="University of Life",
                         roles=[OntologyAnnotation(term='submitter')])
        # testing additon of comment and handling by ISA serializer
        contact1.comments.append(Comment(name="Study Person comment", value="outstanding person"))

        contact2 = Person(first_name="Bob", last_name="Cat",
                         affiliation="University of Life",
                         roles=[OntologyAnnotation(term='submitter')])
        # testing additon of comment and handling by ISA serializer
        contact2.comments.append(Comment(name="Study Person comment", value="cool person"))
        contact2.comments.append(Comment(name="Study Person HR rating", value="#1"))
        study.contacts.append(contact1)
        study.contacts.append(contact2)

        investigation.contacts.append(contact2)

        publication1 = Publication(title="Experiments with Elephants", author_list="A. Robertson, B. Robertson")
        publication1.pubmed_id = "12345678"
        publication1.status = OntologyAnnotation(term="published")
        publication1.comments.append(Comment(name="Study Publication Comment", value="great manuscript"))
        publication1.comments.append(Comment(name="Study Publication addendum", value="retracted manuscript"))
        publication2 = Publication(title="Experiments with Bananas", author_list="C. Olsen, B. Lundgren")
        publication2.pubmed_id = "18888881"
        publication2.status = OntologyAnnotation(term="published")
        publication2.comments.append(Comment(name="Study Publication Comment", value="another great manuscript"))

        study.publications.append(publication1)
        study.publications.append(publication2)

        # To create the study graph that corresponds to the contents of the study
        # table file (the s_*.txt file), we need to create a process sequence.
        # To do this we use the Process class and attach it to the Study object's
        # 'process_sequence' list instance variable. Each process must be linked
        # with a Protocol object that is attached to a Study object's 'protocols'
        # list instance variable. The sample collection Process object usually has
        # as input a Source material and as output a Sample material.

        # Here we create one Source material object and attach it to our study.

        source = Source(name='source_material')
        source.comments.append(Comment(name="Source Comment", value="brilliant"))
        study.sources.append(source)

        # Then we create three Sample objects, with organism as Homo Sapiens, and
        # attach them to the study. We use the utility function
        # batch_create_material() to clone a prototype material object. The
        # function automatically appends an index to the material name. In this
        # case, three samples will be created, with the names 'sample_material-0',
        # 'sample_material-1' and 'sample_material-2'.

        prototype_sample = Sample(name='sample_material', derives_from=[source])

        ncbitaxon = OntologySource(name='NCBITaxon', description="NCBI Taxonomy")
        ncbitaxon.comments.append(Comment(name="reasoning type", value="unreasoned version"))
        ncbitaxon.comments.append(Comment(name="Ontology rating", value="cool resource"))

        investigation.ontology_source_references.append(ncbitaxon)

        characteristic_organism = Characteristic(
            category=OntologyAnnotation(term="Organism"),
            value=OntologyAnnotation(
                term="Homo Sapiens",
                term_source=ncbitaxon,
                term_accession="http://purl.bioontology.org/ontology/NCBITAXON/"
                               "9606"))

        # Adding the description to the ISA Source Material:
        source.characteristics.append(characteristic_organism)
        study.sources.append(source)

        # declaring a new ontology and adding it to the list of resources used
        uberon = OntologySource(name='UBERON', description='Uber Anatomy Ontology')
        uberon.comments.append(Comment(name="reasoning type", value="unreasoned version"))
        uberon.comments.append(Comment(name="Ontology rating", value="resource tres froide"))
        uberon.comments.append(Comment(name="organization", value="obo"))
        investigation.ontology_source_references.append(uberon)

        # preparing an ISA Characteristic object (~Material Property ) to annotate sample materials
        characteristic_organ = Characteristic(
            category=OntologyAnnotation(term="OrganismPart"),
            value=OntologyAnnotation(
                term="liver",
                term_source=uberon,
                term_accession="http://purl.bioontology.org/ontology/UBERON/"
                               "123245"))

        prototype_sample.characteristics.append(characteristic_organ)
        prototype_sample.comments.append(Comment(name="Sample ComText", value="is this real?"))

        study.samples = batch_create_materials(prototype_sample, n=3)
        # creates a batch of 3 samples

        # Now we create a single Protocol object that represents our sample
        # collection protocol, and attach it to the study object. Protocols must be
        # declared before we describe Processes, as a processing event of some sort
        # must execute some defined protocol. In the case of the class model,
        # Protocols should therefore be declared before Processes in order for the
        # Process to be linked to one.

        sample_collection_protocol = Protocol(
            name="sample collection-TEST",
            protocol_type=OntologyAnnotation(term="sample collection-TEST"))

        param1 = ProtocolParameter(parameter_name=OntologyAnnotation(term="Collection Date"))
        sample_collection_protocol.parameters.append(param1)
        sample_collection_protocol.parameters.append(ProtocolParameter(parameter_name=OntologyAnnotation("material description")))
        # sample_collection_protocol.parameters.append(ProtocolParameter(parameter_name="Sample Description"))


        study.protocols.append(sample_collection_protocol)

        # data_collection_protocol = Protocol(
        #     name="data collection",
        #     protocol_type=OntologyAnnotation(term="data collection"))
        # data_collection_protocol.comments.append(Comment(name="Protocol Start Date", value="beep"))
        # data_collection_protocol.comments.append(Comment(name="Protocol End Date", value="2017-08-11"))
        #
        # study.protocols.append(data_collection_protocol)

        sample_collection_process = Process(
            executes_protocol=sample_collection_protocol)

        # Creation of an ISA Study Factor object
        f1 = StudyFactor(name="treatment['modality']", factor_type=OntologyAnnotation(term="treatment['modality']"))
        f2 = StudyFactor(name="duration", factor_type=OntologyAnnotation(term="time"))
        # testing serialization to ISA-TAB of Comments attached to ISA objects.
        f1.comments.append(Comment(name="Factor comment1", value="Saturn"))
        f2.comments.append(Comment(name="Factor comment2", value="2039-12-12"))
        f1.comments.append(Comment(name="Factor comment3", value="the 'wahoo' factor"))
        # print(f1.comments[0].name, "|", f1.comments[0].value)

        # checking that the ISA Factor object has been modified
        study.factors.append(f1)
        study.factors.append(f2)
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

        # IMPORTANT: remember to populate the list of ontology categories used to annotation ISA Material in a Study:
        study.characteristic_categories.append(characteristic_organism.category)
        study.characteristic_categories.append(characteristic_organ.category)
        # Next, we build n Assay object and attach two protocols,
        # extraction and sequencing.

        assay1 = Assay(filename="a_assay.txt")

        assay1.comments.append(Comment(name="Assay Descriptor", value="Intelligent Assay Design"))
        assay1.comments.append(Comment(name="Assay QC", value="pass"))

        # the extraction protocols
        extraction_protocol1 = Protocol(
            name='extraction-TEST',
            protocol_type=OntologyAnnotation(term="material extraction-TEST"))
        study.protocols.append(extraction_protocol1)

        extraction_protocol2 = Protocol(
            name='methylated material extraction-TEST',
            protocol_type=OntologyAnnotation(term="methylated material extraction-TEST"))
        study.protocols.append(extraction_protocol2)

        # the sequencing protocols
        sequencing_protocol = Protocol(
            name='sequencing-TEST',
            protocol_type=OntologyAnnotation(term="material sequencing"))
        study.protocols.append(sequencing_protocol)

        # adding a dummy Comment[] to ISA.protocol object
        study.protocols[0].comments.append(Comment(name="Protocol Start Date", value="Uranus"))
        study.protocols[0].comments.append(Comment(name="Protocol End Date", value="not my pb"))
        study.protocols[0].comments.append(Comment(name="Protocol QC", value="beta"))
        study.protocols[1].comments.append(Comment(name="Protocol Reuse Date", value="2017-08-11"))
        study.protocols[2].comments.append(Comment(name="Protocol QC", value="alpha"))
        study.protocols[3].comments.append(Comment(name="Protocol QC", value="none"))
        # checking that the ISA Protocool object has been modified
        # print(study.protocols[0])



        assay2 = Assay(filename="a_assay-methyl.txt")

        assay2.comments.append(Comment(name="Assay Descriptor", value="Intelligent Methyl Assay Design"))
        assay2.comments.append(Comment(name="Assay QC", value="fail"))
        assay2.comments.append(Comment(name="Assay Safety", value="health hazard"))

        sequencing_protocol_methyl = Protocol(
            name='methylation sequencing-TEST',
            protocol_type=OntologyAnnotation(term="methylation sequencing"))
        study.protocols.append(sequencing_protocol_methyl)

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

            extraction_process1 = Process(executes_protocol=extraction_protocol1)
            extraction_process2 = Process(executes_protocol=extraction_protocol2)
            # extraction process takes as input a sample, and produces an extract
            # material as output

            extraction_process1.inputs.append(sample)
            material1 = Material(name="extract-{}".format(i))
            material1.type = "Extract Name"
            extraction_process1.outputs.append(material1)

            extraction_process2.inputs.append(sample)
            material2 = Material(name="methyl-extract-{}".format(i))
            material2.type = "Extract Name"
            extraction_process2.outputs.append(material2)

            # create a sequencing process that executes the sequencing protocol

            sequencing_process1 = Process(executes_protocol=sequencing_protocol)
            sequencing_process1.name = "assay-name-{}".format(i)
            sequencing_process1.inputs.append(extraction_process1.outputs[0])

            # Sequencing process usually has an output data file

            datafile1 = DataFile(filename="sequenced-data-{}".format(i),
                                label="Raw Data File", generated_from=[material1])
            sequencing_process1.outputs.append(datafile1)

            # create a sequencing process that executes the sequencing protocol

            sequencing_process2 = Process(executes_protocol=sequencing_protocol_methyl)
            sequencing_process2.name = "methyl-assay-name-{}".format(i)
            sequencing_process2.inputs.append(extraction_process2.outputs[0])

            # Sequencing process usually has an output data file

            datafile2 = DataFile(filename="methyl-sequenced-data-{}".format(i),
                                label="Raw Data File", generated_from=[material1])
            sequencing_process2.outputs.append(datafile2)


            # ensure Processes are linked
            plink(extraction_process1, sequencing_process1)
            plink(extraction_process2, sequencing_process2)
            # make sure the extract, data file, and the processes are attached to
            # the assay

            assay1.samples.append(sample)
            assay1.data_files.append(datafile1)
            assay1.other_material.append(material1)
            assay1.process_sequence.append(extraction_process1)
            assay1.process_sequence.append(sequencing_process1)
            assay1.measurement_type = OntologyAnnotation(term="transcription profiling")
            assay1.technology_type = OntologyAnnotation(term="nucleotide sequencing")

            assay2.samples.append(sample)
            assay2.data_files.append(datafile2)
            assay2.other_material.append(material2)
            assay2.process_sequence.append(extraction_process2)
            assay2.process_sequence.append(sequencing_process2)
            assay2.measurement_type = OntologyAnnotation(term="methylation profiling")
            assay2.technology_type = OntologyAnnotation(term="nucleotide sequencing")

        # attach the assay to the study
        study.assays.append(assay1)
        study.assays.append(assay2)

        investigation.studies.append(study)

        try:
            isatab.dump(investigation, self._tmp_dir)
        except IOError as ioe:
            print("ERROR: ", ioe)

        print("in folder:", self._tmp_dir)
        # with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as actual_file, \
        #         open(os.path.join(self._tab_data_dir, 'TEST-ISA-investigation-comments',
        #                           'i_test_investigation.txt')) as expected_file:
        #     self.assertTrue(assert_tab_content_equal(actual_file, expected_file))
        #     self.assertIsInstance(isatab.dumps(investigation), str)


class TestIsaTabLoad(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab_load_issue200(self):
        with open(os.path.join(self._tab_data_dir, 'issue200', 'i_Investigation.txt')) as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len(ISA.studies[0].assays[0].samples), 7)
            self.assertEqual(len(ISA.studies[0].assays[0].other_material), 7)
            self.assertEqual(len(ISA.studies[0].assays[0].data_files), 2)
            self.assertEqual(len(ISA.studies[0].assays[0].process_sequence), 11)

    # def test_isatab_load_issue201(self):  # issue now not relevant due to changes in parser
    #     with open(os.path.join(self._tab_data_dir, 'sdata201411-isa1-parsererror', 'i_Investigation.txt')) as fp:
    #         try:
    #             self.assertRaises(isatab.load(fp, skip_load_tables=True), IOError)
    #         except Exception as ex:  # This now doesn't fail as section loader is now more resilient
    #             self.assertIsInstance(ex, IOError)
    #             self.assertIn("There was a problem parsing the investigation section:", str(ex))

    def test_isatab_load_sdata201414_isa1(self):
        with open(os.path.join(self._tab_data_dir, 'sdata201414-isa1', 'i_Investigation.txt'), encoding='utf-8') as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len(ISA.ontology_source_references), 5)  # 5 ontology sources in investigation
            self.assertListEqual([s.filename for s in ISA.studies], ['s_chambers.txt'])  # 1 study in i_investigation.txt
            self.assertEqual(len(ISA.studies[0].comments), 9)  # 9 comments in study
            self.assertEqual(len(ISA.studies[0].design_descriptors), 3)  # 3 design descriptors in study
            self.assertEqual(len(ISA.studies[0].publications), 0)  # 0 publications in study
            self.assertEqual(len(ISA.studies[0].factors), 2)  # 2 factors in study
            self.assertEqual(len(ISA.studies[0].protocols), 5)  # 5 protocols in study
            self.assertEqual(len(ISA.studies[0].contacts), 2)  # 2 contacts in study
            self.assertEqual(len(ISA.studies[0].contacts[0].comments), 5)  # 5 comments in contact
            self.assertEqual(len(ISA.studies[0].contacts[1].comments), 5)  # 5 comments in contact
            self.assertListEqual([a.filename for a in ISA.studies[0].assays], ['a_chambers.txt'])  # 1 assays in s_chambers.txt

    def test_isatab_load_bii_i_1(self):
        with open(os.path.join(self._tab_data_dir, 'BII-I-1', 'i_investigation.txt')) as fp:
            ISA = isatab.load(fp)

            self.assertListEqual([s.filename for s in ISA.studies], ['s_BII-S-1.txt', 's_BII-S-2.txt'])  # 2 studies in i_investigation.txt

            study_bii_s_1 = [s for s in ISA.studies if s.filename == 's_BII-S-1.txt'][0]

            self.assertEqual(len(study_bii_s_1.sources), 18)  # 18 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_1.samples), 164)  # 164 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_1.process_sequence), 18)  # 18 study processes in s_BII-S-1.txt

            self.assertListEqual([a.filename for a in study_bii_s_1.assays], ['a_proteome.txt', 'a_metabolome.txt', 'a_transcriptome.txt'])  # 2 assays in s_BII-S-1.txt

            assay_proteome = [a for a in study_bii_s_1.assays if a.filename == 'a_proteome.txt'][0]

            self.assertEqual(len(assay_proteome.samples), 8)  # 8 assay samples in a_proteome.txt
            self.assertEqual(len(assay_proteome.other_material), 19)  # 19 other materials in a_proteome.txt

            self.assertEqual(len(assay_proteome.data_files), 7)  # 7 data files  in a_proteome.txt

            self.assertEqual(len(assay_proteome.process_sequence), 25)  # 25 processes in in a_proteome.txt

            assay_metabolome = [a for a in study_bii_s_1.assays if a.filename == 'a_metabolome.txt'][0]

            self.assertEqual(len(assay_metabolome.samples), 92)  # 92 assay samples in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.other_material), 92)  # 92 other materials in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.data_files), 111)  # 111 data files  in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.process_sequence), 203)  # 203 processes in in a_metabolome.txt

            assay_transcriptome = [a for a in study_bii_s_1.assays if a.filename == 'a_transcriptome.txt'][0]

            self.assertEqual(len(assay_transcriptome.samples), 48)  # 48 assay samples in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.other_material), 96)  # 96 other materials in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.data_files), 49)  # 49 data files  in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.process_sequence), 193)  # 193 processes in in a_transcriptome.txt

            study_bii_s_2 = [s for s in ISA.studies if s.filename == 's_BII-S-2.txt'][0]

            self.assertEqual(len(study_bii_s_2.sources), 1)  # 1 sources in s_BII-S-2.txt
            self.assertEqual(len(study_bii_s_2.samples), 2)  # 2 study samples in s_BII-S-2.txt
            self.assertEqual(len(study_bii_s_2.process_sequence), 1)  # 1 study processes in s_BII-S-2.txt

            self.assertEqual(len(study_bii_s_2.assays), 1)  # 1 assays in s_BII-S-2.txt
            self.assertListEqual([a.filename for a in study_bii_s_2.assays], ['a_microarray.txt'])  # 1 assays in s_BII-S-2.txt

            assay_microarray = [a for a in study_bii_s_2.assays if a.filename == 'a_microarray.txt'][0]

            self.assertEqual(len(assay_microarray.samples), 2)  # 2 assay samples in a_microarray.txt
            self.assertEqual(len(assay_microarray.other_material), 28)  # 28 other materials in a_microarray.txt
            self.assertEqual(len(assay_microarray.data_files), 15)  # 15 data files  in a_microarray.txt
            self.assertEqual(len(assay_microarray.process_sequence), 45)  # 45 processes in in a_microarray.txt

    def test_isatab_load_bii_s_3(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt')) as fp:
            ISA = isatab.load(fp)

            self.assertListEqual([s.filename for s in ISA.studies], ['s_BII-S-3.txt'])  # 1 studies in i_gilbert.txt

            study_bii_s_3 = [s for s in ISA.studies if s.filename == 's_BII-S-3.txt'][0]

            self.assertEqual(len(study_bii_s_3.sources), 4)  # 4 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_3.samples), 4)  # 4 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_3.process_sequence), 4)  # 4 study processes in s_BII-S-1.txt

            self.assertListEqual([a.filename for a in study_bii_s_3.assays], ['a_gilbert-assay-Gx.txt', 'a_gilbert-assay-Tx.txt'])  # 2 assays in s_BII-S-1.txt

            assay_gx = [a for a in study_bii_s_3.assays if a.filename == 'a_gilbert-assay-Gx.txt'][0]

            self.assertEqual(len(assay_gx.samples), 4)  # 4 assay samples in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.other_material), 4)  # 4 other materials in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.data_files), 6)  # 6 data files  in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.process_sequence), 18)  # 18 processes in in a_gilbert-assay-Gx.txt

            assay_tx = [a for a in study_bii_s_3.assays if a.filename == 'a_gilbert-assay-Tx.txt'][0]

            self.assertEqual(len(assay_tx.samples), 4)  # 4 assay samples in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.other_material), 4)  # 4 other materials in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.data_files), 24)  # 24 data files  in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.process_sequence), 36)  # 36 processes in in a_gilbert-assay-Tx.txt

    def test_isatab_load_bii_s_7(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt')) as fp:
            ISA = isatab.load(fp)

            self.assertListEqual([s.filename for s in ISA.studies], ['s_BII-S-7.txt'])  # 1 studies in i_gilbert.txt

            study_bii_s_7 = [s for s in ISA.studies if s.filename == 's_BII-S-7.txt'][0]

            self.assertEqual(len(study_bii_s_7.sources), 29)  # 29 sources in s_BII-S-7.txt
            self.assertEqual(len(study_bii_s_7.samples), 29)  # 29 study samples in s_BII-S-7.txt
            self.assertEqual(len(study_bii_s_7.process_sequence), 29)  # 29 study processes in s_BII-S-7.txt

            self.assertListEqual([a.filename for a in study_bii_s_7.assays], ['a_matteo-assay-Gx.txt'])  # 1 assays in s_BII-S-1.txt

            assay_gx = [a for a in study_bii_s_7.assays if a.filename == 'a_matteo-assay-Gx.txt'][0]

            self.assertEqual(len(assay_gx.samples), 29)  # 29 assay samples in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.other_material), 29)  # 29 other materials in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.data_files), 29)  # 29 data files  in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.process_sequence), 116)  # 116 processes in in a_matteo-assay-Gx.txt


class UnitTestIsaTabDump(unittest.TestCase):
    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_source_protocol_ref_sample(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        expected = """Source Name\tProtocol REF\tSample Name
source1\tsample collection\tsample1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_sample_x2(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        source2 = Source(name='source2')
        sample2 = Sample(name='sample2')
        sample_collection_process2 = Process(executes_protocol=s.protocols[0])
        sample_collection_process2.inputs = [source2]
        sample_collection_process2.outputs = [sample2]
        s.process_sequence = [sample_collection_process, sample_collection_process2]
        i.studies = [s]

        expected_line1 = """Source Name\tProtocol REF\tSample Name"""
        expected_line2 = """source1\tsample collection\tsample1"""
        expected_line3 = """source2\tsample collection\tsample2"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_source_protocol_ref_sample_split(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample2 = Sample(name='sample2')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1, sample2]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]

        expected_line1 = """Source Name\tProtocol REF\tSample Name"""
        expected_line2 = """source1\tsample collection\tsample1"""
        expected_line3 = """source1\tsample collection\tsample2"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_source_protocol_ref_sample_pool(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        source1 = Source(name='source1')
        source2 = Source(name='source2')
        sample1 = Sample(name='sample1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1, source2]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]

        expected_line1 = """Source Name\tProtocol REF\tSample Name"""
        expected_line2 = """source1\tsample collection\tsample1"""
        expected_line3 = """source2\tsample collection\tsample1"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_source_protocol_ref_sample_with_characteristics(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        reference_descriptor_category = OntologyAnnotation(term='reference descriptor')
        organism_part_category = OntologyAnnotation(term='organism part')
        source1 = Source(name='source1')
        source1.characteristics = [Characteristic(category=reference_descriptor_category, value='not applicable')]
        sample1 = Sample(name='sample1')
        sample1.characteristics = [
            Characteristic(category=organism_part_category, value=OntologyAnnotation(term='liver'))]
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        expected = """Source Name\tCharacteristics[reference descriptor]\tProtocol REF\tSample Name\tCharacteristics[organism part]
source1\tnot applicable\tsample collection\tsample1\tliver"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_sample_with_parameter_values(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[
                Protocol(name='sample collection',
                         parameters=[ProtocolParameter(parameter_name=OntologyAnnotation(term='temperature'))])
            ]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.parameter_values = [ParameterValue(category=s.protocols[0].parameters[0], value=10)]
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        expected = """Source Name\tProtocol REF\tParameter Value[temperature]\tSample Name
source1\tsample collection\t10\tsample1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_sample_with_factor_values(self):
        i = Investigation()
        s = Study(filename='s_test.txt',
                  protocols=[Protocol(name='sample collection'),
                             Protocol(name='extraction')],
                  factors=[StudyFactor(name='study group')])
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        s.sources = [source1]
        s.samples = [sample1]
        sample1.factor_values = [FactorValue(factor_name=s.factors[0], value="Study group 1")]
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        a = Assay(filename='a_test.txt')
        a.samples = [sample1]
        extract1 = Extract(name='extract1')
        a.other_material = [extract1]
        extraction_process = Process(executes_protocol=s.protocols[1])
        extraction_process.inputs = [sample1]
        a.process_sequence = [extraction_process]
        s.assays = [a]
        expected_study_table = """Source Name\tProtocol REF\tSample Name\tFactor Value[study group]
source1\tsample collection\tsample1\tStudy group 1"""
        self.assertIn(expected_study_table, isatab.dumps(i))
        expected_assay_table = """Sample Name\tFactor Value[study group]\tProtocol REF
sample1\tStudy group 1\textraction"""
        self.assertIn(expected_assay_table,
                      isatab.dumps(i, write_fvs_in_assay_table=True))

    def test_source_protocol_ref_protocol_ref_sample(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection'), Protocol(name='aliquoting')]
        )
        source1 = Source(name='source1')
        aliquot1 = Sample(name='aliquot1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        aliquoting_process = Process(executes_protocol=s.protocols[1])
        sample_collection_process.inputs = [source1]
        aliquoting_process.outputs = [aliquot1]
        plink(sample_collection_process, aliquoting_process)
        s.process_sequence = [sample_collection_process, aliquoting_process]
        i.studies = [s]
        expected = """Source Name\tProtocol REF\tProtocol REF\tSample Name
source1\tsample collection\taliquoting\taliquot1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_sample_protocol_ref_sample(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection'), Protocol(name='aliquoting')]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        aliquot1 = Sample(name='aliquot1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        aliquoting_process = Process(executes_protocol=s.protocols[1])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        aliquoting_process.inputs = [sample1]
        aliquoting_process.outputs = [aliquot1]
        plink(sample_collection_process, aliquoting_process)
        s.process_sequence = [sample_collection_process, aliquoting_process]
        i.studies = [s]
        expected = """Source Name\tProtocol REF\tSample Name\tProtocol REF\tSample Name
source1\tsample collection\tsample1\taliquoting\taliquot1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_sample_protocol_ref_material_protocol_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        extract1 = Material(name='extract1', type_='Extract Name')
        data1 = DataFile(filename='datafile.raw', label='Raw Data File')
        extraction_process = Process(executes_protocol=s.protocols[0])
        scanning_process = Process(executes_protocol=s.protocols[1])
        extraction_process.inputs = [sample1]
        extraction_process.outputs = [extract1]
        scanning_process.inputs = [extract1]
        scanning_process.outputs = [data1]
        plink(extraction_process, scanning_process)
        a = Assay(filename='a_test.txt')
        a.process_sequence = [extraction_process, scanning_process]
        s.assays = [a]
        i.studies = [s]
        expected = """Sample Name\tProtocol REF\tExtract Name\tProtocol REF\tRaw Data File
sample1\textraction\textract1\tscanning\tdatafile.raw"""
        self.assertIn(expected, isatab.dumps(i))

    def test_sample_protocol_ref_material_protocol_ref_data_x2(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        extract1 = Material(name='extract1', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')
        extraction_process1 = Process(executes_protocol=s.protocols[0])
        scanning_process1 = Process(executes_protocol=s.protocols[1])
        extraction_process1.inputs = [sample1]
        extraction_process1.outputs = [extract1]
        scanning_process1.inputs = [extract1]
        scanning_process1.outputs = [data1]
        plink(extraction_process1, scanning_process1)

        sample2 = Sample(name='sample2')
        extract2 = Material(name='extract2', type_='Extract Name')
        data2 = DataFile(filename='datafile2.raw', label='Raw Data File')
        extraction_process2 = Process(executes_protocol=s.protocols[0])
        scanning_process2 = Process(executes_protocol=s.protocols[1])
        extraction_process2.inputs = [sample2]
        extraction_process2.outputs = [extract2]
        scanning_process2.inputs = [extract2]
        scanning_process2.outputs = [data2]
        plink(extraction_process2, scanning_process2)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [scanning_process1, extraction_process1, scanning_process2, extraction_process2]
        s.assays = [a]
        i.studies = [s]

        expected_line1 = """Sample Name\tProtocol REF\tExtract Name\tProtocol REF\tRaw Data File"""
        expected_line2 = """sample1\textraction\textract1\tscanning\tdatafile1.raw"""
        expected_line3 = """sample2\textraction\textract2\tscanning\tdatafile2.raw"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_sample_split_protocol_ref_material_protocol_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        extract1 = Material(name='extract1', type_='Extract Name')
        extract2 = Material(name='extract2', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')
        data2 = DataFile(filename='datafile2.raw', label='Raw Data File')

        extraction_process1 = Process(executes_protocol=s.protocols[0])
        extraction_process1.inputs = [sample1]
        extraction_process1.outputs = [extract1, extract2]

        scanning_process1 = Process(executes_protocol=s.protocols[1])
        scanning_process1.inputs = [extract1]
        scanning_process1.outputs = [data1]

        scanning_process2 = Process(executes_protocol=s.protocols[1])
        scanning_process2.inputs = [extract2]
        scanning_process2.outputs = [data2]
        plink(extraction_process1, scanning_process1)
        plink(extraction_process1, scanning_process2)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [scanning_process1, extraction_process1, scanning_process2]
        s.assays = [a]
        i.studies = [s]
        expected_line1 = """Sample Name\tProtocol REF\tExtract Name\tProtocol REF\tRaw Data File"""
        expected_line2 = """sample1\textraction\textract1\tscanning\tdatafile1.raw"""
        expected_line3 = """sample1\textraction\textract2\tscanning\tdatafile2.raw"""
        dumps_out = isatab.dumps(i)
        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_sample_protocol_ref_material_protocol_split_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        extract1 = Material(name='extract1', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')
        data2 = DataFile(filename='datafile2.raw', label='Raw Data File')

        extraction_process1 = Process(executes_protocol=s.protocols[0])
        extraction_process1.inputs = [sample1]
        extraction_process1.outputs = [extract1]

        scanning_process1 = Process(executes_protocol=s.protocols[1])
        scanning_process1.inputs = [extract1]
        scanning_process1.outputs = [data1]

        scanning_process2 = Process(executes_protocol=s.protocols[1])
        scanning_process2.inputs = [extract1]
        scanning_process2.outputs = [data2]

        plink(extraction_process1, scanning_process1)
        plink(extraction_process1, scanning_process2)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [extraction_process1, scanning_process1, scanning_process2]
        s.assays = [a]
        i.studies = [s]

        expected_line1 = """Sample Name\tProtocol REF\tExtract Name\tProtocol REF\tRaw Data File"""
        expected_line2 = """sample1\textraction\textract1\tscanning\tdatafile1.raw"""
        expected_line3 = """sample1\textraction\textract1\tscanning\tdatafile2.raw"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_sample_pool_protocol_ref_material_protocol_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        sample2 = Sample(name='sample2')
        extract1 = Material(name='extract1', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')
        extraction_process1 = Process(executes_protocol=s.protocols[0])
        scanning_process1 = Process(executes_protocol=s.protocols[1])
        extraction_process1.inputs = [sample1, sample2]
        extraction_process1.outputs = [extract1]

        scanning_process1.inputs = [extract1]
        scanning_process1.outputs = [data1]
        plink(extraction_process1, scanning_process1)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [extraction_process1, scanning_process1]
        s.assays = [a]
        i.studies = [s]

        expected_line1 = """Sample Name\tProtocol REF\tExtract Name\tProtocol REF\tRaw Data File"""
        expected_line2 = """sample1\textraction\textract1\tscanning\tdatafile1.raw"""
        expected_line3 = """sample2\textraction\textract1\tscanning\tdatafile1.raw"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_sample_protocol_ref_material_pool_protocol_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        sample2 = Sample(name='sample2')
        extract1 = Material(name='extract1', type_='Extract Name')
        extract2 = Material(name='extract2', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')

        extraction_process1 = Process(executes_protocol=s.protocols[0])
        extraction_process1.inputs = [sample1]
        extraction_process1.outputs = [extract1]

        extraction_process2 = Process(executes_protocol=s.protocols[0])
        extraction_process2.inputs = [sample2]
        extraction_process2.outputs = [extract2]

        scanning_process1 = Process(executes_protocol=s.protocols[1])
        scanning_process1.inputs = [extract1, extract2]
        scanning_process1.outputs = [data1]
        plink(extraction_process1, scanning_process1)
        plink(extraction_process2, scanning_process1)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [extraction_process1, extraction_process2, scanning_process1]
        s.assays = [a]
        i.studies = [s]

        expected_line1 = """Sample Name\tProtocol REF\tExtract Name\tProtocol REF\tRaw Data File"""
        expected_line2 = """sample1\textraction\textract1\tscanning\tdatafile1.raw"""
        expected_line3 = """sample2\textraction\textract2\tscanning\tdatafile1.raw"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)


class UnitTestIsaTabLoad(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_source_protocol_ref_sample(self):
        factory = ProcessSequenceFactory(study_protocols=[Protocol(name="sample collection")])
        table_to_load = """Source Name\tProtocol REF\tSample Name
source1\tsample collection\tsample1"""
        DF = IsaTabDataFrame(pd.read_csv(StringIO(table_to_load), sep='\t'))
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 1)
        self.assertEqual(len(sa), 1)
        self.assertEqual(len(om), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(pr), 1)

    def test_source_protocol_ref_sample_x2(self):
        factory = ProcessSequenceFactory(study_protocols=[Protocol(name="sample collection")])
        table_to_load = """Source Name\tProtocol REF\tSample Name
source1\tsample collection\tsample1
source2\tsample collection\tsample2"""
        DF = IsaTabDataFrame(pd.read_csv(StringIO(table_to_load), sep='\t'))
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 2)
        self.assertEqual(len(sa), 2)
        self.assertEqual(len(om), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(pr), 2)

    def test_source_protocol_ref_split_sample(self):
        factory = ProcessSequenceFactory(study_protocols=[Protocol(name="sample collection")])
        table_to_load = """Source Name\tProtocol REF\tSample Name
source1\tsample collection\tsample1
source1\tsample collection\tsample2"""
        DF = IsaTabDataFrame(pd.read_csv(StringIO(table_to_load), sep='\t'))
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 1)
        self.assertEqual(len(sa), 2)
        self.assertEqual(len(om), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(pr), 1)

    def test_source_protocol_ref_pool_sample(self):
        factory = ProcessSequenceFactory(study_protocols=[Protocol(name="sample collection")])
        table_to_load = """Source Name\tProtocol REF\tSample Name
source1\tsample collection\tsample1
source2\tsample collection\tsample1"""
        DF = IsaTabDataFrame(pd.read_csv(StringIO(table_to_load), sep='\t'))
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 2)
        self.assertEqual(len(sa), 1)
        self.assertEqual(len(om), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(pr), 1)

    def test_sample_protocol_ref_split_extract_protocol_ref_data(self):
        factory = ProcessSequenceFactory(
            study_samples=[Sample(name="sample1")],
            study_protocols=[Protocol(name="extraction"), Protocol(name="scanning")])
        table_to_load = """Sample Name\tProtocol REF\tExtract Name\tProtocol REF\tRaw Data File
sample1\textraction\te1\tscanning\td1
sample1\textraction\te2\tscanning\td2"""
        DF = IsaTabDataFrame(pd.read_csv(StringIO(table_to_load), sep='\t'))
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 0)
        self.assertEqual(len(sa), 1)
        self.assertEqual(len(om), 2)
        self.assertEqual(len(d), 2)
        self.assertEqual(len(pr), 3)

    def test_isatab_load_issue210_on_MTBLS30(self):
        with open(os.path.join(self._tab_data_dir, 'MTBLS30', 'i_Investigation.txt'), encoding='utf-8') as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len(ISA.studies[0].assays[0].data_files), 1)
            self.assertEqual(len(ISA.studies[0].assays[1].data_files), 1)

    def test_isatab_load_issue210_on_Sacurine(self):
        with open(os.path.join(self._tab_data_dir, 'MTBLS404', 'i_sacurine.txt'), encoding='utf-8') as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len([x for x in ISA.studies[0].assays[0].other_material
                                  if x.type == "Labeled Extract Name"]), 0)

    def test_isatab_preprocess_issue235(self):
        test_isatab_str = b""""Sample Name"	"Protocol REF"	"Parameter Value[medium]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[serum]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[serum concentration]"	"Unit"	"Term Source REF"	"Term Accession Number"	"Parameter Value[medium volume]"	"Unit"	"Term Source REF"	"Term Accession Number"	"Parameter Value[migration modulator]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[modulator concentration]"	"Unit"	"Term Source REF"	"Term Accession Number"	"Parameter Value[modulator distribution]"	"Term Source REF"	"Term Accession Number"	"Protocol REF"	"Parameter Value[imaging technique]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[imaging technique temporal feature]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[acquisition duration]"	"Unit"	"Term Source REF"	"Term Accession Number"	"Parameter Value[time interval]"	"Unit"	"Term Source REF"	"Term Accession Number"	"Parameter Value[objective type]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[objective magnification]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[objective numerical aperture]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[acquisition channel count]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[reporter]"	"Term Source REF"	"Term Accession Number"	"Parameter Value[voxel size]"	"Unit"	"Term Source REF"	"Term Accession Number"	"Assay Name"	"Raw Data File"	"Protocol REF"	"Parameter Value[software]"	"Term Source REF"	"Term Accession Number"	"Data Transformation Name"	"Derived Data File"
"culture1"	"migration assay"	"RPMI-1640"	""	""	"Heat Inactivated Fetal Bovine Serum "	""	""	"10"	"%"	"UO"	"http://purl.obolibrary.org/obo/UO_0000165"	"300"	"microliter"	"UO"	"http://purl.obolibrary.org/obo/UO_0000101"	""	""	""	""	""	""	""	"gradient"	""	""	"imaging"	"phase-contrast microscopy"	""	""	"dynamic"	""	""	"6"	"hour"	"UO"	"http://purl.obolibrary.org/obo/UO_0000032"	"15"	"minute"	"UO"	"http://purl.obolibrary.org/obo/UO_0000031"	""	""	""	"20"	""	""	""	""	""	""	""	""	""	""	""	""	""	""	""	"culture1"	""	"data transformation"	"CELLMIA"	""	""	""	""
"""
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(test_isatab_str)
            tmp.seek(0)
            study_assay_parser = isatab_parser.StudyAssayParser('mock.txt')
            with study_assay_parser._preprocess(tmp.name) as fixed_fp:
                header = next(fixed_fp)
                if """Protocol REF\tData Transformation Name""" in header:
                    self.fail('Incorrectly inserted Protocol REF before '
                              'Data Transformation Name')

    def test_isatab_factor_value_parsing_issue270(self):
        with open(os.path.join(self._tab_data_dir, 'issue270', 'i_matteo.txt'),
                  encoding='utf-8') as fp:
            ISA = isatab.load(fp)
            s = ISA.studies[-1]
            for sample in s.samples:
                self.assertGreater(len(sample.factor_values), 0)


class TestTransposedTabParser(unittest.TestCase):

    def setUp(self):
        self.ttable1 = """label1\trow1_value1\trow1_value2\n
label2\trow2_value1\trow2_value2\n"""
        _, tmp_path = tempfile.mkstemp()
        self.tmp_fp = _
        self.tmp_path = tmp_path
        with open(tmp_path, 'w') as fp:
            fp.write(self.ttable1)

    def tearDown(self):
        os.close(self.tmp_fp)
        os.remove(self.tmp_path)

    def test_parse(self):
        parser = isatab.TransposedTabParser()
        ttable_dict = parser.parse(self.tmp_path)
        expected_ttable = {
            'table': {
                'label1': ['row1_value1', 'row1_value2'],
                'label2': ['row2_value1', 'row2_value2']},
            'header': ['label1', 'label2']
        }
        self.assertEqual(ttable_dict, expected_ttable)


class UnitTestIsaStudyGroups():

    def setUp(self):
        self.fp = open(os.path.join(self._tab_data_dir, 'MTBLS404', 'i_sacurine.txt'), encoding='utf-8')
        self.i_df = isatab.load_investigation(fp=self.fp)
        for i, study_df in enumerate(self.i_df['studies']):
            study_filename = study_df.iloc[0]['Study File Name']
            self.s_fp = open(os.path.join(os.path.dirname(self.fp.name), study_filename), encoding='utf-8')
            self.study_sample_table = isatab.load_table(self.s_fp)
            self.study_sample_table.filename = study_filename

    def tearDown(self):
        self.fp.close()
        self.s_fp.close()

    def test_get_num_study_groups(self):
        num_study_groups = isatab.get_num_study_groups(self.study_sample_table, self.study_filename)
        self.assertEqual(num_study_groups, 1)

    def test_check_study_groups(self):
        self.assertTrue(isatab.NUMBER_OF_STUDY_GROUPS in self.study_df.columns)
        study_group_sizes = self.study_df[isatab.NUMBER_OF_STUDY_GROUPS]
        study_group_size_in_comment = next(iter(study_group_sizes))
        self.assertTrue(isatab.check_study_groups(self.study_sample_table, self.study_filename, study_group_size_in_comment))

