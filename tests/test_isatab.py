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
        return s.graph

    def test_isatab_writer(self):
        isatab.dump(self.i, './data/tmp/')


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

        # assay_graph = nx.DiGraph()
        # assay_graph.add_edge(sample1, rna_extraction)  # rna_extraction is Processing Event
        # assay_graph.add_edge(rna_extraction, extract)
        # assay_graph.add_edge(extract, labeling)  # labeling is Processing Event
        # assay_graph.add_edge(labeling, labeled_extract)  # labeled_extract property includes Label
        # assay_graph.add_edge(labeled_extract, hybridization)  # hybridization is Processing Event
        # assay_graph.add_edge(hybridization, hybridization_assay)  # hybridization_assay property includes Array Design REF
        # assay_graph.add_edge(hybridization_assay, data_collection)  # data_collection is Processing Event
        # assay_graph.add_edge(data_collection, scan)  # scan properties of scan are output files
        # assay_graph.add_edge(scan, data_normalization)  # data_normalization is Processing Event
        # assay_graph.add_edge(data_normalization, normalization)  # normalization has a Derived Array Data File
        # assay_graph.add_edge(normalization, anova)  # anova is Processing Event
        # assay_graph.add_edge(anova, data_transformation)  # data_transformation has a Derived Array Data Matrix File

    def test_isatab_writer(self):
        isatab.dump(self.i, './data/tmp/')


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
        return s.graph

    def test_isatab_writer(self):
        isatab.dump(self.i, './data/tmp/')

