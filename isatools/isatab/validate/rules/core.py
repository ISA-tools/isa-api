from __future__ import annotations, absolute_import
from typing import Callable, List
from typing.io import TextIO

from os import path

from pandas import DataFrame
from pandas.errors import ParserError


from isatools.utils import utf8_text_file_open
from isatools.isatab.defaults import NUMBER_OF_STUDY_GROUPS, default_config_dir
from isatools.isatab.load import load_table
from isatools.isatab.validate.store import validator as message_handler
from isatools.isatab.validate.rules.defaults import (
    DEFAULT_INVESTIGATION_RULES,
    INVESTIGATION_RULES_MAPPING,
    DEFAULT_STUDY_RULES,
    STUDY_RULES_MAPPING,
    DEFAULT_ASSAY_RULES,
    ASSAY_RULES_MAPPING,
)
from isatools.isatab.validate.core import load_investigation


class Rule:

    def __init__(self, rule: Callable, params: List, identifier: str):
        self.rule = rule
        self.params = params
        self.identifier = identifier
        self.executed = False

    def __str__(self):
        return "rule={self.rule.__name__}, params={self.params}, identifier={self.identifier}".format(self=self)

    def get_parameters(self, validator):
        params = []
        for param in self.params:
            params.append(validator.params[param])
        return params

    def execute(self, validator):
        params = self.get_parameters(validator)
        response = self.rule(*params)
        if self.identifier == '3008':
            validator.params['term_source_refs'] = response[0]
        if self.identifier == '4001':
            validator.params['configs'] = response
        self.executed = True


class Rules:

    def __init__(self, rules_to_run: List, available_rules: tuple):
        self.rules = [Rule(**rule_data) for rule_data in rules_to_run]
        self.all_rules = available_rules

    def get_rule(self, rule_name: str | Callable) -> Rule:
        for rule_data in self.rules:
            if isinstance(rule_name, str) and rule_data.identifier == rule_name:
                return rule_data
            elif isinstance(rule_name, Callable) and rule_data.rule == rule_name:
                return rule_data
        raise ValueError("Rule not found: {}".format(rule_name))

    def get_rules(self):
        rules_list = []
        for rule_data in self.all_rules:
            rule = self.get_rule(rule_data)
            if rule:
                rules_list.append(rule)
        return rules_list

    def validate_rules(self, validator):
        for rule in self.get_rules():
            rule.execute(validator)
        validator.has_validated = True


class ISAInvestigationValidator:
    def __init__(self,
                 investigation_df: DataFrame,
                 dir_context: str,
                 configs: str,
                 rules_list: List = INVESTIGATION_RULES_MAPPING):
        self.all_rules = Rules(rules_to_run=rules_list, available_rules=DEFAULT_INVESTIGATION_RULES)
        self.has_validated = False
        self.params = {
            'investigation_df': investigation_df,
            'dir_context': dir_context,
            'configs': configs,
            'term_source_refs': None
        }
        self.all_rules.validate_rules(validator=self)


class ISAStudyValidator:

    def __init__(self,
                 validator: ISAInvestigationValidator,
                 study_index: int,
                 study_filename: str,
                 study_df: DataFrame,
                 rules_list: List = STUDY_RULES_MAPPING):
        self.all_rules = Rules(rules_to_run=rules_list, available_rules=DEFAULT_STUDY_RULES)
        self.has_validated = False
        self.params = {
            **validator.params,
            'study_df': study_df,
            'config': validator.params['configs'][('[sample]', '')]
        }
        with utf8_text_file_open(path.join(self.params['dir_context'], study_filename)) as s_fp:
            self.params['study_sample_table'] = load_table(s_fp)
            self.params['study_sample_table'].filename = study_filename

        protocol_names = self.params['investigation_df']['s_protocols'][study_index]['Study Protocol Name'].tolist()
        protocol_types = self.params['investigation_df']['s_protocols'][study_index]['Study Protocol Type'].tolist()
        self.params['protocol_names_and_types'] = dict(zip(protocol_names, protocol_types))

        self.params['study_group_size_in_comment'] = None
        if NUMBER_OF_STUDY_GROUPS in study_df.columns:
            study_group_sizes = study_df[NUMBER_OF_STUDY_GROUPS]
            self.params['study_group_size_in_comment'] = next(iter(study_group_sizes))
        self.params['study_filename'] = study_df.iloc[0]['Study File Name']
        self.all_rules.validate_rules(validator=self)


class ISAAssayValidator:

    def __init__(self,
                 assay_tables: List,
                 validator: ISAStudyValidator,
                 assay_index: int = None,
                 assay_filename: str = None,
                 assay_df: DataFrame = None,
                 rules_list: List = ASSAY_RULES_MAPPING):
        self.all_rules = Rules(rules_to_run=rules_list, available_rules=DEFAULT_ASSAY_RULES)
        self.has_validated = False
        self.params = {
            **validator.params,
            'assay_tables': assay_tables,
            'assay_filename': assay_filename
        }
        if NUMBER_OF_STUDY_GROUPS in assay_df.columns:
            study_group_sizes = self.params['study_dataframe'][NUMBER_OF_STUDY_GROUPS]
            self.params['study_group_size_in_comment'] = next(iter(study_group_sizes))
        if assay_filename != '':
            lowered_mt = assay_df['Study Assay Measurement Type'].tolist()[assay_index].lower()
            lowered_tt = assay_df['Study Assay Technology Type'].tolist()[assay_index].lower()
            self.params['config'] = self.params['configs'].get((lowered_mt, lowered_tt), None)
            if self.params['config']:
                with utf8_text_file_open(path.join(self.params['dir_context'], assay_filename)) as a_fp:
                    self.params['assay_table'] = load_table(a_fp)
                    self.params['assay_table'].filename = assay_filename
                    self.params['assay_tables'].append(self.params['assay_table'])
            self.all_rules.validate_rules(validator=self)


def validate(investigation_fp: TextIO, conf_dir: str = default_config_dir, mzml: bool = False):
    message_handler.reset_store()
    validated = False
    try:
        i_df = load_investigation(fp=investigation_fp)
        params = {
            "investigation_df": i_df,
            "dir_context": path.dirname(investigation_fp.name),
            "configs": conf_dir,
        }
        investigation_validator = ISAInvestigationValidator(**params)
        for i, study_df in enumerate(i_df['studies']):
            study_filename = study_df.iloc[0]['Study File Name']
            study_validator = ISAStudyValidator(validator=investigation_validator, study_index=i,
                                                study_filename=study_filename, study_df=study_df)
            assay_tables = list()
            assay_df = study_validator.params['investigation_df']['s_assays'][i]
            for x, assay_filename in enumerate(assay_df['Study Assay File Name'].tolist()):
                ISAAssayValidator(assay_tables=assay_tables, validator=study_validator, assay_index=x,
                                  assay_df=assay_df, assay_filename=assay_filename)
            if mzml:
                validate_mzml(fp=investigation_fp)
        validated = True
    except (Exception, ParserError, SystemError, ValueError) as e:
        spl = "The validator could not identify what the error is: {}".format(str(e))
        message_handler.add_error(message="Unknown/System Error", supplemental=spl, code=0)
    return {
        "errors": message_handler.errors,
        "warnings": message_handler.warnings,
        "info": message_handler.info,
        "validation_finished": validated
    }


def validate_mzml(fp):
    from isatools import utils
    try:
        fp.seek(0)
        utils.detect_isatab_process_pooling(fp)
    except BaseException:
        pass