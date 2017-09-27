"""Tests on isatools.model classes"""
from __future__ import absolute_import
import unittest

from isatools.model import *


class CommentTest(unittest.TestCase):

    def setUp(self):
        self.comment_default = Comment()
        self.comment = Comment(name='N', value='V')

    def test_repr(self):
        self.assertEqual('isatools.model.Comment(name="", value="")',
                         repr(self.comment_default))
        self.assertEqual('isatools.model.Comment(name="N", value="V")',
                         repr(self.comment))

    def test_str(self):
        self.assertEqual('Comment[]\t',
                         str(self.comment_default))
        self.assertEqual('Comment[N]\tV',
                         str(self.comment))

    def test_eq(self):
        expected_comment = Comment(name='N', value='V')
        self.assertEqual(expected_comment, self.comment)
        self.assertEqual(hash(expected_comment), hash(self.comment))

    def test_ne(self):
        expected_other_comment = Comment(name='V', value='N')
        self.assertNotEqual(expected_other_comment, self.comment)
        self.assertNotEqual(hash(expected_other_comment), hash(self.comment))

    def test_raises_ISAModelAttributeError(self):
        try:
            self.comment_default.name = 0
        except ISAModelAttributeError:
            pass
        except Exception:
            self.fail('ISAModelAttributeError not raised')

        try:
            self.comment_default.value = 0
        except ISAModelAttributeError:
            pass
        except Exception:
            self.fail('ISAModelAttributeError not raised')