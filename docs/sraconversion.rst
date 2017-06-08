###################
ISA-SRA Conversions
###################

----------------------------------
Converting from ISA-Tab to SRA XML
----------------------------------

To convert from a directory ``./tabdir/`` containing valid ISA-Tab files to a write the SRA XML files to a target directory ``./outdir/``, validating against a given configuration in ``./isaconfig-default_v2015-07-02/``:

.. code-block:: python

   from isatools.convert import isatab2sra
   sra_settings={
            "sra_broker": "MYORG",
            "sra_center": "MYORG",
            "sra_project": "MYORG",
            "sra_broker_inform_on_status": "support@myorg.org",
            "sra_broker_inform_on_error": "support@myorg.org",
            "sra_broker_contact_name": "Support"
        }
   isatab2sra.convert('./tabdir/', './outdir/', sra_settings=sra_settings)

This method writes the SRA files out to ``./outdir/``.

Note that when subitting SRA XML to ENA, you need to supply broker information as shown above in the ``sra_settings`` JSON, customised to your own organisation's settings.

----------------------------------------
Converting from ISA JSON file to SRA XML
----------------------------------------

To convert from a a ISA JSON file ``isa.json`` directory to write out SRA XML files to a target directory ``./outdir/``:

.. code-block:: python

   sra_settings={
            "sra_broker": "MYORG",
            "sra_center": "MYORG",
            "sra_project": "MYORG",
            "sra_broker_inform_on_status": "support@myorg.org",
            "sra_broker_inform_on_error": "support@myorg.org",
            "sra_broker_contact_name": "Support"
        }
   from isatools.convert import json2sra
   json2sra.convert(open('isa.json')), './outdir/', sra_settings=sra_settings)

This method writes the SRA files out to ``./outdir/``.

Note that when subitting SRA XML to ENA, you need to supply broker information as shown above in the ``sra_settings`` JSON, customised to your own organisation's settings.

To turn off pre-conversion validation, use ``validate_first=False``. By default it is set to ``validate_first=True``.
