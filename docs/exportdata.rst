###############################
Exporting data from ISA formats
###############################

We have provided a number of modules that allow you to export data from ISA formats to formats for well-known
databases or services.

----------------------------------
Exporting ISA content to SampleTab
----------------------------------
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