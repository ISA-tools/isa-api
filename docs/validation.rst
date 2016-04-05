###############################
Validating ISA tab and ISA JSON
###############################

Using the ISA API you can validate ISA tab and ISA JSON files. The ISA tab validation utilises the legacy Java validator, so you must have Java 1.6 or later installed on your host machine. The ISA JSON validation checks JSON against the JSON schemas that are included in the API in the `isatools/schemas/isa_model_version_1_0_schemas/core` directory.

Validating ISA tab
------------------

To validate ISA tab files in a given directory ``./tabdir/`` against a given configuration found in a directory ``./isaconfig-default_v2015-07-02/``, do something like the following:

.. code-block:: python
    from isatools import isatab
    isatab.validate('./tabdir/', './isaconfig-default_v2015-07-02/')

Validating ISA JSON
-------------------

To validate an ISA JSON file against the ISA version 1.0 schemas, you need to validate against the ``investigation_schema.json`` schema. You can do this by doing something like:

.. code-block:: python
    from isatools.validate import validate_json
    validate_json.validateJsonAgainstSchemas('investigation_schema.json', 'isa.json')

Make sure you put the full path to the to the location of ``investigation_schema.json``.