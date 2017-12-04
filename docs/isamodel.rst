##############
ISA data model
##############

For the ISA tools API, we have represented the ISA model version 1.0 (see the ISA-Tab specification) with a set of `JSON schemas <http://json-schema.org/>`_, which provide the information the ISA model maintains for each of the objects.

The objective of designing and developing JSON schemas is to support a new serialization of the ISA-Tab model in JSON format, in addition to existing serializations in tabular format and RDF format.

The core set of schemas for ISA model version 1.0 can be found in the folder `isatools/resources/schemas/isa_model_version_1_0_schemas/core <https://github.com/ISA-tools/isa-api/tree/master/isatools/resources/schemas/isa_model_version_1_0_schemas/core>`_.

The main object is the `Investigation <https://github.com/ISA-tools/isa-api/tree/master/isatools/resources/schemas/isa_model_version_1_0_schemas/core/investigation_schema.json>`_, which groups a set of Studies and maintains associated information such as Publications, People involved and the ontologies used for annotating the dataset.