import pandas as pd
from pandas.util.testing import assert_frame_equal
from isatools.isatab import read_investigation_file
import os

_data_dir = os.path.join(os.path.dirname(__file__), 'data')

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'isatools', 'sampledata')

JSON_DATA_DIR = os.path.join(_data_dir, 'json')
UNIT_JSON_DATA_DIR = os.path.join(JSON_DATA_DIR, 'unit')

SRA_DATA_DIR = os.path.join(_data_dir, 'sra')

TAB_DATA_DIR = os.path.join(_data_dir, 'tab')

CONFIGS_DATA_DIR = os.path.join(_data_dir, 'configs')
XML_CONFIGS_DATA_DIR = os.path.join(CONFIGS_DATA_DIR, 'xml')
DEFAULT2015_XML_CONFIGS_DATA_DIR = os.path.join(XML_CONFIGS_DATA_DIR, 'isaconfig-default_v2015-07-02')
SRA2016_XML_CONFIGS_DATA_DIR = os.path.join(XML_CONFIGS_DATA_DIR, 'isaconfig-seq_v2016-08-30-SRA1.5-august2014mod')
JSON_DEFAULT_CONFIGS_DATA_DIR = os.path.join(_data_dir, CONFIGS_DATA_DIR, 'json_default')
JSON_SRA_CONFIGS_DATA_DIR = os.path.join(_data_dir, CONFIGS_DATA_DIR, 'json_sra')


def assert_tab_content_equal(fp_x, fp_y):
    """
    Test for equality of tab files, only down to level of content - should not be taken as canonical equality, but
    rather that all the expected content matches to both input files, but not the order in which they appear.

    For more precise equality, you will need to apply a configuration
        - use assert_tab_equal_by_config(fp_x, fp_y, config)
    :param fp_x: File descriptor of a ISAtab file
    :param fp_y: File descriptor of another  ISAtab file
    :return: True or False plus any AssertionErrors
    """

    def _assert_df_equal(x, y):  # need to sort values to loosen up how equality is calculated
        try:
            assert_frame_equal(x.sort_values(by=x.columns[0]), y.sort_values(by=y.columns[0]))
            return True
        except AssertionError as e:
            print(e)
            return False

    from os.path import basename
    if basename(fp_x.name).startswith('i_'):
        df_dict_x = read_investigation_file(fp_x)
        df_dict_y = read_investigation_file(fp_y)
        eq = True
        for k in df_dict_x.keys():
            dfx = df_dict_x[k]
            dfy = df_dict_y[k]
            if not isinstance(dfx, list):
                if not _assert_df_equal(dfx, dfy):
                    eq = False
                    break
            else:
                try:
                    for x, y in zip(sorted(dfx), sorted(dfy)):
                        if not _assert_df_equal(x, y):
                            eq = False
                            break
                except ValueError as e:
                    print(e)
        return eq
    else:

        def diff(a, b):
            b = set(b)
            return [aa for aa in a if aa not in b]

        import numpy as np
        df_x = pd.read_csv(fp_x, sep='\t', encoding='utf-8')
        df_y = pd.read_csv(fp_y, sep='\t', encoding='utf-8')
        try:
            # drop empty columns
            df_x = df_x.replace('', np.nan)
            df_x = df_x.dropna(axis=1, how='all')
            df_x = df_x.replace(np.nan, '')
            df_y = df_y.replace('', np.nan)
            df_y = df_y.dropna(axis=1, how='all')
            df_y = df_y.replace(np.nan, '')

            is_cols_equal = set([x.split('.', 1)[0] for x in df_x.columns]) == set([x.split('.', 1)[0] for x in df_y.columns])
            if not is_cols_equal:
                print('x: ' + str(df_x.columns))
                print('y: ' + str(df_y.columns))
                print(diff(df_x.columns, df_y.columns))
                raise AssertionError("Columns in x do not match those in y")

            # reindex to add contexts for duplicate named columns (i.e. Term Accession Number, Unit, etc.)
            import re
            char_regex = re.compile('Characteristics\[(.*?)\]')
            pv_regex = re.compile('Parameter Value\[(.*?)\]')
            fv_regex = re.compile('Factor Value\[(.*?)\]')
            newcolsx = list()
            for col in df_x.columns:
                newcolsx.append(col)
            for i, col in enumerate(df_x.columns):
                if char_regex.match(col) or pv_regex.match(col) or fv_regex.match(col):
                    try:
                        if 'Unit' in df_x.columns[i+1]:
                            newcolsx[i+1] = col + '/Unit'
                            if 'Term Source REF' in df_x.columns[i+2]:
                                newcolsx[i+2] = col + '/Unit/Term Source REF'
                            if 'Term Accession Number' in df_x.columns[i+3]:
                                newcolsx[i+3] = col + '/Unit/Term Accession Number'
                        elif 'Term Source REF' in df_x.columns[i+1]:
                            newcolsx[i+1] = col + '/Term Source REF'
                            if 'Term Accession Number' in df_x.columns[i+2]:
                                newcolsx[i+2] = col + '/Term Accession Number'
                    except IndexError:
                        pass
            df_x.columns = newcolsx
            newcolsy = list()
            for col in df_y.columns:
                newcolsy.append(col)
            for i, col in enumerate(df_y.columns):
                if char_regex.match(col) or pv_regex.match(col) or fv_regex.match(col):
                    try:
                        if 'Unit' in df_y.columns[i+1]:
                            newcolsy[i+1] = col + '/Unit'
                            if 'Term Source REF' in df_y.columns[i+2]:
                                newcolsy[i+2] = col + '/Unit/Term Source REF'
                            if 'Term Accession Number' in df_y.columns[i+3]:
                                newcolsy[i+3] = col + '/Unit/Term Accession Number'
                        elif 'Term Source REF' in df_y.columns[i+1]:
                            newcolsy[i+1] = col + '/Term Source REF'
                            if 'Term Accession Number' in df_y.columns[i+2]:
                                newcolsy[i+2] = col + '/Term Accession Number'
                    except IndexError:
                        pass
            df_y.columns = newcolsy
            for colx in df_x.columns:
                for eachx, eachy in zip(df_x.sort_values(by=colx)[colx], df_y.sort_values(by=colx)[colx]):
                    if eachx != eachy:
                        print(df_x[colx])
                        print(df_y[colx])
                        raise AssertionError("Value: " + str(eachx) + ", does not match: " + str(eachy))
            # print("Well, you got here so the files must be same-ish... well done, you!")
            return True
        except AssertionError as e:
            print(str(e))
            return False


def sortlistsj(J):
    if isinstance(J, dict):
        for k in J.keys():
            sortlistsj(J[k])
    elif isinstance(J, list):
        for o in J:
            if isinstance(o, dict) or isinstance(o, list):
                sortlistsj(o)
        if len(J) > 1:
            J.sort(key=lambda i: str(i.values()))


def sortlistsx(X):
    return X


def assert_json_equal(jx, jy):
    import json
    jx = json.loads(json.dumps(jx, sort_keys=True))
    jy = json.loads(json.dumps(jy, sort_keys=True))
    sortlistsj(jx)
    sortlistsj(jy)
    if jx == jy:
        return True
    else:
        from deepdiff import DeepDiff
        print('DeepDiff={}'.format(DeepDiff(jx, jy)))
        return False


def assert_xml_equal(x1, x2):
    # Only counts tags of x1 and x2 to check if the right number appear in each

    def collect_tags(X):
        foundtags = set()
        for node in X.iter():
            foundtags.add(node.tag)
        return foundtags

    x1tags = collect_tags(x1)
    x2tags = collect_tags(x2)
    if len(x1tags - x2tags) > 0 or len(x2tags - x1tags) > 0:
        print("Collected tags don't match: ", x1tags, x2tags)
        return False
    else:
        for tag in x1tags:
            tagcount1 = x1.xpath('count(//{})'.format(tag))
            tagcount2 = x2.xpath('count(//{})'.format(tag))
            if tagcount1 != tagcount2:
                print("Counts of {0} tag do not match {1}:{2}".format(tag, int(tagcount1), int(tagcount2)))
                return False
        return True


def strip_ids(J):
    for k, v in J.items():
        if isinstance(v, dict):
            strip_ids(v)
        elif isinstance(v, list):
            for i in v:
                strip_ids(i)
        else:
            if k == '@id':
                J[k] = ''
