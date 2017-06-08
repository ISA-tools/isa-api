import unittest
from tests import utils
from isatools import sampletab
import os
from isatools.model.v1 import *
import tempfile
import shutil


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class UnitSampleTabLoad(unittest.TestCase):

    def setUp(self):
        self._sampletab_data_dir = utils.SAMPLETAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_sampletab_load_test1(self):
        with open(os.path.join(self._sampletab_data_dir, 'test1.txt')) as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            sources = ISA.studies[0].materials['sources']
            samples = ISA.studies[0].materials['samples']
            self.assertEqual(len(sources), 1)
            self.assertEqual(len(samples), 1)
            process = ISA.studies[0].process_sequence[0]
            for source in sources:
                self.assertIn(source, process.inputs)
            for sample in samples:
                self.assertIn(sample, process.outputs)

    def test_sampletab_load_test2(self):
        with open(os.path.join(self._sampletab_data_dir, 'test2.txt')) as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            sources = ISA.studies[0].materials['sources']
            samples = ISA.studies[0].materials['samples']
            self.assertEqual(len(sources), 1)
            self.assertEqual(len(samples), 2)
            self.assertEqual(len(ISA.studies[0].process_sequence), 1)
            process = ISA.studies[0].process_sequence[0]
            for source in sources:
                self.assertIn(source, process.inputs)
            for sample in samples:
                self.assertIn(sample, process.outputs)

    def test_sampletab_load_GSB_3(self):
        with open(os.path.join(self._sampletab_data_dir, 'GSB-3.txt')) as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            sources = ISA.studies[0].materials['sources']
            samples = ISA.studies[0].materials['samples']
            self.assertEqual(len(sources), 1157)
            self.assertEqual(len(samples), 3858)
            self.assertEqual(len(ISA.studies[0].process_sequence), 1747)

    def test_sampletab_load_GSB_537(self):
        with open(os.path.join(self._sampletab_data_dir, 'GSB-537.txt')) as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            sources = ISA.studies[0].materials['sources']
            samples = ISA.studies[0].materials['samples']
            self.assertEqual(len(sources), 4)
            self.assertEqual(len(samples), 80)
            self.assertEqual(len(ISA.studies[0].process_sequence), 8)

    def test_sampletab_load_dump_round_trip_GSB_537(self):
        with open(os.path.join(self._sampletab_data_dir, 'GSB-537.txt')) as fp:
            ISA = sampletab.load(fp)  # load into ISA objects
            with open(os.path.join(self._tmp_dir, "out.txt"), "w") as out_fp:
                sampletab.dump(ISA, out_fp)  # dump out to SampleTab from ISA objects
            with open(os.path.join(self._tmp_dir, "out.txt"), "r") as in_fp:
                ISA = sampletab.load(in_fp)  # load into ISA objects again from dumped SampleTab and check contents
                self.assertEqual(len(ISA.studies), 1)
                sources = ISA.studies[0].materials['sources']
                samples = ISA.studies[0].materials['samples']
                self.assertEqual(len(sources), 4)
                self.assertEqual(len(samples), 80)
                self.assertEqual(len(ISA.studies[0].process_sequence), 8)

    def test_sampletab_load_GSB_718(self):
        with open(os.path.join(self._sampletab_data_dir, 'GSB-718.txt')) as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            sources = ISA.studies[0].materials['sources']
            samples = ISA.studies[0].materials['samples']
            self.assertEqual(len(sources), 51)
            self.assertEqual(len(samples), 2409)
            self.assertEqual(len(ISA.studies[0].process_sequence), 109)


class UnitSampleTabDump(unittest.TestCase):

    def setUp(self):
        self._sampletab_data_dir = utils.SAMPLETAB_DATA_DIR

    def tearDown(self):
        pass

    def test_sampletab_dump_test1(self):
        ISA = Investigation()
        ISA.title = "Test SampleTab"
        ISA.identifier = "TEST-888"
        ISA.submission_date = "02/03/2017"
        ISA.ontology_source_references = [
            OntologySource(name="NCBI Taxonomy", description="NCBI Taxonomy", file="http://www.ncbi.nlm.nih.gov/taxonomy/"),
            OntologySource(name="EFO", description="EFO", file="http://www.ebi.ac.uk/efo/"),
            OntologySource(name="LBO", description="LBO", file="https://www.ebi.ac.uk/ols/ontologies/lbo/"),
            OntologySource(name="PATO", description="PATO", file="https://www.ebi.ac.uk/ols/ontologies/pato"),
            OntologySource(name="UBERON", description="UBERON", file="https://www.ebi.ac.uk/ols/ontologies/uberon"),
            OntologySource(name="CL", description="CL", file="https://www.ebi.ac.uk/ols/ontologies/cl"),
            OntologySource(name="BTO", description="BTO", file="https://www.ebi.ac.uk/ols/ontologies/bto")
        ]
        ISA.comments = [
            Comment(name="Organization Address", value="Oxford e-Research Centre, 7 Keble Road, Oxford OX1 3QG"),
            Comment(name="Organization Email", value=""),
            Comment(name="Organization Name", value="University of Oxford"),
            Comment(name="Organization Role", value="institution"),
            Comment(name="Organization URI", value="http://www.oerc.ox.ac.uk"),

            Comment(name="Organization Address", value="Wellcome Genome Campus, Hinxton, Cambridge, CB10 1SD, United Kingdom"),
            Comment(name="Organization Email", value=""),
            Comment(name="Organization Name", value="EMBL-EBI"),
            Comment(name="Organization Role", value="curator"),
            Comment(name="Organization URI", value="http://www.ebi.ac.uk/"),
        ]
        study = Study(filename="s_TEST-888.txt")
        study.protocols = [Protocol(name="sample collection", protocol_type=OntologyAnnotation(term="sample collection"))]
        sample_accession_charac = OntologyAnnotation("Sample Accession")
        sample_description_charac = OntologyAnnotation("Sample Description")
        derived_from_charac = OntologyAnnotation("Derived From")
        study.characteristic_categories = [
            sample_accession_charac,
            sample_description_charac,
            derived_from_charac
        ]
        study.materials['sources'] = [Source(name="sample1", characteristics=[
            Characteristic(category=sample_accession_charac, value="S1"),
            Characteristic(category=sample_description_charac, value="A sample"),
        ])]
        study.materials['samples'] = [Sample(name="sample2", characteristics=[
            Characteristic(category=sample_accession_charac, value="S2"),
            Characteristic(category=sample_description_charac, value="Another sample"),
            Characteristic(category=derived_from_charac, value="S1")],
                                             derives_from=[study.materials['sources'][0]])]
        process = Process(executes_protocol=study.protocols[0])
        process.inputs = [study.materials['sources'][0]]
        process.outputs = [study.materials['samples'][0]]
        study.process_sequence = [process]
        ISA.studies = [study]
        sampletab_dump = sampletab.dumps(ISA)
        self.assertIn("""[MSI]
Submission Title	Test SampleTab
Submission Identifier	TEST-888
Submission Description
Submission Version
Submission Reference Layer
Submission Release Date	02/03/2017
Submission Update Date
Organization Name	University of Oxford	EMBL-EBI
Organization Address	Oxford e-Research Centre, 7 Keble Road, Oxford OX1 3QG	Wellcome Genome Campus, Hinxton, Cambridge, CB10 1SD, United Kingdom
Organization URI	http://www.oerc.ox.ac.uk	http://www.ebi.ac.uk/
Organization Email
Organization Role	institution	curator
Person Last Name
Person Initials
Person First Name
Person Email
Person Role
Term Source Name	NCBI Taxonomy	EFO	LBO	PATO	UBERON	CL	BTO
Term Source URI	http://www.ncbi.nlm.nih.gov/taxonomy/	http://www.ebi.ac.uk/efo/	https://www.ebi.ac.uk/ols/ontologies/lbo/	https://www.ebi.ac.uk/ols/ontologies/pato	https://www.ebi.ac.uk/ols/ontologies/uberon	https://www.ebi.ac.uk/ols/ontologies/cl	https://www.ebi.ac.uk/ols/ontologies/bto
Term Source Version
[SCD]
Sample Name	Sample Accession	Sample Description	Derived From	Group Name	Group Accession""", sampletab_dump)
        self.assertIn("""sample1	S1	A sample""", sampletab_dump)
        self.assertIn("""sample2	S2	Another sample	S1""", sampletab_dump)

    def test_sampletab_dump_test2(self):
        ISA = Investigation()
        ISA.title = "Test SampleTab"
        ISA.identifier = "TEST-888"
        ISA.submission_date = "02/03/2017"
        ISA.ontology_source_references = [
            OntologySource(name="NCBI Taxonomy", description="NCBI Taxonomy",
                           file="http://www.ncbi.nlm.nih.gov/taxonomy/"),
            OntologySource(name="EFO", description="EFO", file="http://www.ebi.ac.uk/efo/"),
            OntologySource(name="LBO", description="LBO", file="https://www.ebi.ac.uk/ols/ontologies/lbo/"),
            OntologySource(name="PATO", description="PATO", file="https://www.ebi.ac.uk/ols/ontologies/pato"),
            OntologySource(name="UBERON", description="UBERON", file="https://www.ebi.ac.uk/ols/ontologies/uberon"),
            OntologySource(name="CL", description="CL", file="https://www.ebi.ac.uk/ols/ontologies/cl"),
            OntologySource(name="BTO", description="BTO", file="https://www.ebi.ac.uk/ols/ontologies/bto")
        ]
        ISA.comments = [
            Comment(name="Organization Address", value="Oxford e-Research Centre, 7 Keble Road, Oxford OX1 3QG"),
            Comment(name="Organization Email", value=""),
            Comment(name="Organization Name", value="University of Oxford"),
            Comment(name="Organization Role", value="institution"),
            Comment(name="Organization URI", value="http://www.oerc.ox.ac.uk"),

            Comment(name="Organization Address",
                    value="Wellcome Genome Campus, Hinxton, Cambridge, CB10 1SD, United Kingdom"),
            Comment(name="Organization Email", value=""),
            Comment(name="Organization Name", value="EMBL-EBI"),
            Comment(name="Organization Role", value="curator"),
            Comment(name="Organization URI", value="http://www.ebi.ac.uk/"),
        ]
        study = Study(filename="s_TEST-888.txt")
        study.protocols = [
            Protocol(name="sample collection", protocol_type=OntologyAnnotation(term="sample collection"))]
        sample_accession_charac = OntologyAnnotation("Sample Accession")
        sample_description_charac = OntologyAnnotation("Sample Description")
        derived_from_charac = OntologyAnnotation("Derived From")
        study.characteristic_categories = [
            sample_accession_charac,
            sample_description_charac,
            derived_from_charac
        ]
        study.materials['sources'] = [Source(name="sample1", characteristics=[
            Characteristic(category=sample_accession_charac, value="S1"),
            Characteristic(category=sample_description_charac, value="A sample"),
        ])]
        study.materials['samples'] = [Sample(name="sample2", characteristics=[
            Characteristic(category=sample_accession_charac, value="S2"),
            Characteristic(category=sample_description_charac, value="Another sample"),
            Characteristic(category=derived_from_charac, value="S1")],
                                             derives_from=[study.materials['sources'][0]]),
            Sample(name="sample3", characteristics=[
                Characteristic(category=sample_accession_charac, value="S3"),
                Characteristic(category=sample_description_charac, value="Another sample"),
                Characteristic(category=derived_from_charac, value="S1")],
                derives_from=[study.materials['sources'][0]])
                                      ]
        process = Process(executes_protocol=study.protocols[0])
        process.inputs = [study.materials['sources'][0]]
        process.outputs = [study.materials['samples'][0]]
        study.process_sequence = [process]
        ISA.studies = [study]
        sampletab_dump = sampletab.dumps(ISA)
        self.assertIn("""Sample Name	Sample Accession	Sample Description	Derived From	Group Name	Group Accession""", sampletab_dump)
        self.assertIn("""sample1	S1	A sample""", sampletab_dump)
        self.assertIn("""sample2	S2	Another sample	S1""", sampletab_dump)
        self.assertIn("""sample3	S3	Another sample	S1""", sampletab_dump)
