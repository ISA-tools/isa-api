from abc import ABCMeta


class ProcessSequenceNode(metaclass=ABCMeta):
    sequence_identifier = 0

    def __init__(self):
        self.sequence_identifier = ProcessSequenceNode.sequence_identifier
        ProcessSequenceNode.sequence_identifier += 1

    def assign_identifier(self):
        # ProcessSequenceNode.sequence_identifier += 1
        self.sequence_identifier = ProcessSequenceNode.sequence_identifier
        ProcessSequenceNode.sequence_identifier += 1
