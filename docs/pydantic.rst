Pydantic models
===============

``isatools.pydantic`` provides Pydantic v2 model for ISA JSON documents. The
``Investigation`` model is the root object; it contains studies, protocols,
materials, assays, and related metadata. Models use Python ``snake_case`` field
names and serialize using ISA JSON ``camelCase`` aliases.

Install Pydantic support, and the additional JSON-LD/RDF dependencies when
needed, with::

   pip install 'isatools[pydantic]'
   pip install 'isatools[pydantic,jsonld]'

Reading and writing ISA JSON
----------------------------

Load an investigation from a file, then serialize it as a Python dictionary,
string, bytes, or another JSON file::

   from isatools.pydantic import Investigation
   from isatools.pydantic.models import SerializationOptions

   investigation = Investigation.from_file("i_investigation.json")
   options = SerializationOptions(ignore_empty_fields=True)

   isa_dict = investigation.to_dict(options=options)
   isa_text = investigation.to_str(options=options)
   isa_bytes = investigation.to_bytes(options=options)
   investigation.to_file("i_investigation_copy.json", options=options)

The corresponding constructors are ``from_file``, ``from_bytes``,
``from_str``, and ``from_dict``. Serialization uses ISA JSON aliases such as
``submissionDate`` and ``otherMaterials``. ``ignore_empty_fields=True`` omits
null values, empty strings, and empty collections.

For example, when ISA JSON is already available in memory, use::

   from isatools.pydantic import Investigation

   investigation = Investigation.from_dict(isa_dict)
   # Or parse a JSON string or its UTF-8 encoded bytes.
   investigation_from_text = Investigation.from_str(isa_text)
   investigation_from_bytes = Investigation.from_bytes(isa_bytes)

JSON-LD identifiers can be generated while loading. JSON-LD context and type
metadata are included in serialization when a matching context is configured::

   from isatools.pydantic import Investigation
   from isatools.pydantic.models import (
       JsonLdConfiguration,
       LoadOptions,
       SerializationOptions,
       WIKIDATA_CONTEXT_DIR,
       WIKIDATA_CONTEXT_FILENAME_MATCH_PATTERN,
       WIKIDATA_CONTEXT_ID_FILE_PREFIX,
   )

   context = JsonLdConfiguration(
       jsonld_dir=WIKIDATA_CONTEXT_DIR,
       filename_match_pattern=WIKIDATA_CONTEXT_FILENAME_MATCH_PATTERN,
       context_id_prefix=WIKIDATA_CONTEXT_ID_FILE_PREFIX,
   )
   investigation = Investigation.from_file(
       "i_investigation.json",
       options=LoadOptions(jsonld_config=context, generate_ids=True),
   )
   serialization = SerializationOptions(
       jsonld_config=context,
       ignore_empty_fields=True,
   )
   jsonld_dict = investigation.to_dict(options=serialization)

Conversion to and from the ISA model
------------------------------------

Convert between the Pydantic ``Investigation`` and the
``isatools.model.Investigation`` class::

   from isatools.model import Investigation as ISAToolsInvestigation
   from isatools.pydantic import Investigation
   import json
   from pathlib import Path

   isa_investigation = ISAToolsInvestigation()
   isa_data = json.loads(Path("i_investigation.json").read_text())
   isa_investigation.from_dict(isa_data)

   investigation = Investigation.from_isatools_model(isa_investigation)
   isa_copy = investigation.to_isatools_model()

``from_isatools_model`` requires an ``isatools.model.Investigation`` instance.
The conversion preserves nested study and assay content and maps ``isatools``
contacts to the ``people`` fields in the Pydantic representation.

JSON-LD expansion and RDF
-------------------------

The ``jsonld`` extra installs PyLD and RDFLib. Use ``to_jsonld_expanded`` to
expand the compact JSON-LD document, or ``to_rdf_dataset`` to produce an
``rdflib.Dataset``::

   from pyld import FileDocumentLoader

   jsonld_options = {
       "documentLoader": FileDocumentLoader(),
       "base": "https://example.org/isa",
   }
   expanded = investigation.to_jsonld_expanded(
       serialization_options=serialization,
       jsonld_expand_options=jsonld_options,
   )
   dataset = investigation.to_rdf_dataset(
       serialization_options=serialization,
       jsonld_expand_options=jsonld_options,
       rdf_options={"base": "https://example.org/isa"},
   )

Both methods require JSON-LD contexts for the properties being expanded.
``to_rdf_dataset`` converts through expanded JSON-LD and parses the resulting
N-Quads into an RDFLib dataset.

Scope
-----

These models provide typed data structures and serialization. They do not
replace JSON Schema validation or enforce cross-object ISA graph rules.
