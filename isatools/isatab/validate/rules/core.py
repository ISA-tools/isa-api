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
    """ An ISA rule needs a rule function, a list of parameters and an identifier
    """

    def __init__(self, rule: Callable, params: List, identifier: str):
        """ Constructor of the Rule class

        :param rule: a function to execute as a rule
        :param params: the input parameters of the function
        :param identifier: the identifier of the function for mapping and reporting
        """
        self.rule = rule
        self.params = params
        self.identifier = identifier
        self.executed = False

    def __str__(self):
        return "rule={self.rule.__name__}, params={self.params}, identifier={self.identifier}".format(self=self)

    def get_parameters(self, params: dict) -> list:
        """ Wrapper to get the parameters for the rule function given a dict of parameters from a validator
        """
        selected_params = []
        for param in self.params:
            selected_params.append(params[param])
        return selected_params

    def execute(self, validator_params: dict) -> None:
        """ Execute the rule function with the parameters

        :param validator_params: parameters coming from one of the three validators
        """
        params = self.get_parameters(validator_params)
        try:
            response = self.rule(*params)
            if self.identifier == '3008':
                validator_params['term_source_refs'] = response[0]
            if self.identifier == '4001':
                validator_params['configs'] = response
            self.executed = True
        except Exception as e:
            print(e)


class Rules:

    def __init__(self, rules_to_run: tuple, available_rules: list):
        """ A wrapper containing all the rules to be executed

        :param rules_to_run: the list of rules to run given by identifiers or rule functions
        :param available_rules: a list of customizable rules that are available
        """
        self.available_rules = []
        self.available_rules = [Rule(**rule_data) for rule_data in available_rules]
        self.rules_to_run = rules_to_run

    def get_rule(self, rule_name: str | Callable) -> Rule:
        """
        Get a rule given its identifier or the rule function
        :param rule_name: the identifier or the rule function
        :return: the rule to execute
        """
        for rule_data in self.available_rules:
            if isinstance(rule_name, str) and rule_data.identifier == rule_name:
                return rule_data
            elif isinstance(rule_name, Callable) and rule_data.rule == rule_name:
                return rule_data
        raise ValueError("Rule not found: {}".format(rule_name))

    def get_rules(self):
        """
        Get the list of rules to execute
        :return:
        """
        rules_list = []
        for rule_data in self.rules_to_run:
            rule = self.get_rule(rule_data)
            if rule:
                rules_list.append(rule)
        return rules_list

    def validate_rules(self, validator):
        """ Wrapper to execute all the rules """
        for rule in self.get_rules():
            rule.execute(validator.params)
        validator.has_validated = True


class ISAInvestigationValidator:
    def __init__(self,
                 investigation_df: DataFrame,
                 dir_context: str,
                 configs: str,
                 available_rules: list = INVESTIGATION_RULES_MAPPING,
                 rules_to_run: tuple = DEFAULT_INVESTIGATION_RULES):
        """ The ISA investigation validator class

        :param investigation_df: the investigation dataframe
        :param dir_context: the directory of the investigation
        :param configs: directory of the XML config files
        :param available_rules: a customizable list of all available rules for investigation objects
        :param rules_to_run: a customizable tuple of rules identifiers to run for investigation objects
        """
        self.all_rules = Rules(rules_to_run=rules_to_run, available_rules=available_rules)
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
                 available_rules: List = STUDY_RULES_MAPPING,
                 rules_to_run: tuple = DEFAULT_STUDY_RULES):
        """
        The ISA study validator class
        :param validator: the investigation validator
        :param study_index: the index of the study in the investigation dataframe to validate
        :param study_filename: the filename of the study to validate
        :param study_df: the study dataframe
        :param available_rules: a customizable list of all available rules for investigation objects
        :param rules_to_run: a customizable tuple of rules identifiers to run for investigation objects
        """
        self.all_rules = Rules(rules_to_run=rules_to_run, available_rules=available_rules)
        self.has_validated = False
        self.params = {
            **validator.params,
            'study_df': study_df,
            'config': validator.params['configs'][('[sample]', '')],
            'study_filename': study_filename
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
                 available_rules: List = ASSAY_RULES_MAPPING,
                 rules_to_run: tuple = DEFAULT_ASSAY_RULES):
        """
        The ISA assay validator class
        :param assay_tables: list of assay tables
        :param validator: the study validator
        :param assay_index: the index of the assay in the study dataframe to validate
        :param assay_filename: the filename of the assay to validate
        :param assay_df: the assay dataframe
        :param available_rules: a customizable list of all available rules for investigation objects
        :param rules_to_run: a customizable tuple of rules identifiers to run for investigation objects
        """
        self.all_rules = Rules(rules_to_run=rules_to_run, available_rules=available_rules)
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


def validate(investigation_fp: TextIO,
             conf_dir: str = default_config_dir,
             mzml: bool = False,
             rules: dict = None) -> dict[str, dict[str, dict[str, list]]]:
    """
    A function to validate an ISA investigation tab file
    :param investigation_fp: the investigation file handler
    :param conf_dir: the XML configuration directory
    :param mzml: extra rules for mzML
    :param rules: optional rules to run (default: all rules)
    :return: a dictionary of the validation results (errors, warnings and info)
    """
    message_handler.reset_store()
    validated = False

    built_rules = build_rules(rules)
    try:
        i_df = load_investigation(fp=investigation_fp)
        params = {
            "investigation_df": i_df,
            "dir_context": path.dirname(investigation_fp.name),
            "configs": conf_dir,
        }
        investigation_validator = ISAInvestigationValidator(**params, **built_rules['investigation'])

        for i, study_df in enumerate(i_df['studies']):
            study_filename = study_df.iloc[0]['Study File Name']
            study_validator = ISAStudyValidator(validator=investigation_validator, study_index=i,
                                                study_filename=study_filename, study_df=study_df,
                                                **built_rules['studies'])
            assay_tables = list()
            assay_df = study_validator.params['investigation_df']['s_assays'][i]
            for x, assay_filename in enumerate(assay_df['Study Assay File Name'].tolist()):
                ISAAssayValidator(assay_tables=assay_tables, validator=study_validator, assay_index=x,
                                  assay_df=assay_df, assay_filename=assay_filename, **built_rules['assays'])
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


def validate_mzml(fp: TextIO) -> None:
    """
    A function to validate an mzML file
    :param fp: the investigation file handler
    """
    from isatools import utils
    try:
        fp.seek(0)
        utils.detect_isatab_process_pooling(fp)
    except BaseException:
        pass


def build_rules(user_rules: dict = None) -> dict:
    """ Given a user-defined rules dictionary, build the rules dictionary for the validators

    :param user_rules: a dictionary of rules to run
    :return: a dictionary of rules to run
    """
    rules = {
        'investigation': {},
        'studies': {},
        'assays': {}
    }
    if user_rules:
        if 'investigation' in rules:
            rules['investigation'] = {
                "available_rules": user_rules['investigation'].get('available_rules', INVESTIGATION_RULES_MAPPING),
                "rules_to_run": user_rules['investigation'].get("rules_to_run", DEFAULT_INVESTIGATION_RULES)
            }
        if 'studies' in rules:
            rules['studies'] = {
                "available_rules": user_rules['studies'].get('available_rules', STUDY_RULES_MAPPING),
                "rules_to_run": user_rules['studies'].get("rules_to_run", DEFAULT_STUDY_RULES)
            }
        if 'assays' in rules:
            rules['assays'] = {
                "available_rules": user_rules['assays'].get('available_rules', ASSAY_RULES_MAPPING),
                "rules_to_run": user_rules['assays'].get("rules_to_run", DEFAULT_ASSAY_RULES)
            }
    return rules
