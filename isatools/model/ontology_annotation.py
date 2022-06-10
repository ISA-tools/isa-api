from __future__ import annotations
from typing import List, Any
from isatools.model.comments import Commentable, Comment
from isatools.model.ontology_source import OntologySource
from isatools.model.identifiable import Identifiable
from isatools.model.loader_indexes import loader_states as indexes


class OntologyAnnotation(Commentable, Identifiable):
    """An ontology annotation

    Attributes:
        term : A term taken from an ontology or controlled vocabulary.
        term_source : Reference to the OntologySource from which the term is
            derived.
        term_accession : A URI or resource-specific identifier for the term.
        comments: Comments associated with instances of this class.
    """

    def __init__(self,
                 term: str = '',
                 term_source: OntologySource = None,
                 term_accession: str = '',
                 comments: List[Comment] = None,
                 id_: str = ''):
        super().__init__(comments=comments)

        self.__term = term
        self.__term_source = term_source
        self.__term_accession = term_accession
        self.id = id_

    @property
    def term(self) -> str:
        """:obj:`str`: the ontology annotation name used"""
        return self.__term

    @term.setter
    def term(self, val: str):
        if val is not None and not isinstance(val, str):
            raise AttributeError('OntologyAnnotation.term must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__term = val

    @property
    def term_source(self) -> OntologySource:
        """:obj:`OntologySource: a reference to the ontology source the term is
        taken from"""
        return self.__term_source

    @term_source.setter
    def term_source(self, val: OntologySource):
        if val is not None and not isinstance(val, OntologySource):
            raise AttributeError('OntologyAnnotation.term_source must be a OntologySource or '
                                 'None; got {0}:{1}'.format(val, type(val)))
        self.__term_source = val

    @property
    def term_accession(self) -> str:
        """:obj:`str`: the term accession number of reference of the term"""
        return self.__term_accession

    @term_accession.setter
    def term_accession(self, val: str):
        if val is not None and not isinstance(val, str):
            raise AttributeError('OntologyAnnotation.term_accession must be a str or None')
        self.__term_accession = val

    def __repr__(self):
        return ("isatools.model.OntologyAnnotation("
                "term='{ontology_annotation.term}', "
                "term_source={term_source}, "
                "term_accession='{ontology_annotation.term_accession}', "
                "comments={ontology_annotation.comments})"
                ).format(ontology_annotation=self, term_source=repr(self.term_source))

    def __str__(self):
        if not self.term_source == str and isinstance(self.term_source, OntologySource):
            return ("OntologyAnnotation(\n\t"
                    "term={ontology_annotation.term}\n\t"
                    "term_source={term_source_ref}\n\t"
                    "term_accession={ontology_annotation.term_accession}\n\t"
                    "comments={num_comments} Comment objects\n)"
                    ).format(ontology_annotation=self,
                             term_source_ref=self.term_source.name,
                             num_comments=len(self.comments))
        else:
            return ("OntologyAnnotation(\n\t"
                    "term={ontology_annotation.term}\n\t"
                    "term_source={term_source_ref}\n\t"
                    "term_accession={ontology_annotation.term_accession}\n\t"
                    "comments={num_comments} Comment objects\n)"
                    ).format(ontology_annotation=self,
                             term_source_ref=self.term_source,
                             num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, OntologyAnnotation)
                and self.term == other.term
                and self.term_source == other.term_source
                and self.term_accession == other.term_accession
                and self.comments == other.comments)

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def to_dict(self):
        term_source = "" if not self.term_source else self.term_source
        if self.term_source and isinstance(self.term_source, OntologySource):
            term_source = self.term_source.name

        return {
            '@id': self.id,
            'annotationValue': self.term,
            'termSource': term_source,
            'termAccession': self.term_accession,
            'comments': [comment.to_dict() for comment in self.comments]
        }

    def from_dict(self, ontology_annotation):
        self.id = ontology_annotation.get('@id', '')
        self.term = ontology_annotation.get('annotationValue', '')
        self.term_accession = ontology_annotation.get('termAccession', '')
        self.load_comments(ontology_annotation.get('comments', []))

        if 'termSource' in ontology_annotation and ontology_annotation['termSource']:
            source = indexes.get_term_source(ontology_annotation['termSource'])
            self.term_source = source
