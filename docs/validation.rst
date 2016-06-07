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

From v0.2 of the ISA API, we have started implementing a replacement validator written in Python. To use this one, do something like:

.. code-block:: python
    from isatools import isatab
    isatab.validate2('i_investigation.txt', './isaconfig-default_v2015-07-02/')

making sure to point to the investigation file of your ISA tab, and again providing the old XML configurations.


Validating ISA JSON
-------------------

To validate an ISA JSON file against the ISA JSON version 1.0 specification you can use our new validator from v0.2, by doing this by doing something like:

.. code-block:: python
    from isatools import isajson
    isajson.validate('isa.json')
