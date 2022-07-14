from unittest import TestCase

from isatools.model.loader_indexes import loader_states as indexes, new_store
from isatools.model.sample import Sample
from isatools.model.process import Process


class TestLoaderIndexes(TestCase):

    def test_methods(self):
        attrs = [
            'characteristic_categories',
            'get_characteristic_category',
            'add_characteristic_category',
            'reset_characteristic_category',

            'factors',
            'get_factor',
            'add_factor',
            'reset_factor',

            "parameters",
            'get_parameter',
            'add_parameter',
            'reset_parameter',

            "protocols",
            'get_protocol',
            'add_protocol',
            'reset_protocol',

            "units",
            'get_unit',
            'add_unit',
            'reset_unit',

            "samples",
            'get_sample',
            'add_sample',
            'reset_sample',

            "sources",
            'get_source',
            'add_source',
            'reset_source',

            "processes",
            'get_process',
            'add_process',
            'reset_process',

            "data_files",
            'get_data_file',
            'add_data_file',
            'reset_data_file',

            'term_sources',
            'get_term_source',
            'add_term_source'
        ]
        for attr in attrs:
            self.assertTrue(hasattr(indexes, attr))

        sample = Sample(id_='mysample')
        indexes.add_sample(sample)
        self.assertEqual(sample, indexes.get_sample('mysample'))

        another_store = new_store()
        self.assertNotEqual(indexes.samples, another_store.samples)
        indexes.reset_store()
        self.assertEqual(indexes.samples, another_store.samples)

        expected_string = ("LoaderStore:\n\t"
                           "characteristic_categories: {},\n\t"
                           "factors: {},\n\t"
                           "parameters: {},\n\t"
                           "protocols: {},\n\t"
                           "units: {},\n\t"
                           "samples: {},\n\t"
                           "sources: {},\n\t"
                           "processes: {},\n\t"
                           "term_sources: {},\n\t"
                           "data_files: {},\n\t"
                           "other_materials: {}")
        self.assertEqual(expected_string, str(indexes))

        process = Process(id_='myprocess')
        indexes.add_process(process)
        self.assertEqual(process, indexes.get_process('myprocess'))
        indexes.reset_process()
        self.assertEqual(indexes.processes, {})
