from datetime import datetime
from graphene.types import Scalar
from graphql.language import ast


class DateTime(Scalar):
    """
    Custom DateTime Scalar
    Inspired by: https://docs.graphene-python.org/en/latest/types/scalars/
    """

    @staticmethod
    def serialize(dt):
        return dt

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.strptime(
                node.value, "%Y-%m-%d")
        else:
            raise Exception("You must provide a string containing a date")

    @staticmethod
    def parse_value(value):
        return datetime.strptime(value, "%Y-%m-%d")


class StringOrInt(Scalar):
    """
    Custom String or Integer Scalar
    Inspired by https://kamranicus.com/handling-multiple-scalar-types-in-graphql/
    """

    @staticmethod
    def serialize(dt):
        if not isinstance(dt, str) and not isinstance(dt, int):
            raise Exception("Value must be a string or integer but is " + dt)
        return dt

    @staticmethod
    def parse_value(value):
        if not isinstance(value, str) and not isinstance(value, int):
            raise Exception("You must provide a string or integer")
        return value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue) and isinstance(node, ast.IntValue):
            return node.value
        else:
            raise Exception("You must provide a string or integer")

