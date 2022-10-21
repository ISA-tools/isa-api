from ftplib import error_perm
from os import path
import glob
import logging
import tempfile
from shutil import rmtree
from re import compile as regex

import pandas as pd

from isatools.isatab import load_table, load as isa_load
from isatools.model import OntologyAnnotation
from isatools.net.metabolights.utils import MTBLSDownloader, EBI_FTP_SERVER, MTBLS_BASE_DIR, slice_data_files

log = logging.getLogger('isatools')
_RX_FACTOR_VALUE = regex(r'Factor Value\[(.*?)\]')


class MTBLSInvestigationBase:

    def __init__(self, mtbls_id: str, output_directory: str = None, output_format: str = 'tab') -> None:
        self.mtbls_id = mtbls_id
        self.format = output_format
        self.temp = False
        self.output_dir = output_directory
        self.__executed = False
        self.__ftp_directory = EBI_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_id
        ftp = MTBLSDownloader()
        self.ftp = ftp.ftp
        self.downloaded = False

    @property
    def mtbls_id(self) -> str:
        return self.__mtbls_id

    @mtbls_id.setter
    def mtbls_id(self, mtbls_id: str) -> None:
        if not isinstance(mtbls_id, str):
            raise TypeError('The MTBLS instance ID must be an string but got %s' % type(mtbls_id).__name__)
        self.__mtbls_id = mtbls_id

    @property
    def format(self) -> str:
        return self.__format

    @format.setter
    def format(self, _format: str) -> None:
        if _format not in ['json', 'json-ld', 'tab']:
            raise ValueError('The output format must be one of the following: json, json-ld, tab')
        self.__format = _format

    @property
    def output_dir(self) -> str:
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, output_dir: str) -> None:
        self.temp = False
        if not output_dir:
            log.info('No directory has been provided. Using a temp one instead')
            self.temp = True
            output_dir = tempfile.mkdtemp()
        log.info('Target directory: %s' % output_dir)
        self.__output_dir = output_dir

    def get_investigation(self):
        ftp = self.ftp
        log.info("Looking for study '%s'" % self.mtbls_id)
        ftp.cwd(MTBLS_BASE_DIR + '/' + self.mtbls_id)
        log.info("Using directory '%s'" % self.output_dir)
        files = list(ftp.nlst())
        try:
            investigation_filename = next(filter(lambda x: x.startswith('i_') and x.endswith('.txt'), files))
        except StopIteration:
            raise Exception('Could not find an investigation file for this study')

        try:
            investigation_tab = self.__download_file(investigation_filename)
            lines = self.__open_investigation(investigation_tab)

            s_filenames = [line.split('\t')[1][1:-1] for line in lines if 'Study File Name' in line]
            [self.__download_file(s_filename) for s_filename in s_filenames]
            a_filenames_lines = [line.split('\t') for line in lines if 'Study Assay File Name' in line]
            for a_filename_line in a_filenames_lines:
                [self.__download_file(a_filename) for a_filename in [f[1:-1] for f in a_filename_line[1:]]]
            self.downloaded = True
            return self.output_dir

        except error_perm as e:
            raise Exception('Could not download a file: %s' % e)

    def __download_file(self, filename):
        ftp_dir_path = EBI_FTP_SERVER + MTBLS_BASE_DIR + '/' + self.mtbls_id + '/' + filename
        with open(self.output_dir + '/' + filename, 'wb') as output_file:
            log.info("Retrieving file '%s'" % ftp_dir_path)
            self.ftp.retrbinary('RETR ' + filename, output_file.write)
        return output_file

    @staticmethod
    def __open_investigation(investigation_file):
        with open(investigation_file.name, encoding='utf-8') as i_fp:
            i_bytes = i_fp.read()
        return i_bytes.splitlines()

    def __del__(self) -> None:
        if hasattr(self, 'temp') and self.temp:
            log.info('Removing temp directory %s' % self.output_dir)
            rmtree(self.output_dir)


class MTBLSInvestigation(MTBLSInvestigationBase):
    def __init__(self, mtbls_id: str, output_directory: str = None, output_format: str = 'tab') -> None:
        super().__init__(mtbls_id, output_directory, output_format)
        self.investigation = None
        self.dataframes = None

    def load_dataframes(self):
        if not self.downloaded:
            self.get_investigation()
        if not self.dataframes:
            self.dataframes = {}
            for table_file in glob.iglob(path.join(self.output_dir, '[a|s|i]_*')):
                with open(path.join(self.output_dir, table_file), encoding='utf-8') as fp:
                    self.dataframes[table_file] = load_table(fp)

    def load_investigation(self):
        if not self.downloaded:
            self.get_investigation()
        if not self.investigation:
            with open(glob.glob(path.join(self.output_dir, 'i_*.txt'))[0], encoding='utf-8') as fp:
                self.investigation = isa_load(fp)

    def get(self):
        if self.format == 'json':
            self.load_dataframes()
            self.load_investigation()
            return self.investigation
        elif self.format == 'tab':
            self.load_dataframes()
            return self.output_dir

    def get_factor_names(self):
        self.load_dataframes()
        factors = set()
        for table_file in glob.iglob(path.join(self.output_dir, '[a|s]_*')):
            df = self.dataframes[table_file]
            factors_headers = [header for header in list(df.columns.values) if _RX_FACTOR_VALUE.match(header)]
            [factors.add(header[13:-1]) for header in factors_headers]
        return factors

    def get_factor_values(self, factor_name):
        self.load_dataframes()
        fvs = set()
        for table_file in glob.iglob(path.join(self.output_dir, '[a|s]_*')):
            df = self.dataframes[table_file]
            if 'Factor Value[{factor}]'.format(factor=factor_name) in list(df.columns.values):
                for _, match in df['Factor Value[{factor}]'.format(factor=factor_name)].items():
                    try:
                        match = match.item()
                    except AttributeError:
                        pass
                    if isinstance(match, (str, int, float)):
                        if str(match) != 'nan':
                            fvs.add(match)
        return fvs

    def get_data_files(self, factor_selection=None):
        self.load_dataframes()
        return slice_data_files(self.output_dir, factor_selection=factor_selection)

    def get_factors_summary(self):
        self.load_investigation()
        all_samples = []
        for study in self.investigation.studies:
            all_samples.extend(study.samples)
        samples_and_fvs = []

        for sample in all_samples:
            sample_and_fvs = {'sources': ';'.join([x.name for x in sample.derives_from]), 'name': sample.name}
            for fv in sample.factor_values:
                fv_value = fv.value
                if isinstance(fv.value, OntologyAnnotation):
                    fv_value = fv.value.term
                sample_and_fvs[fv.factor_name.name] = fv_value

            samples_and_fvs.append(sample_and_fvs)

        df = pd.DataFrame(samples_and_fvs)
        nunique = df.apply(pd.Series.nunique)
        cols_to_drop = nunique[nunique == 1].index
        df = df.drop(cols_to_drop, axis=1)
        return df.to_dict(orient='records')

    def get_study_groups(self):
        factors_summary = self.get_factors_summary()
        study_groups = {}
        for factor in factors_summary:
            fvs = tuple(factor[k] for k in factor.keys() if k != 'name')
            if fvs in study_groups.keys():
                study_groups[fvs].append(factor['name'])
            else:
                study_groups[fvs] = [factor['name']]
        return study_groups

    def get_study_groups_samples_sizes(self):
        study_groups = self.get_study_groups()
        return list(map(lambda x: (x[0], len(x[1])), study_groups.items()))
