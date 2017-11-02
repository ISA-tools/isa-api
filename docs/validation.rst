###############################
Validating ISA-Tab and ISA JSON
###############################

Using the ISA API you can validate ISA-Tab and ISA JSON files.


Validating ISA-Tab
------------------

To validate ISA-Tab files in a given directory ``./tabdir/`` against a given configuration found in a directory ``./isaconfig-default_v2015-07-02/``, do something like the following:

.. code-block:: python

   from isatools import isatab
   my_json_report = isatab.validate(open(os.path.join('./tabdir/', 'i_investigation.txt')), './isaconfig-default_v2015-07-02/')

making sure to *point to the investigation file* of your ISA-Tab, and providing the XML configurations. The validator will then read the location of your study and assay table files from the investigation file in order to validate those. If no path to XML configurations is provided, the ISA API will automatically select and use the ``isaconfig-default_v2015-07-02`` configurations.

This ISA-Tab validator has been tested against the sample data sets `BII-I-1
<https://github.com/ISA-tools/ISAdatasets/tree/master/tab/BII-I-1>`_, `BII-S-3
<https://github.com/ISA-tools/ISAdatasets/tree/master/tab/BII-S-3>`_ and `BII-S-7
<https://github.com/ISA-tools/ISAdatasets/tree/master/tab/BII-S-7>`_, that are found in the ``isatools`` package.

The validator will return a JSON-formatted report of warnings and errors.

Validating ISA JSON
-------------------

To validate an ISA JSON file against the ISA JSON version 1.0 specification you can use do so by doing this by doing something like:

.. code-block:: python

    from isatools import isajson
    my_json_report = isajson.validate(open('isa.json'))

The rules we check for in the new validators are documented in `this working document <https://goo.gl/l0YzZt>`_  in Google spreadsheets. Please be aware as this is a working document, some of these rules may be amended as we get more feedback and evolve the ISA API code.

This ISA JSON validator has been tested against `a range of dummy test data <https://github.com/ISA-tools/ISAdatasets/tree/tests/json>`_ found in ``ISAdatasets`` GitHub repository.

The validator will return a JSON-formatted report of warnings and errors.

Batch validation of ISA-Tab and ISA-JSON
----------------------------------------
To validate a batch of ISA-Tabs or ISA-JSONs, you can use the ``batch_validate()`` function.

To validate a batch of ISA-Tabs, you can do something like:

.. code-block:: python

    from isatools import isatab
    my_tabs = [
        '/path/to/study1/',
        '/path/to/study2/'
    ]
    my_json_report = isatab.batch_validate(my_tabs, '/path/to/report.txt')

To validate a batch of ISA-JSONs, you can do something like

.. code-block:: python

    from isatools import isajson
    my_jsons = [
        '/path/to/study1.json',
        '/path/to/study2.json'
    ]
    my_json_report = isajson.batch_validate(my_jsons, '/path/to/report.txt')

In both cases, the batch validation will return a JSON-formatted report of warnings and errors.

Reformatting JSON reports
-------------------------
The JSON reports produced by the validators can be reformatted using a function found in the ``isatools.utils`` module.

For example, to write out the report as a CSV textfile to ``report.txt``, you can do something like:

.. code-block:: python

    from isatools import utils
    with open('report.txt', 'w') as report_file:
        report_file.write(utils.format_report_csv(my_json_report))

