###############################
Importing data into ISA formats
###############################

We have provided a number of modules that allow you to import data into ISA formats from well-known databases or services.

----------------------------------------------------
Importing SRA from the MetaboLights database, to ISA
----------------------------------------------------

Notice: this method depends on SAXON XSLT Processor

To import an MetaboLights study from the `MetaboLights <https://www.ebi.ac.uk/metabolights>`_ as ISA-Tab files, provide an MetaboLights accession number:

.. code-block:: python

   from isatools.io import mtbls
   tmp_dir = MTBLS.get_study('MTBLS1')

This method downloads the ISA-Tab files for a study, and returns a string path to a temporary directory containing the ISA-Tab files.

To import an MetaboLights study from the `MetaboLights <https://www.ebi.ac.uk/metabolights>`_ as ISA JSON files, provide an MetaboLights accession number:

.. code-block:: python

   from isatools.io import mtbls
   isa_json = MTBLS.load('MTBLS1')

This method gets the study and returns the ISA content as ISA JSON.

--------------------------------------------------------------
Importing SRA from the European Nucleotide Archive, to ISA-Tab
--------------------------------------------------------------

Notice: this method depends on SAXON XSLT Processor

To import an SRA study from the `European Nucleotide Archive (ENA) <https://www.ebi.ac.uk/ena>`_ as ISA-Tab files, provide an ENA accession number and your path to the SAXON JAR file:

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
