from unittest import TestCase
import os
import shutil


class JsonToTabTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_source_split(self):
        pass

    def test_sample_pool(self):
        pass

    def test_repeated_measure(self):
        pass

    def test_data_transformation(self):
        pass

    def test_charac_param_factor(self):
        pass