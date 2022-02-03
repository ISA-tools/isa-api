# ISA-QL:

ISA-QL is a syntax querying language built for the ISA model and based on [GraphQL](https://graphql.org/) and 
[Graphene](https://github.com/graphql-python/graphene).
It provides a fast and easy programmatic access to the very complex and nested fields within an ISA Investigation as 
well as the ability to filter attributes based on user inputs.
It is bundled with the ISA-api python library and directly integrated as a method of ISA Investigation objects.

---

## Getting Started
To use the ISA-QL queries, you just need to load an ISA investigation. The example below shows how to load the
INVESTIGATION.txt file from the `/DIRNAME/` directory as an ISA investigation using the ``load()`` function.

```python
from os import path
from isatools.isatab import load

here_path = path.dirname(path.realpath(__file__))
investigation_filepath = path.join(here_path, path.join("DIRNAME", "INVESTIGATION.txt"))
with open(investigation_filepath, "r") as investigation_file:
    investigation = load(investigation_file)
    investigation_file.close()
```

One of the powerful features of GraphQL is its ability to self-document through so-called *introspection 
queries*. This allows interrogating an endpoint information about the queryable fields and their valid inputs.
One such *introspection query* has already been written for ease of use and wrapped in the ``investigation.instropect()``
method (see usage below.)

```python
from json import dumps
documentation = investigation.introspect()
print(dumps(documentation.data, indent=1))
```

The *introspection query* is available from the ``/graphQL/queries/`` directory. Check it out along with its output and use it as a guide before writing your own.

---

## Queryable Objects:
There are 3 mains queryable objects at the root of the ISA-QL syntax: 

- the [investigation](#investigation)

- the [studies](#study)

- the [assays](#assay)
### The Investigation query:

#### Queryable fields:
| Field name                  |             Description                              |                   Type                                  |
|-----------------------------|------------------------------------------------------|---------------------------------------------------------|
| filename                    | Name of the investigation file                       | String                                                  |
| identifier                  | Identifier of the investigation                      | String                                                  |
| title                       | Title of the investigation                           | String                                                  |
| description                 | Description of the investigation                     | String                                                  |
| submissionDate              | Submission date of the investigation                 | DateTime                                                |
| publicReleaseDate           | Public release date of the investigation             | DateTime                                                |
| ontologySourceReferences    | Ontology source references used by the investigation | [OntologySourceReference](#OntologySourceReference)     |
| publications                | Publications associated with the investigation       | [Publication](#Publication)                             |  
| people                      | People to contact for the investigation              | [Person](#Person)                                       |
| studies                     | Studies associated with the investigation            | [Study](#Study)                                       |

Below is a simple example on how to get an investigation title, description and identifier, in that order.

```python
query = '{ investigation { title description identifier }}'
response = investigation.execute_query(query)
if response.data:
    print(dumps(response.data, indent=1))
elif response.errors:
    print(response.errors)
```

As shown in the example above, the `query` is divided into two segments: the first one indicates which object we want to
query (in this case an `investigation`). The second one, located between the second set of curly brackets indicates the 
fields we want to retrieve. 
Queryable fields can be simple, as shown in the example, or represent complex objects, which 
also have their own queryable fields.

### The Studies query:

#### Queryable fields:
| Field name                |             Description                                   |                  Type                      |
|---------------------------|-----------------------------------------------------------|--------------------------------------------|
| filename                  | Name of the study file                                    | String                                     |
| identifier                | Identifier of the study                                   | String                                     |
| title                     | Title of the study file                                   | String                                     |
| description               | Description of the study file                             | String                                     |
| submissionDate            | Date at which the study was submitted                     | DateTime                                   |
| publicReleaseDate         | Date at which the study was publicly released             | DateTime                                   |
| publications              | Publications associated with the study                    | [Publication](#Publication)                |
| people                    | People to contact for the study                           | [Person](#Person)                          |
| studyDesignDescriptors    | Design descriptors of this study                          | [OntologyAnnotation](#OntologyAnnotation)  |
| protocols                 | Protocols associated with the study                       | [Protocol](#Protocol)                      |
| materials                 | Materials associated with the study                       | [Material](#Material)                      |
| processSequence           | Processes associated with the study                       | [Process](#Process)                        |
| assay                     | Assays associated with the study                          | [Assay](#Assay)                           |
| factor                    | Factors associated with the study                         | [Factor](#Factor)                          |
| characteristicCategories  | Categories of characteristics associated with this study  | [OntologyAnnotation](#OntologyAnnotation)  |
| unitCategories            | Categories of units associated with the study             | [OntologyAnnotation](#OntologyAnnotation)  |

We can reuse the previous query to request the same fields but this time for any of the studies present in the ISA document. 

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

### The Assays query:
#### Queryable fields:
| Field name                  |             Description                                  |                      Type                        |
|-----------------------------|----------------------------------------------------------|--------------------------------------------------|
| filename                    | Name of the assay file                                   | String                                           |
| technologyPlatform          | Technology platform used in this assay                   | String                                           |
| technologyType              | Type of technology used in this assay                    | [OntologyAnnotation](#OntologyAnnotation)        |
| measurementType             | Type of measurement used in this assay                   | [OntologyAnnotation](#OntologyAnnotation)        |
| dataFiles                   | List of files used or produced in this assay             | [DataFile](#DataFile)                            |
| materials                   | Materials used in this assay                             | [Material](#Material)                            |
| characteristicCategories    | Categories of characteristics associated with this assay | [OntologyAnnotation](#OntologyAnnotation)        |
| unitCategories              | Categories of units associated with this assay           | [OntologyAnnotation](#OntologyAnnotation)        |
| processSequence             | Processes associated with this assay                     | [Process](#Process)                              |

The assay query is usable on its own (in which cases, all assays from different studies will be concatenated in the same output) or as a field of a `studies` query. 

The request below will retrieve the filename associated with the investigation, with each study in that investigation, and with each assay in each study.

```python
query = "{ investigation { filename studies { filename assays { filename }}}}"
response = investigation.execute_query(query)
if response.data:
  print(dumps(response.data, indent=1))
elif response.errors:
  print(response.errors)
```

#### Filter parameters:

###### Introduction to filters:
The assay query is different from investigations and studies because it accepts parameters that will allow to
filter them based on specific inputs. For instance, a user may want to retrieve only the assays performed using 
`nucleotide sequencing`.
The `assays` query takes two inputs:
- an operator: 'AND' or 'OR', it indicates how filters should be assembled. Its default value is always 'AND'.
- a list of filters to assemble. Each filter contains a key that indicates to which field the filter should be applied 
  and an expression in the form of an object. This expression contains a key that indicates the operation to run and a 
  value to compare with. Typically, this is how a filter would look like:
  
```
filters: {
  technologyType: { eq: "nucleotide sequencing" }
}
```

The first key (`technologyType`) indicated which field to target. The second key (`eq`) indicates which comparison operation should be executed. 

- For strings, it can take the `eq` (equal) or `in` (includes) values. 

- For integers, it can be `lt` (lower than), `lte` (lower than or equal), `gt` (greater than) or `gte` (greater than or equal). 

Finally, the string indicates the filter value is "nucleotide sequencing".

We can now apply this filter to a real query:

```python
query = '{ assays(filters: technologyType: { in: "nucleotide seq" }){ filename }}'
response = investigation.execute_query(query)
if response.data:
  print(dumps(response.data, indent=1))
elif response.errors:
  print(response.errors)
```

This query retrieves filename of assays for which the technology type includes the string "nucleotide seq".


###### Filters:
| Field name       |   Description                                                                                    | Type                                      |    Target                 |                  Controlled values        |
|------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------|---------------------------|-------------------------------------------|
| measurementType  | Type of measurement realised in the assay                                                        | String                                    | measurementType           | X                                         |
| executesProtocol | Protocol executed by a process                                                                   | String                                    | process.executesProtocol  | X                                         |
| technologyType   | Type of technology used in the assay                                                             | String                                    | technologyType            | X                                         |   
| treatmentGroup   | Conditions the group was exposed to                                                              | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                         |
| characteristics  | Characteristics the material should comply with                                                  | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                         |
| parameterValues  | Parameters values a process should comply with                                                   | [ParameterValues](#ParameterValues)       | process.parameterValues   | X                                         |
| on               | Control to which input/output type the treatmentGroup and characteristics filters should apply   | String                                    | see controlled values     | "Sample", "Source, "DataFile", "Material" |


Using the `operator` key, we can assemble multiple filters in a single query. 
However, at this point the code becomes hard to maintain, and we suggest creating dedicated query files in the `.gql` format. 

We now want to retrieve ISA assay filenames given the following constraints:
- the technology used is `nucleotide sequencing` (**exact match**)
- the subjects must have been exposed to a `low dose` of `carbon dioxide`.
- the samples were obtained from an organism part such as `liver`.

Let's create a `my_query.gql` file to store our query:

```
{
  assays(
    operator: "AND"
    filters: {
      technologyType: { eq: "nucleotide sequencing" }
      on: "Sample"
      treatmentGroup: [
        {
          name: { eq: "compound" }
          value: { eq: "carbon dioxide" }
        }
        {
          name: { eq: "dose" }
          value: { eq: "low" }
        }
      ]
      characteristics: [
          {
              name: { eq: "category" }
              value: { eq: "anatomical part" }
          }
          {
              name: { eq: "value" }
              value: { eq: "liver" }
          }
      ]
    }
  ) {
    filename
  }
}
```
We can now read the query file as a text stream and execute it the same way we previously did.

```python
query_filepath = path.join(here_path, "my_query.gql")
with open(query_filepath, "r") as query_file:
    query = query_file.read()
    query_file.close()
response = investigation.execute_query(query)
if response.data:
  print(dumps(response.data, indent=1))
elif response.errors:
  print(response.errors)
```

We now want to be able to harvest user inputs and dynamically pass values to the query instead of using plain strings.
This can be done by modifying the query and passing the values though python variables. <br>
Let's go back to our query and add the variables. To do that, we first need to alias the query, so let's name it
`assaysFilenames`. We can then pass our variable using the `$` prefix and the `ID` keyword type.
Variables can be passed to the `execute_query()` method as an optional parameter in the form of a python dictionary.
Keys match the graphQL variables but are stripped from the `$` prefix.

```
query assaysFilenames(
  $technologyType: ID
  $compound: ID
  $dose: ID
  $source: ID
){
  assays(
    operator: "AND"
    filters: {
      technologyType: { eq: $technologyType }
      on: "Sample"
      treatmentGroup: [
        {
          name: { eq: "compound" }
          value: { eq: $compound }
        }
        {
          name: { eq: "dose" }
          value: { eq: $dose }
        }
      ]
      characteristics: [
          {
              name: { eq: "category" }
              value: { eq: "anatomical part" }
          }
          {
              name: { eq: "value" }
              value: { eq: $source }
          }
      ]
    }
  ) {
    filename
  }
}
```
```python
from os import path
from json import dumps
from isatools.isatab import load

here_path = path.dirname(path.realpath(__file__))
investigation_filepath = path.join(here_path, path.join("DIRNAME", "INVESTIGATION.txt"))
with open(investigation_filepath, "r") as investigation_file:
  investigation = load(investigation_file)
  investigation_file.close()
query_filepath = path.join(here_path, "my_query.gql")
with open(query_filepath, "r") as query_file:
    query = query_file.read()
    query_file.close()
variables = {
  "technologyType": "nucleotide sequencing",
  "compound": "carbon dioxide",
  "dose": "low",
  "source": "liver"
}
response = investigation.execute_query(query, variables)
if response.data:
  print(dumps(response.data, indent=1))
elif response.errors:
  print(response.errors)
```

---

## Fields References:

### Assay:
| Field name                  |             Description                                  |                      Type                        |
|-----------------------------|----------------------------------------------------------|--------------------------------------------------|
| filename                    | Name of the assay file                                   | String                                           |
| technologyPlatform          | Technology platform used in this assay                   | String                                           |
| technologyType              | Type of technology used in this assay                    | [OntologyAnnotation](#OntologyAnnotation)        |
| measurementType             | Type of measurement used in this assay                   | [OntologyAnnotation](#OntologyAnnotation)        |
| dataFiles                   | List of files used or produced in this assay             | [DataFile](#DataFile)                            |
| materials                   | Materials used in this assay                             | [Material](#Material)                            |
| characteristicCategories    | Categories of characteristics associated with this assay | [OntologyAnnotation](#OntologyAnnotation)        |
| unitCategories              | Categories of units associated with this assay           | [OntologyAnnotation](#OntologyAnnotation)        |
| processSequence             | Processes associated with this assay                     | [Process](#Process)                              |

### Characteristic:
| Field name       |   Description                | Type                                      |
|------------------|------------------------------|-------------------------------------------|
| category         | Type of characteristic       | [OntologyAnnotation](#OntologyAnnotation) |
| unit             | Unit of the characteristic   | [OntologyAnnotation](#OntologyAnnotation) |
| value            | Value of the characteristic  | [OntologyAnnotation](#OntologyAnnotation) |

### Component:
| Field name       |   Description          | Type                    |
|------------------|------------------------|-------------------------|
| componentName    | Name of the component  | String                  |

### DataFile:
| Field name      |        Description                              |   Type                    |
|-----------------|-------------------------------------------------|---------------------------|
| name            | name of the file                                | String                    |
| type            | label of the file                               | String                    |
| generatedFrom   | Sample from which this data file was generated  | [Sample](#Sample)         |

### Factor:
| Field name             |   Description          | Type                                      |
|------------------------|------------------------|-------------------------------------------|
| factorName             | Name of the factor     | String                                    |
| factorType             | Type of factor         | [OntologyAnnotation](#OntologyAnnotation) |

### FactorValue:
| Field name       |   Description                  |           Type                            |
|------------------|--------------------------------|-------------------------------------------|
| category         | Category of the factor value   | [Factor](#Factor)                         |
| value            | Value of the factor value      | [OntologyAnnotation](#OntologyAnnotation) |
| unit             | Unit of the factor value       | [OntologyAnnotation](#OntologyAnnotation) |

### Investigation:
| Field name                  |             Description                              |                   Type                                  |
|-----------------------------|------------------------------------------------------|---------------------------------------------------------|
| filename                    | Name of the investigation file                       | String                                                  |
| identifier                  | Identifier of the investigation                      | String                                                  |
| title                       | Title of the investigation                           | String                                                  |
| description                 | Description of the investigation                     | String                                                  |
| submissionDate              | Submission date of the investigation                 | DateTime                                                |
| publicReleaseDate           | Public release date of the investigation             | DateTime                                                |
| ontologySourceReferences    | Ontology source references used by the investigation | [OntologySourceReference](#OntologySourceReference)     |
| publications                | Publications associated with the investigation       | [Publication](#Publication)                             |  
| people                      | People to contact for the investigation              | [Person](#Person)                                       |
| studies                     | Studies associated with the investigation            | [Study](#Studies)                                       |

### Material:
| Field name         |        Description                |   Type                            |
|--------------------|-----------------------------------|-----------------------------------|
| name               | Name of the material              | String                            |
| characteristics    | Characteristics of the material   | [Characteristic](#Characteristic) |
| type               | Type of material                  | String                            |
| derivesFrom        | Source the material derives from  | [Source](#Source)                 |

### OntologyAnnotation:
| Field name      |        Description       |            Type                                     |
|-----------------|--------------------------|-----------------------------------------------------|
| annotationValue | Value of the annotation  | String or Int                                       |
| termSource      | ?                        | [OntologySourceReference](#OntologySourceReference) |
| termAccession   | ?                        | String                                              |

### OntologySourceReference:
| Field name       |   Description                                     | Type   |
|-----------------|----------------------------------------------------|--------|
| description     | Description of the ontology source reference       | String |
| file            | file associated with the ontology source reference | String |
| name            | Name of the ontology source reference              | String |
| version         | Version of the ontology source reference           | String |

### Person:
| Field name     |   Description             | Type                                       |
|----------------|---------------------------|--------------------------------------------|
| lastName       | Person's last name        | String                                     |
| firstName      | Person's first name       | String                                     |
| midInitials    | Person's middle initials  | String                                     |
| email          | Person's email            | String                                     |
| phone          | Person's phone number     | String                                     |
| fax            | Person's fax number       | String                                     |
| address        | Person's full address     | String                                     |
| affiliation    | Person's affiliation      | String                                     |
| roles          | Roles this person has     | [OntologyAnnotation](#OntologyAnnotation)  |

### Process:
| Field name       |             Description                                |                                Type                                                  |
|------------------|--------------------------------------------------------|--------------------------------------------------------------------------------------|
| name             | Name of the process                                    | String                                                                               |
| executesProtocol | Protocol executed by the process                       | [Protocol](#Protocol)                                                                | 
| parameterValues  | Parameters used by the protocol of this process        | [ProtocolParameterValue](#ProtocolParameterValue)                                    |
| performer        | Name of the person who executed the protocol           | String                                                                               |
| date             | ?                                                      | DateTime                                                                             |
| previousProcess  | Pointer to the previous process in the sequence        | [Process](#Process)                                                                  |
| nextProcess      | Pointer to the next process in the sequence            | [Process](#Process)                                                                  |
| inputs           | Input data used by this process                        | [Sample](#Sample), [Material](#Material) or [DataFile](#DataFile)                    |
| outputs          | Output data produced by this process                   | [Source](#Source), [Sample](#Sample), [Material](#Material) or [DataFile](#DataFile) |

### ProtocolParameterValue:
| Field name   |             Description                       |                        Type                   |
|--------------|-----------------------------------------------|-----------------------------------------------|
| characteristicType     | Category of parameter               | [ProtocolParameter](#ProtocolParameter)       |
| unit                   | Unit of the parameter               | [OntologyAnnotation](#OntologyAnnotation)     |
| value                  | Value of the parameter              | String                                        |

### ProtocolParameter:
| Field name               | Description              |                      Type                       |
|--------------------------|--------------------------|-------------------------------------------------|
| parameterName            | Name of the parameter    | [OntologyAnnotation](#OntologyAnnotation)       |

### Protocol:
| Field name   |             Description             |                    Type                    |
|--------------|-------------------------------------|--------------------------------------------|
| name         | Name of the protocol                | String                                     |
| protocolType | Type of protocol                    | [OntologyAnnotation](#OntologyAnnotation)  |
| description  | Textual description of the protocol | String                                     |
| uri          | URI of the protocol                 | String                                     |
| version      | Version of the protocol             | String                                     |
| parameters   | Parameters used by this protocol    | [ProtocolParameter](#ProtocolParameter)    |
| components   | Components used by this protocol    | [Component](#Component)                    |

### Publication:
| Field name     |   Description             | Type                                       |
|----------------|---------------------------|--------------------------------------------|
| pubMedID       | PubMed Identifier         | String                                     |
| doi            | Digital Object Identifier | String                                     |
| authorList     | List of authors           | String                                     |
| title          | Title of the publication  | String                                     |
| status         | Status of the publication | [OntologyAnnotation](#OntologyAnnotation)  |

### Sample:
| Field name       |   Description                             |           Type                    |
|------------------|-------------------------------------------|-----------------------------------|
| name             | Name of the sample                        | String                            |
| characteristics  | Characteristic of the sample              | [Characteristic](#Characteristic) |
| derivesFrom      | Source the sample derives from            | [Source](#Source)                 |
| factorValues     | Factor value assocaited with the sample   | [FactorValue](#FactorValue)       |

### Source:
| Field name       |   Description                  |           Type                    |
|------------------|--------------------------------|-----------------------------------|
| name             | Name of the source             | String                            |
| characteristics  | Characteristic of the source   | [Characteristic](#Characteristic) |

### Study:
| Field name                |             Description                                   |                  Type                      |
|---------------------------|-----------------------------------------------------------|--------------------------------------------|
| filename                  | Name of the study file                                    | String                                     |
| identifier                | Identifier of the study                                   | String                                     |
| title                     | Title of the study file                                   | String                                     |
| description               | Description of the study file                             | String                                     |
| submissionDate            | Date at which the study was submitted                     | DateTime                                   |
| publicReleaseDate         | Date at which the study was publicly released             | DateTime                                   |
| publications              | Publications associated with the study                    | [Publication](#Publication)                |
| people                    | People to contact for the study                           | [Person](#Person)                          |
| studyDesignDescriptors    | Design descriptors of this study                          | [OntologyAnnotation](#OntologyAnnotation)  |
| protocols                 | Protocols associated with the study                       | [Protocol](#Protocol)                      |
| materials                 | Materials associated with the study                       | [Material](#Material)                      |
| processSequence           | Processes associated with the study                       | [Process](#Process)                        |
| assay                     | Assays associated with the study                          | [Assay](#Assays)                           |
| factor                    | Factors associated with the study                         | [Factor](#Factor)                          |
| characteristicCategories  | Categories of characteristics associated with this study  | [OntologyAnnotation](#OntologyAnnotation)  |
| unitCategories            | Categories of units associated with the study             | [OntologyAnnotation](#OntologyAnnotation)  |

---

## Filters References:
All string and integer types should be wrapped in a comparison expression. This takes the form of a dictionary where
the main key represents the comparator. For example: `measurementType: {eq: "transcription profiling"}`. <br>

### Operator based on input type:
| Type      |   Operator  | Description             |
|-----------|-------------|-------------------------|
| String    | eq          | Equal                   |
| String    | in          | Include                 |
| Integer   | eq          | Equal                   |
| Integer   | lt          | Lower than              |
| Integer   | lte         | Lower than or equal     |
| Integer   | gt          | Greater than            |
| Integer   | gte         | Greater than or equal   |


### Assay filters:
| Field name       |   Description                                                                                    | Type                                      |    Target                 |                  Controlled values        |
|------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------|---------------------------|-------------------------------------------|
| measurementType  | Type of measurement realised in the assay                                                        | String                                    | measurementType           | X                                         |
| executesProtocol | Protocol executed by a process                                                                   | String                                    | process.executesProtocol  | X                                         |
| technologyType   | Type of technology used in the assay                                                             | String                                    | technologyType            | X                                         |   
| treatmentGroup   | Conditions the group was exposed to                                                              | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                         |
| characteristics  | Characteristics the material should comply with                                                  | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                         |
| parameterValues  | Parameters values a process should comply with                                                   | [ParameterValues](#ParameterValues)       | process.parameterValues   | X                                         |
| on               | Control to which input/output type the treatmentGroup and characteristics filters should apply   | String                                    | see controlled values     | "Sample", "Source, "DataFile", "Material" |


### ExposureParameters:
| Field name       |   Description               | Type     |
|------------------|-----------------------------|----------|
| name             | Name of the parameter       | String   |
| unit             | Unit of the parameter       | String   |
| value            | Value of the parameter      | String   |

### ParameterValues:
| Field name       |   Description                   | Type     |
|------------------|---------------------------------|----------|
| category         | Category of the parameter value | String   |
| unit             | Unit of the parameter value     | String   |
| value            | Value of the parameter value    | String   |

### Process filters:
| Field name       |   Description                                                                                    | Type                                      |    Target                 |                  Controlled values          |
|------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------|---------------------------|---------------------------------------------|
| executesProtocol | Protocol executed by the process                                                                 | String                                    | process.executesProtocol  | X                                           |
| treatmentGroup   | Conditions the group was exposed to                                                              | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                           |
| characteristics  | Characteristics the material should comply with                                                  | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                           |
| parameterValues  | Parameters values the process should comply with                                                 | [ParameterValues](#ParameterValues)       | process.parameterValues   | X                                           |
| on               | Control to which input/output type the treatmentGroup and characteristics filters should apply   | String                                    | see controlled values     | "Sample", "Source, "DataFile" or "Material" |

### Process Inputs filters:
| Field name       |   Description                                     | Type                                      |    Target                 |                  Controlled values          |
|------------------|---------------------------------------------------|-------------------------------------------|---------------------------|---------------------------------------------|
| treatmentGroup   | Conditions the group was exposed to               | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                           |
| characteristics  | Characteristics the input should comply with      | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                           |
| on               | Control the input to apply the filter to          | String                                    | see controlled values     | "Sample", "Source, "DataFile" or "Material" |

### Process Outputs filters:
| Field name       |   Description                                     | Type                                      |    Target                 |                  Controlled values        |
|------------------|---------------------------------------------------|-------------------------------------------|---------------------------|-------------------------------------------|
| treatmentGroup   | Conditions the group was exposed to               | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                         |
| type             | Name of the output to filter on                   | [ExposureParameters](#ExposureParameters) | process.inputs            | X                                         |
| on               | Control the output to apply the filter to         | String                                    | see controlled values     | "Sample", "DataFile" or "Material"        |