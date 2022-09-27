import unittest
from os import path

from isatools.tests import utils
from isatools.isatab import validate
from isatools.isatab.validate.rules.core import Rule, Rules
from isatools.isatab.validate.rules.defaults import INVESTIGATION_RULES_MAPPING
from isatools.isatab.validate.store import validator as message_handler


class TestValidators(unittest.TestCase):

    def setUp(self) -> None:
        self.default_conf = utils.DEFAULT2015_XML_CONFIGS_DATA_DIR

    def test_b_ii_s_3(self):
        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'tab', 'BII-S-3')
        with open(path.join(data_path, 'i_gilbert.txt'), 'r') as data_file:
            r = validate(fp=data_file, config_dir=self.default_conf, mzml=True)
        self.assertEqual(len(r['warnings']), 12)

    def test_mtbls_1846(self):
        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'mtbls', 'MTBLS1846')
        with open(path.join(data_path, 'i_Investigation.txt'), 'r') as data_file:
            r = validate(fp=data_file, config_dir=self.default_conf)
        self.assertEqual(len(r['errors']), 10)

    def test_bii_i_1(self):
        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'tab', 'BII-I-1')
        with open(path.join(data_path, 'i_investigation.txt'), 'r') as data_file:
            report = validate(fp=data_file, config_dir=self.default_conf)
        self.assertEqual(len(report['warnings']), 40)

    def test_bii_s_7(self):
        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'tab', 'BII-S-7')
        with open(path.join(data_path, 'i_matteo.txt'), 'r') as data_file:
            report = validate(fp=data_file, config_dir=self.default_conf)
        self.assertEqual(len(report['warnings']), 14)

    def test_print_rule(self):
        raw_rule = INVESTIGATION_RULES_MAPPING[0]
        rule = Rule(**raw_rule)
        expected_string = "rule=check_table_files_read, params=['investigation_df', 'dir_context'], identifier=0006"
        self.assertEqual(str(rule), expected_string)

    def test_rules_error(self):
        rules_to_test = ('6006', )
        rules = Rules(rules_to_run=rules_to_test, available_rules=INVESTIGATION_RULES_MAPPING)
        with self.assertRaises(ValueError) as context:
            rules.get_rule('6006')
        self.assertEqual(str(context.exception), 'Rule not found: 6006')

    def test_extend_rules(self):
        from isatools.isatab.validate.rules.defaults import INVESTIGATION_RULES_MAPPING, DEFAULT_INVESTIGATION_RULES

        def is_investigation(investigation_df):
            return 'investigation' in investigation_df

        rules = {
            "investigation": {
                "available_rules": [
                    *INVESTIGATION_RULES_MAPPING,
                    {
                        'rule': is_investigation,
                        'params': ['investigation_df'],
                        'identifier': '6000'
                    }
                ],
                "rules_to_run": (*DEFAULT_INVESTIGATION_RULES, is_investigation)
            },
            "studies": {},
            "assays": {}
        }

        data_path = path.join(path.dirname(path.abspath(__file__)), '..', '..', 'data', 'tab', 'BII-S-3')
        with open(path.join(data_path, 'i_gilbert.txt'), 'r') as data_file:
            r = validate(data_file, rules=rules)
        self.assertEqual(len(r['warnings']), 12)

        rule = '12000'
        expected_error = {
            'message': 'Unknown/System Error',
            'supplemental': 'The validator could not identify what the error is: Rule not found: {}'.format(rule),
            'code': 0
        }
        rules['investigation']['rules_to_run'] = (*DEFAULT_INVESTIGATION_RULES, rule)
        with open(path.join(data_path, 'i_gilbert.txt'), 'r') as data_file:
            r = validate(data_file, rules=rules)
        self.assertEqual(r['errors'], [expected_error])

    def test_store(self):
        message_handler.reset_store()
        self.assertEqual(str(message_handler), "{'errors': [], 'warnings': [], 'info': []}")
