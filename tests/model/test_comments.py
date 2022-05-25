import unittest

from isatools.model.comments import Commentable, Comment


class TestComment(unittest.TestCase):

    def setUp(self):
        self.comment = Comment(name='test_name', value='test_value')

    def test_empty_comment(self):
        comment = Comment()
        self.assertTrue(comment.name == '')
        self.assertTrue(comment.value == '')

    def test_properties(self):
        self.assertTrue(self.comment.name == 'test_name')
        self.assertTrue(self.comment.value == 'test_value')

    def test_builtins(self):
        expected_repr = "isatools.model.Comment(name='test_name', value='test_value')"
        self.assertTrue(self.comment.__repr__() == expected_repr)

        expected_str = "Comment(\n\tname=test_name\n\tvalue=test_value)"
        self.assertTrue(self.comment.__str__() == expected_str)

        expected_hash = hash(expected_repr)
        self.assertTrue(self.comment.__hash__() == expected_hash)

        new_comment = Comment(name='test_name2', value='test_value2')
        self.assertFalse(self.comment == new_comment)
        self.assertTrue(self.comment != new_comment)
        self.assertTrue(self.comment == Comment(name='test_name', value='test_value'))

    def test_setters(self):
        error_msg = 'Comment.name must be a string'
        with self.assertRaises(AttributeError) as context:
            self.comment.name = 1
        self.assertTrue(error_msg in str(context.exception))
        self.comment.name = 'new name'

        error_msg = 'Comment.value must be a string'
        with self.assertRaises(AttributeError) as context:
            self.comment.value = 1
        self.assertTrue(error_msg in str(context.exception))
        self.comment.value = 'new value'


class TestCommentable(unittest.TestCase):

    def setUp(self):
        self.comment = Comment(name='test_name', value='test_value')
        self.commentable = Commentable(comments=[self.comment])

    def test_empty_constructor(self):
        commentable = Commentable()
        self.assertTrue(commentable.comments == [])

    def test_properties(self):
        self.assertTrue(self.commentable.comments == [self.comment])

    def test_setters(self):
        with self.assertRaises(AttributeError) as context:
            self.commentable.comments = None
        self.assertTrue('Commentable.comments must be iterable containing Comments' in str(context.exception))
        self.commentable.comments = [self.comment, 'test']
        self.assertTrue(self.commentable.comments == [self.comment])

        with self.assertRaises(AttributeError) as context:
            self.commentable.comments = {'name': 'test_name2', 'value': 'test_value2'}
        self.assertTrue('Commentable.comments must be iterable containing Comments' in str(context.exception))

    def test_getters(self):
        self.assertIsNone(self.commentable.get_comment(name='123'))
        self.assertTrue(self.commentable.get_comment(name='test_name') == self.comment)
        self.assertTrue(self.commentable.get_comment_names() == ['test_name'])
        self.assertTrue(self.commentable.get_comment_values() == ['test_value'])

    def test_add_comment(self):
        comment = Comment(name='test_name2', value='test_value2')
        self.commentable.add_comment(name='test_name2', value_='test_value2')
        self.assertTrue(self.commentable.comments == [self.comment, comment])
        self.commentable.comments = [self.comment]

    def test_yield_comments(self):
        yield_comments = self.commentable.yield_comments(name='test_name')
        self.assertTrue(isinstance(yield_comments, filter))
        self.assertTrue(list(yield_comments) == [self.comment])
        yield_comments = self.commentable.yield_comments(name='test_name2')
        self.assertTrue(list(yield_comments) == [])
        yield_comments = self.commentable.yield_comments()
        self.assertTrue(list(yield_comments) == [self.comment])
