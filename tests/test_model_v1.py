import unittest


class TestSimpleExamples(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_construct_investigation_object(self):
        try:
            from isatools.model import Investigation
        except ImportError:
            self.fail("Could not import Investigation class")
        I = Investigation()
        self.assertIsInstance(I.identifier, str)
        self.assertIsInstance(I.title, str)
        self.assertIsInstance(I.description, str)
        self.assertIsInstance(I.submission_date, str)  # todo: check if ISO8601
        self.assertIsInstance(I.public_release_date, str)  # todo: check if ISO8601

    def test_batch_create_materials(self):
        try:
            from isatools.model import Source
        except ImportError:
            self.fail("Could not import Source class")
        source = Source(name='source_material')

        try:
            from isatools.model import Sample
        except ImportError:
            self.fail("Could not import Sample class")
        prototype_sample = Sample(name='sample_material', derives_from=source)

        try:
            from isatools.model import batch_create_materials
        except ImportError:
            self.fail("Could not import batch_create_materials function")

        batch = batch_create_materials(prototype_sample, n=3)
        self.assertEqual(len(batch), 3)
        for material in batch:
            self.assertIsInstance(material, Sample)
            self.assertEqual(material.derives_from, source)
        self.assertSetEqual(set([m.name for m in batch]), {'sample_material-0', 'sample_material-1',
                                                           'sample_material-2'})