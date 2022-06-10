from unittest import TestCase

from isatools.model.loader_indexes import loader_states as indexes, new_store
from isatools.model.sample import Sample


class TestLoaderIndexes(TestCase):

    def test_methods(self):
        attrs = [
            'characteristic_categories',
            'get_characteristic_category',
            'add_characteristic_category',

            'factors',
            'get_factor',
            'add_factor',

            "parameters",
            'get_parameter',
            'add_parameter',

            "protocols",
            'get_protocol',
            'add_protocol',

            "units",
            'get_unit',
            'add_unit',

            "samples",
            'get_sample',
            'add_sample',

            "sources",
            'get_source',
            'add_source'
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
                           "term_sources: {}")
        self.assertEqual(expected_string, str(indexes))
