from unittest import TestCase
from isatools.model.v1 import *
from isatools import isatab

#  Manually testing object model to write to isatab, study file-out only to check if model and writer function correctly


class IsatabSplittingTest(TestCase):

    def setUp(self):
        self.i = Investigation()
        uberon = OntologySourceReference(name='UBERON')
        ncbitaxon = OntologySourceReference(name='NCBITAXON')
        self.i.ontology_source_references.append(uberon)
        self.i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_split.txt')
        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(name='sample collection')
        )
        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = \
            CharacteristicCategory(characteristic_type=OntologyAnnotation(name='reference descriptor'))
        material_type_category = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='material type'))
        organism_category = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='organism'))

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='organism part'))
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample2 = Sample(name='sample2')
        sample2.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='heart',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000948',
        )))

        sample3 = Sample(name='sample3')
        sample3.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample4 = Sample(name='sample4')
        sample4.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample_collection_process = ProcessingEvent(executes_protocol=sample_collection_protocol)

        import networkx as nx
        graph = nx.DiGraph()
        graph.add_edge(source1, sample_collection_process)
        graph.add_edges_from([(sample_collection_process, sample1),
                              (sample_collection_process, sample2),
                              (sample_collection_process, sample3),
                              (sample_collection_process, sample4)])
        s.graph = graph
        self.i.studies.append(s)
        # return s.graph

    def test_isatab_writer(self):
        # isatab.dump(self.i, './data/tmp/')
        pass


class IsatabPoolingTest(TestCase):

    def setUp(self):
        #  manually create and populate some minimal ISA objects
        self.i = Investigation()
        uberon = OntologySourceReference(name='UBERON')
        ncbitaxon = OntologySourceReference(name='NCBITAXON')
        self.i.ontology_source_references.append(uberon)
        self.i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_pool.txt')
        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(name='sample collection')
        )
        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = \
            CharacteristicCategory(characteristic_type=OntologyAnnotation(name='reference descriptor'))
        material_type_category = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='material type'))
        organism_category = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='organism'))

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source2 = Source(name='source2')
        source2.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source3 = Source(name='source3')
        source3.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source4 = Source(name='source4')
        source4.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='organism part'))
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample_collection_process = ProcessingEvent(executes_protocol=sample_collection_protocol)

        import networkx as nx
        study_graph = nx.DiGraph()
        study_graph.add_edges_from([(source1, sample_collection_process),
                                   (source2, sample_collection_process),
                                   (source3, sample_collection_process),
                                   (source4, sample_collection_process)])
        study_graph.add_edge(sample_collection_process, sample1)

        s.graph = study_graph
        self.i.studies.append(s)

        rna_extraction_protocol = Protocol(name='rna extraction', protocol_type=OntologyAnnotation(name='rna extraction'))
        labeling_protocol = Protocol(name='labeling', protocol_type=OntologyAnnotation(name='labeling'))
        hybridization_protocol = Protocol(name='nucleic acid hybridization', protocol_type=OntologyAnnotation(name='nucleic acid hybridization'))
        data_collection_protocol = Protocol(name='data collection', protocol_type=OntologyAnnotation(name='data collection'))
        data_normalization_protocol = Protocol(name='data normalization', protocol_type=OntologyAnnotation(name='data normalization'))
        anova_protocol = Protocol(name='anova', protocol_type=OntologyAnnotation(name='anova'))

        rna_extraction_process = Process(executes_protocol=rna_extraction_protocol)
        extract = Extract(name='extract1')  # Material
        labeling_process = Process(executes_protocol=labeling_protocol)
        labeled_extract = LabeledExtract(name='extract1.le1', label=OntologyAnnotation(name='biotin'))  # Material
        hybridization_process = Process(executes_protocol=hybridization_protocol)
        hybridization_process.additional_properties['Hybridization Assay Name'] = 'hyb1'
        hybridization_process.additional_properties['Array Design REF'] = 'HG_U133_2.0'
        scan_process = Process(executes_protocol=data_collection_protocol)
        scan_process.additional_properties['Scan Name'] = 'hyb1.scan1'
        scan_data = Data(data_files=[DataFile(filename='1.dat', label='Image File'),
                                     DataFile(filename='1.cel', label='Array Data File')])  # Data
        data_normalization_process = Process(executes_protocol=data_normalization_protocol)
        data_normalization_process.additional_properties['Normalization Name'] = 'N1'
        normalized_data = Data(data_files=[DataFile(filename='N1.txt', label="Derived Array Data File")])  # Data
        anova_process = Process(executes_protocol=anova_protocol)
        anova_process.additional_properties['Data Transformation Name'] = 'DA1'
        transformed_data = Data(data_files=[DataFile(filename='DA1.txt', label="Derived Array Data Matrix File")])  # Data

        assay_graph = nx.DiGraph()
        assay_graph.add_edge(sample1, rna_extraction_process)  # rna_extraction is Processing Event
        assay_graph.add_edge(rna_extraction_process, extract)
        assay_graph.add_edge(extract, labeling_process)  # labeling is Processing Event
        assay_graph.add_edge(labeling_process, labeled_extract)  # labeled_extract property includes Label
        assay_graph.add_edge(labeled_extract, hybridization_process)  # hybridization is Processing Event
        assay_graph.add_edge(hybridization_process, scan_process)
        assay_graph.add_edge(scan_process, scan_data)  # data_collection is Processing Event
        assay_graph.add_edge(scan_data, data_normalization_process)  # scan properties of scan are output files
        assay_graph.add_edge(data_normalization_process, normalized_data)  # data_normalization is Processing Event
        assay_graph.add_edge(normalized_data, anova_process)  # normalization has a Derived Array Data File
        assay_graph.add_edge(anova_process, transformed_data)  # anova is Processing Event

        assay = Assay(filename='a_pool.txt')
        assay.graph = assay_graph

        s.assays.append(assay)
        return assay_graph

    def test_isatab_writer(self):
        isatab.dump(self.i, './data/tmp/')
        pass


class IsatabRepeatedMeasureTest(TestCase):

    def setUp(self):
        #  manually create and populate some minimal ISA objects
        self.i = Investigation()
        uberon = OntologySourceReference(name='UBERON')
        ncbitaxon = OntologySourceReference(name='NCBITAXON')
        self.i.ontology_source_references.append(uberon)
        self.i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_repeat.txt')

        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(name='sample collection')
        )

        intervention_A_protocol = Protocol(
            name='intervention A',
            protocol_type=OntologyAnnotation(name='intervention A')
        )
        intervention_B_protocol = Protocol(
            name='intervention B',
            protocol_type=OntologyAnnotation(name='intervention B')
        )
        intervention_C_protocol = Protocol(
            name='intervention C',
            protocol_type=OntologyAnnotation(name='intervention C')
        )
        intervention_D_protocol = Protocol(
            name='intervention D',
            protocol_type=OntologyAnnotation(name='intervention D')
        )

        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = \
            CharacteristicCategory(characteristic_type=OntologyAnnotation(name='reference descriptor'))
        material_type_category = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='material type'))
        organism_category = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='organism'))

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source2 = Source(name='source2')
        source2.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = CharacteristicCategory(characteristic_type=OntologyAnnotation(name='organism part'))
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample2 = Sample(name='sample2')
        sample2.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample3 = Sample(name='sample3')
        sample3.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample4 = Sample(name='sample4')
        sample4.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample5 = Sample(name='sample5')
        sample5.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample6 = Sample(name='sample6')
        sample6.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample_collection_1_process = ProcessingEvent(executes_protocol=sample_collection_protocol, date_='01/01/2016')
        sample_collection_2_process = ProcessingEvent(executes_protocol=sample_collection_protocol, date_='08/01/2016')
        sample_collection_3_process = ProcessingEvent(executes_protocol=sample_collection_protocol, date_='15/01/2016')
        sample_collection_4_process = ProcessingEvent(executes_protocol=sample_collection_protocol, date_='22/01/2016')

        intervention_A1_process = ProcessingEvent(executes_protocol=intervention_A_protocol, date_='01/01/2016')
        intervention_A2_process = ProcessingEvent(executes_protocol=intervention_A_protocol, date_='22/01/2016')
        intervention_B1_process = ProcessingEvent(executes_protocol=intervention_B_protocol, date_='01/01/2016')
        intervention_B2_process = ProcessingEvent(executes_protocol=intervention_B_protocol, date_='08/01/2016')
        intervention_C_process = ProcessingEvent(executes_protocol=intervention_C_protocol, date_='15/01/2016')
        intervention_D1_process = ProcessingEvent(executes_protocol=intervention_D_protocol, date_='08/01/2016')
        intervention_D2_process = ProcessingEvent(executes_protocol=intervention_D_protocol, date_='22/01/2016')

        import networkx as nx
        graph = nx.DiGraph()

        graph.add_edges_from([(source1, intervention_A1_process),
                              (source1, intervention_B2_process),
                              (source1, intervention_C_process),
                              (source1, intervention_D2_process)])
        graph.add_edges_from([(source2, intervention_B1_process),
                              (source2, intervention_D1_process),
                              (source2, intervention_C_process),
                              (source2, intervention_A2_process)])
        # no intermediate materials as repeated measures, so ProcessingEvent->ProcessingEvent
        graph.add_edges_from([(intervention_A1_process, sample_collection_1_process),
                              (intervention_B2_process, sample_collection_2_process),
                              (intervention_C_process, sample_collection_3_process),
                              (intervention_D2_process, sample_collection_4_process),
                              (intervention_B1_process, sample_collection_1_process),
                              (intervention_D1_process, sample_collection_2_process),
                              (intervention_C_process, sample_collection_3_process),
                              (intervention_A2_process, sample_collection_4_process)])
        graph.add_edges_from([(sample_collection_1_process, sample1),
                              (sample_collection_2_process, sample2),
                              (sample_collection_3_process, sample3),
                              (sample_collection_4_process, sample4),
                              (sample_collection_4_process, sample5),
                              (sample_collection_1_process, sample6),
                              (sample_collection_2_process, sample6),
                              (sample_collection_3_process, sample6),
                              (sample_collection_4_process, sample6)])
        s.graph = graph
        self.i.studies.append(s)
        # return s.graph

    def test_isatab_writer(self):
        # isatab.dump(self.i, './data/tmp/')
        pass

