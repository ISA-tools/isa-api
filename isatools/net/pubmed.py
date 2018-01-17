"""Functions for querying PubMed.

This module connects to the PubMed API via Entrez.
If you have problems with it, check that it's working at
https://www.ncbi.nlm.nih.gov/pubmed/
"""
from __future__ import absolute_import
from Bio import Entrez, Medline
import logging


from isatools.model import Comment, Publication


log = logging.getLogger('isatools')


def get_pubmed_article(pubmed_id):
    # http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc126
    response = {}
    Entrez.email = "isatools@googlegroups.com"
    handle = Entrez.efetch(db="pubmed", id=pubmed_id.strip(), rettype="medline", retmode="text")
    records = Medline.parse(handle)
    for record in records:
        response["pubmedid"] = pubmed_id
        response["title"] = record.get("TI", "")
        response["authors"] = record.get("AU", "")
        response["journal"] = record.get("TA", "")
        response["year"] = record.get("EDAT", "").split("/")[0]
        lidstring = record.get("LID", "")
        if "[doi]" in lidstring:
            response["doi"] = record.get("LID", "").split(" ")[0]
        else:
            response["doi"] = ""
        if not response["doi"]:
            aids = record.get("AID", "")
            for aid in aids:
                log.debug("AID:" + aid)
                if "[doi]" in aid:
                    response["doi"] = aid.split(" ")[0]
                    break
                else:
                    response["doi"] = ""

        break
    return response


def set_pubmed_article(publication):
    """
        Given a Publication object with pubmed_id set to some value, set the rest of the values from information
        collected via Entrez webservice from PubMed
    """
    if isinstance(publication, Publication):
        response = get_pubmed_article(publication.pubmed_id)
        publication.doi = response["doi"]
        publication.author_list = ", ".join(response["authors"])
        publication.title = response["title"]
        publication.comments = [Comment(name="Journal", value=response["journal"])]
    else:
        raise TypeError("Can only set PubMed details on a Publication object")