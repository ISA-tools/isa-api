from unittest import TestCase
from isatools.model.v1 import *


class TestAbstractModelClasses(TestCase):

    def test_object_comment(self):
        comment = Comment(
            name='',
            value=''
        )
        self.assertIsInstance(comment.name, str)
        self.assertIsInstance(comment.value, str)
        # TODO: Implement test on Comments in other objects

    def test_object_ontology_source_reference(self):
        ontology_source_reference = OntologySourceReference(
            name='',
            description='',
            file='',
            version=''
        )
        self.assertIsInstance(ontology_source_reference.name, str)
        self.assertIsInstance(ontology_source_reference.description, str)
        self.assertIsInstance(ontology_source_reference.file, str)
        self.assertIsInstance(ontology_source_reference.version, str)

    def test_object_ontology_annotation(self):
        ontology_annotation = OntologyAnnotation(
            name='',
            term_source=OntologySourceReference(),
            term_accession=''
        )
        self.assertIsInstance(ontology_annotation.name, str)
        self.assertIsInstance(ontology_annotation.term_source, OntologySourceReference)
        self.assertIsInstance(ontology_annotation.term_accession, str)

    def test_object_publication(self):
        publication = Publication(
            pubmed_id='',
            doi='',
            author_list='',
            title='',
            status=OntologyAnnotation()
        )
        self.assertIsInstance(publication.pubmed_id, str)
        self.assertIsInstance(publication.doi, str)
        self.assertIsInstance(publication.author_list, str)
        self.assertIsInstance(publication.title, str)
        self.assertIsInstance(publication.status, OntologyAnnotation)

    def test_object_contact(self):
        contact = Person(
            last_name='',
            first_name='',
            mid_initials='',
            address='',
            affiliation=''
        )
        contact.roles.append(OntologyAnnotation())
        self.assertIsInstance(contact.first_name, str)
        self.assertIsInstance(contact.mid_initials, str)
        self.assertIsInstance(contact.last_name, str)
        self.assertIsInstance(contact.address, str)
        self.assertIsInstance(contact.affiliation, str)
        self.assertIsInstance(contact.roles, list)
        self.assertIsInstance(contact.roles[0], OntologyAnnotation)

    def test_object_investigation(self):
        investigation = Investigation(
            identifier='',
            title='',
            description='',
            submission_date='',
            public_release_date=''
        )
        investigation.ontology_source_references.append(OntologySourceReference())
        investigation.publications.append(Publication())
        investigation.contacts.append(Person())
        investigation.studies.append(Study())
        self.assertIsInstance(investigation.identifier, str)
        self.assertIsInstance(investigation.title, str)
        self.assertIsInstance(investigation.description, str)
        self.assertIsInstance(investigation.submission_date, str)
        self.assertIsInstance(investigation.public_release_date, str)
        self.assertIsInstance(investigation.ontology_source_references, list)
        self.assertIsInstance(investigation.ontology_source_references[0], OntologySourceReference)
        self.assertIsInstance(investigation.publications, list)
        self.assertIsInstance(investigation.publications[0], Publication)
        self.assertIsInstance(investigation.contacts, list)
        self.assertIsInstance(investigation.contacts[0], Person)
        self.assertIsInstance(investigation.studies, list)
        self.assertIsInstance(investigation.studies[0], Study)

    def test_object_protocol(self):
        protocol = Protocol(
            name='',
            protocol_type=OntologyAnnotation(),
            description='',
            uri='',
            version=''
        )
        protocol.parameters.append(OntologyAnnotation())
        protocol.components.append(OntologyAnnotation())
        self.assertIsInstance(protocol.name, str)
        self.assertIsInstance(protocol.protocol_type, OntologyAnnotation)
        self.assertIsInstance(protocol.description, str)
        self.assertIsInstance(protocol.uri, str)
        self.assertIsInstance(protocol.version, str)


    def test_object_source(self):
        source = Source(
            name=''
        )
        source.characteristics.append(Characteristic())
        self.assertIsInstance(source.name, str)
        self.assertIsInstance(source.characteristics, list)
        self.assertIsInstance(source.characteristics[0], Characteristic)

    def test_object_study_factor(self):
        factor = StudyFactor(
            name='',
            factor_type=OntologyAnnotation()
        )
        self.assertIsInstance(factor.name, str)
        self.assertIsInstance(factor.factor_type, OntologyAnnotation)

    def test_object_sample(self):
        sample = Sample(
            name=''
        )
        sample.characteristics.append(Characteristic())
        sample.factor_values.append(StudyFactor())
        self.assertIsInstance(sample.name, str)
        self.assertIsInstance(sample.characteristics, list)
        self.assertIsInstance(sample.characteristics[0], Characteristic)
        self.assertIsInstance(sample.factor_values, list)
        self.assertIsInstance(sample.factor_values[0], StudyFactor)

    def test_object_material(self):
        material = Material(name='')
        material.characteristics.append(Characteristic())
        self.assertIsInstance(material.name, str)
        self.assertIsInstance(material.characteristics, list)
        self.assertIsInstance(material.characteristics[0], Characteristic)

    def test_object_datafile(self):
        datafile = DataFile(filename='', label='')
        self.assertIsInstance(datafile.filename, str)
        self.assertIsInstance(datafile.label, str)

    def test_object_process(self):
        process = Process(
            name='',
            executes_protocol=Protocol(),
        )
        process.parameter_values.append(OntologyAnnotation())
        process.inputs.append(Material())
        process.inputs.append(DataFile())
        process.outputs.append(Material())
        process.outputs.append(DataFile())
        self.assertIsInstance(process.name, str)
        self.assertIsInstance(process.executes_protocol, Protocol)
        self.assertIsInstance(process.parameter_values, list)
        self.assertIsInstance(process.parameter_values[0], OntologyAnnotation)
        self.assertIsInstance(process.inputs, list)
        self.assertIsInstance(process.inputs[0], Material)
        self.assertIsInstance(process.inputs[1], DataFile)
        self.assertIsInstance(process.outputs, list)
        self.assertIsInstance(process.outputs[0], Material)
        self.assertIsInstance(process.outputs[1], DataFile)

    def test_object_assay(self):
        assay = Assay(
            filename='',
            measurement_type=OntologyAnnotation(),
            technology_type=OntologyAnnotation(),
            technology_platform=''
        )
        self.assertIsInstance(assay.filename, str)
        self.assertIsInstance(assay.measurement_type, OntologyAnnotation)
        self.assertIsInstance(assay.technology_type, OntologyAnnotation)
        self.assertIsInstance(assay.technology_platform, str)

    def test_object_study(self):
        study = Study(
            identifier='',
            title='',
            description='',
            submission_date='',
            public_release_date='',
            filename=''
        )
        study.publications.append(Publication())
        study.contacts.append(Person())
        study.design_descriptors.append(OntologyAnnotation())
        study.protocols.append(Protocol())
        study.materials['sources'].append(Source())
        study.materials['samples'].append(Sample())
        study.process_sequence.append(Process())
        study.assays.append(Assay())
        study.materials['samples'].append(Sample())
        self.assertIsInstance(study.identifier, str)
        self.assertIsInstance(study.title, str)
        self.assertIsInstance(study.description, str)
        self.assertIsInstance(study.submission_date, str)
        self.assertIsInstance(study.public_release_date, str)
        self.assertIsInstance(study.filename, str)
        self.assertIsInstance(study.publications, list)
        self.assertIsInstance(study.publications[0], Publication)
        self.assertIsInstance(study.contacts, list)
        self.assertIsInstance(study.contacts[0], Person)
        self.assertIsInstance(study.design_descriptors, list)
        self.assertIsInstance(study.design_descriptors[0], OntologyAnnotation)
        self.assertIsInstance(study.protocols, list)
        self.assertIsInstance(study.protocols[0], Protocol)
        self.assertIsInstance(study.materials['sources'], list)
        self.assertIsInstance(study.materials['sources'][0], Source)
        self.assertIsInstance(study.materials['samples'], list)
        self.assertIsInstance(study.materials['samples'][0], Sample)
        self.assertIsInstance(study.process_sequence, list)
        self.assertIsInstance(study.process_sequence[0], Process)
        self.assertIsInstance(study.assays, list)
        self.assertIsInstance(study.assays[0], Assay)
        self.assertIsInstance(study.materials['samples'], list)
        self.assertIsInstance(study.materials['samples'][0], Sample)

    def test_batch_create_materials(self):
        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material')
        batch = batch_create_materials(prototype_sample, n=10)
        batch_set_attr(batch, 'derives_from', source)
        self.assertIsInstance(batch, list)
        self.assertEqual(len(batch), 10)
        self.assertIsInstance(batch[0], Sample)
        self.assertIsInstance(batch[0].derives_from, Source)
        self.assertEqual(batch[0].derives_from, batch[9].derives_from)

    def test_batch_create_assays(self):
        # flat end-to-end
        sample = Sample(name='sample')
        data_acquisition = Process(name='data acquisition')
        material = Material(name='material')
        labeling = Process(name='labeling')
        extract = LabeledExtract(name='lextract')
        batch = batch_create_assays(sample, data_acquisition, material, labeling, extract, n=3)
        self.assertIsInstance(batch, list)
        self.assertEqual(len(batch), 6)  # 6 processes, since 2 processes per process sequence
        self.assertIsInstance(batch[0], Process)
        self.assertIsInstance(batch[0].inputs[0], Sample)
        self.assertEqual(batch[0].name, 'data acquisition-0')
        self.assertIsInstance(batch[0].outputs[0], Material)
        self.assertEqual(batch[0].outputs[0].derives_from, batch[0].inputs[0])

        # multiple sample -> process -> multiple material
        sample1 = Sample(name='sample')
        sample2 = Sample(name='sample')
        data_acquisition = Process(name='data acquisition')
        material1 = Material(name='material')
        material2 = Material(name='material')
        batch = batch_create_assays([sample1, sample2], data_acquisition, [material1, material2], n=3)
        self.assertIsInstance(batch, list)
        self.assertEqual(len(batch), 3)  # 3 processes
        self.assertIsInstance(batch[0], Process)
        self.assertEqual(len(batch[0].inputs), 2)
        self.assertIsInstance(batch[0].inputs[0], Sample)
        self.assertEqual(batch[0].name, 'data acquisition-0')
        self.assertEqual(len(batch[0].outputs), 2)
        self.assertIsInstance(batch[0].outputs[0], Material)
        self.assertEqual(batch[0].outputs[0].derives_from, [batch[0].inputs[0], batch[0].inputs[1]])

    def test_create_bii_s_3(self):
        # Create the root investigation object with an identifier
        i = Investigation(identifier='BII-S-3')

        # Create some ontology source references
        term_source_chebi = OntologySourceReference(
            name='CHEBI',
            file='http://data.bioontology.org/ontologies/CHEBI',
            version='78',
            description="Chemical Entities of Biological Interest Ontology")
        term_source_efo = OntologySourceReference(
            name='EFO',
            file='http://data.bioontology.org/ontologies/EFO',
            version='111',
            description="Experimental Factor Ontology")
        term_source_obi = OntologySourceReference(
            name='OBI',
            file='http://data.bioontology.org/ontologies/OBI',
            version='21',
            description="Ontology for Biomedical Investigations")
        term_source_ncbitaxon = OntologySourceReference(
            name='NCBITAXON',
            file='http://data.bioontology.org/ontologies/NCBITAXON',
            version='2',
            description="National Center for Biotechnology Information (NCBI) Organismal Classification")
        term_source_pato = OntologySourceReference(
            name='PATO',
            file='http://data.bioontology.org/ontologies/PATO',
            version='160',
            description="Phenotypic Quality Ontology")
        # Attach ontology sources to the investigation ontology_source_references list
        i.ontology_source_references.append(term_source_chebi)
        i.ontology_source_references.append(term_source_efo)
        i.ontology_source_references.append(term_source_obi)
        i.ontology_source_references.append(term_source_ncbitaxon)
        i.ontology_source_references.append(term_source_pato)

        # Create two comments. The first contains an empty string, the second as some value set
        comment_created_with_config = Comment(name='Created With Configuration')
        comment_last_opened_with_config = Comment(name='Last Opened With Configuration')
        comment_last_opened_with_config.value = "GSC MIxS human gut"
        # Attach comments to the investigation comments list
        i.comments.append(comment_created_with_config)
        i.comments.append(comment_last_opened_with_config)

        # Create study object and associated metadata
        s = Study(
            identifier='BII-S-3',
            title="Metagenomes and Metatranscriptomes of phytoplankton blooms from an ocean acidification mesocosm experiment",
            description="Sequencing the metatranscriptome can provide information about the response of organisms to varying environmental conditions. We present a methodology for obtaining random whole-community mRNA from a complex microbial assemblage using Pyrosequencing. The metatranscriptome had, with minimum contamination by ribosomal RNA, significant coverage of abundant transcripts, and included significantly more potentially novel proteins than in the metagenome. This experiment is part of a much larger experiment. We have produced 4 454 metatranscriptomic datasets and 6 454 metagenomic datasets. These were derived from 4 samples.",
            submission_date='15/08/2008',
            public_release_date='15/08/2008',
            filename='s_BII-S-3.txt'
        )
        # Add some comments that are specific for SRA format submissions to ENA
        comment_sra_broker_name = Comment(name='SRA Broker Name', value='OXFORD')
        comment_sra_center_name = Comment(name='SRA Center Name', value='OXFORD')
        comment_sra_center_project_name = Comment(name='SRA Center Project Name', value='OXFORD')
        comment_sra_lab_name = Comment(name='SRA Lab Name', value='Oxford e-Research Centre')
        comment_sra_submission_action = Comment(name='SRA Submission Action', value='ADD')
        s.comments.append(comment_sra_broker_name)
        s.comments.append(comment_sra_center_name)
        s.comments.append(comment_sra_center_project_name)
        s.comments.append(comment_sra_lab_name)
        s.comments.append(comment_sra_submission_action)
        s.comments.append(Comment(name='Study Funding Agency'))
        s.comments.append(Comment(name='Study Grant Number'))

        # A design descriptor is an ontology annotation. Make sure you point term_source to an ontology_term_source
        dd = OntologyAnnotation(
            name='time series design',
            term_source=term_source_obi,
            term_accession='http://purl.obolibrary.org/obo/OBI_0500020'
        )
        s.design_descriptors.append(dd)  # Add your design descriptors to the design_descriptors list

        # Publications can be associated with a Study, but also to an Investigation (but not in this example)
        pub_1 = Publication(
            pubmed_id='18725995',
            doi='10.1371/journal.pone.0003042',
            author_list="Gilbert JA, Field D, Huang Y, Edwards R, Li W, Gilna P, Joint I.",
            title="Detection of large numbers of novel sequences in the metatranscriptomes of complex marine microbial communities.")
        pub_1.status = OntologyAnnotation(
            name='indexed in PubMed'
        )
        pub_2 = Publication(
            pubmed_id='18783384',
            doi='10.1111/j.1462-2920.2008.01745.x',
            author_list="Gilbert JA, Thomas S, Cooley NA, Kulakova A, Field D, Booth T, McGrath JW, Quinn JP, Joint I.",
            title="Potential for phosphonoacetate utilization by marine bacteria in temperate coastal waters.")
        pub_2.status = OntologyAnnotation(
            name='indexed in PubMed'
        )
        s.publications.append(pub_1)
        s.publications.append(pub_2)

        # Study factors need to be declared before using Factor Values in the study or assay graphs
        factor_dose = StudyFactor(name='dose',  # factor_types are ontology annotations
                                  factor_type=OntologyAnnotation(name='dose',
                                                                 term_source=term_source_efo,
                                                                 term_accession='http://www.ebi.ac.uk/efo/EFO_0000428'))
        factor_compound = StudyFactor(name='compound',
                                      factor_type=OntologyAnnotation(name='chemical substance',
                                                                     term_source=term_source_chebi,
                                                                     term_accession='http://purl.obolibrary.org/obo/CHEBI_59999'))
        factor_collection_time = StudyFactor(name='collection time',
                                             factor_type=OntologyAnnotation(name='time',
                                                                            term_source=term_source_pato,
                                                                            term_accession='http://purl.obolibrary.org/obo/PATO_0000165'))
        s.factors.append(factor_dose)
        s.factors.append(factor_compound)
        s.factors.append(factor_collection_time)

        # Study protocols need to be declared before using Processes and Parameter Values in study and assay graphs
        protocol_sample_collection = Protocol(
            name='sample collection - standard procedure 1',
            description="Waters samples were prefiltered through a 1.6 um GF/A glass fibre filter to reduce Eukaryotic contamination. Filtrate was then collected on a 0.2 um Sterivex (millipore) filter which was frozen in liquid nitrogen until nucelic acid extraction. CO2 bubbled through 11000 L mesocosm to simulate ocean acidification predicted conditions. Then phosphate and nitrate were added to induce a phytoplankton bloom.",
            protocol_type=OntologyAnnotation(name='environmental material collection')  # Protocol types are ontology annotations
        )
        protocol_sample_collection.parameters.append(ProtocolParameter(parameter_name=OntologyAnnotation(name='filter pore size')))  # Protocol parameter names are ontology annotation
        annotation_nucleic_acid_extraction = OntologyAnnotation(name='nucleic acid extraction')
        protocol_nucleic_acid_extraction = Protocol(
            name='nucleic acid extraction - standard procedure 2',
            description="Total nucleic acid extraction was done as quickly as possible using the method of Neufeld et al, 2007.",
            protocol_type=annotation_nucleic_acid_extraction
        )
        protocol_mrna_extraction = Protocol(
            name='mRNA extraction - standard procedure 3',
            description="RNA MinElute + substrative Hybridization + MEGAclear For transcriptomics, total RNA was separated from the columns using the RNA MinElute clean-up kit (Qiagen) and checked for integrity of rRNA using an Agilent bioanalyser (RNA nano6000 chip). High integrity rRNA is essential for subtractive hybridization. Samples were treated with Turbo DNA-free enzyme (Ambion) to remove contaminating DNA. The rRNA was removed from mRNA by subtractive hybridization (Microbe Express Kit, Ambion), and absence of rRNA and DNA contamination was confirmed using the Agilent bioanalyser. The mRNA was further purified with the MEGAclearTM kit (Ambion). Reverse transcription of mRNA was performed using the SuperScript III enzyme (Invitrogen) with random hexamer primers (Promega). The cDNA was treated with RiboShredderTM RNase Blend (Epicentre) to remove trace RNA contaminants. To improve the yield of cDNA, samples were subjected to random amplification using the GenomiPhi V2 method (GE Healthcare). GenomiPhi technology produces branched DNA molecules that are recalcitrant to the pyrosequencing methodology. Therefore amplified samples were treated with S1 nuclease using the method of Zhang et al.2006.",
            protocol_type=OntologyAnnotation(name='RNA extraction')
        )
        protocol_genomic_dna_extraction = Protocol(
            name='genomic DNA extraction - standard procedure 4',
            protocol_type=OntologyAnnotation(name='DNA extraction')
        )
        protocol_reverse_transcription = Protocol(
            name='reverse transcription - standard procedure 5',
            description="superscript+random hexamer primer",
            protocol_type=OntologyAnnotation(name='reverse transcription')
        )
        protocol_library_construction = Protocol(
            name='library construction',
            protocol_type=OntologyAnnotation(name='library construction')
        )
        protocol_library_construction.parameters.append(ProtocolParameter(parameter_name=OntologyAnnotation(name='library strategy')))
        protocol_library_construction.parameters.append(ProtocolParameter(parameter_name=OntologyAnnotation(name='library layout')))
        protocol_library_construction.parameters.append(ProtocolParameter(parameter_name=OntologyAnnotation(name='library selection')))
        protocol_pyrosequencing = Protocol(
            name='pyrosequencing - standard procedure 6',
            description="1. Sample Input and Fragmentation: The Genome Sequencer FLX System supports the sequencing of samples from a wide variety of starting materials including genomic DNA, PCR products, BACs, and cDNA. Samples such as genomic DNA and BACs are fractionated into small, 300- to 800-base pair fragments. For smaller samples, such as small non-coding RNA or PCR amplicons, fragmentation is not required. Instead, short PCR products amplified using Genome Sequencer fusion primers can be used for immobilization onto DNA capture beads as shown below.",
            protocol_type=annotation_nucleic_acid_extraction
        )
        protocol_pyrosequencing.parameters.append(ProtocolParameter(parameter_name=OntologyAnnotation(name='sequencing instrument')))
        protocol_seq_analysis = Protocol(
            name='sequence analysis - standard procedure 7',
            protocol_type=OntologyAnnotation(name='data transformation')
        )
        s.protocols.append(protocol_sample_collection)
        s.protocols.append(protocol_nucleic_acid_extraction)
        s.protocols.append(protocol_mrna_extraction)
        s.protocols.append(protocol_genomic_dna_extraction)
        s.protocols.append(protocol_reverse_transcription)
        s.protocols.append(protocol_library_construction)
        s.protocols.append(protocol_pyrosequencing)
        s.protocols.append(protocol_seq_analysis)

        role_pi = OntologyAnnotation('principal investigator role')
        contact_1 = Person(
            last_name='Gilbert',
            first_name='Jack',
            mid_initials='A',
            email='jagi@pml.ac.uk',
            address="Prospect Place, Plymouth, United Kingdom",
            affiliation='Plymouth Marine Laboratory',
            roles=[
                OntologyAnnotation(name='SRA Inform On Status'),
                OntologyAnnotation(name='SRA Inform On Error')
            ]
        )
        contact_1.roles.append(role_pi)
        contact_2 = Person(
            last_name='Field',
            first_name='Dawn',
            address="CEH Oxford, Oxford, United Kingdom",
            affiliation='NERC Centre for Ecology and Hydrology',
            roles=[role_pi]
        )
        contact_3 = Person(
            last_name='Huang',
            first_name='Ying',
            affiliation='California Institute for Telecommunications and Information Technology',
            address="San Diego State University, San Diego, California, United States of America",
            roles=[role_pi]
        )
        contact_4 = Person(
            last_name='Edwards',
            first_name='Rob',
            affiliation='Department of Computer Science, Mathematics and Computer Science Division,',
            address="Argonne National Laboratory, Argonne, Illinois, United States of America",
            roles=[role_pi]
        )
        contact_5 = Person(
            last_name='Li',
            first_name='Weizhong',
            affiliation='California Institute for Telecommunications and Information Technology',
            address="San Diego State University, San Diego, California, United States of America",
            roles=[role_pi]
        )
        contact_6 = Person(
            last_name='Gilna',
            first_name='Paul',
            affiliation='California Institute for Telecommunications and Information Technology',
            address="San Diego State University, San Diego, California, United States of America",
            roles=[role_pi]
        )
        contact_7 = Person(
            last_name='Joint',
            first_name='Ian',
            affiliation='Plymouth Marine Laboratory',
            address="Prospect Place, Plymouth, United Kingdom",
            roles=[role_pi]
        )
        s.contacts.append(contact_1)
        s.contacts.append(contact_2)
        s.contacts.append(contact_3)
        s.contacts.append(contact_4)
        s.contacts.append(contact_5)
        s.contacts.append(contact_6)
        s.contacts.append(contact_7)

        # Now let's build our study experiment graph. This corresponds to the study table file in ISA tab
        source1 = Source(name='GSM255770')

        # First few characteristics
        charac_organism = Characteristic(category=OntologyAnnotation(name='organism'),
                                         value=OntologyAnnotation(name='marine metagenome',
                                                                  term_source=term_source_ncbitaxon,
                                                                  term_accession='http://purl.obolibrary.org/obo/NCBITaxon_408172'))
        charac_location = Characteristic(category=OntologyAnnotation(name='geographic location (country and/or sea,region)'),
                                         value=OntologyAnnotation(name='Norway, fjord, coastal'))
        charac_longitude = Characteristic(category=OntologyAnnotation(name='geographic location (longitude)'),
                                          value='5.222222')
        charac_lattitude = Characteristic(category=OntologyAnnotation(name='geographic location (latitude)'),
                                          value='60.269444')

        # These units annotations are used on more than one of characteristics, so declare only once here and attach them
        unit_ug_per_l = OntologyAnnotation(name='ug/l')
        unit_number_per_ml = OntologyAnnotation(name='number/ml')
        unit_umol_per_l = OntologyAnnotation(name='umol/l')

        # There's a lot of characteristics in BII-S-3 attached to the sources, but all follow similar patterns throughout
        charac_chlorophyll_a_concentration = Characteristic(category=OntologyAnnotation(name='chlorophyll a concentration'),
                                                            value=9.23,
                                                            unit=unit_ug_per_l)
        charac_fucoxanthin_concentration = Characteristic(category=OntologyAnnotation(name='fucoxanthin concentration'),
                                                          value=0.54,
                                                          unit=unit_ug_per_l)
        charac_peridinin_concentration = Characteristic(category=OntologyAnnotation(name='peridinin concentration'),
                                                        value=0.18,
                                                        unit=unit_ug_per_l)
        charac_butfucoxanthin_concentration = Characteristic(category=OntologyAnnotation(name='butfucoxanthin concentration'),
                                                             value=0.14,
                                                             unit=unit_ug_per_l)
        charac_hexfucoxanthin_concentration = Characteristic(category=OntologyAnnotation(name='hexfucoxanthin concentration'),
                                                             value=0.82,
                                                             unit=unit_ug_per_l)
        charac_alloxanthin_concentration = Characteristic(category=OntologyAnnotation(name='alloxanthin concentration'),
                                                          value=0.36,
                                                          unit=unit_ug_per_l)
        charac_zeaxanthin_concentration = Characteristic(category=OntologyAnnotation(name='zeaxanthin concentration'),
                                                         value=0.35,
                                                         unit=unit_ug_per_l)
        charac_lutein_concentration = Characteristic(category=OntologyAnnotation(name='lutein concentration'),
                                                     value=0.37,
                                                     unit=unit_ug_per_l)
        charac_chl_c3_concentration = Characteristic(category=OntologyAnnotation(name='chl-c3 concentration'),
                                                     value=0.29,
                                                     unit=unit_ug_per_l)
        charac_chl_c2_concentration = Characteristic(category=OntologyAnnotation(name='chl-c2 concentration'),
                                                     value=0.59,
                                                     unit=unit_ug_per_l)
        charac_prasinoxanthin_concentration = Characteristic(category=OntologyAnnotation(name='prasinoxanthin concentration'),
                                                             value=0,
                                                             unit=unit_ug_per_l)
        charac_neoxanthin_concentration = Characteristic(category=OntologyAnnotation(name='neoxanthin concentration'),
                                                         value=0,
                                                         unit=unit_ug_per_l)
        charac_violaxanthin_concentration = Characteristic(category=OntologyAnnotation(name='violaxanthin concentration'),
                                                           value=0.64,
                                                           unit=unit_ug_per_l)

        charac_diadinoxanthin_concentration = Characteristic(category=OntologyAnnotation(name='diadinoxanthin concentration'),
                                                             value=0.46,
                                                             unit=unit_ug_per_l)
        charac_diatoxanthin_concentration = Characteristic(category=OntologyAnnotation(name='diatoxanthin concentration'),
                                                           value=0.1,
                                                           unit=unit_ug_per_l)
        charac_divinyl_chl_b_concentration = Characteristic(category=OntologyAnnotation(name='divinyl-chl-b concentration'),
                                                            value=0,
                                                            unit=unit_ug_per_l)
        charac_chl_b_concentration = Characteristic(category=OntologyAnnotation(name='chl-b concentration'),
                                                    value=5.25,
                                                    unit=unit_ug_per_l)
        charac_divinyl_chl_a_concentration = Characteristic(category=OntologyAnnotation(name='divinyl-chl-a concentration'),
                                                            value=0,
                                                            unit=unit_ug_per_l)
        charac_chl_a_concentration = Characteristic(category=OntologyAnnotation(name='chl-a concentration'),
                                                    value=9.23,
                                                    unit=unit_ug_per_l)
        charac_BB_carotene_concentration = Characteristic(category=OntologyAnnotation(name='BB carotene concentration'),
                                                          value=0.72,
                                                          unit=unit_ug_per_l)
        charac_bacteria_count = Characteristic(category=OntologyAnnotation(name='bacteria count'),
                                               value=4666004,
                                               unit=unit_number_per_ml)
        charac_synechococcus_count = Characteristic(category=OntologyAnnotation(name='synechococcus count'),
                                                    value=7064,
                                                    unit=unit_number_per_ml)
        charac_small_picoeukaryotes_count = Characteristic(category=OntologyAnnotation(name='small picoeukaryotes count'),
                                                           value=36257,
                                                           unit=unit_number_per_ml)
        charac_large_picoeukaryotes_count = Characteristic(category=OntologyAnnotation(name='large picoeukaryotes count'),
                                                           value=5450,
                                                           unit=unit_number_per_ml)
        charac_nanoflagellates_count = Characteristic(category=OntologyAnnotation(name='nanoflagellates count'),
                                                      value=2851,
                                                      unit=unit_number_per_ml)
        charac_cryptophytes_count = Characteristic(category=OntologyAnnotation(name='cryptophytes count'),
                                                   value=660,
                                                   unit=unit_number_per_ml)
        charac_phosphate_concentration = Characteristic(category=OntologyAnnotation(name='phosphate concentration'),
                                                        value=0.23,
                                                        unit=unit_umol_per_l)
        charac_nitrate_concentration = Characteristic(category=OntologyAnnotation(name='nitrate concentration'),
                                                      value=7.53,
                                                      unit=unit_umol_per_l)
        charac_particulate_organic_nitrogen_concentration = Characteristic(category=OntologyAnnotation(name='particulate organic nitrogen concentration'),
                                                                           value=143,
                                                                           unit=unit_ug_per_l)
        charac_particulate_organic_carbon_concentration = Characteristic(category=OntologyAnnotation(name='particulate organic carbon concentration'),
                                                                         value=844,
                                                                         unit=unit_ug_per_l)
        charac_primary_production_depth = Characteristic(category=OntologyAnnotation(name='primary production depth integrated production to 3 m expressed_in mgC m-2 d-1'),
                                                         value=591.4,
                                                         unit=OntologyAnnotation(name='mg/m2/d'))
        charac_water_salinity = Characteristic(category=OntologyAnnotation(name='water salinity'),
                                               value=31.3,
                                               unit=OntologyAnnotation(name='psu'))
        charac_fluorescence = Characteristic(category=OntologyAnnotation(name='fluorescence'), value='17.6')  # this value is a string as it is not expressed as a unit in the tab...
        charac_water_temperature = Characteristic(category=OntologyAnnotation(name='water temperature at 3 meter depth'),
                                                  value=9.7,
                                                  unit=OntologyAnnotation(name='degree celsius'))

        source1.characteristics.append(charac_organism)
        source1.characteristics.append(charac_location)
        source1.characteristics.append(charac_longitude)
        source1.characteristics.append(charac_lattitude)
        source1.characteristics.append(charac_chlorophyll_a_concentration)
        source1.characteristics.append(charac_peridinin_concentration)
        source1.characteristics.append(charac_fucoxanthin_concentration)
        source1.characteristics.append(charac_butfucoxanthin_concentration)
        source1.characteristics.append(charac_hexfucoxanthin_concentration)
        source1.characteristics.append(charac_alloxanthin_concentration)
        source1.characteristics.append(charac_zeaxanthin_concentration)
        source1.characteristics.append(charac_lutein_concentration)
        source1.characteristics.append(charac_chl_c3_concentration)
        source1.characteristics.append(charac_chl_c2_concentration)
        source1.characteristics.append(charac_prasinoxanthin_concentration)
        source1.characteristics.append(charac_neoxanthin_concentration)
        source1.characteristics.append(charac_violaxanthin_concentration)
        source1.characteristics.append(charac_diadinoxanthin_concentration)
        source1.characteristics.append(charac_diatoxanthin_concentration)
        source1.characteristics.append(charac_divinyl_chl_b_concentration)
        source1.characteristics.append(charac_chl_b_concentration)
        source1.characteristics.append(charac_divinyl_chl_a_concentration)
        source1.characteristics.append(charac_chl_a_concentration)
        source1.characteristics.append(charac_BB_carotene_concentration)
        source1.characteristics.append(charac_bacteria_count)
        source1.characteristics.append(charac_synechococcus_count)
        source1.characteristics.append(charac_small_picoeukaryotes_count)
        source1.characteristics.append(charac_large_picoeukaryotes_count)
        source1.characteristics.append(charac_nanoflagellates_count)
        source1.characteristics.append(charac_cryptophytes_count)
        source1.characteristics.append(charac_phosphate_concentration)
        source1.characteristics.append(charac_nitrate_concentration)
        source1.characteristics.append(charac_particulate_organic_nitrogen_concentration)
        source1.characteristics.append(charac_particulate_organic_carbon_concentration)
        source1.characteristics.append(charac_primary_production_depth)
        source1.characteristics.append(charac_water_salinity)
        source1.characteristics.append(charac_fluorescence)
        source1.characteristics.append(charac_water_temperature)

        # Declare a Process (an application of a Protocol). In this case, sample collection is applied.
        sample_collection1 = Process(executes_protocol=protocol_sample_collection)
        sample_collection1.parameter_values.append(
            ParameterValue(category=protocol_sample_collection.parameters[0], # refer back to the parameter we declared in the relevant protocol
                           value=0.22,
                           unit=OntologyAnnotation(name='micrometer')))

        # Create samples. Remember those factors we declared earlier? We can point to them now
        sample1 = Sample()
        factor_value_compound = FactorValue(factor_name=factor_compound,
                                            value=OntologyAnnotation(name='carbon dioxide',
                                                                     term_source=term_source_chebi,
                                                                     term_accession='http://purl.obolibrary.org/obo/CHEBI_16526'))
        factor_value_dose = FactorValue(factor_name=factor_dose, value=OntologyAnnotation(name='high'))
        factor_value_collection_time = FactorValue(factor_name=factor_collection_time,
                                                   value=OntologyAnnotation(name='may 13th, 2006'))
        sample1.factor_values.append(factor_value_compound)
        sample1.factor_values.append(factor_value_dose)
        sample1.factor_values.append(factor_value_collection_time)
        sample1.derives_from = source1  # put a pointer to what the sample derives from

        sample_collection1.inputs.append(source1)  # add source as our input to our process
        sample_collection1.outputs.append(sample1)  # add samples as our output to our process

        # This creates our first source -> sample collection process -> sample assay, to attach to our process_sequence.
        s.process_sequence.append(sample_collection1)

        # Now let's build an assays associated with our study
        assay_1 = Assay(
            filename='a_gilbert-assay-Gx.txt',
            measurement_type=OntologyAnnotation(name='metagenome sequencing', term_source=term_source_obi),
            technology_type=OntologyAnnotation(name='nucleotide sequencing', term_source=term_source_obi),
            technology_platform='454 Genome Sequencer FLX'
        )

        nucleic_acid_extraction = Process(executes_protocol=protocol_nucleic_acid_extraction)
        nucleic_acid_extraction.inputs.append(sample1)  # alternatively prev line could be include inputs=[sample1] as a parameter instead of appending afterwards
        genomic_dna_extraction = Process(executes_protocol=protocol_genomic_dna_extraction)
        nucleic_acid_extraction.next_process = genomic_dna_extraction
        genomic_dna_extraction.prev_process = nucleic_acid_extraction
        extract1 = Extract(name='GSM255770.e1', characteristics=[Characteristic(
            category=OntologyAnnotation(name='Material Type'),
            value=OntologyAnnotation(name='deoxyribonucleic acid', term_source=term_source_chebi, term_accession='http://purl.obolibrary.org/obo/CHEBI_16991')
        )])
        genomic_dna_extraction.outputs.append(extract1)

        library_construction = Process(executes_protocol=protocol_library_construction, inputs=[extract1])
        library_strategy = ParameterValue(category=protocol_library_construction.parameters[0], value=OntologyAnnotation(name='WGS'))  # We added protocol parameters to our protocols earlier. Refer to them directly
        library_selection = ParameterValue(category=protocol_library_construction.parameters[1], value=OntologyAnnotation(name='RANDOM'))  # We added protocol parameters to our protocols earlier. Refer to them directly
        library_layout = ParameterValue(category=protocol_library_construction.parameters[2], value=OntologyAnnotation(name='SINGLE'))  # We added protocol parameters to our protocols earlier. Refer to them directly
        library_construction.parameter_values.append(library_strategy)
        library_construction.parameter_values.append(library_selection)
        library_construction.parameter_values.append(library_layout)
        library_construction.prev_process = genomic_dna_extraction
        genomic_dna_extraction.next_process = library_construction

        pyrosequencing = Process(executes_protocol=protocol_pyrosequencing)
        library_construction.next_process = pyrosequencing
        pyrosequencing.prev_process = library_construction
        sequencing_instrument = ParameterValue(category=protocol_pyrosequencing.parameters[0], value=OntologyAnnotation(name='454 GS-FLX'))
        pyrosequencing.parameter_values.append(sequencing_instrument)
        pyrosequencing.additional_properties['Assay Name'] = 'assay1'
        raw_data_file = DataFile(filename='EWOEPZA01.sff')
        raw_data_file.comments.append(Comment(name='TraceDB', value='ftp://ftp.ncbi.nih.gov/pub/TraceDB/ShortRead/SRA000266/EWOEPZA01.sff'))
        pyrosequencing.outputs.append(raw_data_file)

        assay_1.process_sequence.append(nucleic_acid_extraction)
        assay_1.process_sequence.append(genomic_dna_extraction)
        assay_1.process_sequence.append(library_construction)
        assay_1.process_sequence.append(pyrosequencing)
        assay_1.build_graph()
        s.assays.append(assay_1)
        s.build_graph()
        i.studies.append(s)
