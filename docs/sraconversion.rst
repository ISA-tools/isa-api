###################
ISA-SRA Conversions
###################

----------------------------------
Converting from ISA tab to SRA XML
----------------------------------

To convert from a directory ``./tabdir/`` containing valid ISA tab files to a write the SRA XML files to a target directory ``./outdir/``, validating against a given configuration in ``./isaconfig-default_v2015-07-02/``:

.. code-block:: python

   from isatools.convert import isatab2sra
   isatab2sra.create_sra('./tabdir/', './outdir/', './isaconfig-default_v2015-07-02/')

----------------------------------------
Converting from ISA JSON file to SRA XML
----------------------------------------

To convert from a a ISA JSON file ``isa.json`` directory to write out SRA XML files to a target directory ``./outdir/``, validating against a given configuration in ``./isaconfig-default_v2015-07-02/``:

.. code-block:: python

   from isatools.convert import json2sra
   json2sra.convert(open('isa.json')), './outdir/', './isaconfig-default_v2015-07-02/')

------------------------
Importing SRA to ISA tab
------------------------

.. code-block:: python

   from isatools.convert import sra2isatab
   sra2isatab.sra_to_isatab_batch_convert(...)