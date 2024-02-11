from unittest import TestCase
from isatools.model.context import ContextPath


class TestContextPath(TestCase):

    def setUp(self) -> None:
        self.context = ContextPath()

    def test_attributes(self):
        self.assertEqual(self.context.context, 'obo')
        self.context.context = 'sdo'
        self.assertEqual(self.context.context, 'sdo')

        with self.assertRaises(ValueError) as context:
            self.context.context = 'test'
        self.assertEqual(str(context.exception),
                         "Context name must be one in ['obo', 'sdo', 'wd', 'sio'] but got test")

    def test_repr(self):
        self.context.context = 'sdo'
        self.assertEqual(repr(self.context), "sdo")
        self.assertEqual(str(self.context), "sdo")
