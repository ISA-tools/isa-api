###############################
Importing data into ISA formats
###############################

We have provided a number of modules that allow you to import data into ISA formats from well-known databases or
services. Imports from these services is supported by modules found in the ``isatools.net`` package:

------------------------------------------------
Importing from the MetaboLights database, to ISA
------------------------------------------------

To import an MetaboLights study from the `MetaboLights <https://www.ebi.ac.uk/metabolights>`_ as ISA-Tab files,
provide an MetaboLights accession number:

.. code-block:: python

   from isatools.net import mtbls as MTBLS
   tmp_dir = MTBLS.get('MTBLS1')

This method downloads the ISA-Tab files for a study, and returns a string path to a temporary directory containing the ISA-Tab files.

To import an MetaboLights study from the `MetaboLights <https://www.ebi.ac.uk/metabolights>`_ as ISA JSON files, provide an MetaboLights accession number:

.. code-block:: python

   from isatools.net import mtbls as MTBLS
   isa_json = MTBLS.getj('MTBLS1')

This method gets the study and returns the ISA content as ISA JSON.

You can also do simple queries on MetaboLights studies to retrieve samples and related data files, based on factor
selection:

.. code-block:: python

   from isatools.net import mtbls as MTBLS
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

   from isatools.net import sra2isatab
   sra2isatab.sra_to_isatab_batch_convert('BN000001', 'your/path/to/saxon9.jar')

This method returns the ISA-Tab files as a byte stream (``io.BytesIO``).

------------------------------------------------
Importing from MetabolomicsWorkbench, to ISA-Tab
------------------------------------------------
To import a study from the `Metabolomics Workbench <http://www.metabolomicsworkbench.org/>`_ as ISA-Tab files,
provide an accession number and your local path to write your files to:

.. code-block:: python

    from isatools.net.mw2isa import mw2isa_convert
    success, study_id, validate = mw2isa_convert(studyid="ST000367", outputdir='tmp/', dl_option="no", validate_option="yes")
    #  If success == True, download and conversion ran OK. If validate == True, the ISA-Tabs generated passed validation

See ``isa-api/isatools/convert/mw2isa.py``

------------------------------------
Importing from Biocrates, to ISA-Tab
------------------------------------

Notice: this method depends on SAXON XSLT Processor

See ``isa-api/isatools/net/biocrates2isatab.py``


Importing from third-party formats is supported with our conversion modules found in the ``isatools.convert`` package:

-------------------------
Importing mzML to ISA-Tab
-------------------------
To import metadata from mzML mass spectrometry files, the ISA API integrates with the ``mzml2isa``
tool from https://github.com/ISA-tools/mzml2isa and can be run as follows:

.. code-block:: python

    from isatools.convert import mzml2isa
    mzml2isa.convert('your/path/to/mzml/files/', 'tmp/', "My Study ID")

--------------------------
Importing SampleTab to ISA
--------------------------
To import metadata from SampleTab files (e.g. from EBI BioSamples database), you can do the following to import a
SampleTab to ISA-Tab:

.. code-block:: python

    from isatools.convert import sampletab2isatab
    with open('your/path/to/sampletab.txt', 'r') as input_sampletab:
        sampletab2isatab.convert(input_sampletab, 'tmp/')

To import a SampleTab to ISA JSON, you can do:

.. code-block:: python

    from isatools.convert import sampletab2json
    with open('your/path/to/sampletab.txt', 'r') as input_sampletab:
        with open('your/path/to/myjson.json', 'w') as output_json:'
            sampletab2json.convert(input_sampletab, output_json)

You can also load SampleTab content directly into ISA Python objects:

.. code-block:: python

    from isatools import sampletab
    with open('your/path/to/sampletab.txt', 'r') as input_sampletab:
        ISA = sampletab.load(input_sampletab)

-------------------------
Importing MAGE-TAB to ISA
-------------------------
To import metadata from MAGE-TAB files (e.g. from EBI ArrayExpress database), you can do the following to import a
MAGE-TAB to ISA-Tab:

.. code-block:: python

    from isatools.convert import magetab2isatab
    with open('your/path/to/magetab.idf.txt', 'r') as input_magetab:
        magetab2isatab.convert(input_sampletab, 'tmp/')

To import a MAGE-TAB to ISA JSON, you can do:

.. code-block:: python

    from isatools.convert import sampletab2json
    with open('your/path/to/magetab.idf.txt', 'r') as input_sampletab:
        with open('your/path/to/myjson.json', 'w') as output_json:'
            magetab2json.convert(input_magetab, output_json)
