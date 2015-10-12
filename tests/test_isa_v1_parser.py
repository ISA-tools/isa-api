import unittest
import os
import json
import glob
import filecmp

from isatools.io.isatab_parser import parse
from isatools.convert.isatab_to_json import IsatabToJsonWriter
from isatools.convert.json_to_isatab import JsonToIsatabWriter


class ISATabTest(unittest.TestCase):
    def setUp(self):
        """set up directories etc"""
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._work_dir = os.path.join(self._dir, "BII-I-1")
        self._json_dir = self._work_dir + "-json"
        if not os.path.exists(self._json_dir):
            os.makedirs(self._json_dir)
        self._generated_isatab_dir = self._work_dir + "-generatedIsatab"
        if not os.path.exists(self._generated_isatab_dir):
            os.makedirs(self._generated_isatab_dir)

    def tearDown(self):
        """Remove temporary directories (generated JSON and Tab)?"""
        #shutil.rmtree(self._json_dir, ignore_errors=True)
        #shutil.rmtree(self._generated_isatab_dir, ignore_errors=True)
        pass

    def test_basic_parsing(self):
        """Test general parsing of an example ISA directory.
        """
        rec = parse(self._work_dir)
        assert rec.metadata["Investigation Identifier"] == "BII-I-1"
        assert len(rec.ontology_refs) == 7
        assert rec.ontology_refs[2]["Term Source Name"] == "NEWT"
        assert len(rec.publications) == 1
        assert rec.publications[0]["Investigation Publication DOI"] == "doi:10.1186/jbiol54"

        assert len(rec.studies) == 2
        study = rec.studies[0]
        assert study.metadata["Study File Name"] == "s_BII-S-1.txt"

        assert len(study.assays) == 3
        assert study.assays[0].metadata["Study Assay File Name"] == "a_proteome.txt"

    def test_isatab_json_writer(self):
        """Test general parsing of an example ISA-Tab JSON directory.
        """
        # write out the json files for the isa-tab
        writer = IsatabToJsonWriter()
        writer.parsingIsatab(self._work_dir, self._json_dir)
        if os.path.isdir(self._json_dir):
            fnames = glob.glob(os.path.join(self._json_dir, "i_*.json"))
            assert len(fnames) == 1
            investigation_json_ref = fnames[0]

        assert os.path.exists(investigation_json_ref), "Did not find investigation json file: %s" \
                                                       % investigation_json_ref
        # load up the investigation json file and check whether it matches up with the investigation tabular format
        with open(investigation_json_ref, "rU") as in_handle:
            json_investigation_rec = json.load(in_handle)
            assert json_investigation_rec["investigation"]["investigationIdentifier"] == "BII-I-1"
            assert len(json_investigation_rec["ontologySourceReference"]) == 7
            assert json_investigation_rec["ontologySourceReference"][2]["termSourceName"] == "NEWT"
            assert len(json_investigation_rec["investigation"]["investigationPublications"]) == 1
            assert json_investigation_rec["investigation"]["investigationPublications"][0]
            ["investigationPublicationDOI"] == "doi:10.1186/jbiol54"

            assert len(json_investigation_rec["studies"]) == 2
            study = json_investigation_rec["studies"][0]
            exampleStudyJsonFile = study["study"]["studyFileName"]
            assert exampleStudyJsonFile == "s_BII-S-1.txt"
            assert len(study["study"]["assays"]) == 3
            exampleAssayJsonFile = study["study"]["assays"][0]["studyAssayFileName"]
            assert exampleAssayJsonFile == "a_proteome.txt"

        # check if the study file exists
        study_json_ref = os.path.join(self._json_dir, (str(exampleStudyJsonFile)).split(".")[0] + ".json")
        assert os.path.exists(study_json_ref), "Did not find study json file: %s" % study_json_ref

        # load up one of the study json file and check whether it matches up with the data in the study tabular format
        with open(study_json_ref, "rU") as in_handle:
            json_study_rec = json.load(in_handle)
            assert len(json_study_rec["studySampleTable"]["studyTableData"][0]) == 19
            assert len(json_study_rec["studySampleTable"]["studyTableHeaders"]) == 5

        # check if the expanded study file exists
        study_expanded_json_ref = os.path.join(self._json_dir, (str(exampleStudyJsonFile)).split(".")[0] +
                                               "_expanded.json")
        assert os.path.exists(study_expanded_json_ref), "Did not find study json file: %s" % study_expanded_json_ref

        # load up one of the expanded study json file and check whether it matches up with the data in the study
        # tabular format
        with open(study_expanded_json_ref, "rU") as in_handle:
            json_expanded_study_rec = json.load(in_handle)
            assert len(json_expanded_study_rec["studySamples"]) == 164
            assert json_expanded_study_rec["studySamples"][0][0]["name"] == "Source Name"
            assert json_expanded_study_rec["studySamples"][0][4]["type"] == "isaFactorValue"

        # check if the assay file exists
        assay_json_ref = os.path.join(self._json_dir, (str(exampleAssayJsonFile)).split(".")[0] + ".json")
        assert os.path.exists(assay_json_ref), "Did not find assay json file: %s" % assay_json_ref

        # load up one of the assay json file and check whether it matches up with the data in the assay tabular format
        with open(assay_json_ref, "rU") as in_handle:
            json_assay_rec = json.load(in_handle)
            assert len(json_assay_rec["assaysTable"]["assayTableData"][0]) == 25
            assert len(json_assay_rec["assaysTable"]["assayTableHeaders"]) == 18

        # check if the expanded assay file exists
        assay_expanded_json_ref = os.path.join(self._json_dir,
                                               (str(exampleAssayJsonFile)).split(".")[0] + "_expanded.json")
        assert os.path.exists(assay_expanded_json_ref), "Did not find assay json file: %s" % assay_expanded_json_ref

        # load up one of the expanded assay json file and check whether it matches up with the data in the assay tabular
        # format
        with open(assay_expanded_json_ref, "rU") as in_handle:
            json_expanded_assay_rec = json.load(in_handle)
            assert len(json_expanded_assay_rec["assaysTable"]) == 18
            assert json_expanded_assay_rec["assaysTable"][0][0]["name"] == "Sample Name"
            assert json_expanded_assay_rec["assaysTable"][0][5]["type"] == "isaMaterialLabel"

    def test_isatab_json_writer_single(self):
        """Test general parsing of a single combined JSON ISA-Tab file
        """
        # write out the json files for the isa-tab
        writer = IsatabToJsonWriter()
        writer.parsingIsatab(self._work_dir, self._json_dir)
        if os.path.isdir(self._json_dir):
            investigation_json_ref = os.path.join(self._json_dir, os.path.basename(self._work_dir) + ".json")
            assert os.path.exists(investigation_json_ref)

        assert os.path.exists(investigation_json_ref), "Did not find investigation json file: %s" % \
                                                       investigation_json_ref
        # load up the investigation json file and check whether it matches up with the investigation tabular format
        with open(investigation_json_ref, "rU") as in_handle:
            json_investigation_rec = json.load(in_handle)
            assert json_investigation_rec["investigation"]["investigationIdentifier"] == "BII-I-1"
            assert len(json_investigation_rec["ontologySourceReference"]) == 7
            assert json_investigation_rec["ontologySourceReference"][2]["termSourceName"] == "NEWT"
            assert len(json_investigation_rec["investigation"]["investigationPublications"]) == 1
            assert json_investigation_rec["investigation"]["investigationPublications"][0]
            ["investigationPublicationDOI"] == "doi:10.1186/jbiol54"

            assert len(json_investigation_rec["studies"]) == 2
            study = json_investigation_rec["studies"][0]
            exampleStudyJsonFile = study["study"]["studyFileName"]
            assert exampleStudyJsonFile == "s_BII-S-1.txt"
            assert len(study["study"]["assays"]) == 3
            exampleAssayJsonFile = study["study"]["assays"][0]["studyAssayFileName"]
            assert exampleAssayJsonFile == "a_proteome.txt"

            assert len(study["study"]["assays"][0]["assaysTable"]) == 18
            assert study["study"]["assays"][0]["assaysTable"][0][0]["name"] == "Sample Name"
            assert study["study"]["assays"][0]["assaysTable"][4][0]["type"] == "isaMaterialNode"

            assert len(study["study"]["studySamples"]) == 164
            assert len(study["study"]["studySamples"][0]) == 5
            assert study["study"]["studySamples"][0][0]["name"] == "Source Name"
            assert study["study"]["studySamples"][0][4]["type"] == "isaFactorValue"

    def test_jsonToIsatab_writer(self):
        # write out the json files for the isa-tab. Depends on test_isatab_json_writer()
        writer = IsatabToJsonWriter()
        writer.parsingIsatab(self._work_dir, self._json_dir)
        mywriter = JsonToIsatabWriter()
        output_dir = self._generated_isatab_dir
        original_dir = self._work_dir
        mywriter.parsingJson(self._json_dir, output_dir)

        for iFile in os.listdir(output_dir):
            if "_expanded" in iFile:
                iFile = iFile.replace("_expanded", "")
            # check if file size the same
            assert os.path.getsize(os.path.join(original_dir, iFile)) == \
                   os.path.getsize(os.path.join(output_dir, iFile)), "File size does not match: " + \
                                                                     os.path.join(original_dir, iFile) + ", " + \
                                                                     os.path.join(output_dir, iFile)
            assert filecmp.cmp(os.path.join(original_dir, iFile), os.path.join(output_dir, iFile), shallow=False), \
                "File compare failed: " + os.path.join(original_dir, iFile) + ", " + os.path.join(output_dir, iFile)
            # to print out the difference in the files
            # with open(os.path.join(output_dir, iFile),'r') as f1, open(os.path.join(original_dir, iFile),'r') as f2:
            #     diff = difflib.ndiff(f1.readlines(),f2.readlines())
            #     for line in diff:
            #         if line.startswith('-'):
            #             print line
            #         elif line.startswith('+'):
            #             print '\t\t'+line

        # test against the json single combined file
        for aFile in os.listdir(self._generated_isatab_dir):
            # check if file size the same
            if "_expanded" in aFile:
                aFile = aFile.replace("_expanded", "")
            assert os.path.getsize(os.path.join(original_dir, aFile)) == \
                   os.path.getsize(os.path.join(self._generated_isatab_dir, aFile)), \
                "File size does not match: " + os.path.join(original_dir, aFile) + ", " + \
                os.path.join(self._generated_isatab_dir, aFile)
            assert filecmp.cmp(os.path.join(original_dir, aFile), os.path.join(self._generated_isatab_dir, aFile),
                               shallow=False), \
                "File compare failed: " + os.path.join(original_dir, aFile) + ", " + \
                os.path.join(self._generated_isatab_dir, aFile)

    # def test_minimal_parsing(self):
    #     """Parse a minimal ISA-Tab file without some field values filled in.
    #     """
    #     work_dir = os.path.join(self._dir, "minimal")
    #     rec = isatab.parse(work_dir)
    #     assert len(rec.publications) == 0
    #     assert len(rec.metadata) == 0
    #
    #     assert len(rec.studies) == 1
    #     assert len(rec.studies[0].design_descriptors) == 0
    #
    #     sname = "C2C12 sample1 rep3"
    #     study = rec.studies[0]
    #     assay_node = study.assays[0].nodes["AFFY#35C.CEL"]
    #     assert assay_node.metadata["Sample Name"] == [sname]
    #     assert study.nodes[sname].metadata["strain"][0][0] == "C3H"
    #
    # def test_nextgen_parsing(self):
    #     """Parse ISA-Tab file representing next gen sequencing data
    #     """
    #     work_dir = os.path.join(self._dir, "BII-S-3")
    #     rec = isatab.parse(work_dir)
    #     assay = rec.studies[0].assays[0]
    #     assert assay.metadata['Study Assay Technology Platform'] == '454 Genome Sequencer FLX'
    #     assert assay.nodes.has_key("ftp://ftp.ncbi.nih.gov/pub/TraceDB/ShortRead/"
    #                                "SRA000266/EWOEPZA01.sff")
    #
    # def test_get_genelists(self):
    #     """Identify derived genelists available in ISA-Tab experiment
    #     """
    #     work_dir = os.path.join(self._dir, "genelist")
    #     rec = isatab.parse(work_dir)
    #     study = rec.studies[0]
    #     assay = study.assays[0]
    #     assay_node = assay.nodes["KLS1nature.CEL"]
    #     study_node = study.nodes[assay_node.metadata["Sample Name"][0]]
    #     assert "16862118-Figure2bSRAS.txt" in assay_node.metadata["Derived Data File"]
    #     expects = ["Mus musculus (Mouse)", "C57BL/6", "bone marrow"]
    #     attrs = ["Organism", "strain", "Organism Part"]
    #     for attr, expect in zip(attrs, expects):
    #         assert study_node.metadata[attr][0][0] == expect
    #
    # def test_mage(self):
    #     """Parse MAGE ISATab from ArrayExpress.
    #     """
    #     work_dir = os.path.join(self._dir, "mage")
    #     rec = isatab.parse(work_dir)
    #     assert len(rec.studies) == 1
    #     study = rec.studies[0]
    #     node = study.nodes["ERS025105"]
    #     assert node.metadata["FASTQ_URI"][0].FASTQ_URI == \
    #            "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR030/ERR030907/ERR030907.fastq.gz"
    #
    # def test_repeated_header(self):
    #     """Handle ISA-Tab inputs with repeated header names.
    #     """
    #     work_dir = os.path.join(self._dir, "BII-S-6")
    #     rec = isatab.parse(work_dir)