import os
from ftplib import FTP
import glob
import logging

import pandas as pd

from isatools import isatab

EBI_FTP_SERVER = 'ftp.ebi.ac.uk'
MTBLS_BASE_DIR = '/pub/databases/metabolights/studies/public'
log = logging.getLogger('isatools')


class MTBLSDownloader:
    _instance = None

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super(MTBLSDownloader, cls).__new__(cls)
            cls.ftp = cls.__connect()
        return cls._instance

    def __init__(self) -> None:
        pass

    @staticmethod
    def __connect() -> FTP:
        try:
            log.info('Connecting to %s' % EBI_FTP_SERVER)
            ftp = FTP(EBI_FTP_SERVER)
            ftp.login()
            return ftp
        except Exception as e:
            raise Exception("Cannot contact the remote FTP server: %s" % e)

    def __del__(self) -> None:
        if hasattr(self, 'ftp'):
            log.info("Closing FTP connection")
            self.ftp.close()


def slice_data_files(dir, factor_selection=None):
    """
    This function gets a list of samples and related data file URLs for a given
    MetaboLights study, optionally filtered by factor value (currently by
    matching on exactly 1 factor value)

    :param mtbls_study_id: Study identifier for MetaboLights study to get, as
    a str (e.g. MTBLS1)
    :param factor_selection: A list of selected factor values to filter on
    samples
    :return: A list of dicts {sample_name, list of data_files} containing
    sample names with associated data filenames

    Example usage:
        samples_and_data = mtbls.get_data_files('MTBLS1', [{'Gender': 'Male'}])

    TODO:  Need to work on more complex filters e.g.:
        {"gender": ["male", "female"]} selects samples matching "male" or
        "female" factor value
        {"age": {"equals": 60}} selects samples matching age 60
        {"age": {"less_than": 60}} selects samples matching age less than 60
        {"age": {"more_than": 60}} selects samples matching age more than 60

        To select samples matching "male" and age less than 60:
        {
            "gender": "male",
            "age": {
                "less_than": 60
            }
        }
    """
    results = []
    # first collect matching samples
    for table_file in glob.iglob(os.path.join(dir, '[a|s]_*')):
        log.info('Loading {table_file}'.format(table_file=table_file))

        with open(table_file, encoding='utf-8') as fp:
            df = isatab.load_table(fp)
            df = df[[x for x in df.columns if 'Factor Value' in x or 'Sample Name' in x]]
            df.columns = ['sample' if 'Sample Name' in x else x for x in df.columns]
            df.columns = [x[13:-1] if 'Factor Value' in x else x for x in df.columns]
            df.columns = [x.replace(' ', '_') for x in df.columns]
            # build query
            sample_names_series = df['sample'].drop_duplicates()
            if factor_selection is None:
                results = sample_names_series.apply(
                    lambda x: {'sample': x, 'data_files': [], 'query_used': ''}
                ).tolist()
            else:
                factor_query = ''
                for factor_name, factor_value in factor_selection.items():
                    factor_name = factor_name.replace(' ', '_')
                    factor_query += '%s=="%s" and ' % (factor_name, factor_value)
                factor_query = factor_query[:-5]
                try:
                    query_results = df.query(factor_query)['sample'].drop_duplicates()
                    results = query_results.apply(
                        lambda x: {'sample': x, 'data_files': [], 'query_used': factor_selection}
                    ).tolist()
                except pd.errors.UndefinedVariableError:
                    pass

    # now collect the data files relating to the samples
    for table_file in glob.iglob(os.path.join(dir, 'a_*.txt')):
        with open(table_file, encoding='utf-8') as fp:
            df = isatab.load_table(fp)
            df = df[[x for x in df.columns if 'File' in x or 'Sample Name' in x]]
            df.columns = ['sample' if 'Sample Name' in x else x for x in df.columns]
            for result in results:
                sample_name = result['sample']
                sample_rows = df.loc[df['sample'] == sample_name]

                for data_col in [x for x in sample_rows.columns if 'File' in x]:
                    data_files = sample_rows[data_col]
                    result['data_files'] = [i for i in data_files if str(i) != 'nan']
    return results
