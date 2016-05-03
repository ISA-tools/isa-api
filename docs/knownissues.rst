############
Known issues
############

isatools v0.1 package
---------------------

- Characteristics and Factor Values declared in assay tables in ISAtab are associated to Sample objects only. This means that when writing from Python objects, or converting from ISA JSON, to ISAtab these columns appear at the study table.
- Chained processes (i.e. a process followed by another process without any intermediate inputs and outputs, in ISAtab a ``Protocol REF`` columns followed by another ``Protocol REF`` columns without any materials in between) are not currently supported. It is not recommended to attempt to use such patterns with this version of the ``isatools`` package.
- For experimental graph patterns to work, should follow relatively simple patterns. e.g. Straight Sample -> ... -> Materials -> ... -> Data paths (per assay), or simple splitting and pooling. See test package code for examples of what works.

For a full up-to-date list of issues, please also see the `issue tracker <https://github.com/ISA-tools/isa-api/issues>`_.