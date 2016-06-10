############
Known issues
############

isatools v0.2 package
---------------------
- ``required`` constraints on JSON schemas causes validation failure for ``@id`` objects, meaning some constraints using JSON schemas cannot be used for validation #108
- When converting to ISA JSON in using ``UUID`` or ``counter`` Identifier Types, some elements are not detected, such as ``Array_Design_REF`` #101
- ``Protocol REF`` columns must be present in order for the ISA tab to JSON conversion to pick up processes in the process sequences #111
- Characteristics and Factor Values declared in assay tables in ISAtab are associated to Sample objects only. This means that when writing from Python objects, or converting from ISA JSON, to ISAtab these columns appear at the study table.
- Chained processes (i.e. a process followed by another process without any intermediate inputs and outputs, in ISAtab a ``Protocol REF`` columns followed by another ``Protocol REF`` columns without any materials in between) are not currently supported. It is not recommended to attempt to use such patterns with this version of the ``isatools`` package.
- For experimental graph patterns to work, should follow relatively simple patterns. e.g. Straight Sample -> ... -> Materials -> ... -> Data paths (per assay), or simple splitting and pooling. See test package code for examples of what works.
- No ISA JSON configurations have been included that correspond with the following default XML configurations: ``clinical_chemistry.xml`` and most are as yet untested.

isatools v0.1 package
---------------------

- Characteristics and Factor Values declared in assay tables in ISAtab are associated to Sample objects only. This means that when writing from Python objects, or converting from ISA JSON, to ISAtab these columns appear at the study table.
- Chained processes (i.e. a process followed by another process without any intermediate inputs and outputs, in ISAtab a ``Protocol REF`` columns followed by another ``Protocol REF`` columns without any materials in between) are not currently supported. It is not recommended to attempt to use such patterns with this version of the ``isatools`` package.
- For experimental graph patterns to work, should follow relatively simple patterns. e.g. Straight Sample -> ... -> Materials -> ... -> Data paths (per assay), or simple splitting and pooling. See test package code for examples of what works.

For a full up-to-date list of issues, or to report an issue or ask a question, please see the `issue tracker <https://github.com/ISA-tools/isa-api/issues>`_.