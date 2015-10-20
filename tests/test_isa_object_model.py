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

        # INVESTIGATION
        i = isa_model_warlock.investigation_factory(
            identifier="BII-I-1",
            title="Growth control of the eukaryote cell: a systems biology study in yeast",
            description="Background Cell growth underlies many key cellular and developmental processes, yet a limited number of studies have been carried out on cell-growth regulation. Comprehensive studies at the transcriptional, proteomic and metabolic levels under defined controlled conditions are currently lacking. Results Metabolic control analysis is being exploited in a systems biology study of the eukaryotic cell. Using chemostat culture, we have measured the impact of changes in flux (growth rate) on the transcriptome, proteome, endometabolome and exometabolome of the yeast Saccharomyces cerevisiae. Each functional genomic level shows clear growth-rate-associated trends and discriminates between carbon-sufficient and carbon-limited conditions. Genes consistently and significantly upregulated with increasing growth rate are frequently essential and encode evolutionarily conserved proteins of known function that participate in many protein-protein interactions. In contrast, more unknown, and fewer essential, genes are downregulated with increasing growth rate; their protein products rarely interact with one another. A large proportion of yeast genes under positive growth-rate control share orthologs with other eukaryotes, including humans. Significantly, transcription of genes encoding components of the TOR complex (a major controller of eukaryotic cell growth) is not subject to growth-rate regulation. Moreover, integrative studies reveal the extent and importance of post-transcriptional control, patterns of control of metabolic fluxes at the level of enzyme synthesis, and the relevance of specific enzymatic reactions in the control of metabolic fluxes during cell growth. Conclusion This work constitutes a first comprehensive systems biology study on growth-rate control in the eukaryotic cell. The results have direct implications for advanced studies on cell growth, in vivo regulation of metabolic fluxes for comprehensive metabolic engineering, and for the design of genome-scale systems biology models of the eukaryotic cell.",
            submissionDate="30/04/2007",
            publicReleaseDate="10/03/2009"
        )

        i_ontology_source = isa_model_warlock.ontology_source_reference_factory(
            name="OBI",
            description="Ontology for Biomedical Investigations",
            file="http://bioportal.bioontology.org/ontologies/1123",
            version="47893"
        )
        i.ontologySourceReferences.append(i_ontology_source)

        i_publication = isa_model_warlock.publication_factory(
            pubMedID="17439666",
            doi="doi:10.1186/jbiol54",
            authorList="Castrillo JI, Zeef LA, Hoyle DC, Zhang N, Hayes A, Gardner DC, Cornell MJ, Petty J, Hakes L, Wardleworth L, Rash B, Brown M, Dunn WB, Broadhurst D, O'Donoghue K, Hester SS, Dunkley TP, Hart SR, Swainston N, Li P, Gaskell SJ, Paton NW, Lilley KS, Kell DB, Oliver SG.",
            title="Growth control of the eukaryote cell: a systems biology study in yeast.",
            status=isa_model_warlock.ontology_annotation_factory(name="published")
        )
        i.publications.append(i_publication)

        # STUDY - 1/2
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

        s1_assay1 = isa_model_warlock.assay_factory(
            fileName="a_proteome.txt",
            measurementType=isa_model_warlock.ontology_annotation_factory(
                name="protein expression profiling",
                termSource="OBI",
                termAccession="http://purl.obolibrary.org/obo/OBI_0000615"
            ),
            technologyType=isa_model_warlock.ontology_annotation_factory(
                name="mass spectrometry",
                termSource="OBI"
            ),
            technologyPlatform="iTRAQ"
        )
        s1_assay2 = isa_model_warlock.assay_factory(
            fileName="a_metabolome.txt",
            measurementType=isa_model_warlock.ontology_annotation_factory(
                name="metabolite profiling",
                termSource="OBI",
                termAccession="http://purl.obolibrary.org/obo/OBI_0000366"
            ),
            technologyType=isa_model_warlock.ontology_annotation_factory(
                name="mass spectrometry",
                termSource="OBI"
            ),
            technologyPlatform="LC-MS/MS"
        )
        s1_assay3 = isa_model_warlock.assay_factory(
            fileName="a_transcriptome.txt",
            measurementType=isa_model_warlock.ontology_annotation_factory(
                name="transcription profiling",
                termSource="OBI",
                termAccession="http://purl.obolibrary.org/obo/OBI_0000366"
            ),
            technologyType=isa_model_warlock.ontology_annotation_factory(
                name="DNA microarray",
                termSource="OBI",
                termAccession="http://purl.obolibrary.org/obo/OBI_0400148"
            ),
            technologyPlatform="Affymetrix"
        )
        s1.assays.append(s1_assay1)
        s1.assays.append(s1_assay2)
        s1.assays.append(s1_assay3)

        s1_protocol1 = isa_model_warlock.study_protocol_factory(
            name="growth protocol",
            protocolType=isa_model_warlock.ontology_annotation_factory(name="growth"),
            description="1. Biomass samples (45 ml) were taken via the sample port of the Applikon fermenters. The cells were pelleted by centrifugation for 5 min at 5000 rpm. The supernatant was removed and the RNA pellet resuspended in the residual medium to form a slurry. This was added in a dropwise manner directly into a 5 ml Teflon flask (B. Braun Biotech, Germany) containing liquid nitrogen and a 7 mm-diameter tungsten carbide ball. After allowing evaporation of the liquid nitrogen the flask was reassembled and the cells disrupted by agitation at 1500 rpm for 2 min in a Microdismembranator U (B. Braun Biotech, Germany) 2. The frozen powder was then dissolved in 1 ml of TriZol reagent (Sigma-Aldrich, UK), vortexed for 1 min, and then kept at room temperature for a further 5min. 3. Chloroform extraction was performed by addition of 0.2 ml chloroform, shaking vigorously or 15 s, then 5min incubation at room temperature. 4. "
        )
        s1_protocol2 = isa_model_warlock.study_protocol_factory(
            name="mRNA extraction",
            protocolType=isa_model_warlock.ontology_annotation_factory(name="mRNA extraction"),
            description="1. Biomass samples (45 ml) were taken via the sample port of the Applikon fermenters. The cells were pelleted by centrifugation for 5 min at 5000 rpm. The supernatant was removed and the RNA pellet resuspended in the residual medium to form a slurry. This was added in a dropwise manner directly into a 5 ml Teflon flask (B. Braun Biotech, Germany) containing liquid nitrogen and a 7 mm-diameter tungsten carbide ball. After allowing evaporation of the liquid nitrogen the flask was reassembled and the cells disrupted by agitation at 1500 rpm for 2 min in a Microdismembranator U (B. Braun Biotech, Germany) 2. The frozen powder was then dissolved in 1 ml of TriZol reagent (Sigma-Aldrich, UK), vortexed for 1 min, and then kept at room temperature for a further 5min. 3. Chloroform extraction was performed by addition of 0.2 ml chloroform, shaking vigorouslyor 15 s, then 5min incubation at room temperature. 4. Following centrifugation at 12,000 rpm for 5 min, the RNA (contained in the aqueous phase) was precipitated with 0.5 vol of 2-propanol at room temperature for 15 min. 5. After further centrifugation (12,000 rpm for 10 min at 4 C) the RNA pellet was washed twice with 70 % (v/v) ethanol, briefly air-dried, and redissolved in 0.5 ml diethyl pyrocarbonate (DEPC)-treated water. 6. The single-stranded RNA was precipitated once more by addition of 0.5 ml of LiCl bffer (4 M LiCl, 20 mM Tris-HCl, pH 7.5, 10 mM EDTA), thus removing tRNA and DNA from the sample. 7. After precipitation (20 C for 1 h) and centrifugation (12,000 rpm, 30 min, 4 C), the RNA was washed twice in 70 % (v/v) ethanol prior to being dissolved in a minimal volume of DEPC-treated water. 8. Total RNA quality was checked using the RNA 6000 Nano Assay, and analysed on an Agilent 2100 Bioanalyser (Agilent Technologies). RNA was quantified using the Nanodrop ultra low volume spectrophotometer (Nanodrop Technologies)."
        )
        s1_protocol3 = isa_model_warlock.study_protocol_factory(
            name="protein extraction",
            protocolType=isa_model_warlock.ontology_annotation_factory(name="protein extraction")
        )
        s1_protocol4 = isa_model_warlock.study_protocol_factory(
            name="biotin labeling",
            protocolType=isa_model_warlock.ontology_annotation_factory(name="labeling"),
            description="This was done using Enzo BioArrayTM HighYieldTM RNA transcript labelling kit (T7) with 5 ul cDNA. The resultant cRNA was again purified using the GeneChip Sample Clean Up Module. The column was eluted in the first instance using 10 l RNase-free water, and for a second time using 11 ul RNase-free water. cRNA was quantified using the Nanodrop spectrophotometer. A total of 15 ug of cRNA (required for hybridisation) was fragmented. Fragmentation was carried out by using 2 ul of fragmentation buffer for every 8 ul cRNA."
        )
        s1_protocol5 = isa_model_warlock.study_protocol_factory(
            name="ITRAQ labeling",
            protocolType=isa_model_warlock.ontology_annotation_factory(name="labeling")
        )
        s1_protocol6 = isa_model_warlock.study_protocol_factory(
            name="EukGE-WS4",
            protocolType=isa_model_warlock.ontology_annotation_factory(name="hybridization"),
            description="For each target, a hybridisation cocktail was made using the standard array recipe as described in the GeneChip Expression Analysis technical manual. GeneChip control oligonucleotide and 20x eukaryotic hybridisation controls were used. Hybridisation buffer was made as detailed in the GeneChip manual and the BSA and herring sperm DNA was purchased from Invitrogen. The cocktail was heated to 99 C for 5 min, transferred to 45 C for 5 min and then spun for 5 min to remove any insoluble material. Affymetrix Yeast Yg_s98 S. cerevisiae arrays were pre-hybridised with 200 ul 1x hybridisation buffer and incubated at 45 C for 10 min. 200 ul of the hybridisation cocktail was loaded onto the arrays. The probe array was incubated in a rotisserie at 45 C, rotating at 60 rpm. Following hybridisation, for 16 hr, chips were loaded onto a Fluidics station for washing and staining using the EukGe WS2v4 programme controlled using Microarray Suite 5 software."
        )
        s1_protocol7 = isa_model_warlock.study_protocol_factory(
            name="metabolite extraction",
            protocolType=isa_model_warlock.ontology_annotation_factory(
                name="extraction",
                termSource="OBI",
                termAccession="http://purl.obolibrary.org/obo/OBI_0302884"
            ),
            description="For each target, a hybridisation cocktail was made using the standard array recipe as described in the GeneChip Expression Analysis technical manual. GeneChip control oligonucleotide and 20x eukaryotic hybridisation controls were used. Hybridisation buffer was made as detailed in the GeneChip manual and the BSA and herring sperm DNA was purchased from Invitrogen. The cocktail was heated to 99 C for 5 min, transferred to 45 C for 5 min and then spun for 5 min to remove any insoluble material. Affymetrix Yeast Yg_s98 S. cerevisiae arrays were pre-hybridised with 200 ul 1x hybridisation buffer and incubated at 45 C for 10 min. 200 ul of the hybridisation cocktail was loaded onto the arrays. The probe array was incubated in a rotisserie at 45 C, rotating at 60 rpm. Following hybridisation, for 16 hr, chips were loaded onto a Fluidics station for washing and staining using the EukGe WS2v4 programme controlled using Microarray Suite 5 software."
        )
        s1_protocol7.parameters.append(isa_model_warlock.ontology_annotation_factory(name="sample value"))
        s1_protocol7.parameters.append(isa_model_warlock.ontology_annotation_factory(name="standard volume"))

        s1.protocols.append(s1_protocol1)
        s1.protocols.append(s1_protocol2)
        s1.protocols.append(s1_protocol3)
        s1.protocols.append(s1_protocol4)
        s1.protocols.append(s1_protocol5)
        s1.protocols.append(s1_protocol6)
        s1.protocols.append(s1_protocol7)

        s1_contact1 = isa_model_warlock.contact_factory(
            lastName="Oliver",
            firstName="Stephen",
            midInitials="G",
            address="Oxford Road, Manchester M13 9PT, UK",
            affiliation="Faculty of Life Sciences, Michael Smith Building, University of Manchester"
        )
        s1_contact1.roles.append(isa_model_warlock.ontology_annotation_factory(name="corresponding author"))

        s1_contact2 = isa_model_warlock.contact_factory(
            lastName="Juan",
            firstName="Castrillo",
            midInitials="I",
            address="Oxford Road, Manchester M13 9PT, UK",
            affiliation="Faculty of Life Sciences, Michael Smith Building, University of Manchester"
        )
        s1_contact2.roles.append(isa_model_warlock.ontology_annotation_factory(name="author"))

        s1_contact3 = isa_model_warlock.contact_factory(
            lastName="Leo",
            firstName="Zeef",
            midInitials="A",
            address="Oxford Road, Manchester M13 9PT, UK",
            affiliation="Faculty of Life Sciences, Michael Smith Building, University of Manchester"
        )
        s1_contact3.roles.append(isa_model_warlock.ontology_annotation_factory(name="author"))

        s1.contacts.append(s1_contact1)
        s1.contacts.append(s1_contact2)
        s1.contacts.append(s1_contact3)


        # STUDY - 2/2


        # assert i.identifier == "BII-I-1"
        # assert i.title == "Growth control of the eukaryote cell: a systems biology study in yeast"
        # assert i.description == "Background Cell growth underlies many key cellular and developmental processes, yet a limited number of studies have been carried out on cell-growth regulation. Comprehensive studies at the transcriptional, proteomic and metabolic levels under defined controlled conditions are currently lacking. Results Metabolic control analysis is being exploited in a systems biology study of the eukaryotic cell. Using chemostat culture, we have measured the impact of changes in flux (growth rate) on the transcriptome, proteome, endometabolome and exometabolome of the yeast Saccharomyces cerevisiae. Each functional genomic level shows clear growth-rate-associated trends and discriminates between carbon-sufficient and carbon-limited conditions. Genes consistently and significantly upregulated with increasing growth rate are frequently essential and encode evolutionarily conserved proteins of known function that participate in many protein-protein interactions. In contrast, more unknown, and fewer essential, genes are downregulated with increasing growth rate; their protein products rarely interact with one another. A large proportion of yeast genes under positive growth-rate control share orthologs with other eukaryotes, including humans. Significantly, transcription of genes encoding components of the TOR complex (a major controller of eukaryotic cell growth) is not subject to growth-rate regulation. Moreover, integrative studies reveal the extent and importance of post-transcriptional control, patterns of control of metabolic fluxes at the level of enzyme synthesis, and the relevance of specific enzymatic reactions in the control of metabolic fluxes during cell growth. Conclusion This work constitutes a first comprehensive systems biology study on growth-rate control in the eukaryotic cell. The results have direct implications for advanced studies on cell growth, in vivo regulation of metabolic fluxes for comprehensive metabolic engineering, and for the design of genome-scale systems biology models of the eukaryotic cell."
        # assert i.submissionDate == "30/04/2007"
        # assert i.publicReleaseDate == "10/03/2009"
        #
        # assert s1.identifier == "BII-I-1"
        # assert s1.title == "Growth control of the eukaryote cell: a systems biology study in yeast"
        # assert s1.description == "Background Cell growth underlies many key cellular and developmental processes, yet..."
        # assert s1.submissionDate == "30/04/2007"
        # assert s1.publicReleaseDate == "10/03/2009"

        i.studies.append(s1)
        from json import dumps
        print(dumps(i, indent=4, sort_keys=True))

