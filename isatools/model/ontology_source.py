import os

from typing import List, Any
from isatools.model.comments import Commentable, Comment
from isatools.model.utils import get_context_path


class OntologySource(Commentable):
    """An OntologySource describes the resource from which the value of an
    OntologyAnnotation is derived from.

    Attributes:
        name: The name of the source of a term; i.e. the source controlled
            vocabulary or ontology.
        file: A file name or a URI of an official resource.
        version: The version number of the Term Source to support terms
            tracking.
        description: A free text description of the resource.
        comments: Comments associated with instances of this class.
    """

    def __init__(self,
                 name: str,
                 file: str = '',
                 version: str = '',
                 description: str = '',
                 comments: List[Comment] = None):
        super().__init__(comments)

        self.__name = name
        self.__file = file
        self.__version = version
        self.__description = description

        self.name = name
        self.file = file
        self.version = version
        self.description = description

    @property
    def name(self):
        """:obj:`str`: name of the ontology source"""
        return self.__name

    @staticmethod
    def validate_field(val: Any, field_name: str):
        """ Validates that the given value is a valid value for the given field

        @param val: the value to validate
        @param field_name: the name of the field to validate
        """
        if not isinstance(val, str):
            raise AttributeError('OntologySource.{0} must be a str; got {1}:{2}'.format(field_name,
                                                                                        val,
                                                                                        type(val)))

    @name.setter
    def name(self, val):
        self.validate_field(val, 'name')
        self.__name = val

    @property
    def file(self):
        """:obj:`str`: file of the ontology source"""
        return self.__file

    @file.setter
    def file(self, val):
        self.validate_field(val, 'file')
        self.__file = val

    @property
    def version(self):
        """:obj:`str`: version of the ontology source"""
        return self.__version

    @version.setter
    def version(self, val):
        self.validate_field(val, 'version')
        self.__version = val

    @property
    def description(self):
        """:obj:`str`: description of the ontology source"""
        return self.__description

    @description.setter
    def description(self, val):
        self.validate_field(val, 'description')
        self.__description = val

    def __repr__(self):
        return ("isatools.model.OntologySource(name='{ontology_source.name}', "
                "file='{ontology_source.file}', "
                "version='{ontology_source.version}', "
                "description='{ontology_source.description}', "
                "comments={ontology_source.comments})").format(ontology_source=self)

    def __str__(self):
        return ("OntologySource(\n\t"
                "name={ontology_source.name}\n\t"
                "file={ontology_source.file}\n\t"
                "version={ontology_source.version}\n\t"
                "description={ontology_source.description}\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(ontology_source=self, num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, OntologySource) \
               and self.name == other.name \
               and self.file == other.file \
               and self.version == other.version \
               and self.description == other.description \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {
            '@id': self.id,
            'name': self.name,
            'file': self.file,
            'version': self.version,
            'description': self.description,
            'comments': [comment.to_dict() for comment in self.comments]
        }

    def to_ld(self, context: str = "obo"):
        if context not in ["obo", "sdo", "wdt"]:
            raise ValueError("context should be obo, sdo or wdt but got %s" % context)

        context_path = get_context_path("ontology_source_reference", context)
        ontology_source_reference = self.to_dict()
        ontology_source_reference["@type"] = "OntologySourceReference"
        ontology_source_reference["@context"] = context_path
        ontology_source_reference["@id"] = "#ontology_source_reference/" + self.id

    def from_dict(self, ontology_source):
        self.name = ontology_source['name'] if 'name' in ontology_source else ''
        self.file = ontology_source['file'] if 'file' in ontology_source else ''
        self.version = ontology_source['version'] if 'version' in ontology_source else ''
        self.description = ontology_source['description'] if 'description' in ontology_source else ''
        self.load_comments(ontology_source.get('comments', []))
