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

    def test_sortlist(self):
        j1 = self.j1
        j2 = self.j2
        utils.sortlists(j1)
        utils.sortlists(j2)
        self.assertEqual(j1, j2)

    def test_assert_json_equal(self):
        self.assertTrue(utils.assert_json_equal(self.j1, self.j2))
        self.assertFalse(utils.assert_json_equal(self.j1, self.j3))

    def test_assert_xml_equal(self):
        self.fail()

    def test_assert_tab_content_equal(self):
        self.fail()
