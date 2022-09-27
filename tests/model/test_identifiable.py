from unittest import TestCase
from unittest.mock import patch

from isatools.model.identifiable import Identifiable


class TestIdentifiable(TestCase):

    def setUp(self):
        self.identifiable = Identifiable(id_='#identifiable/test_id')

    @patch('isatools.model.identifiable.uuid4', return_value='test_uuid')
    def test_id(self, mock_uuid4):
        self.assertTrue(self.identifiable.id == '#identifiable/test_id')
        self.identifiable.id = 'test_id_2'
        self.assertTrue(self.identifiable.id == 'test_id_2')
        self.identifiable.id = None
        self.assertEqual(self.identifiable.id, "#identifiable/" + mock_uuid4.return_value)

        with self.assertRaises(AttributeError) as context:
            self.identifiable.id = 1
        self.assertTrue("Identifiable.id must be a str or None; got 1:<class 'int'>" in str(context.exception))