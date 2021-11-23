import os
from rdflib import Graph


class JSONLDToTTLConverter:

    def __init__(self, json_path, output_path):
        full_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), json_path)
        full_output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path)
        graph = Graph()
        graph.parse(full_json_path)
        rdf_path = os.path.join(full_output_path)
        with open(rdf_path, 'w') as rdf_file:
            rdf_file.write(graph.serialize(format='turtle'))
