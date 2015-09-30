__author__ = 'dj'
import unittest, datetime
from api.io.isa_v1_model import *

class TestISAModel(unittest.TestCase):

    def setUp(self):
        """Create an empty ISA object

        This is based on BII-I-1 test data.
        """
        #TODO: Check test data is correct. Ontology Source References are possibly malformed.

        i = Investigation()

        ontology_obi = OntologySourceReference()
        ontology_obi.name = "OBI"
        ontology_obi.file = "http://bioportal.bioontology.org/ontologies/1123"
        ontology_obi.version = "47893"
        ontology_obi.description = "Ontology for Biomedical Investigations"
        i.ontologySourceReferences.append(ontology_obi)

        ontology_bto = OntologySourceReference()
        ontology_bto.name = "BTO"
        ontology_bto.file = "ArrayExpress Experimental Factor Ontology"
        ontology_bto.version = "v 1.26"
        ontology_bto.description = "BRENDA tissue / enzyme source"
        i.ontologySourceReferences.append(ontology_bto)

        ontology_newt = OntologySourceReference()
        ontology_newt.name = "NEWT"
        ontology_newt.version = "v 1.26"
        ontology_newt.description = "NEWT UniProt Taxonomy Database"
        i.ontologySourceReferences.append(ontology_newt)

        ontology_uo = OntologySourceReference()
        ontology_uo.name = "UO"
        ontology_uo.version = "v 1.26"
        ontology_uo.description = "Unit Ontology"
        i.ontologySourceReferences.append(ontology_uo)

        ontology_chebi = OntologySourceReference()
        ontology_chebi.name = "CHEBI"
        ontology_chebi.version = "v 1.26"
        ontology_chebi.description = "Chemical Entities of Biological Interest"
        i.ontologySourceReferences.append(ontology_chebi)

        ontology_pato = OntologySourceReference()
        ontology_pato.name = "PATO"
        ontology_pato.version = "v 1.26"
        ontology_pato.description = "Phenotypic qualities (properties)"
        i.ontologySourceReferences.append(ontology_pato)

        ontology_efo = OntologySourceReference()
        ontology_efo.name = "EFO"
        ontology_efo.version = "v 1.26"
        ontology_efo.description = "ArrayExpress Experimental Factor Ontology"
        i.ontologySourceReferences.append(ontology_efo)

        i.title = "Growth control of the eukaryote cell: a systems biology study in yeast"
        i.description = "Background Cell growth underlies many key cellular and developmental processes, yet a limited number of studies have been carried out on cell-growth regulation. Comprehensive studies at the transcriptional, proteomic and metabolic levels under defined controlled conditions are currently lacking. Results Metabolic control analysis is being exploited in a systems biology study of the eukaryotic cell. Using chemostat culture, we have measured the impact of changes in flux (growth rate) on the transcriptome, proteome, endometabolome and exometabolome of the yeast Saccharomyces cerevisiae. Each functional genomic level shows clear growth-rate-associated trends and discriminates between carbon-sufficient and carbon-limited conditions. Genes consistently and significantly upregulated with increasing growth rate are frequently essential and encode evolutionarily conserved proteins of known function that participate in many protein-protein interactions. In contrast, more unknown, and fewer essential, genes are downregulated with increasing growth rate; their protein products rarely interact with one another. A large proportion of yeast genes under positive growth-rate control share orthologs with other eukaryotes, including humans. Significantly, transcription of genes encoding components of the TOR complex (a major controller of eukaryotic cell growth) is not subject to growth-rate regulation. Moreover, integrative studies reveal the extent and importance of post-transcriptional control, patterns of control of metabolic fluxes at the level of enzyme synthesis, and the relevance of specific enzymatic reactions in the control of metabolic fluxes during cell growth. Conclusion This work constitutes a first comprehensive systems biology study on growth-rate control in the eukaryotic cell. The results have direct implications for advanced studies on cell growth, in vivo regulation of metabolic fluxes for comprehensive metabolic engineering, and for the design of genome-scale systems biology models of the eukaryotic cell."
        i.submissionDate = datetime.date(2007, 4, 30)
        i.publicReleaseDate = datetime.date(2009, 3, 10)

        pub = Publication()
        pub.title = "Growth control of the eukaryote cell: a systems biology study in yeast."
        pub.authorList = "Castrillo JI, Zeef LA, Hoyle DC, Zhang N, Hayes A, Gardner DC, Cornell MJ, Petty J, Hakes L, Wardleworth L, Rash B, Brown M, Dunn WB, Broadhurst D, O'Donoghue K, Hester SS, Dunkley TP, Hart SR, Swainston N, Li P, Gaskell SJ, Paton NW, Lilley KS, Kell DB, Oliver SG."
        pub.DOI = "doi:10.1186/jbiol54"
        pub.pubMedID = "174.39666"
        pub.status = "indexed in Pubmed"
        i.publications.append(pub)

        contact_oliver_sg = Person()
        contact_oliver_sg.lastName = "Oliver"
        contact_oliver_sg.midInitials = "G"
        contact_oliver_sg.firstName = "Stephen"
        contact_oliver_sg.address = "Oxford Road, Manchester M13 9PT, UK"
        contact_oliver_sg.affiliation = "Faculty of Life Sciences, Michael Smith Building, University of Manchester"
