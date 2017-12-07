"""Tests on isatools.utils package"""
from __future__ import absolute_import

import json
import logging
import os
import shutil
import tempfile
import unittest
from io import StringIO
from jsonschema.exceptions import ValidationError


from isatools import isajson
from isatools import isatab
from isatools import utils
from isatools.model import *
from isatools.net import mtbls as MTBLS
from isatools.net import ols
from isatools.net import pubmed

from isatools.tests import utils as test_utils


log = logging.getLogger('isatools')


def setUpModule():
    if not os.path.exists(test_utils.DATA_DIR):
        raise FileNotFoundError('Could not fine test data directory in {0}. '
                                'Ensure you have cloned the ISAdatasets '
                                'repository using git clone -b tests '
                                '--single-branch git@github.com:ISA-tools/'
                                'ISAdatasets {0}'
                                .format(test_utils.DATA_DIR))


class TestIsaGraph(unittest.TestCase):

    def test_detect_graph_process_pooling(self):
        with open(os.path.join(
                test_utils.JSON_DATA_DIR, 'MTBLS1', 'MTBLS1.json')) as \
                isajson_fp:
            ISA = isajson.load(isajson_fp)
            for study in ISA.studies:
                utils.detect_graph_process_pooling(study.graph)
                for assay in study.assays:
                    pooling_list = utils.detect_graph_process_pooling(
                        assay.graph)
                    self.assertListEqual(
                        sorted(pooling_list),
                        sorted(['#process/Extraction1', '#process/NMR_assay1']))

    def test_detect_graph_process_pooling_batch_on_mtbls(self):
        for i in range(1, 1):
            try:
                J = MTBLS.getj('MTBLS{}'.format(i))
                ISA = isajson.load(StringIO(json.dumps(J)))
                for study in ISA.studies:
                    utils.detect_graph_process_pooling(study.graph)
                    for assay in study.assays:
                        utils.detect_graph_process_pooling(assay.graph)
            except IOError:
                log.error('IO Error, skipping...')
            except KeyError:
                log.error('KeyError, skipping...')
            except AttributeError:
                log.error('AttributeError, skipping...')
            except ValidationError:
                log.error('jsonschema ValidationError, skipping...')


class TestOlsSearch(unittest.TestCase):

    def test_get_ontologies(self):
        ontology_sources = ols.get_ols_ontologies()
        self.assertGreater(len(ontology_sources), 0)
        self.assertIsInstance(ontology_sources, list)
        self.assertIsInstance(ontology_sources[0], OntologySource)

    def test_get_ontology(self):
        ontology_source = ols.get_ols_ontology('efo')
        self.assertIsInstance(ontology_source, OntologySource)
        self.assertEqual(ontology_source.name, 'efo')
        self.assertEqual(
            ontology_source.file,
            'https://www.ebi.ac.uk/ols/api/ontologies/efo')
        self.assertIsInstance(ontology_source.version, str)
        self.assertEqual(
            ontology_source.description, 'Experimental Factor Ontology')

    def test_search_for_term(self):
        ontology_source = ols.get_ols_ontology('efo')
        ontology_annotations = ols.search_ols('cell type', ontology_source)
        self.assertIsInstance(ontology_annotations, list)
        self.assertGreater(len(ontology_annotations), 0)
        ontology_anotations = [oa for oa in ontology_annotations if 
                               oa.term == 'cell type']
        self.assertIsInstance(ontology_anotations[-1], OntologyAnnotation)
        self.assertEqual(ontology_anotations[-1].term, 'cell type')
        self.assertIn('http://www.ebi.ac.uk/efo/EFO_0000324',
                      [oa.term_accession for oa in ontology_anotations])
        self.assertEqual(ontology_anotations[-1].term_source, ontology_source)


class TestISArchiveExport(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_create_isatab_archive_missing_files(self):
        with open(os.path.join(
                test_utils.TAB_DATA_DIR, 'BII-I-1', 
                'i_investigation.txt')) as fp:
            result = utils.create_isatab_archive(inv_fp=fp)
            self.assertIsNone(result)  # returns None if can't create archive

    def test_create_isatab_archive(self):
        with open(os.path.join(
                test_utils.TAB_DATA_DIR, 'BII-S-3', 'i_gilbert.txt')) as fp:
            result = utils.create_isatab_archive(inv_fp=fp)
            self.assertIsInstance(result, list)
            self.assertListEqual(sorted(result),
                                 sorted(['i_gilbert.txt', 
                                         's_BII-S-3.txt', 
                                         'a_gilbert-assay-Gx.txt',
                                         'a_gilbert-assay-Tx.txt', 
                                         'EXHS9OF02.sff', 'EXHS9OF01.sff',
                                         'EWOEPZA01.sff', 'EWOEPZA02.sff', 
                                         'EX398L101.sff', 'EX398L102.sff',
                                         'EVHINN105.sff', 'EVNG8PH04.sff', 
                                         'EVUSNDQ01.sff', 'EVHINN102.sff',
                                         'EVHINN113.sff', 'EVUSNDQ02.sff', 
                                         'EVHINN101.sff', 'EVNG8PH01.sff',
                                         'EVHINN106.sff', 'EVHINN108.sff', 
                                         'EVHINN116.sff', 'EVHINN104.sff',
                                         'EVHINN110.sff', 'EVHINN107.sff', 
                                         'EVUSNDQ03.sff', 'EVHINN103.sff',
                                         'EVHINN112.sff', 'EVUSNDQ04.sff', 
                                         'EVHINN115.sff', 'EVNG8PH02.sff',
                                         'EVHINN114.sff', 'EVHINN111.sff', 
                                         'EVNG8PH03.sff', 'EVHINN109.sff']))

    def test_create_isatab_archive_filter_on_transcription_profiling(self):
        with open(os.path.join(
                test_utils.TAB_DATA_DIR, 'BII-S-3', 'i_gilbert.txt')) as fp:
            result = utils.create_isatab_archive(
                inv_fp=fp, filter_by_measurement='transcription profiling')
            self.assertIsInstance(result, list)
            self.assertListEqual(sorted(result),
                                 sorted(['i_gilbert.txt', 's_BII-S-3.txt', 
                                         'a_gilbert-assay-Tx.txt', 
                                         'EVHINN105.sff', 'EVNG8PH04.sff', 
                                         'EVUSNDQ01.sff', 'EVHINN102.sff', 
                                         'EVHINN113.sff', 'EVUSNDQ02.sff', 
                                         'EVHINN101.sff', 'EVNG8PH01.sff', 
                                         'EVHINN106.sff', 'EVHINN108.sff', 
                                         'EVHINN116.sff', 'EVHINN104.sff', 
                                         'EVHINN110.sff', 'EVHINN107.sff', 
                                         'EVUSNDQ03.sff', 'EVHINN103.sff', 
                                         'EVHINN112.sff', 'EVUSNDQ04.sff', 
                                         'EVHINN115.sff', 'EVNG8PH02.sff', 
                                         'EVHINN114.sff', 'EVHINN111.sff', 
                                         'EVNG8PH03.sff', 'EVHINN109.sff']))


class TestPubMedIDUtil(unittest.TestCase):

    def test_get_pubmed_article(self):
        J = pubmed.get_pubmed_article('25520553')
        self.assertEqual(J['doi'], '10.4137/CIN.S13895')
        self.assertEqual(J['authors'], ['Johnson D', 'Connor AJ', 'McKeever S', 
                                        'Wang Z', 'Deisboeck TS', 'Quaiser T', 
                                        'Shochat E'])
        self.assertEqual(J['year'], '2014')
        self.assertEqual(J['journal'], 'Cancer Inform')
        self.assertEqual(
            J['title'], 'Semantically linking in silico cancer models.')

    def test_set_pubmed_article(self):
        p = Publication(pubmed_id='25520553')
        pubmed.set_pubmed_article(p)
        self.assertEqual(p.doi, '10.4137/CIN.S13895')
        self.assertEqual(p.author_list, 'Johnson D, Connor AJ, McKeever S, '
                                        'Wang Z, Deisboeck TS, Quaiser T, '
                                        'Shochat E')
        self.assertEqual(
            p.title, 'Semantically linking in silico cancer models.')
        self.assertIsInstance(p.comments[0], Comment)
        self.assertEqual(p.comments[0].name, 'Journal')
        self.assertEqual(p.comments[0].value, 'Cancer Inform')


class TestIsaTabFixer(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        src_tab = os.path.join(test_utils.TAB_DATA_DIR, 'BII-S-3')
        dst_tab = os.path.join(self._tmp_dir, 'BII-S-3')
        shutil.copytree(src_tab, dst_tab)

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_replace_factor_with_source_characteristic(self):
        s_table_path = os.path.join(self._tmp_dir, 'BII-S-3', 's_BII-S-3.txt')
        fixer = utils.IsaTabFixer(s_table_path)
        fixer.replace_factor_with_source_characteristic('dose')

        expected_field_names = [
            'Source Name',
            'Characteristics[dose]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[organism]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (country and/or sea,region)]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (longitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (latitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chlorophyll a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[peridinin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[butfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[hexfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[alloxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[zeaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[lutein concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c3 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c2 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[prasinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[neoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[violaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diadinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diatoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[BB carotene concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[bacteria count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[synechococcus count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[small picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[large picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nanoflagellates count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[cryptophytes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[phosphate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nitrate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic nitrogen concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic carbon concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[primary production depth integrated production to '
            '3 m expressed_in mgC m-2 d-1]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[water salinity]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fluorescence]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[water temperature at 3 meter depth]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Protocol REF',
            'Parameter Value[filter pore size]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Sample Name',
            'Factor Value[compound]',
            'Term Source REF', 'Term Accession Number',
            'Factor Value[collection time]',
            'Term Source REF', 'Term Accession Number']

        with open(s_table_path) as fixed_tab_fp:
            actual_field_names = list(
                map(lambda field_name: field_name.strip(),
                    next(fixed_tab_fp).split('\t')))
            self.assertListEqual(actual_field_names, expected_field_names)

    def test_replace_factor_with_protocol_parameter_value(self):
        s_table_path = os.path.join(self._tmp_dir, 'BII-S-3', 's_BII-S-3.txt')
        fixer = utils.IsaTabFixer(s_table_path)
        fixer.replace_factor_with_protocol_parameter_value(
            'dose', 'environmental material collection - standard procedure 1')

        expected_field_names = [
            'Source Name',
            'Characteristics[organism]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (country and/or sea,region)]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (longitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (latitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chlorophyll a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[peridinin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[butfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[hexfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[alloxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[zeaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[lutein concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c3 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c2 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[prasinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[neoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[violaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diadinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diatoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[BB carotene concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[bacteria count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[synechococcus count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[small picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[large picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nanoflagellates count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[cryptophytes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[phosphate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nitrate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic nitrogen concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic carbon concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[primary production depth integrated production to '
            '3 m expressed_in mgC m-2 d-1]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[water salinity]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fluorescence]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[water temperature at 3 meter depth]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Protocol REF',
            'Parameter Value[dose]',
            'Term Source REF', 'Term Accession Number',
            'Parameter Value[filter pore size]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Sample Name',
            'Factor Value[compound]',
            'Term Source REF', 'Term Accession Number',
            'Factor Value[collection time]',
            'Term Source REF', 'Term Accession Number']

        with open(s_table_path + '.fix') as fixed_tab_fp:
            actual_field_names = list(
                map(lambda field_name: field_name.strip(),
                    next(fixed_tab_fp).split('\t')))
            self.assertListEqual(actual_field_names, expected_field_names)


        # check the parameter got added to the protocol
        with open(os.path.dirname(
                s_table_path) + '/i_Investigation.txt.fix') as fixed_i_fp:
            investigation = isatab.load(fixed_i_fp)
            study = investigation.studies[-1]
            protocol = study.get_prot(
                'environmental material collection - standard procedure 1')
            param = protocol.get_param('dose')
            self.assertIsNotNone(param)

    def test_fix_factor_one_arg(self):
        s_table_path = os.path.join(self._tmp_dir, 'BII-S-3', 's_BII-S-3.txt')
        fixer = utils.IsaTabFixer(s_table_path)
        fixer.fix_factor('dose')

        expected_field_names = [
            'Source Name',
            'Characteristics[dose]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[organism]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (country and/or sea,region)]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (longitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (latitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chlorophyll a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[peridinin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[butfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[hexfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[alloxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[zeaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[lutein concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c3 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c2 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[prasinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[neoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[violaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diadinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diatoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[BB carotene concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[bacteria count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[synechococcus count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[small picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[large picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nanoflagellates count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[cryptophytes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[phosphate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nitrate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic nitrogen concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic carbon concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[primary production depth integrated production to '
            '3 m expressed_in mgC m-2 d-1]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[water salinity]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fluorescence]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[water temperature at 3 meter depth]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Protocol REF',
            'Parameter Value[filter pore size]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Sample Name',
            'Factor Value[compound]',
            'Term Source REF', 'Term Accession Number',
            'Factor Value[collection time]',
            'Term Source REF', 'Term Accession Number']

        with open(s_table_path) as fixed_tab_fp:
            actual_field_names = list(
                map(lambda field_name: field_name.strip(),
                    next(fixed_tab_fp).split('\t')))
            self.assertListEqual(actual_field_names, expected_field_names)

    def test_fix_factor_two_args(self):
        s_table_path = os.path.join(self._tmp_dir, 'BII-S-3', 's_BII-S-3.txt')
        fixer = utils.IsaTabFixer(s_table_path)
        fixer.fix_factor(
            'dose', 'environmental material collection - standard procedure 1')

        expected_field_names = [
            'Source Name',
            'Characteristics[organism]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (country and/or sea,region)]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (longitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (latitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chlorophyll a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[peridinin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[butfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[hexfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[alloxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[zeaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[lutein concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c3 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c2 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[prasinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[neoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[violaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diadinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diatoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[BB carotene concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[bacteria count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[synechococcus count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[small picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[large picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nanoflagellates count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[cryptophytes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[phosphate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nitrate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic nitrogen concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic carbon concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[primary production depth integrated production to '
            '3 m expressed_in mgC m-2 d-1]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[water salinity]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fluorescence]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[water temperature at 3 meter depth]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Protocol REF',
            'Parameter Value[dose]',
            'Term Source REF', 'Term Accession Number',
            'Parameter Value[filter pore size]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Sample Name',
            'Factor Value[compound]',
            'Term Source REF', 'Term Accession Number',
            'Factor Value[collection time]',
            'Term Source REF', 'Term Accession Number']

        # check the columns got moved in the study file
        with open(s_table_path + '.fix') as fixed_tab_fp:
            actual_field_names = list(
                map(lambda field_name: field_name.strip(),
                    next(fixed_tab_fp).split('\t')))
            self.assertListEqual(actual_field_names, expected_field_names)

        # check the param got added to protocol and factor removed from study
        with open(os.path.dirname(
                s_table_path) + '/i_Investigation.txt.fix') as fixed_i_fp:
            investigation = isatab.load(fixed_i_fp)
            study = investigation.studies[-1]
            protocol = study.get_prot(
                'environmental material collection - standard procedure 1')
            param = protocol.get_param('dose')
            self.assertIsNotNone(param)
            factor = study.get_factor('dose')
            self.assertIsNone(factor)

    def test_batch_fixer(self):
        s_table_path = os.path.join(self._tmp_dir, 'BII-S-3', 's_BII-S-3.txt')
        settings = {
            s_table_path: {
                        "factor": "dose",
                        "protocol_ref": "environmental material collection - "
                                        "standard procedure 1"
                    }
                }
        utils.batch_fix_isatabs(settings)

        expected_field_names = [
            'Source Name',
            'Characteristics[organism]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (country and/or sea,region)]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (longitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[geographic location (latitude)]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chlorophyll a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[peridinin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[butfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[hexfucoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[alloxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[zeaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[lutein concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c3 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-c2 concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[prasinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[neoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[violaxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diadinoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[diatoxanthin concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-b concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[divinyl-chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[chl-a concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[BB carotene concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[bacteria count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[synechococcus count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[small picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[large picoeukaryotes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nanoflagellates count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[cryptophytes count]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[phosphate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[nitrate concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic nitrogen concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[particulate organic carbon concentration]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[primary production depth integrated production to '
            '3 m expressed_in mgC m-2 d-1]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[water salinity]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Characteristics[fluorescence]',
            'Term Source REF', 'Term Accession Number',
            'Characteristics[water temperature at 3 meter depth]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Protocol REF',
            'Parameter Value[dose]',
            'Term Source REF', 'Term Accession Number',
            'Parameter Value[filter pore size]',
            'Unit', 'Term Source REF', 'Term Accession Number',
            'Sample Name',
            'Factor Value[compound]',
            'Term Source REF', 'Term Accession Number',
            'Factor Value[collection time]',
            'Term Source REF', 'Term Accession Number']

        # check the columns got moved in the study file
        with open(s_table_path + '.fix') as fixed_tab_fp:
            actual_field_names = list(
                map(lambda field_name: field_name.strip(),
                    next(fixed_tab_fp).split('\t')))
            self.assertListEqual(actual_field_names, expected_field_names)

        # check the parameter got added to the protocol
        with open(os.path.dirname(
                s_table_path) + '/i_Investigation.txt.fix') as fixed_i_fp:
            investigation = isatab.load(fixed_i_fp)
            study = investigation.studies[-1]
            protocol = study.get_prot(
                'environmental material collection - standard procedure 1')
            param = protocol.get_param('dose')
            self.assertIsNotNone(param)