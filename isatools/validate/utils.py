import re
import iso8601
import chardet
import os


class ValidationError(Exception):
    pass


class ValidationReport:

    def __init__(self, file_name):
        self.report = dict()
        self.report['warnings'] = list()
        self.report['errors'] = list()
        self.report['fatal'] = list()
        self.file_name = file_name

    def fatal(self, msg):
        self.report['fatal'].append({
            'message': msg,
        })

    def warn(self, msg):
        self.report['warnings'].append({
            'message': msg,
        })

    def error(self, msg):
        self.report['errors'].append({
            'message': msg,
        })

    def generate_report_json(self, reporting_level=3):
        if reporting_level == 0:
            return {
                'warnings': self.report['warnings']
            }
        if reporting_level == 1:
            return {
                'errors': self.report['errors']
            }
        if reporting_level == 2:
            return {
                'warnings': self.report['fatal']
            }
        if reporting_level == 3:
            return self.report

    def print_report(self, reporting_level=3):
        report_json = self.generate_report_json(reporting_level)
        if len(self.report['fatal']) > 0: print(self.file_name + ' ::: Fatal errors:')
        for message in report_json['fatal']:
            print(message['message'])
        if len(self.report['errors']) > 0: print(self.file_name + ' ::: Errors:')
        for message in report_json['errors']:
            print(message['message'])
        if len(self.report['warnings']) > 0: print(self.file_name + ' ::: Warnings:')
        for message in report_json['warnings']:
            print(message['message'])


def check_pubmed_id(pubmed_id_str, report):
    if pubmed_id_str is not '':
        pmid_regex = re.compile('[0-9]{8}')
        pmcid_regex = re.compile('PMC[0-9]{8}')
        if pmid_regex.match(pubmed_id_str) is not None and pmcid_regex.match(pubmed_id_str) is not None:
            report.warn("PubMed ID {} is not valid format".format(pubmed_id_str))
    # TODO: Check if publication exists and consistency with other metadata in section; needs network connection


def date_is_iso8601(string):
    r"""Dates must be ISO8601 formatted, e.g. YYYY-MM-DD, YYYY-MM, YYYYMMDD

    Okay: 2016-04-07
    Okay: 2016-04
    Okay: 20160407
    Exxx: 201604
    """
    if string is not '':
        try:
            iso8601.parse_date(string)
        except iso8601.ParseError:
            return string, "Date is not ISO8601 format"


def check_iso8601_date(date_str, report):
    if date_str is not '':
        try:
            iso8601.parse_date(date_str)
        except iso8601.ParseError:
            report.warn("Date {} does not conform to ISO8601 format".format(date_str))


def is_iso8601_date(date_str):
    if date_str is not '':
        try:
            iso8601.parse_date(date_str)
        except iso8601.ParseError:
            return False
        return True
    return False


def check_doi(doi_str, report):
    if doi_str is not '':
        regexDOI = re.compile('[doi|DOI][\s\.\:]{0,2}(10\.\d{4}[\d\:\.\-\/a-z]+)[A-Z\s]')
        if not regexDOI.match(doi_str):
            report.warn("DOI {} does not conform to DOI format".format(doi_str))


def check_encoding(fp, report):
    charset = chardet.detect(open(fp.name, 'rb').read())
    if charset['encoding'] is not 'UTF-8':
        report.warn("File should be UTF-8 encoding but found it is '{0}' encoding with {1} confidence"
                    .format(charset['encoding'], charset['confidence']))


def check_data_files(data_files, dir_context, report):
    for data_file in data_files:
        try:
            filename = data_file['name']
            with open(os.path.join(dir_context, filename)) as file:
                pass
        except IOError as e:
            report.warn("Cannot open file {}".format(filename))