# ISA data model

+++

For the ISA tools API, we have represented the ISA model version 1.0
(see the ISA-Tab specification) with a set of [JSON
schemas](http://json-schema.org/), which provide the information the ISA
model maintains for each of the objects.

***

```{figure} ../_static/images/isa-model.png
:height: 450px
:name: ISA

an overview of the ISA model
```

***

The objective of designing and developing JSON schemas is to support a
**new serialization of the ISA model in JSON format**, in addition to
existing serializations in *tabular format*and RDF format.

The core set of schemas for ISA model version 1.0 can be found in the
folder
[isatools/resources/schemas/isa\_model\_version\_1\_0\_schemas/core](https://github.com/ISA-tools/isa-api/tree/master/isatools/resources/schemas/isa_model_version_1_0_schemas/core).

The main object is the
`[Investigation](https://github.com/ISA-tools/isa-api/tree/master/isatools/resources/schemas/isa_model_version_1_0_schemas/core/investigation_schema.json)`,
which groups a set of `Studies` and maintains associated information such
as `Publications`, `People` involved and the `Ontologies` used for annotating
the dataset made up of `Raw or Derived Data File` and metadata about `Materials` and `Protocols` acting on those.	
