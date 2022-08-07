import unittest
from os import path

from cProfile import runctx
from pstats import SortKey, Stats

from isatools.tests import utils
from isatools.isatab.validate.core import validate as o_validate
from isatools.isatab.validate.rules.core import Rule, Rules, validate
from isatools.isatab.validate.rules.defaults import INVESTIGATION_RULES_MAPPING
from isatools.isatab.validate.store import validator as message_handler


class TestValidators(unittest.TestCase):

    def setUp(self) -> None:
        message_handler.reset_store()
        self.default_conf = utils.DEFAULT2015_XML_CONFIGS_DATA_DIR

    def test_b_ii_s_3(self):
        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'tab', 'BII-S-3')
        with open(path.join(data_path, 'i_gilbert.txt'), 'r') as data_file:
            validate(investigation_fp=data_file, conf_dir=self.default_conf)

    def test_bii_i_1(self):
        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'tab', 'BII-I-1')
        with open(path.join(data_path, 'i_investigation.txt'), 'r') as data_file:
            validate(investigation_fp=data_file, conf_dir=self.default_conf)

    def test_bii_s_7(self):
        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'tab', 'BII-S-7')
        with open(path.join(data_path, 'i_matteo.txt'), 'r') as data_file:
            validate(investigation_fp=data_file, conf_dir=self.default_conf)

    def test_print_rule(self):
        raw_rule = INVESTIGATION_RULES_MAPPING[0]
        rule = Rule(**raw_rule)
        expected_string = "rule=check_table_files_read, params=['investigation_df', 'dir_context'], identifier=0006"
        self.assertEqual(str(rule), expected_string)

    def test_rules_error(self):
        rules_to_test = ('6006', )
        rules = Rules(rules_to_run=INVESTIGATION_RULES_MAPPING, available_rules=rules_to_test)
        with self.assertRaises(ValueError) as context:
            rules.get_rule('6006')
        self.assertEqual(str(context.exception), 'Rule not found: 6006')

    @unittest.skip('Deprecation test')
    def test_old_vs_new(self):
        self.maxDiff = None
        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'tab', 'BII-I-1')
        with open(path.join(data_path, 'i_investigation.txt'), 'r') as data_file:
            o_report = {**o_validate(data_file)}
        with open(path.join(data_path, 'i_investigation.txt'), 'r') as data_file:
            n_report = validate(data_file)
        self.assertEqual(o_report['warnings'], n_report['warnings'])
        self.assertEqual(o_report['errors'], n_report['errors'])
        self.assertEqual(o_report['info'], n_report['info'])
