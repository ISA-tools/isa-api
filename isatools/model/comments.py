from typing import List, Any
from abc import ABCMeta


class Comment(object):
    """A Comment allows arbitrary annotation of all Commentable ISA classes

    Attributes:
        name: A string name for the comment context (maps to Comment[{name}])
        value: A string value for the comment.
    """

    def __init__(self, name: str = '', value: str = ''):
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        """:obj:`str`: name for the comment context"""
        return self.__name

    @name.setter
    def name(self, val: str):
        if not isinstance(val, str):
            raise AttributeError('Comment.name must be a string')
        self.__name = val

    @property
    def value(self) -> str:
        """:obj:`str`: value for the comment content"""
        return self.__value

    @value.setter
    def value(self, val: str):
        if not isinstance(val, str):
            raise AttributeError('Comment.value must be a string')
        self.__value = val

    def __repr__(self):
        return "isatools.model.Comment(name='{comment.name}', value='{comment.value}')".format(comment=self)

    def __str__(self):
        return "Comment(\n\tname={comment.name}\n\tvalue={comment.value})".format(comment=self)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: Any):
        return isinstance(other, Comment) and self.name == other.name and self.value == other.value

    def __ne__(self, other: Any):
        return not self == other

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value
        }


class Commentable(metaclass=ABCMeta):
    """Abstract class to enable containment of Comments

    Attributes:
        comments: Comments associated with the implementing ISA class.
    """

    def __init__(self, comments: List[Comment] = None):
        self.__comments = [] if comments is None else comments

    @property
    def comments(self) -> List[Comment]:
        """:obj:`list` of :obj:`Comment`: Container for ISA comments"""
        return self.__comments

    @comments.setter
    def comments(self, val: List[Comment]):
        if not isinstance(val, list):
            raise AttributeError('Commentable.comments must be iterable containing Comments')
        if val == [] or all(isinstance(x, Comment) for x in val):
            self.__comments = list(val)

    def add_comment(self, name: str = None, value_: str = None):
        """Adds a new comment to the comment list.

        Args:
            name: Comment name
            value_: Comment value
        """
        self.comments.append(Comment(name=name, value=value_))

    def yield_comments(self, name: str = None) -> filter:
        """Gets an iterator of matching comments for a given name.

        Args:
            name: Comment name

        Returns:
            :obj:`filter` of :obj:`Comments` that can be iterated on.
        """
        return filter(lambda x: x.name == name if name else x, self.comments)

    def get_comment(self, name: str) -> Comment: 
        """Gets the first matching comment for a given name

        Args:
            name: Comment name

        Returns:
            :obj:`Comment` matching the name. Only returns the first found.

        """
        comments = list(self.yield_comments(name=name))
        return comments[-1] if len(comments) > 0 else None

    def get_comment_names(self) -> List[str]:
        """ Gets all the comments names
        """
        return [x.name for x in self.comments]

    def get_comment_values(self) -> List[str]:
        """ Gets all the comments values
        """
        return [x.value for x in self.comments]
