###############################
Importing data into ISA formats
###############################

We have provided a number of modules that allow you to import data into ISA formats from well-known databases or services.

------------------------------------------------
Importing from the MetaboLights database, to ISA
------------------------------------------------

To import an MetaboLights study from the `MetaboLights <https://www.ebi.ac.uk/metabolights>`_ as ISA-Tab files,
provide an MetaboLights accession number:

.. code-block:: python

   from isatools.io import mtbls as MTBLS
   tmp_dir = MTBLS.get('MTBLS1')

This method downloads the ISA-Tab files for a study, and returns a string path to a temporary directory containing the ISA-Tab files.

To import an MetaboLights study from the `MetaboLights <https://www.ebi.ac.uk/metabolights>`_ as ISA JSON files, provide an MetaboLights accession number:

.. code-block:: python

   from isatools.io import mtbls as MTBLS
   isa_json = MTBLS.getj('MTBLS1')

This method gets the study and returns the ISA content as ISA JSON.

You can also do simple queries on MetaboLights studies to retrieve samples and related data files, based on factor
selection:

.. code-block:: python

   from isatools.io import mtbls as MTBLS
   MTBLS.get_factor_names('MTBLS1')
   # response:
   # {'Gender', 'Age'}
   MTBLS.get_factor_values('MTBLS1', 'Gender')
   # response:
   # {'Male', 'Female'}
   query = {
         "Gender": "Male"
      }
   samples_and_files = MTBLS.get_data_files('MTBLS1', factor_query=query)
   # response:
   #  [
   #     {
   #        'sample': 'ADG10003u_007'},
   #        'data_files': ['ADG10003u_007.zip'],
   #        'query_used': {'Gender': 'Male'}
   #     }, ...
   #  ]

--------------------------------------------------------------
Importing SRA from the European Nucleotide Archive, to ISA-Tab
--------------------------------------------------------------

Notice: this method depends on SAXON XSLT Processor

To import an SRA study from the `European Nucleotide Archive (ENA) <https://www.ebi.ac.uk/ena>`_ as ISA-Tab files,
provide an ENA accession number and your path to the SAXON JAR file:

.. code-block:: python

   from isatools.convert import sra2isatab
   sra2isatab.sra_to_isatab_batch_convert('BN000001', 'your/path/to/saxon9.jar')

This method returns the ISA-Tab files as a byte stream (``io.BytesIO``).

----------------------------------------------------
Importing SRA from MetabolomicsWorkbench, to ISA-Tab
----------------------------------------------------

See ``isa-api/isatools/convert/mw2isa.py``

----------------------------------------
Importing SRA from Biocrates, to ISA-Tab
----------------------------------------

Notice: this method depends on SAXON XSLT Processor

See ``isa-api/isatools/convert/biocrates2isatab.py``
