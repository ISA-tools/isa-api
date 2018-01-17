"""Functions for connecting the Ontology Lookup Service.

This module connects to the European Bioinformatics Institute's OLS.
If you have problems with it, check that it's working at
http://www.ebi.ac.uk/ols/
"""
from __future__ import absolute_import
import json
import logging
from urllib.request import urlopen
from urllib.parse import urlencode


from isatools.model import OntologySource, OntologyAnnotation

OLS_API_BASE_URI = "http://www.ebi.ac.uk/ols/api"
OLS_PAGINATION_SIZE = 500


log = logging.getLogger('isatools')


def get_ols_ontologies():
    """Returns a list of OntologySource objects according to what's in OLS"""
    ontologiesUri = OLS_API_BASE_URI + "/ontologies?size=" + str(OLS_PAGINATION_SIZE)
    log.debug(ontologiesUri)
    J = json.loads(urlopen(ontologiesUri).read().decode("utf-8"))
    ontology_sources = []
    for ontology_source_json in J["_embedded"]["ontologies"]:
        ontology_sources.append(OntologySource(
            name=ontology_source_json["ontologyId"],
            version=ontology_source_json["config"]["version"],
            description=ontology_source_json["config"]["title"],
            file=ontology_source_json['_links']['self']
        ))
    return ontology_sources


def get_ols_ontology(ontology_name):
    """Returns a single OntologySource objects according to what's in OLS"""
    ontologiesUri = OLS_API_BASE_URI + "/ontologies?size=" + str(OLS_PAGINATION_SIZE)
    log.debug(ontologiesUri)
    J = json.loads(urlopen(ontologiesUri).read().decode("utf-8"))
    ontology_sources = []
    for ontology_source_json in J["_embedded"]["ontologies"]:
        ontology_sources.append(OntologySource(
            name=ontology_source_json["ontologyId"],
            version=ontology_source_json["config"]["version"],
            description=ontology_source_json["config"]["title"],
            file=ontology_source_json['_links']['self']['href']
        ))
    hits = [o for o in ontology_sources if o.name == ontology_name]
    if len(hits) == 1:
        return hits[0]
    else:
        return None


def search_ols(term, ontology_source):
    """Returns a list of OntologyAnnotation objects according to what's returned by OLS search"""
    url = OLS_API_BASE_URI + "/search"
    if isinstance(ontology_source, str):
        os_search = ontology_source
    elif isinstance(ontology_source, OntologySource):
        os_search = ontology_source.name
    else:
        os_search = None
    query = "{0}&queryFields=label&ontology={1}&exact=True".format(term, os_search)
    url += '?q={}'.format(query)
    log.debug(url)
    import requests
    req = requests.get(url)
    J = json.loads(req.text)
    ontology_annotations = []
    for search_result_json in J["response"]["docs"]:
        ontology_annotations.append(
            OntologyAnnotation(
                term=search_result_json["label"],
                term_accession=search_result_json["iri"],
                term_source=ontology_source if isinstance(ontology_source, OntologySource) else None
            ))
    return ontology_annotations
