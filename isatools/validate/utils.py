import re, iso8601, chardet

def check_pubmed_id(pubmed_id_str, report):
    if pubmed_id_str is not '':
        pmid_regex = re.compile('[0-9]{8}')
        pmcid_regex = re.compile('PMC[0-9]{8}')
        if pmid_regex.match(pubmed_id_str) is not None and pmcid_regex.match(pubmed_id_str) is not None:
            report.warn("PubMed ID {} is not valid format".format(pubmed_id_str))
    # TODO: Check if publication exists and consistency with other metadata in section; needs network connection


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
    pass


def check_encoding(fp, report):
    charset = chardet.detect(open(fp.name, 'rb').read())
    if charset['encoding'] is not 'UTF-8':
        report.warn("File should be UTF-8 encoding but found it is '{0}' encoding with {1} confidence"
                    .format(charset['encoding'], charset['confidence']))