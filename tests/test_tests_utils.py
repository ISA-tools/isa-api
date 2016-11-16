# coding: utf-8
import unittest
import os
from lxml import etree

from tests import utils


class TestUtils(unittest.TestCase):

    j1 = {
        "k1": "v1",
        "k2": "v2",
        "k3": [
            {
                "@id": "id1",
                "k1": "v1"
            },
            {
                "@id": "id2",
                "k1": "v2"
            }
        ],
        "k4": [
            {
                "@id": "id1"
            },
            {
                "@id": "id2"
            }
        ]
    }

    j2 = {
        "k3": [
            {
                "@id": "id2",
                "k1": "v2"
            },
            {
                "@id": "id1",
                "k1": "v1"
            }
        ],
        "k4": [
            {
                "@id": "id2"
            },
            {
                "@id": "id1"
            }
        ],
        "k2": "v2",
        "k1": "v1"
    }

    j3 = {
        "k3": [
            {
                "@id": "id2",
                "k1": "v2"
            },
            {
                "@id": "id1",
                "k1": "v1"
            }
        ],
        "k4": [
            {
                "@id": "id2"
            },
            {
                "@id": "id1"
            }
        ],
        "k2": "v2",
        "k1": "v1",
        "k5": "v1"
    }

    x1 = """<root>
        <e1>cdata1</e1>
        <e2>cdata2</e2>
        <e3>
            <e1 id="id1">cdata1</e1>
            <e1 id="id2">cdata2</e1>
        </e3>
        <e4>
            <e1 id="id2">cdata2</e1>
            <e1 id="id1">cdata1</e1>
        </e4>
    </root>"""

    x2 = """<root>
        <e3>
            <e1 id="id1">cdata1</e1>
            <e1 id="id2">cdata2</e1>
        </e3>
        <e4>
            <e1 id="id2">cdata2</e1>
            <e1 id="id1">cdata1</e1>
        </e4>
        <e2>cdata2</e2>
        <e1>cdata1</e1>
    </root>"""

    def setUp(self):
        self.i_tab1 = open(os.path.join(utils.TAB_DATA_DIR, 'BII-I-1', 'i_investigation.txt'))
        self.i_tab2 = open(os.path.join(utils.TAB_DATA_DIR, 'BII-I-1', 'i_investigation.txt'))
        self.s_tab1 = open(os.path.join(utils.TAB_DATA_DIR, 'BII-I-1', 's_BII-S-1.txt'))
        self.s_tab2 = open(os.path.join(utils.TAB_DATA_DIR, 'BII-I-1', 's_BII-S-1.txt'))

    def tearDown(self):
        self.i_tab1.close()
        self.i_tab2.close()
        self.s_tab1.close()
        self.s_tab2.close()

    def test_sortlistsj(self):
        j1 = self.j1
        j2 = self.j2
        utils.sortlistsj(j1)
        utils.sortlistsj(j2)
        self.assertEqual(j1, j2)

    def test_assert_json_equal(self):
        self.assertTrue(utils.assert_json_equal(self.j1, self.j2))
        self.assertFalse(utils.assert_json_equal(self.j1, self.j3))

    def test_assert_tab_content_equal_investigation(self):
        self.assertTrue(utils.assert_tab_content_equal(self.i_tab1, self.i_tab2))

    def test_assert_tab_content_equal_assay_table(self):
        self.assertTrue(utils.assert_tab_content_equal(self.s_tab1, self.s_tab2))

    def test_assert_xml_equal(self):
        self.assertTrue(utils.assert_xml_equal(etree.fromstring(self.x1), etree.fromstring(self.x2)))
