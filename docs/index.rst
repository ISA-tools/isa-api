#############
ISA tools API
#############

The ISA tools API is published on PyPI as the ``isatools`` Python package. The package aims to provide you, the
developer, with a set of tools to help you easily and quickly build your own ISA objects, validate, and convert
between serializations of ISA-formatted datasets and other formats/schemas
(e.g. `SRA schemas <https://www.ebi.ac.uk/ena/submit/read-xml-format-1-5>`_). The goal of this package is to provide a
flexible way to build and use ISA content, as well as provide utility functions for format validation and file conversions.

.. note:: ``isatools`` is currently only supported in Python 3.4 and 3.5. Python 2.7 support is present in the ``py2`` source code branch in Github.

#. :doc:`Installation </installation>`
#. :doc:`ISA model </isamodel>`
#. :doc:`Creating ISA objects </creation>`
#. :doc:`Writing ISA objects as ISA-Tab or ISA-JSON</writingtofile>`
#. :doc:`Tutorial: Describing a simple experiment with objects </creationtutorial>`
#. :doc:`Tutorial: Quantitative and Qualitative Annotations on ISA objects <annotation>`
#. :doc:`Tutorial: Creating ISA objects based on Study Design <studydesigncreation>`
#. :doc:`Tutorial: Creating ISA content with a Sample and Assay plan </sampleassayplan>`
#. :doc:`Creating ISA objects based on study-design </studydesigncreation>`
#. :doc:`Converting between ISA formats </conversions>`
#. :doc:`Downloading files stored in Github </github>`
#. :doc:`Validating ISA-Tab and ISA JSON </validation>`
#. :doc:`Importing data in ISA formats </importdata>`
#. :doc:`Exporting data in ISA formats </exportdata>`
#. :doc:`Known Issues </knownissues>`

License
-------
This code is licensed under the `CPAL License <https://raw.githubusercontent.com/ISA-tools/isa-api/master/LICENSE.txt>`_.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   Installation <installation>
   ISA model <isamodel>
   Creating ISA objects <creation>
   Writing ISA objects to file <writingtofile>
   Tutorial: Describing a simple experiment with ISA objects <creationtutorial>
   Tutorial: Quantitative and Qualitative Annotations on ISA objects <annotation>
   Tutorial: Creating ISA objects based on study-design <studydesigncreation>
   Tutorial: Creating ISA content with a Sample and Assay plan </sampleassayplan>
   Converting between ISA formats <conversions>
   Contributing your work <contributing>
   Downloading files stored in Github <github>
   Validating ISA-Tab and ISA JSON <validation>
   Importing data in ISA formats <importdata>
   Exporting data from ISA formats <exportdata>
   Example: createSimpleISAtab.py <example-createSimpleISAtab>
   Example: createSimpleISAJSON.py <example-createSimpleISAJSON>
   Example: validateISAtab.py <example-validateISAtab>
   Example: validateISAjson.py <example-validateISAjson>
   Known Issues <knownissues>