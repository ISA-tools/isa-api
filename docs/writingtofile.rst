###########################################################
Tutorial: writing ISA objects to file in TAB or JSON format
###########################################################

To write out the ISA-Tab, you can use the ``isatab.dumps()`` function:

.. code-block:: python

    >>> from isatools import isatab
    >>> return isatab.dumps(investigation)  # dumps() writes out the ISA as a string representation of the ISA-Tab

The function listed above is designed to return all three files as a single string output for ease of inspection.
Alternatively you could do something like ``dump(isa_obj=investigation, output_path='./')`` to write the files to
the file system.

.. code-block:: python

    >>> from isatools import isatab
    >>> isatab.dump(investigation, 'tmp/')  # dump out ISA-Tab  to tmp/ directory
    <isatools.model.Investigation object>


To write out the ISA JSON, you can use the ``ISAJSONEncoder`` class with the Python ``json`` package:

.. code-block:: python

    >>> import json
    >>> from isatools.isajson import ISAJSONEncoder
        # Note that the extra parameters sort_keys, indent and separators are to make the output more human-readable.
    >>> return json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))


