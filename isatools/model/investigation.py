import os

from isatools.model.comments import Commentable
from isatools.model.mixins import MetadataMixin
from isatools.model.ontology_annotation import OntologySource
from isatools.model.study import Study
from isatools.model.identifiable import Identifiable
from isatools.model.person import Person
from isatools.model.publication import Publication
from isatools.graphQL.models import IsaSchema
from isatools.model.loader_indexes import loader_states as indexes


class Investigation(Commentable, MetadataMixin, Identifiable, object):
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
        Identifiable.__init__(self)

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
            raise AttributeError(
                'Investigation.ontology_source_references must be iterable '
                'containing OntologySource objects')

    def add_ontology_source_reference(self, name='', version='',
                                      description='',
                                      file='', comments=None):
        """
        Adds a new ontology_source_reference to the ontology_source_reference
        list.

        Args:
            name: OntologySource name
            version: OntologySource version
            description: OntologySource description
            file: OntologySource file
            comments: list
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
            return filter(lambda x: x, self.ontology_source_references)
        else:
            return filter(lambda x: x.name == name, self.ontology_source_references)

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
            raise AttributeError('Investigation.studies must be iterable containing Study objects')

    def execute_query(self, query, variables=None):
        """
        Executes the given graphQL query with the given variables on the investigation
        :param query: a graphQL query to execute
        :param variables: the variables to bind to the graphQL query
        :return: a response containing the selected data
        """
        IsaSchema.set_investigation(self)
        return IsaSchema.execute(query, variables=variables)

    @staticmethod
    def introspect():
        """
        Executes the introspection query to get the schemas properties
        :return: a response to the introspection query
        """
        project_root = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(project_root, os.path.join("../graphQL/queries", "introspection.gql"))
        with open(filepath, "r") as introspectionFile:
            introspection_query = introspectionFile.read()
            introspectionFile.close()
        return IsaSchema.execute(introspection_query)

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
    ontology_source_references={num_ontology_source_references} OntologySources
    publications={num_publications} Publication objects
    contacts={num_contacts} Person objects
    studies={num_studies} Study objects
    comments={num_comments} Comment objects
)""".format(investigation=self,
            num_ontology_source_references=len(
                self.ontology_source_references),
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
               and self.ontology_source_references == other.ontology_source_references \
               and self.publications == other.publications \
               and self.contacts == other.contacts \
               and self.studies == other.studies \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {
            "identifier": self.identifier,
            "title": self.title,
            "description": self.description,
            "publicReleaseDate": self.public_release_date,
            "submissionDate": self.submission_date,
            "comments": [comment.to_dict() for comment in self.comments],
            "ontologySourceReferences": [
                ontology_source.to_dict() for ontology_source in self.ontology_source_references
            ],
            "people": [person.to_dict() for person in self.contacts],
            "publications": [publication.to_dict() for publication in self.publications],
            "studies": [study.to_dict() for study in self.studies]
        }

    def from_dict(self, investigation):
        self.identifier = investigation.get('identifier', '')
        self.title = investigation.get('title', '')
        self.public_release_date = investigation.get('publicReleaseDate', '')
        self.submission_date = investigation.get('submissionDate', '')
        self.description = investigation.get('description', '')
        self.load_comments(investigation.get('comments', []))

        # ontology source references
        for ontology_source_data in investigation.get('ontologySourceReferences', []):
            ontology_source = OntologySource('')
            ontology_source.from_dict(ontology_source_data)
            self.ontology_source_references.append(ontology_source)
            indexes.add_term_source(ontology_source)

        # people
        for person_data in investigation.get('people', []):
            person = Person()
            person.from_dict(person_data)
            self.contacts.append(person)

        # publications
        for publication_data in investigation.get('publications', []):
            publication = Publication()
            publication.from_dict(publication_data)
            self.publications.append(publication)

        # studies
        for study_data in investigation.get('studies', []):
            study = Study()
            study.from_dict(study_data)
            self.studies.append(study)

        indexes.reset_store()
