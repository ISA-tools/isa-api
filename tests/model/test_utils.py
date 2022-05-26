from unittest import TestCase

from isatools.model.datafile import DataFile
from isatools.model.sample import Sample
from isatools.model.material import Material, Extract, LabeledExtract
from isatools.model.process import Process
from isatools.model.source import Source
from isatools.model.utils import (
    _build_assay_graph,
    find, plink,
    batch_create_materials,
    batch_create_assays,
    _deep_copy
)


class TestUtils(TestCase):

    def test_empty_process_sequence(self):
        graph = _build_assay_graph()
        self.assertTrue(len(graph.indexes.keys()) == 0)

    def test_process_sequence(self):
        first_process = Process(name='First process', inputs=[Sample(name='s1')], outputs=[Material(name='m1')])
        second_process = Process(name='Second process', inputs=[Material(name='m1')])
        third_process = Process(name='Third process', outputs=[DataFile(filename='d1.txt')])
        plink(first_process, second_process)
        plink(second_process, third_process)
        process_sequence = [first_process, second_process, third_process]
        graph = _build_assay_graph(process_sequence)
        self.assertEqual(len(graph.nodes), 6)
        self.assertTrue(len(graph.indexes.keys()) == 6)
        self.assertTrue(len(graph.edges()) == 4)

    def test_find(self):
        self.assertEqual(find(lambda x: x == 1, [1, 2, 3]), (1, 0))
        self.assertEqual(find(lambda x: x == 1, [5, 6, 7]), (None, 3))

    def test_plink(self):
        first_process = Process()
        second_process = Process()
        plink(first_process, second_process)
        self.assertEqual(first_process.next_process, second_process)
        self.assertEqual(second_process.prev_process, first_process)

    def test__deep_copy(self):
        process = Process()
        self.assertTrue(process == _deep_copy(process))

        extract = Extract()
        self.assertTrue(extract == _deep_copy(extract))

        material = Material()
        self.assertNotEqual(material, _deep_copy(material))

    def test_batch_create_materials(self):
        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material', derives_from=[source])
        batch = batch_create_materials(prototype_sample, n=2)
        for sample in batch:
            self.assertTrue(isinstance(sample, Sample))
            self.assertEqual(sample.derives_from, [source])

    def test_batch_create_assays(self):
        sample = Sample(name='sample', derives_from=[Source(name='source')])
        data_acquisition = Process(name='data acquisition')
        material = Material(name='material')
        process = Process(name='process name')
        labeled_extract = LabeledExtract(name='lextract')
        batch = batch_create_assays(sample, data_acquisition, material, process, labeled_extract, n=2)
        self.assertEqual(len(batch), 4)
        self.assertEqual(batch[0].name, 'data acquisition-0')
        self.assertEqual(batch[1].name, 'process name-0')
        self.assertEqual(batch[2].name, 'data acquisition-1')
        self.assertEqual(batch[3].name, 'process name-1')
        for item in batch:
            self.assertIsInstance(item, Process)

        sample1 = Sample(name='sample')
        sample2 = Sample(name='sample')
        process = Process(name='data acquisition')
        material1 = Material(name='material')
        material2 = Material(name='material')
        batch = batch_create_assays([sample1, sample2], process, [material1, material2], n=2)
        self.assertEqual(batch[0].name, 'data acquisition-0')
        self.assertEqual(batch[1].name, 'data acquisition-1')
        self.assertEqual(len(batch), 2)
        for item in batch:
            self.assertIsInstance(item, Process)

        process = Process(name='data acquisition')
        batch = batch_create_assays([process], [material1, material2], n=2)
        self.assertEqual(len(batch), 1)

        source = Source()
        first_batch = batch_create_assays([sample1], [process], [source], n=2)
        second_batch = batch_create_assays([process], [sample1], [source], n=2)
        third_batch = batch_create_assays([process], [source], [sample1], n=2)
        self.assertEqual(first_batch, second_batch)
        self.assertFalse(first_batch == third_batch)

        first_batch = batch_create_assays(sample1, [process], source, n=2)
        self.assertFalse(first_batch == third_batch)
        self.assertFalse(first_batch == second_batch)

