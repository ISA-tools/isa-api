import unittest
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

    def test_sortlistsj(self):
        j1 = self.j1
        j2 = self.j2
        utils.sortlistsj(j1)
        utils.sortlistsj(j2)
        self.assertEqual(j1, j2)

    def test_sortlistsx(self):
        x1 = self.x1
        x2 = self.x2
        utils.sortlistsx(x1)
        utils.sortlistsx(x2)
        self.assertEqual(x1, x2)

    def test_assert_json_equal(self):
        self.assertTrue(utils.assert_json_equal(self.j1, self.j2))
        self.assertFalse(utils.assert_json_equal(self.j1, self.j3))

    def test_assert_xml_equal(self):
        self.fail("Unfinished test code")

    def test_assert_tab_content_equal(self):
        self.fail("Unfinished test code")
