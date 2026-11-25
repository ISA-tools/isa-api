#############
ISA tools API
#############

The ISA tools API is published on PyPI as the ``isatools`` Python package. The package aims to provide you, the
developer, with a set of tools to help you easily and quickly build your own ISA objects, validate, and convert
between serializations of ISA-formatted datasets and other formats/schemas
(e.g. `SRA schemas <https://www.ebi.ac.uk/ena/submit/read-xml-format-1-5>`_). The goal of this package is to provide a
flexible way to build and use ISA content, as well as provide utility functions for file conversions and validation.

#. :doc:`Installation </installation>`
#. :doc:`ISA model </isamodel>`
#. :doc:`Pydantic models <pydantic>`
#. :doc:`Creating objects </creation>`
#. :doc:`Tutorial: describing a simple experiment with objects <creationtutorial>`
#. :doc:`Creating ISA objects based on study-design </studydesigncreation>`
#. :doc:`Converting between ISA formats </conversions>`
#. :doc:`Downloading files stored in Github </github>`
#. :doc:`Validating ISA-Tab and ISA JSON </validation>`
#. :doc:`Importing data in ISA formats </importdata>`
#. :doc:`Exporting data in ISA formats </exportdata>`
#. :doc:`Creating ISA content with a Sample and Assay plan </sampleassayplan>`
#. :doc:`Known Issues </knownissues>`

License
-------
This code is licensed under the `CPAL License <https://raw.githubusercontent.com/ISA-tools/isa-api/master/LICENSE.txt>`_.

Pydantic models
---------------

The optional ``isatools.pydantic`` package provides typed models for ISA JSON,
including serialization and conversion to and from the ``isatools`` model. Install
the optional dependencies with::

   pip install 'isatools[pydantic,jsonld]'

Load an investigation, inspect it as an ISA JSON dictionary, and write it back
to a file::

   from isatools.pydantic import Investigation
   from isatools.pydantic.models import SerializationOptions

   investigation = Investigation.from_file("i_investigation.json")
   isa_json = investigation.to_dict(
       options=SerializationOptions(ignore_empty_fields=True)
   )
   investigation.to_file("i_investigation_copy.json")

You can also create a Pydantic investigation from an
``isatools.model.Investigation`` object, or convert it back::

   from isatools.model import Investigation as ISAToolsInvestigation
   from isatools.pydantic import Investigation
   import json
   from pathlib import Path

   isa_investigation = ISAToolsInvestigation()
   isa_data = json.loads(Path("i_investigation.json").read_text())
   isa_investigation.from_dict(isa_data)

   investigation = Investigation.from_isatools_model(isa_investigation)
   isa_copy = investigation.to_isatools_model()

JSON-LD expansion and RDF conversion use the configured local contexts. PyLD
and RDFLib must be installed for these methods::

   from pyld import FileDocumentLoader
   from isatools.pydantic import Investigation
   from isatools.pydantic.models import LoadOptions

   jsonld_config = Investigation.get_jsonld_config("wdt", use_file_context_id_prefix=True)
   investigation = Investigation.from_file(
       "i_investigation.json",
       options=LoadOptions(jsonld_config=jsonld_config, generate_ids=True),
   )
   jsonld_options = {
       "documentLoader": FileDocumentLoader(),
       "base": "https://example.org/isa",
   }

   expanded = investigation.to_jsonld_expanded(
       ontology="wdt",
       jsonld_expand_options=jsonld_options,
   )
   rdf_dataset = investigation.to_rdf_dataset(
       ontology="wdt",
       jsonld_expand_options=jsonld_options,
       rdf_options={"base": "https://example.org/isa"},
   )

See :doc:`Pydantic models <pydantic>` for loading from dictionaries, strings, and
bytes, serialization options, and additional examples.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   Installation <installation>
   ISA model <isamodel>
   Pydantic ISA model <pydantic>
   Creating objects <creation>
   Tutorial: describing a simple experiment with objects <creationtutorial>
   Example: createSimpleISAtab.py <example-createSimpleISAtab>
   Example: createSimpleISAJSON.py <example-createSimpleISAJSON>
   Example: validateISAtab.py <example-validateISAtab>
   Example: validateISAjson.py <example-validateISAjson>
   Converting between ISA formats <conversions>
   Contributing your work <contributing>
   Downloading files stored in Github <github>
   Validating ISA-Tab and ISA JSON <validation>
   Importing data in ISA formats <importdata>
   Exporting data from ISA formats <exportdata>
   Creating ISA content with a Sample and Assay plan </sampleassayplan>
   Known Issues <knownissues>
