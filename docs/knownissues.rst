############
Known issues
############

isatools v0.5 package
---------------------
- All issues inherited from v0.4 (see below)
- Currently only Python 3.4 and 3.5 is supported. Python 2.7 support is present in the ``py2`` source branch on Github.

isatools v0.4 package
---------------------
- For certain of ISA-Tab table files, the ISA-Tab parser cannot disambiguate between process instances where a ``Name`` column is required to qualify a ``Protocol REF`` has been left blank. Utility functions have been written to detect these anomalies and to assist in correcting them, in the ``isatools.utils`` package. #146 (see detail after bullet points)
- When converting to ISA JSON in using ``UUID`` or ``counter`` Identifier Types, some elements are not detected, such as ``Array_Design_REF`` #101
- The ISA-Tab parser does not support reading ``Protein Assignment File``, ``Peptide Assignment File``, ``Post Translational Modification Assignment File`` columns, and therefore the ``isatab2*`` converters also do not support these #174
- The SRA/ENA importer in ``sra2isatab`` relies on XSLT2 processing functionality only available with SAXON, so you must provide the JAR file yourself to use this
- ``sra2isatab`` converter does not support SRA pools #153
- The legacy functionality (marked in the documentation) relies on Java 1.6

To check for possible erroneous pooling events in an ISA-Tab archive, you can try something like:

.. code-block:: python

    >>> from isatools import utils
    >>> utils.detect_isatab_process_pooling('tests/data/tab/MTBLS1/')
    INFO: Converting ISA-Tab to ISA JSON...
    INFO: Converting ISAtab to ISAjson for tests/data/tab/MTBLS1/
    INFO: ... conversion finished.
    Checking s_MTBLS1.txt
    Checking a_mtbls1_metabolite_profiling_NMR_spectroscopy.txt
    Possible process pooling detected on:  #process/Extraction1
    Possible process pooling detected on:  #process/ADG_normalized_data.xlsx
    [{'a_mtbls1_metabolite_profiling_NMR_spectroscopy.txt': ['#process/Extraction1', '#process/ADG_normalized_data.xlsx']}]
    >>>

In this case, ``#process/Extraction1`` is the pooling that we did not expect. This is a pooling on a single
``Extraction``. From manual inspection of the ISA-Tab file ``a_mtbls1_metabolite_profiling_NMR_spectroscopy.txt`` we can
 then confirm that values are entirely missing from ``Extract Name``, causing the parser to think the experimental graph
  converges on one process node. To rectify this, individual values should be put into this ``Name`` column. We can try
fix erroneous pooling by filling out an empty ``Name`` column with a corresponding ``Protocol REF`` by doing the following:

.. code-block:: python

    >>> utils.insert_distinct_parameter(open('tests/data/tab/MTBLS1/a_mtbls1_metabolite_profiling_NMR_spectroscopy.txt', 'r+'), 'Extraction')
    Are you sure you want to add a column of hash values in Extract Name? Y/(N)
    >? Y

If successful, this will fill out the empty column with 8 character-long UUIDs (e.g. 4078cb03).

Please be aware that these utility functions ``detect_isatab_process_pooling()`` and ``insert_distinct_parameter()`` are
there to help you manually fix your ISA-Tabs, not to automatically fix them for you. We wil address this issue in more
depth in following releases.

isatools v0.3 package
---------------------
- ``required`` constraints on JSON schemas causes validation failure for ``@id`` objects, meaning some constraints using JSON schemas cannot be used for validation #108
- Chained processes (i.e. a process followed by another process without any intermediate inputs and outputs, in ISAtab a ``Protocol REF`` columns followed by another ``Protocol REF`` columns without any materials in between) are not currently supported. It is not recommended to attempt to use such patterns with this version of the ``isatools`` package #111
- When converting to ISA JSON in using ``UUID`` or ``counter`` Identifier Types, some elements are not detected, such as ``Array_Design_REF`` #101
- The SRA/ENA importer in ``sra2isatab`` relies on XSLT2 processing functionality only available with SAXON, so you must provide the JAR file yourself to use this
- The legacy functionality (marked in the documentation) relies on Java 1.6

isatools v0.2 package
---------------------
- ``required`` constraints on JSON schemas causes validation failure for ``@id`` objects, meaning some constraints using JSON schemas cannot be used for validation #108
- When converting to ISA JSON in using ``UUID`` or ``counter`` Identifier Types, some elements are not detected, such as ``Array_Design_REF`` #101
- ``Protocol REF`` columns must be present in order for the ISA-Tab to JSON conversion to pick up processes in the process sequences #111
- Characteristics and Factor Values declared in assay tables in ISAtab are associated to Sample objects only. This means that when writing from Python objects, or converting from ISA JSON, to ISAtab these columns appear at the study table.
- Chained processes (i.e. a process followed by another process without any intermediate inputs and outputs, in ISAtab a ``Protocol REF`` columns followed by another ``Protocol REF`` columns without any materials in between) are not currently supported. It is not recommended to attempt to use such patterns with this version of the ``isatools`` package #111
- For experimental graph patterns to work, should follow relatively simple patterns. e.g. Straight Sample -> ... -> Materials -> ... -> Data paths (per assay), or simple splitting and pooling. See test package code for examples of what works.
- No ISA JSON configurations have been included that correspond with the following default XML configurations: ``clinical_chemistry.xml`` and most are as yet untested.

isatools v0.1 package
---------------------
- Characteristics and Factor Values declared in assay tables in ISAtab are associated to Sample objects only. This means that when writing from Python objects, or converting from ISA JSON, to ISAtab these columns appear at the study table.
- Chained processes (i.e. a process followed by another process without any intermediate inputs and outputs, in ISAtab a ``Protocol REF`` columns followed by another ``Protocol REF`` columns without any materials in between) are not currently supported. It is not recommended to attempt to use such patterns with this version of the ``isatools`` package #111
- For experimental graph patterns to work, should follow relatively simple patterns. e.g. Straight Sample -> ... -> Materials -> ... -> Data paths (per assay), or simple splitting and pooling. See test package code for examples of what works.

For a full up-to-date list of issues, or to report an issue or ask a question, please see the `issue tracker <https://github.com/ISA-tools/isa-api/issues>`_.