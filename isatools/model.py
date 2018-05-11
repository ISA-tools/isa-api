"""ISA Model 1.0 implementation in Python.

This module implements the ISA Abstract Model 1.0 as Python classes, as
specified in the `ISA Model and Serialization Specifications 1.0`_, and
additional classes to support compatibility between ISA-Tab and ISA-JSON.

Todo:
    * Check consistency with published ISA Model
    * Finish docstringing rest of the module
    * Add constraints on attributes throughout, and test

.. _ISA Model and Serialization Specs 1.0: http://isa-specs.readthedocs.io/

"""
from __future__ import absolute_import
import abc
import logging
import networkx as nx
import warnings


from isatools.errors import ISAModelAttributeError


log = logging.getLogger('isatools')

def _build_assay_graph(process_sequence=None):
    """:obj:`networkx.DiGraph` Returns a directed graph object based on a
    given ISA process sequence."""
    g = nx.DiGraph()
    if process_sequence is None:
        return g
    for process in process_sequence:
        if process.next_process is not None or len(
                process.outputs) > 0:
            if len([n for n in process.outputs if
                    not isinstance(n, DataFile)]) > 0:
                for output in [n for n in process.outputs if
                               not isinstance(n, DataFile)]:
                    g.add_edge(process, output)
            else:
                g.add_edge(process, process.next_process)

        if process.prev_process is not None or len(process.inputs) > 0:
            if len(process.inputs) > 0:
                for input_ in process.inputs:
                    g.add_edge(input_, process)
            else:
                g.add_edge(process.prev_process, process)
    return g


class Comment(object):
    """A Comment allows arbitrary annotation of all Commentable ISA classes

    Attributes:
        name: A string name for the comment context (maps to Comment[{name}])
        value: A string value for the comment.
    """

    def __init__(self, name='', value=''):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        """:obj:`str`: name for the comment context"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and isinstance(val, str):
            self.__name = val
        else:
            raise ISAModelAttributeError('Comment.name must be a string')

    @property
    def value(self):
        """:obj:`str`: value for the comment content"""
        return self.__value

    @value.setter
    def value(self, val):
        if isinstance(val, str):
            self.__value = val
        raise ISAModelAttributeError('Comment.value must be a string')

    def __repr__(self):
        return "isatools.model.Comment(name='{comment.name}', " \
               "value='{comment.value}')".format(comment=self)

    def __str__(self):
        return """Comment(
    name={comment.name}
    value={comment.value}
)""".format(comment=self)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Comment) \
               and self.name == other.name \
               and self.value == other.value

    def __ne__(self, other):
        return not self == other


class Commentable(metaclass=abc.ABCMeta):
    """Abstract class to enable containment of Comments

    Attributes:
        comments: Comments associated with the implementing ISA class.
    """
    def __init__(self, comments=None):
        if comments is None:
            self.__comments = []
        else:
            self.__comments = comments

    @property
    def comments(self):
        """:obj:`list` of :obj:`Comment`: Container for ISA comments"""
        return self.__comments

    @comments.setter
    def comments(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Comment) for x in val):
                self.__comments = list(val)
        else:
            raise ISAModelAttributeError(
                '{0}.comments must be iterable containing Comments'
                .format(type(self).__name__))

    def add_comment(self, name=None, value_=None):
        """Adds a new comment to the comment list.

        Args:
            name: Comment name
            value_: Comment value
        """
        c = Comment(name=name, value=value_)
        self.comments.append(c)

    def yield_comments(self, name=None):
        """Gets an iterator of matching comments for a given name.

        Args:
            name: Comment name

        Returns:
            :obj:`filter` of :obj:`Comments` that can be iterated on.
        """
        if name is None:
            return filter(True, self.comments)
        else:
            return filter(lambda x: x.name == name, self.comments)

    def get_comments(self):
        """Gets a list of all comments.

        Returns:
            :obj:`list` of :obj:`Comment` of all comments, if any
        """
        return self.comments

    def get_comment(self, name):
        """Gets the first matching comment for a given name

        Args:
            name: Comment name

        Returns:
            :obj:`Comment` matching the name. Only returns the first found.

        """
        clist = list(self.yield_comments(name=name))
        if len(clist) > 0:
            return clist[-1]
        else:
            return None

    def get_comment_names(self):
        """Gets all of the comment names

        Returns:
            :obj:`list` of str.

        """
        return [x.name for x in self.comments]

    def get_comment_values(self):
        """Gets all of the comment values

        Returns:
            :obj:`list` of str.

        """
        return [x.value for x in self.comments]


class MetadataMixin(metaclass=abc.ABCMeta):
    """Abstract mixin class to contain metadata fields found in Investigation
    and Study sections of ISA

    Attributes:
        identifier: An identifier associated with objects of this class.
        title: A title associated with objects of this class.
        description: A description associated with objects of this class.
        submission_date: A submission date associated with objects of this
            class.
        public_release_date: A submission date associated with objects of this
            class.
    """

    def __init__(self, filename='', identifier='', title='', description='',
                 submission_date='', public_release_date='', publications=None,
                 contacts=None):

        self.__filename = filename
        self.__identifier = identifier
        self.__title = title
        self.__description = description
        self.__submission_date = submission_date
        self.__public_release_date = public_release_date

        if publications is None:
            self.__publications = []
        else:
            self.__publications = publications

        if contacts is None:
            self.contacts = []
        else:
            self.__contacts = contacts
            
    @property
    def filename(self):
        """:obj:`str`: A filename"""
        return self.__filename

    @filename.setter
    def filename(self, val):
        if val is not None and isinstance(val, str):
                self.__filename = val
        else:
            raise ISAModelAttributeError('{0}.filename must be a string'
                                         .format(type(self).__name__))

    @property
    def identifier(self):
        """:obj:`str`: An identifier"""
        return self.__identifier

    @identifier.setter
    def identifier(self, val):
        if val is not None and isinstance(val, str):
                self.__identifier = val
        else:
            raise ISAModelAttributeError('{0}.identifier must be a string'
                                         .format(type(self).__name__))

    @property
    def title(self):
        """:obj:`str`: A title"""
        return self.__title

    @title.setter
    def title(self, val):
        if val is not None and isinstance(val, str):
            self.__title = val
        else:
            raise ISAModelAttributeError('{0}.title must be a string'
                                         .format(type(self).__name__))

    @property
    def description(self):
        """:obj:`str`: A description"""
        return self.__description

    @description.setter
    def description(self, val):
        if val is not None and isinstance(val, str):
            self.__description = val
        else:
            raise ISAModelAttributeError('{0}.description must be a string'
                                         .format(type(self).__name__))

    @property
    def submission_date(self):
        """:obj:`str`: A submission date"""
        return self.__submission_date

    @submission_date.setter
    def submission_date(self, val):
        if val is not None and isinstance(val, str):
            self.__submission_date = val
        else:
            raise ISAModelAttributeError('{0}.submission_date must be a string'
                                         .format(type(self).__name__))

    @property
    def public_release_date(self):
        """:obj:`str`: A public release date"""
        return self.__public_release_date

    @public_release_date.setter
    def public_release_date(self, val):
        if val is not None and isinstance(val, str):
            self.__public_release_date = val
        else:
            raise ISAModelAttributeError('{0}.public_release_date must be a '
                                         'string'.format(type(self).__name__))

    @property
    def publications(self):
        """:obj:`list` of :obj:`Publication`: Container for ISA publications"""
        return self.__publications

    @publications.setter
    def publications(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Publication) for x in val):
                self.__publications = list(val)
        else:
            raise ISAModelAttributeError(
                '{0}.publications must be iterable containing Publications'
                .format(type(self).__name__))

    @property
    def contacts(self):
        """:obj:`list` of :obj:`Person`: Container for ISA contacts"""
        return self.__contacts

    @contacts.setter
    def contacts(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Person) for x in val):
                self.__contacts = list(val)
        else:
            raise ISAModelAttributeError(
                '{0}.contacts must be iterable containing Person objects'
                .format(type(self).__name__))


class Investigation(Commentable, MetadataMixin, object):
    """An investigation maintains metadata about the project context and links
    to one or more studies. There can only be 1 Investigation in an ISA
    descriptor. Investigations have the following properties:

    Attributes:
        identifier: A locally unique identifier or an accession number provided
            by a repository.
        title: A concise name given to the investigation.
            description: A textual description of the investigation.
        submission_date  date on which the investigation was reported to the
            repository. This should be ISO8601 formatted.
        public_release_date: The date on which the investigation should be
            released publicly. This should be ISO8601 formatted.
        ontology_source_references: OntologySources to be referenced by
            OntologyAnnotations used in this ISA descriptor.
        publications: A list of Publications associated with an Investigation.
        contacts: A list of People/contacts associated with an Investigation.
        studies: Study is the central unit, containing information on the
            subject under study.
        comments: Comments associated with instances of this class.
    """

    def __init__(self, id_='', filename='', identifier='', title='',
                 description='', submission_date='', public_release_date='',
                 ontology_source_references=None, publications=None,
                 contacts=None, studies=None, comments=None):
        MetadataMixin.__init__(self, filename=filename, identifier=identifier,
                               title=title, description=description,
                               submission_date=submission_date,
                               public_release_date=public_release_date,
                               publications=publications, contacts=contacts)
        Commentable.__init__(self, comments=comments)

        self.id = id_

        if ontology_source_references is None:
            self.__ontology_source_references = []
        else:
            self.__ontology_source_references = ontology_source_references

        if studies is None:
            self.__studies = []
        else:
            self.__studies = studies

    @property
    def ontology_source_references(self):
        """:obj:`list` of :obj:`OntologySource`: Container for ontology
                sources
        """
        return self.__ontology_source_references

    @ontology_source_references.setter
    def ontology_source_references(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologySource) for x in val):
                self.__ontology_source_references = list(val)
        else:
            raise ISAModelAttributeError(
                'Investigation.ontology_source_references must be iterable '
                'containing OntologySource objects')

    def add_ontology_source_reference(self, name='', version='', description='',
                                      file='', comments=None):
        """Adds a new ontology_source_reference to the ontology_source_reference list.

        Args:
            name: OntologySource name
            version: OntologySource version
            description: OntologySource description
            file: OntologySource file
        """
        c = OntologySource(name=name, version=version, description=description,
                           file=file, comments=comments)
        self.ontology_source_references.append(c)

    def yield_ontology_source_references(self, name=None):
        """Gets an iterator of matching ontology_source_references for a given
        name.

        Args:
            name: OntologySource name

        Returns:
            :obj:`filter` of :obj:`OntologySources` that can be iterated on.
        """
        if name is None:
            return filter(True, self.ontology_source_references)
        else:
            return filter(lambda x: x.name == name,
                          self.ontology_source_references)

    def get_ontology_source_references(self):
        """Gets a list of all ontology_source_references.

        Returns:
            :obj:`list` of :obj:`OntologySource` of all
            ontology_source_references, if any
        """
        return self.ontology_source_references

    def get_ontology_source_reference(self, name):
        """Gets the first matching ontology_source_reference for a given name

        Args:
            name: OntologySource name

        Returns:
            :obj:`OntologySource` matching the name. Only returns the first
            found.

        """
        clist = list(self.yield_ontology_source_references(name=name))
        if len(clist) > 0:
            return clist[-1]
        else:
            return None

    def get_ontology_source_reference_names(self):
        """Gets all of the ontology_source_reference names

        Returns:
            :obj:`list` of str.

        """
        return [x.name for x in self.ontology_source_references]

    @property
    def studies(self):
        """:obj:`list` of :obj:`Study`: Container for studies"""
        return self.__studies

    @studies.setter
    def studies(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Study) for x in val):
                self.__studies = list(val)
        else:
            raise ISAModelAttributeError(
                'Investigation.studies must be iterable containing Study '
                'objects')

    def __repr__(self):
        return "isatools.model.Investigation(" \
               "identifier='{investigation.identifier}', " \
               "filename='{investigation.filename}', " \
               "title='{investigation.title}', " \
               "submission_date='{investigation.submission_date}', " \
               "public_release_date='{investigation.public_release_date}', " \
               "ontology_source_references=" \
               "{investigation.ontology_source_references}, " \
               "publications={investigation.publications}, " \
               "contacts={investigation.contacts}, " \
               "studies={investigation.studies}, " \
               "comments={investigation.comments})".format(investigation=self)

    def __str__(self):
        return """Investigation(
    identifier={investigation.identifier}
    filename={investigation.filename}
    title={investigation.title}
    submission_date={investigation.submission_date}
    public_release_date={investigation.public_release_date}
    ontology_source_references={num_ontology_source_references} OntologySource objects
    publications={num_publications} Publication objects
    contacts={num_contacts} Person objects
    studies={num_studies} Study objects
    comments={num_comments} Comment objects
)""".format(investigation=self,
            num_ontology_source_references=len(self.ontology_source_references),
            num_publications=len(self.publications),
            num_contacts=len(self.contacts),
            num_studies=len(self.studies),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Investigation) \
            and self.filename == other.filename \
            and self.identifier == other.identifier \
            and self.title == other.title \
            and self.submission_date == other.submission_date \
            and self.public_release_date == other.public_release_date \
            and self.ontology_source_references \
            == other.ontology_source_references \
            and self.publications == other.publications \
            and self.contacts == other.contacts \
            and self.studies == other.studies \
            and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


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

    def __init__(self, name, file='', version='', description='',
                 comments=None):
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
            raise ISAModelAttributeError(
                'OntologySource.name must be a str; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__name = val

    @property
    def file(self):
        """:obj:`str`: file of the ontology source"""
        return self.__file
    
    @file.setter
    def file(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'OntologySource.file must be a str; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__file = val

    @property
    def version(self):
        """:obj:`str`: version of the ontology source"""
        return self.__version

    @version.setter
    def version(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'OntologySource.version must be a str; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__version = val   

    @property
    def description(self):
        """:obj:`str`: description of the ontology source"""
        return self.__description

    @description.setter
    def description(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'OntologySource.description must be a str; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__description = val

    def __repr__(self):
        return "isatools.model.OntologySource(name='{ontology_source.name}', " \
               "file='{ontology_source.file}', " \
               "version='{ontology_source.version}', " \
               "description='{ontology_source.description}', " \
               "comments={ontology_source.comments})" \
                .format(ontology_source=self)

    def __str__(self):
        return """OntologySource(
    name={ontology_source.name}
    file={ontology_source.file}
    version={ontology_source.version}
    description={ontology_source.description}
    comments={num_comments} Comment objects
)""".format(ontology_source=self, num_comments=len(self.comments))

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


class OntologyAnnotation(Commentable):
    """An ontology annotation

    Attributes:
        term : A term taken from an ontology or controlled vocabulary.
        term_source : Reference to the OntologySource from which the term is
            derived.
        term_accession : A URI or resource-specific identifier for the term.
        comments: Comments associated with instances of this class.
    """

    def __init__(self, term='', term_source=None, term_accession='',
                 comments=None, id_=''):
        super().__init__(comments)

        self.__term = term
        self.__term_source = term_source
        self.__term_accession = term_accession
        self.id = id_

    @property
    def term(self):
        """:obj:`str`: the ontology annotation name used"""
        return self.__term

    @term.setter
    def term(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'OntologyAnnotation.term must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__term = val

    @property
    def term_source(self):
        """:obj:`OntologySource: a reference to the ontology source the term is
        taken from"""
        return self.__term_source

    @term_source.setter
    def term_source(self, val):
        if val is not None and not isinstance(val, OntologySource):
            raise ISAModelAttributeError(
                'OntologyAnnotation.term_source must be a OntologySource or '
                'None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__term_source = val

    @property
    def term_accession(self):
        """:obj:`str`: the term accession number of reference of the term"""
        return self.__term_accession

    @term_accession.setter
    def term_accession(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'OntologyAnnotation.term_accession must be a str or None')
        else:
            self.__term_accession = val

    def __repr__(self):
        return "isatools.model.OntologyAnnotation(" \
               "term='{ontology_annotation.term}', " \
               "term_source={term_source}, " \
               "term_accession='{ontology_annotation.term_accession}', " \
               "comments={ontology_annotation.comments})" \
                .format(ontology_annotation=self,
                        term_source=repr(self.term_source))

    def __str__(self):
        return """OntologyAnnotation(
    term={ontology_annotation.term}
    term_source={term_source_ref}
    term_accession={ontology_annotation.term_accession}
    comments={num_comments} Comment objects
)""".format(ontology_annotation=self,
            term_source_ref=self.term_source.name if self.term_source else '',
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, OntologyAnnotation) \
            and self.term == other.term \
            and self.term_source == other.term_source \
            and self.term_accession == other.term_accession \
            and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class Publication(Commentable):
    """A publication associated with an investigation or study.

    Attributes:
        pubmed_id: The PubMed IDs of the described publication(s) associated
            with this investigation.
        doi: A Digital Object Identifier (DOI) for that publication (where
            available).
        author_list: The list of authors associated with that publication.
        title: The title of publication associated with the investigation.
        status: A term describing the status of that publication (i.e.
            submitted, in preparation, published).
        comments: Comments associated with instances of this class.
    """

    def __init__(self, pubmed_id='', doi='', author_list='', title='', 
                 status=None, comments=None):
        super().__init__(comments)

        self.__pubmed_id = pubmed_id
        self.__doi = doi
        self.__author_list = author_list
        self.__title = title
        self.__status = status

    @property
    def pubmed_id(self):
        """:obj:`str`: the PubMed ID of the publication"""
        return self.__pubmed_id

    @pubmed_id.setter
    def pubmed_id(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Publication.pubmed_id must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__pubmed_id = val
            
    @property
    def doi(self):
        """:obj:`str`: the DOI of the publication"""
        return self.__doi

    @doi.setter
    def doi(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Publication.doi must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__doi = val
            
    @property
    def author_list(self):
        """:obj:`str`: the author list (comma separated) of the publication"""
        return self.__author_list

    @author_list.setter
    def author_list(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Publication.author_list must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__author_list = val
            
    @property
    def title(self):
        """:obj:`str`: the title of the publication"""
        return self.__title

    @title.setter
    def title(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Publication.title must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__title = val

    @property
    def status(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        publication status"""
        return self.__status

    @status.setter
    def status(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'Publication.status must be a OntologyAnnotation or '
                'None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__status = val

    def __repr__(self):
        return "isatools.model.Publication(" \
               "pubmed_id='{publication.pubmed_id}', doi='{publication.doi}', " \
               "author_list='{publication.author_list}', " \
               "title='{publication.title}', status={status}, " \
               "comments={publication.comments})".format(
                publication=self, status=repr(self.status))

    def __str__(self):
        return """Publication(
    pubmed_id={publication.pubmed_id}
    doi={publication.doi}
    author_list={publication.author_list}
    title={publication.title}
    status={status}
    comments={num_comments} Comment objects
)""".format(publication=self,
            status=self.status.term if self.status else '',
            num_comments=len(self.comments))
    
    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        return isinstance(other, Publication) \
               and self.pubmed_id == other.pubmed_id \
               and self.doi == other.doi \
               and self.author_list == other.author_list \
               and self.title == other.title \
               and self.status == other.status \
               and self.comments == other.comments
    
    def __ne__(self, other):
        return not self == other


class Person(Commentable):
    """A person/contact that can be attributed to an Investigation or Study.

    Attributes:
        last_name: The last name of a person.
        first_name: The first name of a person.
        mid_initials: The middle initials of a person.
        email: The email address of a person.
        phone: The telephone number.
        fax: The fax number.
        address: The address of a person.
        affiliation: The organization affiliation for a person.
        roles: A list of Orole(s) performed by this person. Roles reported here
            need not correspond to roles held withing their affiliated
            organization.
        comments: Comments associated with instances of this class.
    """

    def __init__(self, last_name='', first_name='', mid_initials='', email='', 
                 phone='', fax='', address='', affiliation='', roles=None, 
                 comments=None, id_=''):
        super().__init__(comments)

        self.id = id_
        self.__last_name = last_name
        self.__first_name = first_name
        self.__mid_initials = mid_initials
        self.__email = email
        self.__phone = phone
        self.__fax = fax
        self.__address = address
        self.__affiliation = affiliation

        if roles is None:
            self.__roles = []
        else:
            self.__roles = roles

    @property
    def last_name(self):
        """:obj:`str`: the last_name of the person"""
        return self.__last_name
    
    @last_name.setter
    def last_name(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Person.last_name must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__last_name = val

    @property
    def first_name(self):
        """:obj:`str`: the first_name of the person"""
        return self.__first_name

    @first_name.setter
    def first_name(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Person.first_name must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__first_name = val

    @property
    def mid_initials(self):
        """:obj:`str`: the mid_initials of the person"""
        return self.__mid_initials

    @mid_initials.setter
    def mid_initials(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Person.mid_initials must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__mid_initials = val

    @property
    def email(self):
        """:obj:`str`: the email of the person"""
        return self.__email

    @email.setter
    def email(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Person.email must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__email = val

    @property
    def phone(self):
        """:obj:`str`: the phone number of the person"""
        return self.__phone

    @phone.setter
    def phone(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Person.phone must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__phone = val

    @property
    def fax(self):
        """:obj:`str`: the fax number of the person"""
        return self.__fax

    @fax.setter
    def fax(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Person.fax must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__fax = val

    @property
    def address(self):
        """:obj:`str`: the address of the person"""
        return self.__address

    @address.setter
    def address(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Person.address must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__address = val

    @property
    def affiliation(self):
        """:obj:`str`: the affiliation of the person"""
        return self.__affiliation

    @affiliation.setter
    def affiliation(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Person.affiliation must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__affiliation = val

    @property
    def roles(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for person roles
        """
        return self.__roles

    @roles.setter
    def roles(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation) for x in val):
                self.__roles = list(val)
        else:
            raise ISAModelAttributeError(
                '{0}.roles must be iterable containing OntologyAnnotations'
                .format(type(self).__name__))

    def __repr__(self):
        return "isatools.model.Person(last_name='{person.last_name}', " \
               "first_name='{person.first_name}', " \
               "mid_initials='{person.mid_initials}', " \
               "email='{person.email}', phone='{person.phone}', " \
               "fax='{person.fax}', address='{person.address}', " \
               "affiliation='{person.affiliation}', roles={person.roles}, " \
               "comments={person.comments})" \
                .format(person=self)

    def __str__(self):
        return """Person(
    last_name={person.last_name}
    first_name={person.first_name}
    mid_initials={person.mid_initials}
    email={person.email}
    phone={person.phone}
    fax={person.fax}
    address={person.address}
    roles={num_roles} OntologyAnnotation objects
    comments={num_comments} Comment objects
)""".format(person=self,
            num_roles=len(self.roles),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Person) \
               and self.last_name == other.last_name \
               and self.first_name == other.first_name \
               and self.mid_initials == other.mid_initials \
               and self.email == other.email \
               and self.phone == other.phone \
               and self.fax == other.fax \
               and self.address == other.address \
               and self.affiliation == other.affiliation \
               and self.roles == other.roles \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class StudyAssayMixin(metaclass=abc.ABCMeta):
    """Abstract mixin class to contain common fields found in Study
    and Assay sections of ISA

    Attributes:
        filename: A field to specify the file for compatibility with ISA-Tab.
        materials: Materials associated with the Study or Assay.
        sources: Sources associated with the Study or Assay.
        samples: Samples associated with the Study or Assay.
        other_material: Other Material types associated with the Study or Assay.
        units: A list of Units used in the annotation of materials.
        characteristic_categories-: A list of OntologyAnnotation used in
            the annotation of material characteristics.
        process_sequence: A list of Process objects representing the
            experimental graphs.
        graph: Graph representation of the experimental graph.

    """

    def __init__(self, filename='', sources=None, samples=None,
                 other_material=None, units=None,
                 characteristic_categories=None, process_sequence=None):
        self.__filename = filename

        self.__materials = {
            'sources': [],
            'samples': [],
            'other_material': []
        }
        if not (sources is None):
            self.__materials['sources'] = sources
        if not (samples is None):
            self.__materials['samples'] = samples
        if not (other_material is None):
            self.__materials['other_material'] = other_material

        if units is None:
            self.__units = []
        else:
            self.__units = units

        if process_sequence is None:
            self.__process_sequence = []
        else:
            self.__process_sequence = process_sequence

        if characteristic_categories is None:
            self.__characteristic_categories = []
        else:
            self.__characteristic_categories = characteristic_categories
            
    @property
    def filename(self):
        """:obj:`str`: the filename of the study or assay"""
        return self.__filename

    @filename.setter
    def filename(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                '{0}.filename must be a str or None; got {1}:{2}'
                .format(type(self).__name__, val, type(val)))
        else:
            self.__filename = val

    @property
    def units(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for study units
        """
        return self.__units

    @units.setter
    def units(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation) for x in val):
                self.__units = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.units must be iterable containing OntologyAnnotations'
                .format(type(self).__name__))

    @property
    def sources(self):
        """:obj:`list` of :obj:`Source`: Container for study sources"""
        return self.__materials['sources']

    @sources.setter
    def sources(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Source) for x in val):
                self.__materials['sources'] = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.sources must be iterable containing Sources'
                .format(type(self).__name__))

    def add_source(self, name='', characteristics=None, comments=None):
        """Adds a new source to the source materials list.

        Args:
            name: Source name
            characteristics: Source characteristics
            comments: Source comments
        """
        s = Source(name=name, characteristics=characteristics,
                   comments=comments)
        self.sources.append(s)

    def yield_sources(self, name=None):
        """Gets an iterator of matching sources for a given name.

        Args:
            name: Source name

        Returns:
            :obj:`filter` of :obj:`Source` that can be iterated on.  If name is
                None, yields all sources.
        """
        if name is None:
            return filter(True, self.sources)
        else:
            return filter(lambda x: x.name == name, self.sources)

    def get_source(self, name):
        """Gets the first matching source material for a given name.

        Args:
            name: Source name

        Returns:
            :obj:`Source` matching the name. Only returns the first found.

        """
        slist = list(self.yield_sources(name=name))
        if len(slist) > 0:
            return slist[-1]
        else:
            return None

    def yield_sources_by_characteristic(self, characteristic=None):
        """Gets an iterator of matching sources for a given characteristic.

        Args:
            characteristic: Source characteristic

        Returns:
            :obj:`filter` of :obj:`Source` that can be iterated on. If
                characteristic is None, yields all sources.
        """
        if characteristic is None:
            return filter(True, self.sources)
        else:
            return filter(lambda x: characteristic in x.characteristics,
                          self.sources)

    def get_source_by_characteristic(self, characteristic):
        """Gets the first matching source material for a given characteristic.

        Args:
            characteristic: Source characteristic

        Returns:
            :obj:`Source` matching the characteristic. Only returns the first
                found.

        """
        slist = list(self.yield_sources_by_characteristic(characteristic=
                                                          characteristic))
        if len(slist) > 0:
            return slist[-1]
        else:
            return None

    def get_source_names(self):
        """Gets all of the source names.

        Returns:
            :obj:`list` of str.

        """
        return [x.name for x in self.sources]

    @property
    def samples(self):
        """:obj:`list` of :obj:`Sample`: Container for study samples"""
        return self.__materials['samples']

    @samples.setter
    def samples(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Sample) for x in val):
                self.__materials['samples'] = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.samples must be iterable containing Samples'
                .format(type(self).__name__))

    def add_sample(self, name='', characteristics=None, factor_values=None, 
                   derives_from=None, comments=None):
        """Adds a new sample to the sample materials list.

        Args:
            name: Source name
            characteristics: Source characteristics
            comments: Source comments
        """
        s = Sample(name=name, characteristics=characteristics, 
                   factor_values=factor_values, derives_from=derives_from,
                   comments=comments)
        self.samples.append(s)

    def yield_samples(self, name=None):
        """Gets an iterator of matching samples for a given name.

        Args:
            name: Sample name

        Returns:
            :obj:`filter` of :obj:`Source` that can be iterated on.  If name is
                None, yields all samples.
        """
        if name is None:
            return filter(True, self.samples)
        else:
            return filter(lambda x: x.name == name, self.samples)

    def get_sample(self, name):
        """Gets the first matching sample material for a given name.

        Args:
            name: Sample name

        Returns:
            :obj:`Sample` matching the name. Only returns the first found.

        """
        slist = list(self.yield_samples(name=name))
        if len(slist) > 0:
            return slist[-1]
        else:
            return None

    def yield_samples_by_characteristic(self, characteristic=None):
        """Gets an iterator of matching samples for a given characteristic.

        Args:
            characteristic: Sample characteristic

        Returns:
            :obj:`filter` of :obj:`Sample` that can be iterated on. If
                characteristic is None, yields all samples.
        """
        if characteristic is None:
            return filter(True, self.samples)
        else:
            return filter(lambda x: characteristic in x.characteristics,
                          self.samples)

    def get_sample_by_characteristic(self, characteristic):
        """Gets the first matching sample material for a given characteristic.

        Args:
            characteristic: Sample characteristic

        Returns:
            :obj:`Sample` matching the characteristic. Only returns the first
                found.

        """
        slist = list(self.yield_samples_by_characteristic(characteristic=
                                                          characteristic))
        if len(slist) > 0:
            return slist[-1]
        else:
            return None

    def yield_samples_by_factor_value(self, factor_value=None):
        """Gets an iterator of matching samples for a given factor_value.

        Args:
            factor_value: Sample factor value

        Returns:
            :obj:`filter` of :obj:`Sample` that can be iterated on. If
                factor_value is None, yields all samples.
        """
        if factor_value is None:
            return filter(True, self.samples)
        else:
            return filter(lambda x: factor_value in x.factor_values,
                          self.samples)

    def get_sample_by_factor_value(self, factor_value):
        """Gets the first matching sample material for a given factor_value.

        Args:
            factor_value: Sample factor value

        Returns:
            :obj:`Sample` matching the factor_value. Only returns the first
                found.

        """
        slist = list(self.yield_samples_by_factor_value(factor_value=
                                                        factor_value))
        if len(slist) > 0:
            return slist[-1]
        else:
            return None

    def get_sample_names(self):
        """Gets all of the sample names.

        Returns:
            :obj:`list` of str.

        """
        return [x.name for x in self.samples]

    @property
    def other_material(self):
        """:obj:`list` of :obj:`Material`: Container for study other_material
        """
        return self.__materials['other_material']

    @other_material.setter
    def other_material(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Material) for x in val):
                self.__materials['other_material'] = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.other_material must be iterable containing Materials'
                .format(type(self).__name__))

    def yield_materials_by_characteristic(self, characteristic=None):
        """Gets an iterator of matching materials for a given characteristic.

        Args:
            characteristic: Material characteristic

        Returns:
            :obj:`filter` of :obj:`Material` that can be iterated on. If
                characteristic is None, yields all materials.
        """
        if characteristic is None:
            return filter(True, self.other_material)
        else:
            return filter(lambda x: characteristic in x.characteristics,
                          self.other_materials)

    def get_material_by_characteristic(self, characteristic):
        """Gets the first matching material material for a given characteristic.

        Args:
            characteristic: Material characteristic

        Returns:
            :obj:`Material` matching the characteristic. Only returns the first
                found.

        """
        mlist = list(self.yield_materials_by_characteristic(characteristic=
                                                            characteristic))
        if len(mlist) > 0:
            return mlist[-1]
        else:
            return None

    @property
    def materials(self):
        """:obj:`dict` of :obj:`list`: Container for sources, samples and
        other_material"""
        warnings.warn(
            "the `materials` dict property is being deprecated in favour of "
            "`sources`, `samples`, and `other_material` properties.",
            DeprecationWarning
        )
        return self.__materials

    @property
    def process_sequence(self):
        """:obj:`list` of :obj:`Process`: Container for study Processes"""
        return self.__process_sequence

    @process_sequence.setter
    def process_sequence(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Process) for x in val):
                self.__process_sequence = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.process_sequence must be iterable containing Processes'
                .format(type(self).__name__))

    @property
    def characteristic_categories(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for study
        characteristic categories used"""
        return self.__characteristic_categories

    @characteristic_categories.setter
    def characteristic_categories(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation) for x in val):
                self.__characteristic_categories = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.characteristic_categories must be iterable containing '
                'OntologyAnnotation'.format(type(self).__name__))

    @property
    def graph(self):
        """:obj:`networkx.DiGraph` A graph representation of the study's 
        process sequence"""
        if len(self.process_sequence) > 0:
            return _build_assay_graph(self.process_sequence)
        else:
            return None

    @graph.setter
    def graph(self, graph):
        raise ISAModelAttributeError('{}.graph is not settable'
                                     .format(type(self).__name__))


class Study(Commentable, StudyAssayMixin, MetadataMixin, object):
    """Study is the central unit, containing information on the subject under 
    study, its characteristics and any treatments applied.

    Attributes:
        identifier: A unique identifier: either a temporary identifier supplied 
            by users or one generated by a repository or other database.
        title: A concise phrase used to encapsulate the purpose and goal of the 
            study.
        description: A textual description of the study, with components such
            as objective or goals.
        submission_date: The date on which the study was reported to the
            repository. This should be ISO8601 formatted.
        public_release_date: The date on which the study should be released
            publicly. This should be ISO8601 formatted.
        filename: A field to specify the name of the Study file corresponding
            the definition of that Study.
        design_descriptors: Classifications of the study based on the overall
            experimental design.
        publications: A list of Publications associated with the Study.
        contacts: A list of People/contacts associated with the Study.
        factors: A factor corresponds to an independent variable manipulated by
            the experimentalist with the intention to affect biological systems
            in a way that can be measured by an assay.
        protocols: Protocols used within the ISA artifact.
        assays: An Assay represents a portion of the experimental design.
        materials: Materials associated with the study, contains lists of
            'sources', 'samples' and 'other_material'. DEPRECATED.
        sources: Sources associated with the study, is equivalent to
            materials['sources'].
        samples: Samples associated with the study, is equivalent to
            materials['samples'].
        other_material: Other Materials associated with the study, is
            equivalent to materials['other_material'].
        units: A list of Units used in the annotation of material units in the
            study.
        characteristic_categories: Annotations of material characteristics used
            in the study.
        process_sequence: A list of Process objects representing the
            experimental graphs at the study level.
        comments: Comments associated with instances of this class.
        graph: Graph representation of the study graph.
    """

    def __init__(self, id_='', filename='', identifier='', title='',
                 description='', submission_date='', public_release_date='',
                 contacts=None, design_descriptors=None, publications=None,
                 factors=None, protocols=None, assays=None, sources=None,
                 samples=None, process_sequence=None, other_material=None,
                 characteristic_categories=None, comments=None, units=None):
        MetadataMixin.__init__(self, filename=filename, identifier=identifier,
                               title=title, description=description,
                               submission_date=submission_date,
                               public_release_date=public_release_date,
                               publications=publications, contacts=contacts)
        StudyAssayMixin.__init__(self, filename=filename, sources=sources,
                                 samples=samples, other_material=other_material,
                                 process_sequence=process_sequence,
                                 characteristic_categories=
                                 characteristic_categories,
                                 units=units)
        Commentable.__init__(self, comments=comments)

        self.id = id_

        if design_descriptors is None:
            self.__design_descriptors = []
        else:
            self.__design_descriptors = design_descriptors

        if protocols is None:
            self.__protocols = []
        else:
            self.__protocols = protocols

        if assays is None:
            self.__assays = []
        else:
            self.__assays = assays

        if factors is None:
            self.__factors = []
        else:
            self.__factors = factors

    @property
    def design_descriptors(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for study design
        descriptors"""
        return self.__design_descriptors

    @design_descriptors.setter
    def design_descriptors(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation) for x in val):
                self.__design_descriptors = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.design_descriptors must be iterable containing '
                'OntologyAnnotations'.format(type(self).__name__))
        
    @property
    def protocols(self):
        """:obj:`list` of :obj:`Protocol`: Container for study protocols"""
        return self.__protocols

    @protocols.setter
    def protocols(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Protocol) for x in val):
                self.__protocols = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.protocols must be iterable containing Protocol'
                .format(type(self).__name__))

    @staticmethod
    def __get_default_protocol(protocol_type):
        """Return default Protocol object based on protocol_type and from
        isaconfig_v2015-07-02"""
        default_protocol = Protocol(protocol_type=
                                    OntologyAnnotation(term=protocol_type))
        parameter_list = []
        if protocol_type == 'mass spectrometry':
            parameter_list = ['instrument',
                              'ion source',
                              'detector',
                              'analyzer',
                              'chromatography instrument',
                              'chromatography column']
        elif protocol_type == 'nmr spectroscopy':
            parameter_list = ['instrument',
                              'NMR probe',
                              'number of acquisition',
                              'magnetic field strength',
                              'pulse sequence']
        elif protocol_type == 'nucleic acid hybridization':
            parameter_list = ['Array Design REF']
        elif protocol_type == 'nucleic acid sequencing':
            parameter_list = ['sequencing instrument',
                              'quality scorer',
                              'base caller']
        default_protocol.parameters = [
            ProtocolParameter(parameter_name=OntologyAnnotation(term=x))
            for x in parameter_list]
        # TODO: Implement this for other defaults OR generate from config #51
        return default_protocol

    def add_prot(self, protocol_name='', protocol_type=None, use_default_params=True):
        if self.get_prot(protocol_name=protocol_name) is not None:
            log.warning('A protocol with name "{}" has already been declared in the study'.format(protocol_name))
        else:
            if isinstance(protocol_type, str) and use_default_params:
                default_protocol = self.__get_default_protocol(protocol_type)
                default_protocol.name = protocol_name
                self.protocols.append(default_protocol)
            else:
                self.protocols.append(Protocol(name=protocol_name,
                                               protocol_type=OntologyAnnotation(
                                                   term=protocol_type)))

    def get_prot(self, protocol_name):
        prot = None
        try:
            prot = next(x for x in self.protocols if x.name == protocol_name)
        except StopIteration:
            pass
        return prot

    def add_factor(self, name, factor_type):
        if self.get_factor(name=name) is not None:
            log.warning(
                'A factor with name "{}" has already been declared in the study'
                    .format(name))
        else:
            self.factors.append(StudyFactor(
                name=name, factor_type=OntologyAnnotation(term=factor_type)))

    def del_factor(self, name, are_you_sure=False):
        if self.get_factor(name=name) is None:
            log.warning(
                'A factor with name "{}" hasnot been found in the study'
                .format(name))
        else:
            if are_you_sure:  # force user to say yes, to be sure to be sure
                self.factors.remove(self.get_factor(name=name))

    def get_factor(self, name):
        factor = None
        try:
            factor = next(x for x in self.factors if x.name == name)
        except StopIteration:
            pass
        return factor
        
    @property
    def assays(self):
        """:obj:`list` of :obj:`Assay`: Container for study Assays"""
        return self.__assays

    @assays.setter
    def assays(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Assay) for x in val):
                self.__assays = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.assays must be iterable containing Assays'
                .format(type(self).__name__))

    @property
    def factors(self):
        """:obj:`list` of :obj:`StudyFactor`: Container for study
        StudyFactors"""
        return self.__factors

    @factors.setter
    def factors(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, StudyFactor) for x in val):
                self.__factors = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.factors must be iterable containing StudyFactors'
                .format(type(self).__name__))

    def __repr__(self):
        return "isatools.model.Study(filename='{study.filename}', " \
               "identifier='{study.identifier}', title='{study.title}', " \
               "description='{study.description}', " \
               "submission_date='{study.submission_date}', " \
               "public_release_date='{study.public_release_date}', " \
               "contacts={study.contacts}, " \
               "design_descriptors={study.design_descriptors}, " \
               "publications={study.publications}, factors={study.factors}, " \
               "protocols={study.protocols}, assays={study.assays}, " \
               "sources={study.sources}, samples={study.samples}, " \
               "process_sequence={study.process_sequence}, " \
               "other_material={study.other_material}, " \
               "characteristic_categories={study.characteristic_categories}, " \
               "comments={study.comments}, units={study.units})"\
                .format(study=self)

    def __str__(self):
        return """Study(
    identifier={study.identifier}
    filename={study.filename}
    title={study.title}
    description={study.description}
    submission_date={study.submission_date}
    public_release_date={study.public_release_date}
    contacts={num_contacts} Person objects
    design_descriptors={num_design_descriptors} OntologyAnnotation objects
    publications={num_publications} Publication objects
    factors={num_study_factors} StudyFactor objects
    protocols={num_protocols} Protocol objects
    assays={num_assays} Assay objects
    sources={num_sources} Source objects
    samples={num_samples} Sample objects
    process_sequence={num_processes} Process objects
    other_material={num_other_material} Material objects
    characteristic_categories={num_characteristic_categories} OntologyAnnotation objects
    comments={num_comments} Comment objects
    units={num_units} Unit objects
)""".format(study=self, num_contacts=len(self.contacts),
            num_design_descriptors=len(self.design_descriptors),
            num_publications=len(self.publications),
            num_study_factors=len(self.factors),
            num_protocols=len(self.protocols),
            num_assays=len(self.assays),
            num_sources=len(self.sources),
            num_samples=len(self.samples),
            num_processes=len(self.process_sequence),
            num_other_material=len(self.other_material),
            num_characteristic_categories=len(self.characteristic_categories),
            num_comments=len(self.comments),
            num_units=len(self.units))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Study) \
               and self.filename == other.filename \
               and self.identifier == other.identifier \
               and self.title == other.title \
               and self.description == other.description \
               and self.submission_date == other.submission_date \
               and self.public_release_date == other.public_release_date \
               and self.contacts == other.contacts \
               and self.design_descriptors == other.design_descriptors \
               and self.publications == other.publications \
               and self.factors == other.factors \
               and self.protocols == other.protocols \
               and self.assays == other.assays \
               and self.sources == other.sources \
               and self.samples == other.samples \
               and self.process_sequence == other.process_sequence \
               and self.other_material == other.other_material \
               and self.characteristic_categories \
               == other.characteristic_categories \
               and self.comments == other.comments \
               and self.units == other.units

    def __ne__(self, other):
        return not self == other


class StudyFactor(Commentable):
    """A Study Factor corresponds to an independent variable manipulated by the
    experimentalist with the intention to affect biological systems in a way
    that can be measured by an assay.

    Attributes:
        name: Study factor name
        factor_type: An ontology source reference of the study factor type
        comments: Comments associated with instances of this class.
    """
    def __init__(self, id_='', name='', factor_type=None, comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name

        if factor_type is None:
            self.__factor_type = OntologyAnnotation()
        else:
            self.__factor_type = factor_type

    @property
    def name(self):
        """:obj:`str`: the name of the study factor"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'StudyFactor.name must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__name = val

    @property
    def factor_type(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        study factor type"""
        return self.__factor_type

    @factor_type.setter
    def factor_type(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'StudyFactor.factor_type must be a OntologyAnnotation or '
                'None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__factor_type = val

    def __repr__(self):
        return "isatools.model.StudyFactor(name='{study_factor.name}', " \
               "factor_type={factor_type}, comments={study_factor.comments})" \
                .format(study_factor=self, factor_type=repr(self.factor_type))

    def __str__(self):
        return """StudyFactor(
    name={factor.name}
    factor_type={factor_type}
    comments={num_comments} Comment objects
)""".format(factor=self,
            factor_type=self.factor_type.term if self.factor_type else '',
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, StudyFactor) \
               and self.name == other.name \
               and self.factor_type == other.factor_type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class Assay(Commentable, StudyAssayMixin, object):
    """An Assay represents a test performed either on material taken from a
    subject or on a whole initial subject, producing qualitative or quantitative
    measurements. An Assay groups descriptions of provenance of sample
    processing for related tests. Each test typically follows the steps of one
    particular experimental workflow described by a particular protocol.

    Attributes:
        measurement_type: An Ontology Annotation to qualify the endpoint, or
            what is being measured (e.g. gene expression profiling or protein
            identification).
        technology_type: An Ontology Annotation to identify the technology
            used to perform the measurement.
        technology_platform: Manufacturer and platform name, e.g. Bruker AVANCE.
        filename: A field to specify the name of the Assay file for
            compatibility with ISA-Tab.
        materials: Materials associated with the Assay, lists of 'samples' and
            'other_material'.
        units: A list of Units used in the annotation of material units.
        characteristic_categories: A list of OntologyAnnotation used in the
            annotation of material characteristics in the Assay.
        process_sequence: A list of Process objects representing the
            experimental graphs at the Assay level.
        comments: Comments associated with instances of this class.
        graph: A graph representation of the assay graph.
    """
    def __init__(self, measurement_type=None, technology_type=None,
                 technology_platform='', filename='', process_sequence=None,
                 data_files=None, samples=None, other_material=None,
                 characteristic_categories=None, units=None, comments=None):
        super().__init__(comments)
        StudyAssayMixin.__init__(self, filename=filename, samples=samples,
                                 other_material=other_material,
                                 process_sequence=process_sequence,
                                 characteristic_categories=
                                 characteristic_categories, units=units)

        if measurement_type is None:
            self.__measurement_type = OntologyAnnotation()
        else:
            self.__measurement_type = measurement_type

        if technology_type is None:
            self.__technology_type = OntologyAnnotation()
        else:
            self.__technology_type = technology_type

        self.__technology_platform = technology_platform

        if data_files is None:
            self.__data_files = []
        else:
            self.__data_files = data_files

    @property
    def measurement_type(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        assay measurement_type"""
        return self.__measurement_type

    @measurement_type.setter
    def measurement_type(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'Assay.measurement_type must be a OntologyAnnotation or '
                'None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__measurement_type = val

    @property
    def technology_type(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        assay technology type"""
        return self.__technology_type

    @technology_type.setter
    def technology_type(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'Assay.technology_type must be a OntologyAnnotation or '
                'None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__technology_type = val

    @property
    def technology_platform(self):
        """:obj:`str`: the technology_platform of the assay"""
        return self.__technology_platform

    @technology_platform.setter
    def technology_platform(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Assay.technology_platform must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__technology_platform = val

    @property
    def data_files(self):
        """:obj:`list` of :obj:`DataFile`: Container for data files"""
        return self.__data_files

    @data_files.setter
    def data_files(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, DataFile) for x in val):
                self.__data_files = list(val)
        else:
            raise ISAModelAttributeError(
                '{0}.data_files must be iterable containing DataFiles'
                .format(type(self).__name__))

    def __repr__(self):
        return "isatools.model.Assay(measurement_type={measurement_type}, " \
               "technology_type={technology_type}, " \
               "technology_platform='{assay.technology_platform}', " \
               "filename='{assay.filename}', data_files={assay.data_files}, " \
               "samples={assay.samples}, " \
               "process_sequence={assay.process_sequence}, " \
               "other_material={assay.other_material}, " \
               "characteristic_categories={assay.characteristic_categories}, " \
               "comments={assay.comments}, units={assay.units})" \
                .format(assay=self, 
                        measurement_type=repr(self.measurement_type), 
                        technology_type=repr(self.technology_type))

    def __str__(self):
        return """Assay(
    measurement_type={measurement_type}
    technology_type={technology_type}
    technology_platform={assay.technology_platform}
    filename={assay.filename}
    data_files={num_datafiles} DataFile objects
    samples={num_samples} Sample objects
    process_sequence={num_processes} Process objects
    other_material={num_other_material} Material objects
    characteristic_categories={num_characteristic_categories} OntologyAnnotation objects
    comments={num_comments} Comment objects
    units={num_units} Unit objects
)""".format(assay=self,
            measurement_type=self.measurement_type.term if
            self.measurement_type else '',
            technology_type=self.technology_type.term if
            self.technology_type else '', num_datafiles=len(self.data_files),
            num_samples=len(self.samples),
            num_processes=len(self.process_sequence),
            num_other_material=len(self.other_material),
            num_characteristic_categories=len(self.characteristic_categories),
            num_comments=len(self.comments), num_units=len(self.units))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Assay) \
               and self.measurement_type == other.measurement_type \
               and self.technology_type == other.technology_type \
               and self.technology_platform == other.technology_platform \
               and self.filename == other.filename \
               and self.data_files == other.data_files \
               and self.samples == other.samples \
               and self.process_sequence == other.process_sequence \
               and self.other_material == other.other_material \
               and self.characteristic_categories \
               == other.characteristic_categories \
               and self.comments == other.comments \
               and self.units == other.units

    def __ne__(self, other):
        return not self == other


class Protocol(Commentable):
    """An experimental Protocol used in the study.

    Attributes:
        name: The name of the protocol used
        protocol_type: Term to classify the protocol.
        description: A free-text description of the protocol.
        uri: Pointer to protocol resources externally that can be accessed by
            their Uniform Resource Identifier (URI).
        version: An identifier for the version to ensure protocol tracking.
        parameters: A list of ProtocolParameter describing the list of
            parameters required to execute the protocol.
        components: A list of OntologyAnnotation describing a protocol's
            components; e.g. instrument names, software names, and reagents
            names.
        comments: Comments associated with instances of this class.
    """
    def __init__(self, id_='', name='', protocol_type=None, uri='',
                 description='', version='', parameters=None, components=None,
                 comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name

        if protocol_type is None:
            self.__protocol_type = OntologyAnnotation()
        else:
            self.__protocol_type = protocol_type

        self.__description = description
        self.__uri = uri
        self.__version = version

        if parameters is None:
            self.__parameters = []
        else:
            self.__parameters = parameters

        if components is None:
            self.__components = []
        else:
            self.__components = components

    @property
    def name(self):
        """:obj:`str`: the name of the protocol"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Protocol.name must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__name = val

    @property
    def protocol_type(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        study protocol type"""
        return self.__protocol_type

    @protocol_type.setter
    def protocol_type(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'Protocol.protocol_type must be a OntologyAnnotation or '
                'None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__protocol_type = val

    @property
    def description(self):
        """:obj:`str`: the description of the protocol"""
        return self.__description

    @description.setter
    def description(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Protocol.description must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__description = val

    @property
    def uri(self):
        """:obj:`str`: the uri of the protocol"""
        return self.__uri

    @uri.setter
    def uri(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Protocol.uri must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__uri = val

    @property
    def version(self):
        """:obj:`str`: the version of the protocol"""
        return self.__version

    @version.setter
    def version(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Protocol.version must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__version = val

    @property
    def parameters(self):
        """:obj:`list` of :obj:`ProtocolParameter`: Container for protocol
        parameters"""
        return self.__parameters

    @parameters.setter
    def parameters(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, ProtocolParameter) for x in val):
                self.__parameters = list(val)
        else:
            raise ISAModelAttributeError('Protocol.parameters must be iterable '
                                         'containing ProtocolParameters')

    def add_param(self, parameter_name=''):
        if self.get_param(parameter_name=parameter_name) is not None:
            pass
        else:
            if isinstance(parameter_name, str):
                self.parameters.append(ProtocolParameter(
                    parameter_name=OntologyAnnotation(term=parameter_name)))
            else:
                raise ISAModelAttributeError('Parameter name must be a string')

    def get_param(self, parameter_name):
        param = None
        try:
            param = next(x for x in self.parameters if
                         x.parameter_name.term == parameter_name)
        except StopIteration:
            pass
        return param

    @property
    def components(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for protocol
        components"""
        return self.__components

    @components.setter
    def components(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation) for x in val):
                self.__components = list(val)
        else:
            raise ISAModelAttributeError('Protocol.components must be iterable '
                                         'containing OntologyAnnotations')

    def __repr__(self):
        return "isatools.model.Protocol(name='{protocol.name}', " \
               "protocol_type={protocol_type}, " \
               "uri='{protocol.uri}', version='{protocol.version}', " \
               "parameters={protocol.parameters}, " \
               "components={protocol.components}, " \
               "comments={protocol.comments})".format(
            protocol=self, protocol_type=repr(self.protocol_type))

    def __str__(self):
        return """Protocol(
    name={protocol.name}
    protocol_type={protocol_type}
    uri={protocol.uri}
    version={protocol.version}
    parameters={num_parameters} ProtocolParameter objects
    components={num_components} OntologyAnnotation objects
    comments={num_comments} Comment objects
)""".format(protocol=self, protocol_type=
            self.protocol_type.term if self.protocol_type else '',
            num_parameters=len(self.parameters),
            num_components=len(self.components),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Protocol) \
               and self.name == other.name \
               and self.protocol_type == other.protocol_type \
               and self.uri == other.uri \
               and self.version == other.version \
               and self.parameters == other.parameters \
               and self.components == other.components \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class ProtocolParameter(Commentable):
    """A parameter used by a protocol.

    Attributes:
        parameter_name: A parameter name as an ontology term
        comments: Comments associated with instances of this class.
    """
    def __init__(self, id_='', parameter_name=None, comments=None):
        super().__init__(comments)

        self.id = id_

        if parameter_name is None:
            self.__parameter_name = OntologyAnnotation()
        else:
            self.__parameter_name = parameter_name

    @property
    def parameter_name(self):
        """:obj:`OntologyAnnotation`: an ontology annotation representing the
        parameter name"""
        return self.__parameter_name

    @parameter_name.setter
    def parameter_name(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'ProtocolParameter.parameter_name must be a OntologyAnnotation '
                'or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__parameter_name = val

    def __repr__(self):
        return 'isatools.model.ProtocolParameter(' \
               'parameter_name={parameter_name}, ' \
               'comments={parameter.comments})'.format(
                parameter=self, parameter_name=repr(self.parameter_name))

    def __str__(self):
        return """ProtocolParameter(
    parameter_name={parameter_name}
    comments={num_comments} Comment objects
)""".format(parameter_name=self.parameter_name.term if
        self.parameter_name else '', num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ProtocolParameter) \
               and self.parameter_name == other.parameter_name \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class ParameterValue(Commentable):
    """A ParameterValue represents the instance value of a ProtocolParameter,
    used in a Process.

    Attributes:
        category: A link to the relevant ProtocolParameter that the value is
            set for.
        value: The value of the parameter.
        unit: The qualifying unit classifier, if the value is numeric.
        comments: Comments associated with instances of this class.
    """
    def __init__(self, category=None, value=None, unit=None, comments=None):
        super().__init__(comments)

        self.__category = category
        self.__value = value
        self.__unit = unit

    @property
    def category(self):
        """:obj:`ProtocolParameter`: a references to the ProtocolParameter the
        value applies to"""
        return self.__category

    @category.setter
    def category(self, val):
        if val is not None and not isinstance(val, ProtocolParameter):
            raise ISAModelAttributeError(
                'ParameterValue.category must be a ProtocolParameter '
                'or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__category = val

    @property
    def value(self):
        """:obj:`str` or :obj:`int` or :obj:`float`
        or :obj:`OntologyAnnotation`: a parameter value"""
        return self.__value

    @value.setter
    def value(self, val):
        if val is not None \
                and not isinstance(val, (str, int, float, OntologyAnnotation)):
            raise ISAModelAttributeError(
                'ParameterValue.value must be a string, numeric, an '
                'OntologyAnnotation, or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__value = val

    @property
    def unit(self):
        """ :obj:`OntologyAnnotation`: a unit for the parameter value"""
        return self.__unit

    @unit.setter
    def unit(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'ParameterValue.unit must be a OntologyAnnotation, or None; '
                'got {0}:{1}'.format(val, type(val)))
        else:
            self.__unit = val

    def __repr__(self):
        return 'isatools.model.ParameterValue(category={category}, ' \
               'value={value}, unit={unit}, comments={comments})'.format(
            category=repr(self.category), value=repr(self.value),
            unit=repr(self.unit), comments=repr(self.comments))

    def __str__(self):
        return """ParameterValue(
    category={category}
    value={value}
    unit={unit}
    comments={num_comments} Comment objects
)""".format(category=self.category.parameter_name.term if self.category else '',
            value=self.value.term if isinstance(
            self.value, OntologyAnnotation) else repr(self.value),
            unit=self.unit.term if self.unit else '',
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ParameterValue) \
               and self.category == other.category \
               and self.value == other.value \
               and self.unit == other.unit \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class ProtocolComponent(Commentable):
    """A component used in a protocol.

    Attributes:
        name: A component name.
        component_type: The classifier as a term for the component.
        comments: Comments associated with instances of this class.
    """
    def __init__(self, id_='', name='', component_type=None, comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name

        if component_type is None:
            self.__component_type = OntologyAnnotation()
        else:
            self.__component_type = component_type

    @property
    def name(self):
        """:obj:`str`: the name of the protocol component"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'ProtocolComponent.name must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__name = val

    @property
    def component_type(self):
        """ :obj:`OntologyAnnotation`: a component_type for the protocol
        component"""
        return self.__component_type

    @component_type.setter
    def component_type(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'ProtocolComponent.component_type must be a OntologyAnnotation,'
                ' or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__component_type = val

    def __repr__(self):
        return "isatools.model.ProtocolComponent(name='{component.name}', " \
               "category={component_type}, " \
               "comments={component.comments})".format(
                component=self, component_type=repr(self.component_type))

    def __str__(self):
        return """ProtocolComponent(
    name={component.name}
    category={component_type}
    comments={num_comments} Comment objects
)""".format(component=self, component_type=self.component_type.term if
    self.component_type else '', num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ProtocolComponent) \
               and self.name == other.name \
               and self.component_type == other.component_type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class Source(Commentable):
    """Represents a Source material in an experimental graph.

    Attributes:
        name: A name/reference for the source material.
        characteristics: A list of Characteristics used to qualify the material
            properties.
        comments: Comments associated with instances of this class.
    """
    def __init__(self, name='', id_='', characteristics=None, comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name

        if characteristics is None:
            self.__characteristics = []
        else:
            self.__characteristics = characteristics

    @property
    def name(self):
        """:obj:`str`: the name of the source material"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Source.name must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__name = val

    @property
    def characteristics(self):
        """:obj:`list` of :obj:`Characteristic`: Container for source material
        characteristics"""
        return self.__characteristics

    @characteristics.setter
    def characteristics(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Characteristic) for x in val):
                self.__characteristics = list(val)
        else:
            raise ISAModelAttributeError(
                'Source.characteristics must be iterable containing '
                'Characteristics')

    def has_char(self, char):
        if isinstance(char, str):
            char = Characteristic(category=OntologyAnnotation(term=char))
        if isinstance(char, Characteristic):
            return char in self.characteristics

    def get_char(self, name):
        hits = [x for x in self.characteristics if x.category.term == name]
        try:
            result = next(iter(hits))
        except StopIteration:
            result = None
        return result

    def __repr__(self):
        return "isatools.model.Source(name='{source.name}', " \
               "characteristics={source.characteristics}, " \
               "comments={source.comments})".format(source=self)

    def __str__(self):
        return """Source(
    name={source.name}
    characteristics={num_characteristics} Characteristic objects
    comments={num_comments} Comment objects
)""".format(source=self, num_characteristics=len(self.characteristics),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Source) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class Characteristic(Commentable):
    """A Characteristic acts as a qualifying property to a material object.

    Attributes:
        category: The classifier of the type of characteristic being described.
        value: The value of this instance of a characteristic as relevant to
            the attached material.
        unit: If applicable, a unit qualifier for the value (if the value is
            numeric).
        """
    def __init__(self, category=None, value=None, unit=None, comments=None):
        super().__init__(comments)

        if category is None:
            self.__category = OntologyAnnotation()
        else:
            self.__category = category

        if value is None:
            self.__value = OntologyAnnotation()
        else:
            self.__value = value

        self.__unit = unit

    @property
    def category(self):
        """ :obj:`OntologyAnnotation`: a category for the characteristic
        component"""
        return self.__category

    @category.setter
    def category(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'Characteristic.category must be a OntologyAnnotation,'
                ' or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__category = val

    @property
    def value(self):
        """:obj:`str` or :obj:`int` or :obj:`float`
        or :obj:`OntologyAnnotation`: a characteristic value"""
        return self.__value

    @value.setter
    def value(self, val):
        if val is not None \
                and not isinstance(val, (str, int, float, OntologyAnnotation)):
            raise ISAModelAttributeError(
                'Characteristic.value must be a string, numeric, an '
                'OntologyAnnotation, or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__value = val

    @property
    def unit(self):
        """ :obj:`OntologyAnnotation`: a unit for the characteristic value"""
        return self.__unit

    @unit.setter
    def unit(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'Characteristic.unit must be a OntologyAnnotation, or None; '
                'got {0}:{1}'.format(val, type(val)))
        else:
            self.__unit = val

    def __repr__(self):
        return 'isatools.model.Characteristic(' \
               'category={category}, value={value}, ' \
               'unit={unit}, comments={characteristic.comments})'.format(
                characteristic=self, category=repr(self.category),
                value=repr(self.value), unit=repr(self.unit))

    def __str__(self):
        return """Characteristic(
    category={category}
    value={value}
    unit={unit}
    comments={num_comments} Comment objects
)""".format(characteristic=self,
           category=self.category.term if self.category else '',
           value=self.value.term if isinstance(
               self.value, OntologyAnnotation) else self.value,
           unit=self.unit.term if self.unit else '',
           num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Characteristic) \
               and self.category == other.category \
               and self.value == other.value \
               and self.unit == other.unit \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class Sample(Commentable):
    """Represents a Sample material in an experimental graph.

    Attributes:
        name: A name/reference for the sample material.
        characteristics: A list of Characteristics used to qualify the material
            properties.
        factor_values: A list of FactorValues used to qualify the material in
            terms of study factors/design.
        derives_from: A link to the source material that the sample is derived
            from.
        comments: Comments associated with instances of this class.
    """
    def __init__(self, name='', id_='', factor_values=None,
                 characteristics=None, derives_from=None, comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name

        if factor_values is None:
            self.__factor_values = []
        else:
            self.__factor_values = factor_values

        if characteristics is None:
            self.__characteristics = []
        else:
            self.__characteristics = characteristics

        if derives_from is None:
            self.__derives_from = []
        else:
            self.__derives_from = derives_from

    @property
    def name(self):
        """:obj:`str`: the name of the sample material"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                'Sample.name must be a str or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__name = val

    @property
    def factor_values(self):
        """:obj:`list` of :obj:`FactorValue`: Container for sample material
        factor_values"""
        return self.__factor_values

    @factor_values.setter
    def factor_values(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, FactorValue) for x in val):
                self.__factor_values = list(val)
        else:
            raise ISAModelAttributeError(
                'Sample.factor_values must be iterable containing '
                'FactorValues')

    @property
    def characteristics(self):
        """:obj:`list` of :obj:`Characteristic`: Container for sample material
        characteristics"""
        return self.__characteristics

    @characteristics.setter
    def characteristics(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Characteristic) for x in val):
                self.__characteristics = list(val)
        else:
            raise ISAModelAttributeError(
                'Sample.characteristics must be iterable containing '
                'Characteristics')

    def has_char(self, char):
        if isinstance(char, str):
            char = Characteristic(category=OntologyAnnotation(term=char))
        if isinstance(char, Characteristic):
            return char in self.characteristics

    def get_char(self, name):
        hits = [x for x in self.characteristics if x.category.term == name]
        try:
            result = next(iter(hits))
        except StopIteration:
            result = None
        return result

    @property
    def derives_from(self):
        """:obj:`list` of :obj:`Source`: a list of references from this sample
        material to a source material(s)"""
        return self.__derives_from

    @derives_from.setter
    def derives_from(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Source) for x in val):
                self.__derives_from = list(val)
        else:
            raise ISAModelAttributeError(
                'Sample.derives_from must be iterable containing Sources')

    def __repr__(self):
        return "isatools.model.Sample(name='{sample.name}', " \
               "characteristics={sample.characteristics}, " \
               "factor_values={sample.factor_values}, " \
               "derives_from={sample.derives_from}, " \
               "comments={sample.comments})".format(sample=self)

    def __str__(self):
        return """Sample(
    name={sample.name}
    characteristics={num_characteristics} Characteristic objects
    factor_values={num_factor_values} FactorValue objects
    derives_from={num_derives_from} Source objects
    comments={num_comments} Comment objects
)""".format(sample=self, num_characteristics=len(self.characteristics),
            num_factor_values=len(self.factor_values),
            num_derives_from=len(self.derives_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Sample) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.factor_values == other.factor_values \
               and self.derives_from == other.derives_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class Material(Commentable, metaclass=abc.ABCMeta):
    """Represents a generic material in an experimental graph.
    """
    def __init__(self, name='', id_='', type_='', characteristics=None,
                 comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name
        self.__type = type_

        if characteristics is None:
            self.__characteristics = list()
        else:
            self.__characteristics = characteristics

    @property
    def name(self):
        """:obj:`str`: the name of the material"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                '{0}.name must be a str or None; got {1}:{2}'
                .format(type(self).__name__, val, type(val)))
        else:
            self.__name = val

    @property
    def type(self):
        """:obj:`str`: the type of the material"""
        return self.__type

    @type.setter
    def type(self, val):
        if val is not None and not isinstance(val, str) \
                and val not in ('Extract Name', 'Labeled Extract Name'):
            raise ISAModelAttributeError(
                '{0}.type must be a str in ("Extract Name", "Labeled Extract '
                'Name") or None; got {1}:{2}'
                .format(type(self).__name__, val, type(val)))
        else:
            self.__type = val

    @property
    def characteristics(self):
        """:obj:`list` of :obj:`Characteristic`: Container for material
        characteristics"""
        return self.__characteristics

    @characteristics.setter
    def characteristics(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Characteristic) for x in val):
                self.__characteristics = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.characteristics must be iterable containing '
                'Characteristics'.format(type(self).__name__))


class Extract(Material):
    """Represents a extract material in an experimental graph."""
    def __init__(self, name='', id_='', characteristics=None, comments=None):
        super().__init__(name=name, id_=id_, characteristics=characteristics,
                         comments=comments)

        self.type = 'Extract Name'

    def __repr__(self):
        return "isatools.model.Extract(name='{extract.name}', " \
               "type='{extract.type}', " \
               "characteristics={extract.characteristics}, " \
               "comments={extract.comments})".format(extract=self)

    def __str__(self):
        return """Extract(
    name={extract.name}
    type={extract.type}
    characteristics={num_characteristics} Characteristic objects
    comments={num_comments} Comment objects
)""".format(extract=self, num_characteristics=len(self.characteristics),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Extract) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.type == other.type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class LabeledExtract(Material):
    """Represents a labeled extract material in an experimental graph."""
    def __init__(self, name='', id_='', characteristics=None, comments=None):
        super().__init__(name=name, id_=id_, characteristics=characteristics,
                         comments=comments)

        self.type = 'Labeled Extract Name'

    def __repr__(self):
        return "isatools.model.LabeledExtract(name='{labeled_extract.name}', " \
               "type='Labeled Extract Name', " \
               "characteristics={labeled_extract.characteristics}, " \
               "comments={labeled_extract.comments})"\
                .format(labeled_extract=self)

    def __str__(self):
        return """LabeledExtract(
    name={labeled_extract.name}
    type=LabeledExtract Name
    characteristics={num_characteristics} Characteristic objects
    comments={num_comments} Comment objects
)""".format(labeled_extract=self, num_characteristics=len(self.characteristics),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, LabeledExtract) \
               and self.name == other.name \
               and self.characteristics == other.characteristics \
               and self.type == other.type \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class FactorValue(Commentable):
    """A FactorValue represents the value instance of a StudyFactor.

    Attributes:
        factor_name: Reference to an instance of a relevant StudyFactor.
        value: The value of the factor at hand.
        unit: If numeric, the unit qualifier for the value.
        comments: Comments associated with instances of this class.
    """
    def __init__(self, factor_name=None, value=None, unit=None, comments=None):
        super().__init__(comments)
        self.__factor_name = factor_name
        self.__value = value
        self.__unit = unit

    @property
    def factor_name(self):
        """:obj:`StudyFactor`: a references to the StudyFactor the
        value applies to"""
        return self.__factor_name

    @factor_name.setter
    def factor_name(self, val):
        if val is not None and not isinstance(val, StudyFactor):
            raise ISAModelAttributeError(
                'FactorValue.factor_name must be a StudyFactor '
                'or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__factor_name = val

    @property
    def value(self):
        """:obj:`str` or :obj:`int` or :obj:`float` 
        or :obj:`OntologyAnnotation`: a parameter value"""
        return self.__value

    @value.setter
    def value(self, val):
        if val is not None \
                and not isinstance(val, (str, int, float, OntologyAnnotation)):
            raise ISAModelAttributeError(
                'FactorValue.value must be a string, numeric, an '
                'OntologyAnnotation, or None; got {0}:{1}'
                .format(val, type(val)))
        else:
            self.__value = val

    @property
    def unit(self):
        """ :obj:`OntologyAnnotation`: a unit for the parameter value"""
        return self.__unit

    @unit.setter
    def unit(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise ISAModelAttributeError(
                'FactorValue.unit must be a OntologyAnnotation, or None; '
                'got {0}:{1}'.format(val, type(val)))
        else:
            self.__unit = val

    def __repr__(self):
        return "isatools.model.FactorValue(factor_name={factor_name}, " \
               "value={value}, unit={unit})" \
                .format(factor_name=repr(self.factor_name), 
                        value=repr(self.value), unit=repr(self.unit))

    def __str__(self):
        return """FactorValue(
    factor_name={factor_name}
    value={value}
    unit={unit}
)""".format(factor_name=self.factor_name.name if self.factor_name else '',
            value=self.value.term if isinstance(
                self.value, OntologyAnnotation) else repr(self.value),
            unit=self.unit.term if self.unit else '')

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, FactorValue) \
               and self.factor_name == other.factor_name \
               and self.value == other.value \
               and self.unit == other.unit

    def __ne__(self, other):
        return not self == other


class Process(Commentable):
    """Process nodes represent the application of a protocol to some input
    material (e.g. a Source) to produce some output (e.g.a Sample).

    Attributes:
        name : If relevant, a unique name for the process to disambiguate it
            from other processes.
        executes_protocol: A reference to the Protocol that this process
            executes.
        date_: A date formatted as an ISO8601 string corresponding to when the
            process event occurred.
        performer: The name of the person or organisation that carried out the
            process.
        parameter_values: A list of ParameterValues relevant to the executing
            protocol.
        inputs: A list of input materials, possibly Sources, Samples,
            Materials, DataFiles
        outputs: A list of output materials, possibly Samples, Materials,
            DataFiles
        comments: Comments associated with instances of this class.
    """
    # TODO: replace with above but need to debug where behaviour starts varying
    def __init__(self, id_='', name='', executes_protocol=None, date_=None,
                 performer=None, parameter_values=None, inputs=None,
                 outputs=None, comments=None):
        super().__init__(comments)

        self.id = id_
        self.__name = name

        if executes_protocol is None:
            self.__executes_protocol = Protocol()
        else:
            self.__executes_protocol = executes_protocol

        self.__date = date_
        self.__performer = performer
        
        if parameter_values is None:
            self.__parameter_values = []
        else:
            self.__parameter_values = parameter_values
            
        if inputs is None:
            self.__inputs = []
        else:
            self.__inputs = inputs

        if outputs is None:
            self.__outputs = []
        else:
            self.__outputs = outputs

        self.__prev_process = None
        self.__next_process = None

    @property
    def name(self):
        """:obj:`str`: disambiguation name for the process"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and isinstance(val, str):
            self.__name = val
        else:
            raise ISAModelAttributeError('Process.name must be a string')

    @property
    def executes_protocol(self):
        """:obj:`Protocol`: a references to the study protocol the process has
        applied"""
        return self.__executes_protocol

    @executes_protocol.setter
    def executes_protocol(self, val):
        if val is not None and not isinstance(val, Protocol):
            raise ISAModelAttributeError(
                'Process.executes_protocol must be a Protocol '
                'or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__executes_protocol = val

    @property
    def date(self):
        """:obj:`str`: date the process event occurred"""
        return self.__date

    @date.setter
    def date(self, val):
        if val is not None and isinstance(val, str):
            self.__date = val
        else:
            raise ISAModelAttributeError('Process.date must be a string')

    @property
    def performer(self):
        """:obj:`str`: name of the performer responsible for the process"""
        return self.__performer

    @performer.setter
    def performer(self, val):
        if val is not None and isinstance(val, str):
            self.__performer = val
        else:
            raise ISAModelAttributeError('Process.performer must be a string')

    @property
    def parameter_values(self):
        """:obj:`list` of :obj:`ParameterValue`: Container for
        process parameter values"""
        return self.__parameter_values

    @parameter_values.setter
    def parameter_values(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, ParameterValue) for x in val):
                self.__parameter_values = list(val)
        else:
            raise ISAModelAttributeError(
                'Process.parameter_values must be iterable containing '
                'ParameterValues')

    @property
    def inputs(self):
        """:obj:`list` of :obj:`Material` or :obj:`DataFile`: Container for
        process inputs"""
        return self.__inputs

    @inputs.setter
    def inputs(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(
                    isinstance(x, (Material, Source, Sample, DataFile)) for
                    x in
                    val):
                self.__inputs = list(val)
        else:
            raise ISAModelAttributeError(
                'Process.inputs must be iterable containing objects of types '
                '(Material, Source, Sample, DataFile)')

    @property
    def outputs(self):
        """:obj:`list` of :obj:`Material` or :obj:`DataFile`: Container for
        process outputs"""
        return self.__outputs

    @outputs.setter
    def outputs(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(
                    isinstance(x, (Material, Source, Sample, DataFile)) for
                    x in val):
                self.__outputs = list(val)
        else:
            raise ISAModelAttributeError(
                'Process.outputs must be iterable containing objects of types '
                '(Material, Source, Sample, DataFile)')

    @property
    def prev_process(self):
        """:obj:`Process`: a reference to another process, previous in the
        process sequence to the current process"""
        return self.__prev_process

    @prev_process.setter
    def prev_process(self, val):
        if val is not None and not isinstance(val, Process):
            raise ISAModelAttributeError(
                'Process.prev_process must be a Process '
                'or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__prev_process = val

    @property
    def next_process(self):
        """:obj:`Process`: a reference to another process, next in the process
        sequence to the current process"""
        return self.__next_process

    @next_process.setter
    def next_process(self, val):
        if val is not None and not isinstance(val, Process):
            raise ISAModelAttributeError(
                'Process.next_process must be a Process '
                'or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__next_process = val

    # def __repr__(self):
    #     return 'Process(name="{0.name}", ' \
    #            'executes_protocol={0.executes_protocol}, ' \
    #            'date="{0.date}", performer="{0.performer}", ' \
    #            'inputs={0.inputs}, outputs={0.outputs})'.format(self)
    #
    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Process) \
               and self.name == other.name \
               and self.executes_protocol == other.executes_protocol \
               and self.date == other.date \
               and self.performer == other.performer \
               and self.inputs == other.inputs \
               and self.outputs == other.outputs

    def __ne__(self, other):
        return not self == other


class DataFile(Commentable):
    """Represents a data file in an experimental graph.

    Attributes:
        filename : A name/reference for the data file.
        label: The data file type, as indicated by a label such as 
            'Array Data File' or 'Raw Data File'
        generated_from: Reference to Sample(s) the DataFile is generated from
        comments: Comments associated with instances of this class.
    """
    def __init__(self, filename='', id_='', label='', generated_from=None, 
                 comments=None):
        super().__init__(comments)
        
        self.id = id_
        self.__filename = filename
        self.__label = label
        
        if generated_from is None:
            self.__generated_from = []
        else:
            self.__generated_from = generated_from
            
    @property
    def filename(self):
        """:obj:`str`: the filename of the data file"""
        return self.__filename

    @filename.setter
    def filename(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                '{0}.name must be a str or None; got {1}:{2}'
                .format(type(self).__name__, val, type(val)))
        else:
            self.__filename = val

    @property
    def label(self):
        """:obj:`str`: the ISA-Tab file heading label of the data file"""
        return self.__label

    @label.setter
    def label(self, val):
        if val is not None and not isinstance(val, str):
            raise ISAModelAttributeError(
                '{0}.label must be a str or None; got {1}:{2}'
                .format(type(self).__name__, val, type(val)))
        else:
            self.__label = val
            
    @property
    def generated_from(self):
        """:obj:`list` of :obj:`Sample`: a list of references from this data
        file to samples that the file was generated from"""
        return self.__generated_from

    @generated_from.setter
    def generated_from(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Sample) for x in val):
                self.__generated_from = list(val)
        else:
            raise ISAModelAttributeError(
                '{}.generated_from must be iterable containing Samples'.format(
                    type(self).__name__))

    def __repr__(self):
        return "isatools.model.DataFile(filename='{data_file.filename}', " \
               "label='{data_file.label}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})" \
               .format(data_file=self)

    def __str__(self):
        return """DataFile(
    filename={data_file.filename}
    label={data_file.label}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DataFile) \
               and self.filename == other.filename \
               and self.label == other.label \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other
            

class RawDataFile(DataFile):
    """Represents a raw data file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Raw Data File'

    def __repr__(self):
        return "isatools.model.RawDataFile(filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """RawDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, RawDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class DerivedDataFile(DataFile):
    """Represents a derived data file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Derived Data File'

    def __repr__(self):
        return "isatools.model.DerivedDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """DerivedDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DerivedDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class RawSpectralDataFile(DataFile):
    """Represents a raw spectral data file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Raw Spectral Data File'

    def __repr__(self):
        return "isatools.model.RawSpectralDataFile(filename='{0.filename}', " \
               "generated_from={0.generated_from}, comments={0.comments})" \
            .format(self)

    def __str__(self):
        return """RawSpectralDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, RawSpectralDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class DerivedArrayDataFile(DataFile):
    """Represents a derived array data file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Derived Array Data File'

    def __repr__(self):
        return "isatools.model.DerivedArrayDataFile(" \
               "filename='{data_file.filename}' " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """DerivedArrayDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DerivedArrayDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class ArrayDataFile(DataFile):
    """Represents a array data file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Array Data File'

    def __repr__(self):
        return "isatools.model.ArrayDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """ArrayDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ArrayDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class DerivedSpectralDataFile(DataFile):
    """Represents a derived spectral data file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Derived Spectral Data File'

    def __repr__(self):
        return "isatools.model.DerivedSpectralDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """DerivedSpectralDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DerivedSpectralDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class ProteinAssignmentFile(DataFile):
    """Represents a protein assignment file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Protein Assignment File'

    def __repr__(self):
        return "isatools.model.ProteinAssignmentFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """ProteinAssignmentFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ProteinAssignmentFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class PeptideAssignmentFile(DataFile):
    """Represents a peptide assignment file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Peptide Assignment File'

    def __repr__(self):
        return "isatools.model.PeptideAssignmentFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """PeptideAssignmentFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, PeptideAssignmentFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class DerivedArrayDataMatrixFile(DataFile):
    """Represents a derived array data matrix file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Derived Array Data Matrix File'

    def __repr__(self):
        return "isatools.model.DerivedArrayDataMatrixFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """DerivedArrayDataMatrixFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DerivedArrayDataMatrixFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class PostTranslationalModificationAssignmentFile(DataFile):
    """Represents a post translational modification assignment file in an
    experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Post Translational Modification Assignment File'

    def __repr__(self):
        return "isatools.model.PostTranslationalModificationAssignmentFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """PostTranslationalModificationAssignmentFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, PostTranslationalModificationAssignmentFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class AcquisitionParameterDataFile(DataFile):
    """Represents a acquisition parameter data file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Acquisition Parameter Data File'

    def __repr__(self):
        return "isatools.model.AcquisitionParameterDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """AcquisitionParameterDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, AcquisitionParameterDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class FreeInductionDecayDataFile(DataFile):
    """Represents a free induction decay data file in an experimental graph."""
    def __init__(self, filename='', id_='', generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Free Induction Decay Data File'

    def __repr__(self):
        return "isatools.model.FreeInductionDecayDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """FreeInductionDecayDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, FreeInductionDecayDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


def batch_create_materials(material=None, n=1):
    """Creates a batch of material objects (Source, Sample or Material) from a
    prototype material object

    :param material: existing material object to use as a prototype
    :param n: Number of material objects to create in the batch
    :returns: List of material objects

    :Example:

        # Create 10 sample materials derived from one source material

        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material', derives_from=source)
        batch = batch_create_materials(prototype_sample, n=10)

        [Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>,
        Sample<>, Sample<>, Sample<>, ]

    """
    material_list = list()
    if isinstance(material, (Source, Sample, Material)):
        from copy import deepcopy
        for x in range(0, n):
            new_obj = deepcopy(material)
            new_obj.name = material.name + '-' + str(x)

            if hasattr(material, 'derives_from'):
                new_obj.derives_from = material.derives_from

            material_list.append(new_obj)

    return material_list


def batch_create_assays(*args, n=1):
    """Creates a batch of assay process sequences (Material->Process->Material)
    from a prototype sequence (currently works only as flat end-to-end
    processes of Material->Process->Material->...)

    :param *args: An argument list representing the process sequence prototype
    :param n: Number of process sequences to create in the batch
    :returns: List of process sequences replicating the prototype sequence

    :Example:

        # Create 3 assays of (Sample -> Process -> Material -> Process ->
        LabeledExtract)

        sample = Sample(name='sample')
        data_acquisition = Process(name='data acquisition')
        material = Material(name='material')
        labeling = Process(name='labeling')
        extract = LabeledExtract(name='lextract')
        batch = batch_create_assays(sample, data_acquisition, material,
        labeling, extract, n=3)

        [Process<> Process<>, Process<> Process<>, Process<>, Process<>]

        # Create 3 assays of ([Sample, Sample] -> Process -> [Material,
        Material])

        sample1 = Sample(name='sample')
        sample2 = Sample(name='sample')
        process = Process(name='data acquisition')
        material1 = Material(name='material')
        material2 = Material(name='material')
        batch = batch_create_assays([sample1, sample2], process, [material1,
        material2], n=3)

    """
    process_sequence = []
    materialA = None
    process = None
    materialB = None
    from copy import deepcopy
    for x in range(0, n):
        for arg in args:
            if isinstance(arg, list) and len(arg) > 0:
                if isinstance(arg[0], (Source, Sample, Material)):
                    if materialA is None:
                        materialA = deepcopy(arg)
                        y = 0
                        for material in materialA:
                            material.name = material.name + '-' + str(x) + '-' \
                                            + str(y)
                            y += 1
                    else:
                        materialB = deepcopy(arg)
                        y = 0
                        for material in materialB:
                            material.name = material.name + '-' + str(x) + '-' \
                                            + str(y)
                            y += 1
                elif isinstance(arg[0], Process):
                    process = deepcopy(arg)
                    y = 0
                    for p in process:
                        p.name = p.name + '-' + str(x) + '-' + str(y)
                        y += 1
            if isinstance(arg, (Source, Sample, Material)):
                if materialA is None:
                    materialA = deepcopy(arg)
                    materialA.name = materialA.name + '-' + str(x)
                else:
                    materialB = deepcopy(arg)
                    materialB.name = materialB.name + '-' + str(x)
            elif isinstance(arg, Process):
                process = deepcopy(arg)
                process.name = process.name + '-' + str(x)
            if materialA is not None and materialB is not None \
                    and process is not None:
                if isinstance(process, list):
                    for p in process:
                        if isinstance(materialA, list):
                            p.inputs = materialA
                        else:
                            p.inputs.append(materialA)
                        if isinstance(materialB, list):
                            p.outputs = materialB
                            for material in materialB:
                                material.derives_from = materialA
                        else:
                            p.outputs.append(materialB)
                            materialB.derives_from = materialA
                else:
                    if isinstance(materialA, list):
                        process.inputs = materialA
                    else:
                        process.inputs.append(materialA)
                    if isinstance(materialB, list):
                        process.outputs = materialB
                        for material in materialB:
                            material.derives_from = materialA
                    else:
                        process.outputs.append(materialB)
                        materialB.derives_from = materialA
                    process_sequence.append(process)
                materialA = materialB
                process = None
                materialB = None
    return process_sequence


class ISADocument:


    valid_isajson = False

    def __init__(self, isa_obj):
        self._root = None
        if isinstance(isa_obj, Investigation):
            self._root = isa_obj
        elif isinstance(isa_obj, Study):
            self._root = Investigation(studies=[isa_obj])
        elif isinstance(isa_obj, Assay):
            self._root = Investigation(studies=[Study(assays=[isa_obj])])

    @property
    def valid_isatab(self):
        if self._root.filename is None or self._root.filename == '':
            return False
        for study in self._root.studies:
            if study.filename is None or study.filename == '':
                return False
            for assay in study.assays:
                if assay.filename is None or assay.filename == '':
                    return False
        return True

    @property
    def valid_isajson(self):
        return True


def plink(p1, p2):
    if isinstance(p1, Process) and isinstance(p2, Process):
        p1.next_process = p2
        p2.prev_process = p1
