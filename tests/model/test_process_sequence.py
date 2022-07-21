from unittest import TestCase

from isatools.model import ProcessSequenceNode


class TestProcessSequenceNode(TestCase):

    def test_(self):
        ProcessSequenceNode.sequence_identifier = 0
        self.assertTrue(ProcessSequenceNode.sequence_identifier == 0)
        process_sequence_node = ProcessSequenceNode()
        self.assertTrue(process_sequence_node.sequence_identifier == 0)
        self.assertTrue(ProcessSequenceNode.sequence_identifier == 1)

        process_sequence_node.assign_identifier()
        self.assertTrue(process_sequence_node.sequence_identifier == 1)
        self.assertTrue(ProcessSequenceNode.sequence_identifier == 2)
