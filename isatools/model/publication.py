from isatools.model.comments import Commentable
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.utils import get_context_path


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
            raise AttributeError('Publication.pubmed_id must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__pubmed_id = val

    @property
    def doi(self):
        """:obj:`str`: the DOI of the publication"""
        return self.__doi

    @doi.setter
    def doi(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('Publication.doi must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__doi = val

    @property
    def author_list(self):
        """:obj:`str`: the author list (comma separated) of the publication"""
        return self.__author_list

    @author_list.setter
    def author_list(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('Publication.author_list must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__author_list = val

    @property
    def title(self):
        """:obj:`str`: the title of the publication"""
        return self.__title

    @title.setter
    def title(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('Publication.title must be a str or None; got {0}:{1}'.format(val, type(val)))
        self.__title = val

    @property
    def status(self):
        """:obj:`OntologyAnnotation: an ontology annotation representing the
        publication status"""
        return self.__status

    @status.setter
    def status(self, val):
        if val is not None and not isinstance(val, OntologyAnnotation):
            raise AttributeError('Publication.status must be a OntologyAnnotation or None; got {0}:{1}'
                                 .format(val, type(val)))
        self.__status = val

    def __repr__(self):
        return ("isatools.model.Publication("
                "pubmed_id='{publication.pubmed_id}', "
                "doi='{publication.doi}', "
                "author_list='{publication.author_list}', "
                "title='{publication.title}', status={status}, "
                "comments={publication.comments})"
                ).format(publication=self, status=repr(self.status))

    def __str__(self):
        return ("Publication(\n\t"
                "pubmed_id={publication.pubmed_id}\n\t"
                "doi={publication.doi}\n\t"
                "author_list={publication.author_list}\n\t"
                "title={publication.title}\n\t"
                "status={status}\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(publication=self,
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

    def to_dict(self):
        status = self.status if self.status else {"@id": ''}
        if isinstance(self.status, OntologyAnnotation):
            status = self.status.to_dict()
        return {
            "authorList": self.author_list,
            "doi": self.doi,
            "pubMedID": self.pubmed_id,
            "status": status,
            "title": self.title,
            "comments": [comment.to_dict() for comment in self.comments]
        }

    def to_ld(self, context: str = "obo"):
        if context not in ["obo", "sdo", "wdt"]:
            raise ValueError("context should be obo, sdo or wdt but got %s" % context)

        context_path = get_context_path("publication", context)
        publication = self.to_dict()
        publication["@type"] = "Publication"
        publication["@context"] = context_path
        publication["@id"] = "#publication/" + self.id

    def from_dict(self, publication):
        self.author_list = publication['authorList'] if 'authorList' in publication else ''
        self.doi = publication['doi'] if 'doi' in publication else ''
        self.pubmed_id = publication['pubMedID'] if 'pubMedID' in publication else ''
        self.title = publication['title'] if 'title' in publication else ''
        self.load_comments(publication.get('comments', []))

        status = OntologyAnnotation()
        status.from_dict(publication.get('status', {}))
        self.status = status
