from unittest import TestCase
from re import sub, compile

from isatools.model.datafile import *
from isatools.model.sample import Sample


class TestDataFile(TestCase):

    def setUp(self):
        self.datafile = DataFile(id_='id1')

    def test_init(self):
        self.assertTrue(isinstance(self.datafile, DataFile))
        self.assertEqual(self.datafile.id, 'id1')
        self.assertEqual(self.datafile.comments, [])

        sample = Sample()
        datafile = DataFile(filename='test_filename', generated_from=[sample])
        self.assertEqual(datafile.filename, 'test_filename')
        self.assertEqual(datafile.generated_from, [sample])

    def test_filename(self):
        self.assertEqual(self.datafile.filename, '')
        self.datafile.filename = 'test_filename'
        self.assertEqual(self.datafile.filename, 'test_filename')

        with self.assertRaises(AttributeError) as context:
            self.datafile.filename = 1
        self.assertEqual(str(context.exception), "DataFile.name must be a str or None; got 1:<class 'int'>")

    def test_label(self):
        self.assertEqual(self.datafile.label, '')
        self.datafile.label = 'test_label'
        self.assertEqual(self.datafile.label, 'test_label')

        with self.assertRaises(AttributeError) as context:
            self.datafile.label = 1
        self.assertEqual(str(context.exception), "DataFile.label must be a str or None; got 1:<class 'int'>")

    def test_generated_from(self):
        self.assertEqual(self.datafile.generated_from, [])
        sample = Sample()
        self.datafile.generated_from = [sample]
        self.assertEqual(self.datafile.generated_from, [sample])

        with self.assertRaises(AttributeError) as context:
            self.datafile.generated_from = 1
        self.assertEqual(str(context.exception), "DataFile.generated_from must be iterable containing Samples")

    def test_repr(self):
        expected_str = "isatools.model.DataFile(filename='', label='', generated_from=[], comments=[])"
        self.assertEqual(repr(self.datafile), expected_str)
        self.assertEqual(hash(self.datafile), hash(expected_str))

    def test_str(self):
        expected_str = ("DataFile(\n\t"
                        "filename=\n\t"
                        "label=\n\t"
                        "generated_from=0 Sample objects\n\t"
                        "comments=0 Comment objects\n)")
        self.assertEqual(str(self.datafile), expected_str)

    def test_equalities(self):
        first_datafile = DataFile(filename='test_name', id_="id1")
        second_datafile = DataFile(filename='test_name', id_="id2")
        self.assertTrue(first_datafile == second_datafile)
        self.assertTrue(self.datafile != first_datafile)


class TestSubDataFile(TestCase):

    def setUp(self):
        self.types = {
            "RawDataFile": RawDataFile,
            "DerivedDataFile": DerivedDataFile,
            "RawSpectralDataFile": RawSpectralDataFile,
            "DerivedArrayDataFile": DerivedArrayDataFile,
            "ArrayDataFile": ArrayDataFile,
            "DerivedSpectralDataFile": DerivedSpectralDataFile,
            "ProteinAssignmentFile": ProteinAssignmentFile,
            "PeptideAssignmentFile": PeptideAssignmentFile,
            "DerivedArrayDataMatrixFile": DerivedArrayDataMatrixFile,
            "PostTranslationalModificationAssignmentFile": PostTranslationalModificationAssignmentFile,
            "AcquisitionParameterDataFile": AcquisitionParameterDataFile,
            "FreeInductionDecayDataFile": FreeInductionDecayDataFile,
        }
        self.classes = {}
        for filetype in self.types:
            filename = 'file_' + filetype.lower()
            id_ = 'id_' + filetype.lower()
            item = self.types[filetype](filename=filename, id_=id_)
            self.classes[filetype] = item

    def test_repr(self):
        for filetype in self.types:
            datafile = self.classes[filetype]
            name = sub(r'(?<!^)(?=[A-Z])', ' ', filetype)
            filename = 'file_' + filetype.lower()
            self.assertEqual(datafile.label, name)

            expected_repr = "isatools.model.{0}(filename='{1}', generated_from=[], comments=[])"\
                .format(filetype, filename)
            self.assertEqual(repr(datafile), expected_repr)
            self.assertEqual(hash(datafile), hash(expected_repr))

    def test_str(self):
        for filetype in self.types:
            datafile = self.classes[filetype]
            name = sub(r'(?<!^)(?=[A-Z])', ' ', filetype)
            filename = 'file_' + filetype.lower()
            self.assertEqual(datafile.label, name)

            expected_str = """{0}(
    filename={1}
    generated_from=0 Sample objects
    comments=0 Comment objects
)""".format(filetype, filename)
            self.assertEqual(str(datafile), expected_str)

    def test_equalities(self):
        for filetype in self.types:
            first_datafile = self.types[filetype](filename='test_name', id_="id1")
            second_datafile = self.types[filetype](filename='test_name', id_="id2")
            self.assertTrue(first_datafile == second_datafile)
            self.assertTrue(self.classes[filetype] != first_datafile)

    def test_to_dict(self):
        for filetype in self.types:
            type_ = sub(r'(?<!^)(?=[A-Z])', ' ', filetype)
            datafile = self.classes[filetype]
            expected_dict = {
                '@id': 'id_' + filetype.lower(),
                'name': 'file_' + filetype.lower(),
                'type': type_,
                'comments': []
            }
            self.assertEqual(datafile.to_dict(), expected_dict)
