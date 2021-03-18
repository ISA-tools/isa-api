# ISA-API and custom assay definition

The ISA specification allows for a certain amount of customization and extensibility to support diverse type of assay.

The extension works as long as users conforms to key syntactic rules, which identify ISA Nodes (Material or Data Nodes) and ISA Edges (protocol application and their associated protocols, parameter and parameter value sets).

The new ISA python API relies on a specific data structures known as an `Ordered Dictionary` to do so.

This chapter describes the key attributes and how to create a new assay definition which can be used with the new `ISA create mode module`.

## General Structure and Key Objects

The overall structure of an assay definition is presented below.
it contains a set of `housekeeping` and provenance metadata tags, some of which are optional.
other metadata element as ignored by the ISA-API but are used by the graphical user interface of the `Datascriptor` app.


|metadata element|function|consumed by|
|----------------|--------|-----------|
|id|identification|DataScriptor|
|name|provenance|ISA API,DataScriptor|
|creation_date|provenance|ISA API|
|mtbls_owl_sha256|validation|ISA API,DataScriptor|
|mtbls_assaymaster_sha256|validation|ISA API,DataScriptor|
|icon|display|DataScriptor|
|color|display|DataScriptor|


```python
    {
        "id": 0,
        "name": "metabolite profiling by LC-MS",
        "icon": "fas fa-chart-bar",
        "color": "blue",
        "mtbls_owl_sha256": "f49a7bcf2179b0e8531439ee52aabee940b4fdfe754fb830c24000ad1bca3e51",
        "mtbls_assaymaster_sha256": "1532abcf0b2b901fcabc3434c7159d1466923d9eba3a10df4149d74e168f3fbb",
        "creation_date": "2020-11-21 12:56:16",
        "measurement_type": {
            "term": "metabolite profiling",
            "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
            "source": "OBI"
        },
        "technology_type": {
            "term": "liquid chromatography mass spectrometry",
            "uri": "http://purl.obolibrary.org/obo/OBI_0000051",
            "source": "OBI"
        },
        "workflow": [...
        ],
        "@context": {
            "measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
            "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521",
            "Liquid Chromatography Instrument Model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000324",
            "Liquid Chromatography Autosampler Model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000319",
            "Liquid Chromatography Column model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000328",
            "Liquid Chromatography Column type": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000323",
            "Liquid Chromatography Guard Column model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000329",
            "Mass Spectrometry Instrument Model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000330",
            "Mass Spectrometry Ion Source": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000317",
            "Mass Spectrometry Mass Analyzer": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000331"
        }
    },

``` 





We know focus on the `workflow` definition.
All assay worflows are assumed to start with a Sample Node, which is not represented.
Therefore, all workflows *must* start with a `process` element, which is characterised by its 'protocol type' string, **extraction** in the example below.
The first element of the array is a protocol type dictionary may be annotated with controled terminology thanks to the `iri` and `source` keys.
The second element of the array is made up of a fixed part #replicates, which accepts a positive integer to indicate the number of technical replication for the protocol execution
and a variable part, which is a list of ISA Protocol Parameters and their associated valid 'value sets', i.e. the list of values users may choose from.
For those, the specification allows for `default values` to be set and a boolean flag `newValuesAllowed` enables users / curators to define new entries beyond those listed.


```python

        "workflow": [
            [
                {
                    "term": "extraction",
                    "iri": null,
                    "source": null
                },
                {
                    "#replicates": {
                        "value": 1
                    },
                    "Post Extraction": {
                        "description": "",
                        "options": [],
                        "values": []
                    },
                    "Derivatization": {
                        "description": "",
                        "options": [],
                        "values": []
                    }
                }
            ]

```

Protocol element may be chained as one can see with 'Liquid Chromatrography' and 'mass spectrometry' protocols  in the example below.

Individual protocols, unless daisy-chained, should be followed by Nodes, which can be either Material or Data Nodes.
Material Nodes have 3 explicit types [sample, extract, labeled extract]
Material Nodes may be qualified with `characteristics`,
Data Nodes have 2 explicit types [raw data file, derived data file ]

Both Node types bear a `is_input_to_next_protocols `boolean flag, to indicate whether the workflow terminates or not.


```python

        "workflow": [
            [
                {
                    "term": "extraction",
                    "iri": null,
                    "source": null
                },
                {
                    "#replicates": {
                        "value": 1
                    },
                    "Post Extraction": {
                        "description": "",
                        "options": [],
                        "values": []
                    },
                    "Derivatization": {
                        "description": "",
                        "options": [],
                        "values": []
                    }
                }
            ],
            [
                "extract",
                {
                    "node_type": "extract",
                    "characteristics_category": "extract type",
                    "characteristics_value": {
                        "options": [
                            "polar fraction",
                            "non-polar fraction"
                        ],
                        "values": []
                    },
                    "is_input_to_next_protocols": {
                        "value": true
                    }
                }
            ],
            [
                {
                    "term": "chromatography",
                    "iri": null,
                    "source": null
                },
                {
                    "#replicates": {
                        "value": 1
                    },
                    "Liquid Chromatography Instrument Model": {
                        "description": "",
                        "options": [
                            {
                                "term": "Agilent 1200 Series HPLC-Chip",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_001110",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "Thermo Scientific UltiMate 3000 Standard HPLC system",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_001108",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "Aglient 1290 Infinity II LC",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000894",
                                "source": "Metabolights.owl"
                            }
                        ],
                        "values": []
                    },
                    "Liquid Chromatography Autosampler Model": {
                        "description": "",
                        "options": [
                            {
                                "term": "Thermo Scientific UltiMate WPS-3000 TLS A Autosampler",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_001128",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "Thermo Scientific Accela Open Autosampler",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000560",
                                "source": "Metabolights.owl"
                            }
                        ],
                        "values": []
                    },
                    "Liquid Chromatography Column model": {
                        "description": "",
                        "options": [
                            {
                                "term": "Hypersil GOLD aQ (1.9 \u00b5m, 2.1 mm x 100 mm; Thermo Scientific)",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000822",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "Jupiter C18 300 \u00c5 (5 \u00b5m, 2 mm x 250 mm; Phenomenex)",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000745",
                                "source": "Metabolights.owl"
                            }
                        ],
                        "values": []
                    },
                    "Liquid Chromatography Column type": {
                        "description": "",
                        "options": [
                            {
                                "term": "",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000854",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "normal phase",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000855",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "reverse phase",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000853",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "HILIC",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000856",
                                "source": "Metabolights.owl"
                            }
                        ],
                        "values": []
                    },
                    "Liquid Chromatography Guard Column model": {
                        "description": "",
                        "options": [
                            {
                                "term": "ACQUITY UPLC BEH Phenyl VanGuard Pre-column, 130\u00c5 (1.7 \u00b5m, 2.1 mm x 5 mm; Waters)",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000571",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "Ascentis Express C18 Guard Cartridge (2.7 \u00b5m, 2.1 mm x 5 mm; Supelco)",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_001133",
                                "source": "Metabolights.owl"
                            }
                        ],
                        "values": []
                    }
                }
            ],
            [
                {
                    "term": "mass spectrometry",
                    "iri": null,
                    "source": null
                },
                {
                    "#replicates": {
                        "value": 1
                    },
                    "Mass Spectrometry Scan polarity": {
                        "description": "",
                        "options": [],
                        "values": []
                    },
                    "Mass Spectrometry Scan m/z range": {
                        "description": "",
                        "options": [],
                        "values": []
                    },
                    "Mass Spectrometry Instrument Model": {
                        "description": "",
                        "options": [
                            {
                                "term": "Thermo Scientific Orbitrap Elite",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000654",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "Thermo Scientific Orbitrap ID-X Tribrid",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_001123",
                                "source": "Metabolights.owl"
                            }
                        ],
                        "values": []
                    },
                    "Mass Spectrometry Ion Source": {
                        "description": "",
                        "options": [
                            {
                                "term": "MS:chemical ionization",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_001098",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "atmospheric pressure matrix-assisted laser desorption ionization",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_001186",
                                "source": "Metabolights.owl"
                            }
                        ],
                        "values": []
                    },
                    "Mass Spectrometry Mass Analyzer": {
                        "description": "",
                        "options": [
                            {
                                "term": "linear quadrupole ion trap mass-to-charge analyser",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000701",
                                "source": "Metabolights.owl"
                            },
                            {
                                "term": "triple quadrupole",
                                "iri": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000698",
                                "source": "Metabolights.owl"
                            }
                        ],
                        "values": []
                    }
                }
            ],
            [
                {
                    "term": "raw spectral data file",
                    "iri": "http://purl.obolibrary.org/obo/MS_1003083",
                    "source": null
                },
                {
                    "node_type": "data file",
                    "is_input_to_next_protocols": {
                        "value": true
                    }
                }
            ]
        ],
```


## Ontology Markup and Semantic context

The ISA Assay definition can be produced without any semantic annotation, simply by providing user defined strings for keys and value sets, where applicable
However,  the data structure has been conceived to allow for semantic types to be supplied by data managers and curators. 

### direct annotation of values associated with keys

The data structure for ISA assay definitions provides the necessary elements for associating a string defining a key or a value in a value set to an resolveable persistent identifier and the relevant minting authority, aka `source`

i. string only 

```python
        "measurement_type": {
            "term": "metabolite profiling",
            "uri": ""
            "source": ""
        },
```
ii. with semantic markup

```python
        "measurement_type": {
            "term": "metabolite profiling",
            "uri": "http://purl.obolibrary.org/obo/OBI_0000366",
            "source": "OBI"
        },


		{
            "term": "raw spectral data file",
            "iri": "http://purl.obolibrary.org/obo/MS_1003083",
            "source": null
        }
```

### Annotation of keys via the @context

In this section, we should how to supply semantic markup of the main key of the data dictionary defining an ISA Assay.
This is achieved via a `@context` element in the python OrderedDict.

```python
        "@context": {
            "measurement type": "http://purl.obolibrary.org/obo/OBI_0000070",
            "technology type": "http://www.ebi.ac.uk/efo/EFO_0005521",
            "Liquid Chromatography Instrument Model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000324",
            "Liquid Chromatography Autosampler Model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000319",
            "Liquid Chromatography Column model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000328",
            "Liquid Chromatography Column type": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000323",
            "Liquid Chromatography Guard Column model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000329",
            "Mass Spectrometry Instrument Model": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000330",
            "Mass Spectrometry Ion Source": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000317",
            "Mass Spectrometry Mass Analyzer": "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000331"
        }
```

## ISA Assay Definition and DataScriptor tool

The assay definition format used by the ISA-API is also used to power the user interface of a new application developed by our group, `DataScriptor`.

The assay definitions are stored in `./datascriptor/packages/api/test/fixtures` in the `assay-configs.json` file. 
The assay definitions shipping by default with the ISA-API and DataScriptor support the data management of Functional Genomics studies compatible with deposition to EMBL-EBI ENA and Metabolights databases.
For the latter, the ISA Assay definitions are generated programmatically from curated assay workflows defined by Metabolights
For the former, the ISA Assay definitions have been created from existing ISA xml configurations files used by ISAcreator and by the python ISA-API.


```{caution}

When used with the Datascriptor app, the ISA Assay Definitions present users with all possible values available to users to choose from to describe a particular setting or experimental condition.

When used with the ISA-API, the ISA Assay definition will only contain the values selected by end users and will be used to create ISA objects. The following jupyter-notebooks provide examples of this.
```