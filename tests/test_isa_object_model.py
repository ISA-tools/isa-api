import unittest
import os
from isatools.io import isa_v1_model
__author__ = 'dj'

from isatools.io import isa_v1_model
from isatools.io import isa_model_warlock
import uuid

class TestISAObjectModel(unittest.TestCase):

    # def setUp(self):
    #     self._dir = os.path.join(os.path.dirname(__file__), "data")
    #     self._work_dir = os.path.join(self._dir, "BII-I-1")

    def test_build_isa_objects(self):
        # model = isa_v1_model.fromISArchive(self._work_dir)
        i = isa_model_warlock.investigation_factory(
            ontologySourceReferences=[],
            identifier="BII-I-1",
            title="Growth control of the eukaryote cell: a systems biology study in yeast",
            description="Background Cell growth underlies many key cellular and developmental processes, yet a limited number of studies have been carried out on cell-growth regulation. Comprehensive studies at the transcriptional, proteomic and metabolic levels under defined controlled conditions are currently lacking. Results Metabolic control analysis is being exploited in a systems biology study of the eukaryotic cell. Using chemostat culture, we have measured the impact of changes in flux (growth rate) on the transcriptome, proteome, endometabolome and exometabolome of the yeast Saccharomyces cerevisiae. Each functional genomic level shows clear growth-rate-associated trends and discriminates between carbon-sufficient and carbon-limited conditions. Genes consistently and significantly upregulated with increasing growth rate are frequently essential and encode evolutionarily conserved proteins of known function that participate in many protein-protein interactions. In contrast, more unknown, and fewer essential, genes are downregulated with increasing growth rate; their protein products rarely interact with one another. A large proportion of yeast genes under positive growth-rate control share orthologs with other eukaryotes, including humans. Significantly, transcription of genes encoding components of the TOR complex (a major controller of eukaryotic cell growth) is not subject to growth-rate regulation. Moreover, integrative studies reveal the extent and importance of post-transcriptional control, patterns of control of metabolic fluxes at the level of enzyme synthesis, and the relevance of specific enzymatic reactions in the control of metabolic fluxes during cell growth. Conclusion This work constitutes a first comprehensive systems biology study on growth-rate control in the eukaryotic cell. The results have direct implications for advanced studies on cell growth, in vivo regulation of metabolic fluxes for comprehensive metabolic engineering, and for the design of genome-scale systems biology models of the eukaryotic cell.",
            submissionDate="30/04/2007",
            publicReleaseDate="10/03/2009",
            studies=[],
            publications=[],
            people=[]
        )

        s1 = isa_model_warlock.study_factory(
            identifier="BII-S-1",
            title="Study of the impact of changes in flux on the transcriptome, proteome, endometabolome and "
                  "exometabolome of the yeast Saccharomyces cerevisiae under different nutrient limitations",
            description="We wished to study the impact of growth rate on the total complement of mRNA molecules, proteins, and metabolites in S. cerevisiae, independent of any nutritional or other physiological effects. To achieve this, we carried out our analyses on yeast grown in steady-state chemostat culture under four different nutrient limitations (glucose, ammonium, phosphate, and sulfate) at three different dilution (that is, growth) rates (D = u = 0.07, 0.1, and 0.2/hour, equivalent to population doubling times (Td) of 10 hours, 7 hours, and 3.5 hours, respectively; u = specific growth rate defined as grams of biomass generated per gram of biomass present per unit time).",
            submissionDate="30/04/2007",
            publicReleaseDate="10/03/2009",
            studyFileName="s_BII-S-1.txt"
        )
        s1_design_descriptor = isa_model_warlock.ontology_annotation_factory(
            name="intervention design",
            termSource="OBI",
            termAccession="http://purl.obolibrary.org/obo/OBI_0000115"
        )
        s1.studyDesignDescriptors.append(s1_design_descriptor)
        s1_publication = isa_model_warlock.publication_factory(
            pubMedID="17439666",
            doi="doi:10.1186/jbiol54",
            authorList="Castrillo JI, Zeef LA, Hoyle DC, Zhang N, Hayes A, Gardner DC, Cornell MJ, Petty J, Hakes L, Wardleworth L, Rash B, Brown M, Dunn WB, Broadhurst D, O'Donoghue K, Hester SS, Dunkley TP, Hart SR, Swainston N, Li P, Gaskell SJ, Paton NW, Lilley KS, Kell DB, Oliver SG.",
            title="Growth control of the eukaryote cell: a systems biology study in yeast.",
            status=isa_model_warlock.ontology_annotation_factory(name="published")
        )
        s1.publications.append(s1_publication)
        s1_factor1 = isa_model_warlock.study_factor_factory(
            name="limiting nutrient",
            type=isa_model_warlock.ontology_annotation_factory(name="chemical compound")
        )
        s1_factor2 = isa_model_warlock.study_factor_factory(
            name="rate",
            type=isa_model_warlock.ontology_annotation_factory(
                name="rate",
                termSource="PATO",
                termAccession="http://purl.obolibrary.org/obo/PATO_0000161"
            )
        )
        s1.studyFactors.append(s1_factor1)
        s1.studyFactors.append(s1_factor2)

        assert i.identifier == "BII-I-1"
        assert i.title == "Growth control of the eukaryote cell: a systems biology study in yeast"
        assert i.description == "Background Cell growth underlies many key cellular and developmental processes, yet a limited number of studies have been carried out on cell-growth regulation. Comprehensive studies at the transcriptional, proteomic and metabolic levels under defined controlled conditions are currently lacking. Results Metabolic control analysis is being exploited in a systems biology study of the eukaryotic cell. Using chemostat culture, we have measured the impact of changes in flux (growth rate) on the transcriptome, proteome, endometabolome and exometabolome of the yeast Saccharomyces cerevisiae. Each functional genomic level shows clear growth-rate-associated trends and discriminates between carbon-sufficient and carbon-limited conditions. Genes consistently and significantly upregulated with increasing growth rate are frequently essential and encode evolutionarily conserved proteins of known function that participate in many protein-protein interactions. In contrast, more unknown, and fewer essential, genes are downregulated with increasing growth rate; their protein products rarely interact with one another. A large proportion of yeast genes under positive growth-rate control share orthologs with other eukaryotes, including humans. Significantly, transcription of genes encoding components of the TOR complex (a major controller of eukaryotic cell growth) is not subject to growth-rate regulation. Moreover, integrative studies reveal the extent and importance of post-transcriptional control, patterns of control of metabolic fluxes at the level of enzyme synthesis, and the relevance of specific enzymatic reactions in the control of metabolic fluxes during cell growth. Conclusion This work constitutes a first comprehensive systems biology study on growth-rate control in the eukaryotic cell. The results have direct implications for advanced studies on cell growth, in vivo regulation of metabolic fluxes for comprehensive metabolic engineering, and for the design of genome-scale systems biology models of the eukaryotic cell."
        assert i.submissionDate == "30/04/2007"
        assert i.publicReleaseDate == "10/03/2009"

        assert s1.identifier == "BII-I-1"
        assert s1.title == "Growth control of the eukaryote cell: a systems biology study in yeast"
        assert s1.description == "Background Cell growth underlies many key cellular and developmental processes, yet..."
        assert s1.submissionDate == "30/04/2007"
        assert s1.publicReleaseDate == "10/03/2009"

        i.studies.append(s1)
        from json import dumps
        print(dumps(i, indent=4, sort_keys=True))

