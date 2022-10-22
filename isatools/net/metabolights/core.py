from __future__ import annotations

from ftplib import error_perm
from os import path
import glob
import logging
import tempfile
from typing import TextIO
from shutil import rmtree
from re import compile as regex
from json import dump, loads as json_loads, load as json_load

import pandas as pd

from isatools.isatab import load_table, load as isa_load
from isatools.model import OntologyAnnotation
from isatools.net.metabolights.utils import MTBLSDownloader, EBI_FTP_SERVER, MTBLS_BASE_DIR, slice_data_files
from isatools.net.metabolights.html import build_html_summary

log = logging.getLogger('isatools')
_RX_FACTOR_VALUE = regex(r'Factor Value\[(.*?)\]')


class MTBLSInvestigationBase:

    def __init__(
            self,
            mtbls_id: str,
            output_directory: str = None,
            output_format: str = 'tab',
            ftp_server: object = None
    ) -> None:
        self.mtbls_id = mtbls_id
        self.format = output_format
        self.temp = False
        self.output_dir = output_directory
        self.__executed = False
        self.__ftp_directory = EBI_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_id
        self.ftp = ftp_server
        if not ftp_server:
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

            s_filenames = [self.__get_filename(line) for line in lines if 'Study File Name' in line]
            [self.__download_file(s_filename) for s_filename in s_filenames]

            a_filenames_lines = [line.split('\t') for line in lines if 'Study Assay File Name' in line]
            for filenames in [a_filename_line[1:] for a_filename_line in a_filenames_lines]:
                [self.__download_file(filename.replace('"', "")) for filename in filenames]
            self.downloaded = True
            return self.output_dir

        except error_perm as e:
            raise Exception('Could not download a file: %s for %s' % (e, self.mtbls_id))

    @staticmethod
    def __get_filename(line):
        file_val = line.split('\t')[1]
        if file_val.startswith('"') and file_val.endswith('"'):
            return file_val[1:-1]
        return file_val  # pragma: no cover

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
    def __init__(
            self,
            mtbls_id: str,
            output_directory: str = None,
            output_format: str = 'tab',
            ftp_server: object = None
    ) -> None:
        super().__init__(mtbls_id, output_directory, output_format, ftp_server)
        self.investigation = None
        self.dataframes = None

    def load_dataframes(self) -> None:
        if not self.downloaded:
            self.get_investigation()
        if not self.dataframes:
            self.dataframes = {}
            for table_file in glob.iglob(path.join(self.output_dir, '[a|s|i]_*')):
                with open(path.join(self.output_dir, table_file), encoding='utf-8') as fp:
                    self.dataframes[table_file] = load_table(fp)

    def load_json(self) -> None:
        if not self.downloaded:
            self.get_investigation()
        if not self.investigation:
            with open(glob.glob(path.join(self.output_dir, 'i_*.txt'))[0], encoding='utf-8') as fp:
                self.investigation = isa_load(fp)

    def get_factor_names(self) -> set:
        self.load_dataframes()
        factors = set()
        for table_file in glob.iglob(path.join(self.output_dir, '[a|s]_*')):
            df = self.dataframes[table_file]
            factors_headers = [header for header in list(df.columns.values) if _RX_FACTOR_VALUE.match(header)]
            [factors.add(header[13:-1]) for header in factors_headers]
        return factors

    def get_factor_values(self, factor_name: str) -> set:
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

    def get_data_files(self, factor_selection: dict = None) -> list:
        self.load_dataframes()
        return slice_data_files(self.output_dir, factor_selection=factor_selection)

    def get_factors_summary(self) -> list:
        self.load_json()
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

    def get_study_groups(self) -> dict:
        factors_summary = self.get_factors_summary()
        study_groups = {}
        for factor in factors_summary:
            fvs = tuple(factor[k] for k in factor.keys() if k != 'name')
            if fvs in study_groups.keys():
                study_groups[fvs].append(factor['name'])
            else:
                study_groups[fvs] = [factor['name']]
        return study_groups

    def get_study_groups_samples_sizes(self) -> list:
        study_groups = self.get_study_groups()
        return list(map(lambda x: (x[0], len(x[1])), study_groups.items()))

    def get_sources_for_sample(self, sample_name: str) -> list:
        self.load_json()
        hits = []
        for study in self.investigation.studies:
            for sample in study.samples:
                if sample.name == sample_name:
                    log.info('Found a hit: %s' % sample.name)
                    for source in sample.derives_from:
                        hits.append(source.name)
        return hits

    def get_data_for_sample(self, sample_name: str) -> list:
        self.load_json()
        hits = []
        for study in self.investigation.studies:
            for assay in study.assays:
                for data in assay.data_files:
                    if sample_name in [x.name for x in data.generated_from]:
                        log.info('found a hit: %s' % data.filename)
                        hits.append(data)
        return hits

    def get_study_groups_data_sizes(self) -> list:
        study_groups = self.get_study_groups()
        return list(map(lambda x: (x[0], len(x[1])), study_groups.items()))

    def get_characteristics_summary(self) -> list:
        self.load_json()
        all_samples = []
        for study in self.investigation.studies:
            all_samples.extend(study.samples)

        samples_and_characs = []
        for sample in all_samples:
            sample_and_characs = {'name': sample.name}
            for source in sample.derives_from:
                for c in source.characteristics:
                    c_value = c.value
                    if isinstance(c.value, OntologyAnnotation):
                        c_value = c.value.term
                    sample_and_characs[c.category.term] = c_value
            samples_and_characs.append(sample_and_characs)

        df = pd.DataFrame(samples_and_characs)
        nunique = df.apply(pd.Series.nunique)
        cols_to_drop = nunique[nunique == 1].index
        df = df.drop(cols_to_drop, axis=1)
        return df.to_dict(orient='records')

    def get_study_variable_summary(self) -> list:
        self.load_json()
        all_samples = []
        for study in self.investigation.studies:
            all_samples.extend(study.samples)
        samples_and_variables = []
        for sample in all_samples:
            sample_and_vars = {'sample_name': sample.name}
            for fv in sample.factor_values:
                fv_value = fv.value
                if isinstance(fv.value, OntologyAnnotation):
                    fv_value = fv.value.term
                sample_and_vars[fv.factor_name.name] = fv_value
            for source in sample.derives_from:
                sample_and_vars['source_name'] = source.name
                for c in source.characteristics:
                    c_value = c.value
                    if isinstance(c.value, OntologyAnnotation):
                        c_value = c.value.term
                    sample_and_vars[c.category.term] = c_value
            samples_and_variables.append(sample_and_vars)

        df = pd.DataFrame(samples_and_variables)
        nunique = df.apply(pd.Series.nunique)
        cols_to_drop = nunique[nunique == 1].index
        df = df.drop(cols_to_drop, axis=1)
        return df.to_dict(orient='records')

    def get_study_group_factors(self) -> list:
        self.load_dataframes()
        factors_list = []
        for table_file in glob.iglob(path.join(self.output_dir, '[a|s]_*')):
            df = self.dataframes[table_file]
            factor_columns = [x for x in df.columns if x.startswith('Factor Value')]
            if len(factor_columns) > 0:
                factors_list = df[factor_columns].drop_duplicates().to_dict(orient='records')
        return factors_list

    def get_filtered_df_on_factors_list(self):
        factors_list = self.get_study_group_factors()
        queries = []

        for factor in factors_list:
            query_str = []
            for k, v in factor.items():
                k = k.replace(' ', '_').replace('[', '_').replace(']', '_')
                if isinstance(v, str):
                    v = v.replace(' ', '_').replace('[', '_').replace(']', '_')
                    query_str.append("{k} == '{v}' and ".format(k=k, v=v))
            query_str = ''.join(query_str)[:-4]
            queries.append(query_str)
        for table_file in glob.iglob(path.join(self.output_dir, '[a|s]_*')):
            df = self.dataframes[table_file]
            cols = df.columns
            cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, str) else x)
            df.columns = cols
            cols = df.columns
            cols = cols.map(lambda x: x.replace('[', '_') if isinstance(x, str) else x)
            df.columns = cols
            cols = df.columns
            cols = cols.map(lambda x: x.replace(']', '_') if isinstance(x, str) else x)
            df.columns = cols
            for query in queries:
                df2 = df.query(query)  # query uses pandas.eval, which evaluates
                # queries like pure Python notation
                if 'Sample_Name' in df.columns:
                    print('Group: %s / Sample_Name: %s' % (query, list(df2['Sample_Name'])))

                if 'Source_Name' in df.columns:
                    print('Group: %s / Sources_Name: %s' % (query, list(df2['Source_Name'])))

                if 'Raw_Spectral_Data_File' in df.columns:
                    print('Group: %s / Raw_Spectral_Data_File: %s' %
                          (query[13:-2], list(df2['Raw_Spectral_Data_File'])))
        return queries

    ''' Not implemented '''
    def get_study_command(self, isa_format, output):
        raise NotImplementedError()

    def get_factors_command(self, output_file: TextIO) -> list:
        log.info("Getting factors for study %s. Writing to %s." % (self.mtbls_id, output_file.name))
        factor_names = self.get_factor_names()
        if factor_names is None:
            raise RuntimeError("Error downloading factors.")  # pragma: no cover
        dump(list(factor_names), output_file, indent=4)
        log.debug("Factor names written")
        return list(factor_names)

    def get_factor_values_command(self, factor: str, output: TextIO) -> list:
        log.info("Getting values for factor %s in study %s. Writing to %s." % (factor, self.mtbls_id, output.name))
        fvs = self.get_factor_values(factor)
        if fvs is None:
            raise RuntimeError("Error downloading factor values.")  # pragma: no cover
        dump(list(fvs), output, indent=4)
        log.debug("Factor values written")
        return list(fvs)

    ''' Not Tested '''
    def get_data_files_command(
            self,
            output: TextIO,
            json_query: str = None,
            galaxy_parameters_file: str = None
    ) -> None:
        log.info("Getting data files for study %s. Writing to %s." % (self.mtbls_id, output.name))
        if json_query:
            log.debug("This is the specified query:\n%s", json_query)
            json_struct = json_loads(json_query)
            data_files = self.get_data_files(json_struct)
        elif galaxy_parameters_file:
            log.debug("Using input Galaxy JSON parameters from:\n%s" % galaxy_parameters_file)
            with open(galaxy_parameters_file) as json_fp:
                galaxy_json = json_load(json_fp)
                json_struct = {}
                for fv_item in galaxy_json['factor_value_series']:
                    json_struct[fv_item['factor_name']] = fv_item['factor_value']
                data_files = self.get_data_files(json_struct)
        else:
            log.debug("No query was specified")
            data_files = self.get_data_files()

        log.debug("Result data files list: %s", data_files)
        if data_files is None:
            raise RuntimeError("Error getting data files with isatools")
        log.debug("dumping data files to %s", output.name)
        dump(list(data_files), output, indent=4)
        log.info("Finished writing data files to {}".format(output))

    ''' Not Tested '''
    def get_summary_command(self, json_output: TextIO, html_output: str):
        log.info("Getting summary for study %s. Writing to %s." % (self.mtbls_id, json_output.name))
        summary = self.get_study_variable_summary()
        if summary is not None:
            dump(summary, json_output, indent=4)
            log.debug("Summary dumped to JSON")
            html_summary = build_html_summary(summary)
            with html_output as html_fp:
                html_fp.write(html_summary)
            return summary
        raise RuntimeError("Error getting study summary")

    ''' Not Tested '''
    def datatype_get_summary_command(self, output):
        log.info("Getting summary for study %s. Writing to %s." % (self.mtbls_id, output.name))
        summary = self.get_study_variable_summary()
        if summary is not None:
            dump(summary, output, indent=4)
            log.debug("Summary dumped")
            return summary
        raise RuntimeError("Error getting study summary")
