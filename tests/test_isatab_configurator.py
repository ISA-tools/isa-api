from unittest import TestCase
import os


class ISATabConfiguratorTest(TestCase):

    def setUp(self):
        """set up directories etc"""
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._config_dir = os.path.join(self._dir, "Configurations/isaconfig-default_v2015-07-02")

    def tearDown(self):
        pass

    def test_parse(self):
        from isatools.io import isatab_configurator as configurator
        config_obj = configurator.parse(os.path.join(self._config_dir, 'genome_seq.xml'), True)  # Silent output
        self.assertEqual(len(config_obj.get_isatab_configuration()), 1)
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_table_name(), 'genome_seq')
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_isatab_assay_type(), 'generic_assay')
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_isatab_conversion_target(), 'sra')
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_measurement().get_term_label(),
                         'genome sequencing')
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_technology().get_term_label(),
                         'nucleotide sequencing')
        self.assertEqual(len(config_obj.get_isatab_configuration()[0].get_field()), 15)
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_field()[0].get_header(), 'Sample Name')
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_field()[0].get_data_type(), 'String')
        self.assertFalse(config_obj.get_isatab_configuration()[0].get_field()[0].get_is_file_field())
        self.assertFalse(config_obj.get_isatab_configuration()[0].get_field()[0].get_is_multiple_value())
        self.assertTrue(config_obj.get_isatab_configuration()[0].get_field()[0].get_is_required())
        self.assertFalse(config_obj.get_isatab_configuration()[0].get_field()[0].get_is_hidden())
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_field()[0].get_description(), 'sample name')
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_field()[0].get_default_value(), '')
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_field()[0].get_generated_value_template(),
                         '[INSTITUTION].Group-[GROUP_NO].Subject-[SUBJECT_NO].[SAMPLE_EXTRACT]')
        self.assertEqual(len(config_obj.get_isatab_configuration()[0].get_protocol_field()), 4)
        self.assertEqual(config_obj.get_isatab_configuration()[0].get_protocol_field()[0].get_protocol_type(),
                         'nucleic acid extraction')

    def test_load_configs(self):
        from isatools.io import isatab_configurator as configurator
        config_dict = configurator.load(self._config_dir)
        self.assertEqual(len(config_dict), 30)
        self.assertEqual(config_dict[('metagenome sequencing', 'nucleotide sequencing')].get_isatab_configuration()[0]
                         .get_table_name(),'metagenome_seq')
