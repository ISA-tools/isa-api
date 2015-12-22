__author__ = 'agbeltran'

import os
from isatools.convert.isatab2json import ISATab2ISAjson_v1
import unittest


class ISAtab2jsonTest(unittest.TestCase):

      def setUp(self):
        self._dir = os.path.dirname(__file__)
        print(self._dir)


      def test_bii_i_1_conversion(self):
        self.isatab2json = ISATab2ISAjson_v1()
        test_data_dir = os.path.join(self._dir, "./data/BII-I-1")
        self.sample_data_dir = os.path.join(self._dir, "../isatools/sampledata/")
        isa_json = self.isatab2json.convert(test_data_dir, self.sample_data_dir)
        assert(isa_json["identifier"] == "BII-I-1")
        assert(isa_json["title"] == "Growth control of the eukaryote cell: a systems biology study in yeast")
        assert(isa_json["description"] == "Background Cell growth underlies many key cellular and developmental processes, yet a limited number of studies have been carried out on cell-growth regulation. Comprehensive studies at the transcriptional, proteomic and metabolic levels under defined controlled conditions are currently lacking. Results Metabolic control analysis is being exploited in a systems biology study of the eukaryotic cell. Using chemostat culture, we have measured the impact of changes in flux (growth rate) on the transcriptome, proteome, endometabolome and exometabolome of the yeast Saccharomyces cerevisiae. Each functional genomic level shows clear growth-rate-associated trends and discriminates between carbon-sufficient and carbon-limited conditions. Genes consistently and significantly upregulated with increasing growth rate are frequently essential and encode evolutionarily conserved proteins of known function that participate in many protein-protein interactions. In contrast, more unknown, and fewer essential, genes are downregulated with increasing growth rate; their protein products rarely interact with one another. A large proportion of yeast genes under positive growth-rate control share orthologs with other eukaryotes, including humans. Significantly, transcription of genes encoding components of the TOR complex (a major controller of eukaryotic cell growth) is not subject to growth-rate regulation. Moreover, integrative studies reveal the extent and importance of post-transcriptional control, patterns of control of metabolic fluxes at the level of enzyme synthesis, and the relevance of specific enzymatic reactions in the control of metabolic fluxes during cell growth. Conclusion This work constitutes a first comprehensive systems biology study on growth-rate control in the eukaryotic cell. The results have direct implications for advanced studies on cell growth, in vivo regulation of metabolic fluxes for comprehensive metabolic engineering, and for the design of genome-scale systems biology models of the eukaryotic cell.")
        assert(isa_json["submissionDate"] == "2007-04-30")
        assert(isa_json["publicReleaseDate"] == "2009-03-10")
        assert(isa_json["commentCreatedWithConfiguration"]["name"] == "Created With Configuration")
        assert(isa_json["commentCreatedWithConfiguration"]["value"] == "")
        assert(isa_json["commentLastOpenedWithConfiguration"]["name"] == "Last Opened With Configuration")
        assert(isa_json["commentLastOpenedWithConfiguration"]["value"] == "isaconfig-default_v2013-02-13")
        assert(len(isa_json["ontologySourceReferences"])==7)
        assert(len(isa_json["publications"])==1)
        assert(isa_json["publications"][0]["pubMedID"]=="17439666")
        assert(isa_json["publications"][0]["doi"]=="doi:10.1186/jbiol54")
        assert(isa_json["publications"][0]["authorList"]=="Castrillo JI, Zeef LA, Hoyle DC, Zhang N, Hayes A, Gardner DC, Cornell MJ, Petty J, Hakes L, Wardleworth L, Rash B, Brown M, Dunn WB, Broadhurst D, O'Donoghue K, Hester SS, Dunkley TP, Hart SR, Swainston N, Li P, Gaskell SJ, Paton NW, Lilley KS, Kell DB, Oliver SG.")
        assert(isa_json["publications"][0]["title"]=="Growth control of the eukaryote cell: a systems biology study in yeast.")
        assert(isa_json["publications"][0]["status"]["name"]=="indexed in Pubmed")

        assert(len(isa_json["people"])==3)
        assert(isa_json["people"][0]["firstName"]=="Oliver")
        assert(isa_json["people"][1]["firstName"]=="Juan")
        assert(isa_json["people"][2]["firstName"]=="Leo")
        assert(isa_json["people"][0]["lastName"]=="Stephen")
        assert(isa_json["people"][1]["lastName"]=="Castrillo")
        assert(isa_json["people"][2]["lastName"]=="Zeef")
        assert(isa_json["people"][0]["midInitials"]=="G")
        assert(isa_json["people"][1]["midInitials"]=="I")
        assert(isa_json["people"][2]["midInitials"]=="A")
        assert(isa_json["people"][0]["address"]=="Oxford Road, Manchester M13 9PT, UK")
        assert(isa_json["people"][1]["address"]=="Oxford Road, Manchester M13 9PT, UK")
        assert(isa_json["people"][2]["address"]=="Oxford Road, Manchester M13 9PT, UK")
        assert(isa_json["people"][0]["affiliation"]=="Faculty of Life Sciences, Michael Smith Building, University of Manchester")
        assert(isa_json["people"][1]["affiliation"]=="Faculty of Life Sciences, Michael Smith Building, University of Manchester")
        assert(isa_json["people"][2]["affiliation"]=="Faculty of Life Sciences, Michael Smith Building, University of Manchester")

        assert(len(isa_json["studies"])==2)
        assert(isa_json["studies"][0]["identifier"]=="BII-S-1")
        assert(isa_json["studies"][1]["identifier"]=="BII-S-2")

        assert(len(isa_json["studies"][0]["factors"])==2)
        assert(isa_json["studies"][0]["factors"][0]["factorName"]=="limiting nutrient")
        assert(isa_json["studies"][0]["factors"][1]["factorName"]=="rate")
        assert(isa_json["studies"][0]["factors"][0]["factorType"]["name"]=="chemical compound")
        assert(isa_json["studies"][0]["factors"][1]["factorType"]["name"]=="rate")

        assert(len(isa_json["studies"][0]["sources"])==18)
        assert(len(isa_json["studies"][0]["samples"])==163)
        assert(len(isa_json["studies"][1]["sources"])==1)
        assert(len(isa_json["studies"][1]["samples"])==2)


      # def test_bii_s_3_conversion(self):
      #   self.isatab2json = ISATab2ISAjson_v1()
      #   test_data_dir = os.path.join(self._dir, "./data/BII-S-3")
      #   self.sample_data_dir = os.path.join(self._dir, "../isatools/sampledata/")
      #   isa_json = self.isatab2json.convert(test_data_dir, self.sample_data_dir)
      #   assert(isa_json["identifier"] == "BII-S-3")
