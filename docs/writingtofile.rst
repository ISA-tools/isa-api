###########################################################
Tutorial: writing ISA objects to file in TAB or JSON format
###########################################################

The ISA-API provides 2 serialization mechanisms for ISA objects, one for each of the format, TAB or JSON.
For each, following  current practice in Python, 2 modes are available which are invoked using either `dump()` or `dumps()` methods.
For former taking an ISA '
`Investigation` object and a `path to a directory` as input,
while the latter `dumps()` takes only an ISA `Investigation` objects and returns a `string` object (hence, the `s` in the method's name)

Serialization to ISA-Tab
------------------------

To write out the ISA-Tab to files, to a specific location, you can use the  ``isatab.dump(isa_obj=investigation, output_path='./')`` function:

.. code-block:: python

    >>> from isatools import isatab
    >>> isatab.dump(investigation, 'tmp/')  # dump out ISA-Tab  to tmp/ directory
    <isatools.model.Investigation object>


Alternatively you could use the `isatad.dumps()` function to view the ISA-Tab


.. code-block:: python

    >>> from isatools import isatab
    >>> return isatab.dumps(investigation)  # dumps() writes out the ISA as a string representation of the ISA-Tab

The function listed above is designed to return all three files as a single string output for ease of inspection.





Serialization to ISA-JSON
-------------------------

To write out the ISA JSON, you can use the ``ISAJSONEncoder`` class with the Python ``json`` package. This means that `json.dump()` or `json.dumps()` methods may be used to serialize.
the difference between the 2 methods is as mentioned before, that fact that `json.dump()` uses a file handle as input, while `json.dumps()` returns a string object.

.. code-block:: python

    >>> import json
    >>> from isatools.isajson import ISAJSONEncoder
        # Note that the extra parameters sort_keys, indent and separators are to make the output more human-readable.
    >>> return json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
    >>> isa_j = json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
    >>> open("isa_as_json_from_dumps.json","w").write(isa_j) # this call write the string 'isa_j' to the file called 'isa_as_json_from_dumps.json'


Another way to write directly to file from the ISA Object, one needs to invoke the json.dump function as documented below, bearing in mind that this **requires** that the ISA object is first converted to a suitable representation
This means first invoking the `json.dumps()` function and then the `json.loads()` function on the output of the `json.dumps()` function, before calling the json.dump()' function on the datastructure and a filehandle.

.. code-block:: python

    >>> import json
    >>> from isatools.isajson import ISAJSONEncoder
        # Note that the extra parameters sort_keys, indent and separators are to make the output more human-readable.
    >>> isa_j = json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
    >>> with open('./outputdir/isaj-file.json', 'w') as isafh:
    >>>     json.dump(json.loads(isa_j), isafh)


