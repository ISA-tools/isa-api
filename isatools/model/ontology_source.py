from isatools.model.comments import Commentable


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

    def __init__(self, name, file='', version='', description='', comments=None):
        super().__init__(comments)

        self.__name = name
        self.__file = file
        self.__version = version
        self.__description = description

    @property
    def name(self):
        """:obj:`str`: name of the ontology source"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('OntologySource.name must be a str; got {0}:{1}'.format(val, type(val)))
        else:
            self.__name = val

    @property
    def file(self):
        """:obj:`str`: file of the ontology source"""
        return self.__file

    @file.setter
    def file(self, val):
        if not isinstance(val, str):
            raise AttributeError('OntologySource.file must be a str; got {0}:{1}'.format(val, type(val)))
        self.__file = val

    @property
    def version(self):
        """:obj:`str`: version of the ontology source"""
        return self.__version

    @version.setter
    def version(self, val):
        if not isinstance(val, str):
            raise AttributeError('OntologySource.version must be a str; got {0}:{1}'.format(val, type(val)))
        self.__version = val

    @property
    def description(self):
        """:obj:`str`: description of the ontology source"""
        return self.__description

    @description.setter
    def description(self, val):
        if not isinstance(val, str):
            raise AttributeError('OntologySource.description must be a str; got {0}:{1}'.format(val, type(val)))
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