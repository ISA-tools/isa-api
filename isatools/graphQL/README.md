# ISA-QL:

ISA-QL is a syntax querying language for ISA Assay and Process objects based on [GraphQL](https://graphql.org/) and 
[Graphene](https://github.com/graphql-python/graphene).
It provides a fast and easy programmatic access to the very complex and nested fields within an ISA Investigation as 
well as the ability to filter attributes based on user inputs.
It is bundled with the ISA-api python library and directly integrated as a method of ISA Investigation objects.

---

## Getting Started
To use the ISA-QL queries, you just need to load an ISA investigation. The example below shows how to load the
INVESTIGATION.txt file from the "/DIRNAME/" directory as an ISA investigation using the ``load()`` function.

```python
from os import path
from isatools.isatab import load

here_path = path.dirname(path.realpath(__file__))
investigation_filepath = path.join(here_path, path.join("DIRNAME", "INVESTIGATION.txt"))
with open(investigation_filepath, "r") as investigation_file:
    investigation = load(investigation_file)
    investigation_file.close()
```

One of the very powerful features of GraphQL is its ability to self document through what are called introspection 
queries. These queries can ask an endpoint information about the queryable fields and their valid inputs.
One of these queries has already been written for easiness of use and wrapped in the ``investivagation.instropect()``
method (see usage below.)

```python
from json import dumps
documentation = investigation.introspect()
print(dumps(documentation.data, indent=1))
```

The introspection query is accessible inside the ``/graphQL/queries/`` directory. Feel free to explore the query and its
outputs before writing your own.

---

## Queryable Objects:
There are 3 mains queryable objects at the root of the ISA-QL syntax: the investigation, the studies and the assays.

### Investigation:

#### Queryable fields:
- filename: a string representing the name of the investigation file.
- identifier: a string representing an identifier for this investigation.
- title: a string representing a title for this investigation.
- description: a string representing a description for this investigation.
- submissionDate: a datetime representing the submission date of the investigation.
- publicReleaseDate: a datetime representing the public release date of the investigation.
- ontologySourceReferences: a list of ontology source references used by this investigation.
- publications: a list of publications associated with the investigation.
- people: a list of people to be contacted.
- [studies](#studies): the list of queryable and filterable studies bound to this investigation.

Below is a simple example on how to get an investigation title, description and identifier, in that order.

```python
query = '{ investigation { title description identifier }}'
response = investigation.execute_query(query)
if response.data:
    print(dumps(response.data, indent=1))
elif response.errors:
    print(response.errors)
```

As shown in the example above, the query is divided into two segments: the first one indicates which object we want to
query (in this case an `investigation`). The second one, located between the second set of curly brackets indicated the 
fields we want to retrieve. Queryable fields can be simple, as shown in the example, or represent complex objects which 
also have their own queryable fields.

### Studies:

#### Queryable fields:
- filename: a string representing the name of the study file.
- identifier: a string representing an identifier for this study.
- title: a string representing a study for this study.
- description: a string representing a study for this study.
- submissionDate: a datetime representing the submission date of the study.
- publicReleaseDate: a datetime representing the public release date of the study.
- publications: a list of publications associated with the study.
- people: a list of people to be contacted.
- studyDesignDescriptors: a list of ontology annotation representing the design descriptors of this study.
- protocols: a list of protocols associated with this study.
- materials: a list of materials associated with this study.
- processSequence: a list of processes (represented as a sequences) associated with this study.
- [assay](#assays): a list of assay types associated with this study.
- factor: a list of factors associated with this study.
- characteristicCategories: a list of ontology annotations representing the categories of characteristics associated 
  with this study.
- unitCategories: a list of ontology annotations representing the categories of units associated with this study.

We could rewrite the previous example's query to request the same fields but for studies. 

```python
query = '{ studies { title description identifier }}'
response = investigation.execute_query(query)
if response.data:
    print(dumps(response.data, indent=1))
elif response.errors:
    print(response.errors)
```

We can now increase the complexity of the query. We could request the title of the investigation, and the title,
description and identifier of all the studies associated with it.

```python
query = "{ investigation { title studies { title description identifier }}}"
response = investigation.execute_query(query)
if response.data:
  print(dumps(response.data, indent=1))
elif response.errors:
  print(response.errors)
```

### Assays:
#### Queryable fields:
- filename = String()
- measurement_type = Field(OntologyAnnotation, name="measurementType")
- technology_type = Field(OntologyAnnotation, name="technologyType")
- technology_platform = String(name="technologyPlatform")
- data_files = List(DataFile, name="dataFiles", label=Argument(StringComparator, required=False))
- materials = Field(Materials)
- characteristic_categories = List(MaterialAttribute, name="characteristicCategories")
- unit_categories = List(OntologyAnnotation, name="unitCategories")
- process_sequence