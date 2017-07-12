###############################
Exporting data from ISA formats
###############################

We have provided a number of modules that allow you to export data from ISA formats to formats ready for consumption by
well-known databases or services in the following conversion modules found in the ``isatools.convert`` package:

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


-----------------------------------
Converting ISA content to SampleTab
-----------------------------------
To export metadata from SampleTab files (e.g. for EBI BioSamples database), you can do the following to export a
ISA-Tab to SampleTab:

.. code-block:: python

    from isatools.convert import isatab2sampletab
    with open('your/path/to/i_investigation.txt', 'r') as input_investigation_file:
        with open('your/path/to/sampletab.txt', 'w') as output_sampletab_file:
            isatab2sampletab.convert(input_investigation_file, output_sampletab_file)

To export an ISA JSON file to SampleTab, you can do:

.. code-block:: python

    from isatools.convert import isatab2sampletab
    with open('your/path/to/i_investigation.txt', 'r') as input_investigation_file:
        with open('your/path/to/sampletab.txt', 'w') as output_sampletab_file:
            isatab2sampletab.convert(input_investigation_file, output_sampletab_file)

You can also dump SampleTab content directly from ISA Python objects:

.. code-block:: python

    from isatools import sampletab
    with open('your/path/to/sampletab.txt', 'w') as output_sampletab:
        # Note: ISA would be a previously loaded or constructed root Investigation object
        sampletab.dump(ISA, output_sampletab)

---------------------------------
Exporting ISA content to MAGE-TAB
---------------------------------
To export metadata to MAGE-TAB files (e.g. for EBI ArrayExpress database), you can do the following to export a
ISA-Tab to  MAGE-TAB:

.. code-block:: python

    from isatools.convert import isatab2magetab
    with open('your/path/to/i_investigation.txt', 'r') as input_investigation_file:
        isatab2magetab.convert(input_investigation_file, 'your/output/path/')

To export an ISA JSON file to SampleTab, you can do:

.. code-block:: python

    from isatools.convert import json2magetab
    with open('your/path/to/i.json', 'r') as input_isajson_file:
        json2magetab.convert(input_isajson_file, 'your/output/path/')
