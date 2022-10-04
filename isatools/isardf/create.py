from rdflib import Namespace, Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD

OBO = Namespace("http://purl.obolibrary.org/obo/")
SDO = Namespace("https://schema.org/")
WDTP = Namespace("https://www.wikidata.org/wiki/Property:")
WDT = Namespace("http://www.wikidata.org/wiki/")


def convert_to_rdf(investigations):
    g = Graph(store="Oxigraph")
    g.bind("obo", OBO)
    g.bind("xsd", XSD)
    g.bind("sdo", SDO)
    g.bind("wdt", WDT)
    g.bind("wdtp", WDTP)

    for investigation in investigations:
        inv = URIRef("https://example.org/investigation/1")

        # Start with the investigation itself
        g.add((inv, RDF.type, OBO['OBI_0000066']))
        g.add((inv, RDF.type, SDO['ResearchProject']))
        g.add((inv, RDF.type, WDT['Q170584']))

        # Now the title
        title = Literal(investigation['title'])
        g.add((inv, OBO['OBI_0001622'], title))
        g.add((inv, SDO['headline'], title))
        g.add((inv, WDTP['P1476'], title))

        # Now the description
        description = Literal(investigation['description'])
        g.add((inv, OBO['IAO_0000300'], description))
        g.add((inv, SDO['description'], description))
        g.add((inv, WDTP['P1552'], description))

        # Now the submission date
        submission_date = Literal(investigation['submissionDate'], datatype=XSD.date)
        g.add((inv, OBO['RO_0002537'], submission_date))
        g.add((inv, SDO['uploadDate'], submission_date))
        g.add((inv, WDTP['P585'], submission_date))
    return g


if __name__ == '__main__':
    from isatools.model import Investigation

    investigation_ = Investigation(title='My first investigation', description='This is a test',
                                   submission_date='2019-01-01')
    gr = convert_to_rdf([investigation_.to_dict()])

    # QUERYING FOR TEST
    q = """
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        PREFIX sdo: <https://schema.org/>
        PREFIX wdt: <http://www.wikidata.org/wiki/>

        SELECT distinct *
        WHERE {
            ?p rdf:type obo:OBI_0000066 .
            ?p rdf:type wdt:Q170584 .
            ?p rdf:type sdo:ResearchProject .
            
            ?p obo:OBI_0001622 ?title .
            filter contains(?title, "first")
            ?p sdo:headline ?headline .
            filter contains(?headline, "investigation")
        }
    """
    print(gr.serialize())
    print('RESULTS:')
    for r in gr.query(q):
        print(r.asdict())
