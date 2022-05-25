from unittest import TestCase

from isatools.model.material import Material


class TestMaterial(TestCase):

    def test_material_init(self):
        material = Material()
        self.assertEqual(material.name, '')
        self.assertEqual(material.id, '')
        self.assertEqual(material.type, '')
        self.assertEqual(material.characteristics, [])
        self.assertEqual(material.comments, [])

        material = Material(name='test_name', id_='test_id', type_='test_type', characteristics=[], comments=[])
        self.assertEqual(material.name, 'test_name')
        self.assertEqual(material.id, 'test_id')
        self.assertEqual(material.type, 'test_type')
        self.assertEqual(material.characteristics, [])
        self.assertEqual(material.comments, [])

    def test_name(self):
        pass
