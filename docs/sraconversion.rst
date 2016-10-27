###################
ISA-SRA Conversions
###################

----------------------------------------------------------------
Converting from ISA-Tab to SRA XML (using legacy Java converter)
----------------------------------------------------------------

To convert from a directory ``./tabdir/`` containing valid ISA-Tab files to a write the SRA XML files to a target directory ``./outdir/``, validating against a given configuration in ``./isaconfig-default_v2015-07-02/``:

.. code-block:: python

   from isatools.convert import isatab2sra
   isatab2sra.create_sra('./tabdir/', './outdir/', './isaconfig-default_v2015-07-02/')

This method writes the SRA files out to ``./outdir/sra/``.

------------------------------------------------------------
Converting from ISA-Tab to SRA XML (native Python converter)
------------------------------------------------------------

To convert from a directory ``./tabdir/`` containing valid ISA-Tab files to a write the SRA XML files to a target directory ``./outdir/``, validating against a given configuration in ``./isaconfig-default_v2015-07-02/``:

.. code-block:: python

   from isatools.convert import isatab2sra
   isatab2sra.convert('./tabdir/', './outdir/')

This method writes the SRA files out to ``./outdir/``.

----------------------------------------
Converting from ISA JSON file to SRA XML
----------------------------------------

To convert from a a ISA JSON file ``isa.json`` directory to write out SRA XML files to a target directory ``./outdir/``:

.. code-block:: python

   from isatools.convert import json2sra
   json2sra.convert(open('isa.json')), './outdir/')

This method writes the SRA files out to ``./outdir/``.

To turn off pre-conversion validation, use ``validate_first=False``. By default it is set to ``validate_first=True``.
