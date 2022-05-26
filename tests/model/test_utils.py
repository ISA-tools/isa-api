from unittest import TestCase

from isatools.model.datafile import DataFile
from isatools.model.sample import Sample
from isatools.model.material import Material
from isatools.model.process import Process
from isatools.model.utils import _build_assay_graph, find, plink


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
