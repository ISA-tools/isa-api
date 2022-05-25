from unittest import TestCase

from isatools.model.material import Material, Extract, LabeledExtract
from isatools.model.characteristic import Characteristic
from isatools.model.process_sequence import ProcessSequenceNode


class TestMaterial(TestCase):

    def setUp(self):
        self.material = Material()

    def test_init(self):
        self.assertTrue(isinstance(self.material, (Material, ProcessSequenceNode)))
        characteristic = Characteristic()
        material = Material(name='test_name',
                            id_='test_id',
                            type_='test_type',
                            characteristics=[characteristic],
                            comments=[])
        self.assertEqual(material.name, 'test_name')
        self.assertEqual(material.id, 'test_id')
        self.assertEqual(material.type, 'test_type')
        self.assertEqual(material.characteristics, [characteristic])
        self.assertEqual(material.comments, [])

    def test_name(self):
        self.assertEqual(self.material.name, '')
        self.material.name = 'test_name'
        self.assertEqual(self.material.name, 'test_name')

        with self.assertRaises(AttributeError) as context:
            self.material.name = 1
        self.assertEqual(str(context.exception), "Material.name must be a str or None; got 1:<class 'int'>")

    def test_type(self):
        self.assertEqual(self.material.type, '')
        self.material.type = 'Extract Name'
        self.assertEqual(self.material.type, 'Extract Name')

        expecter_error = 'Material.type must be a str in ("Extract Name", "Labeled Extract Name") or None; ' \
                         'got just a name:<class \'str\'>'
        with self.assertRaises(AttributeError) as context:
            self.material.type = "just a name"
        self.assertEqual(str(context.exception), expecter_error)

    def test_characteristics(self):
        self.assertEqual(self.material.characteristics, [])
        characteristic = Characteristic()
        self.material.characteristics = [characteristic]
        self.assertEqual(self.material.characteristics, [characteristic])
        self.material.characteristics = [12]
        self.assertTrue(self.material.characteristics, [characteristic])

        with self.assertRaises(AttributeError) as context:
            self.material.characteristics = 1
        self.assertEqual(str(context.exception),
                         "Material.characteristics must be iterable containing Characteristics")


class TestExtract(TestCase):

    def setUp(self):
        self.extract = Extract()

    def test_init(self):
        self.assertTrue(isinstance(self.extract, (Extract, Material, ProcessSequenceNode)))
        self.assertTrue(self.extract.type == "Extract Name")

    def test_repr(self):
        expected_str = "isatools.model.Extract(name='', type='Extract Name', characteristics=[], comments=[])"
        self.assertTrue(repr(self.extract) == expected_str)
        self.assertEqual(hash(self.extract), hash(expected_str))

    def test_str(self):
        expected_str = ("Extract(\n\t"
                        "name=\n\t"
                        "type=Extract Name\n\t"
                        "characteristics=0 Characteristic objects\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.extract) == expected_str)

    def test_equalities(self):
        first_extract = Extract(name='test_name', id_='id1')
        second_extract = Extract(name='test_name', id_='id2')
        self.assertTrue(first_extract == second_extract)
        self.assertTrue(first_extract != self.extract)


class TestLabeledExtract(TestCase):

    def setUp(self):
        self.labeled_extract = LabeledExtract()

    def test_init(self):
        self.assertTrue(isinstance(self.labeled_extract, (LabeledExtract, Extract, Material, ProcessSequenceNode)))
        self.assertTrue(self.labeled_extract.type == "Labeled Extract Name")

    def test_repr(self):
        expected_str = ("isatools.model.LabeledExtract(name='', type='Labeled Extract Name', "
                        "characteristics=[], comments=[])")
        self.assertTrue(repr(self.labeled_extract) == expected_str)
        self.assertEqual(hash(self.labeled_extract), hash(expected_str))

    def test_str(self):
        expected_str = ("LabeledExtract(\n\t"
                        "name=\n\t"
                        "type=Labeled Extract Name\n\t"
                        "characteristics=0 Characteristic objects\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.labeled_extract) == expected_str)

    def test_equalities(self):
        first_labeled_extract = LabeledExtract(name='test_name', id_='id1')
        second_labeled_extract = LabeledExtract(name='test_name', id_='id2')
        self.assertTrue(first_labeled_extract == second_labeled_extract)
        self.assertTrue(first_labeled_extract != self.labeled_extract)
