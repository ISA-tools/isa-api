###############
ISA Conversions
###############

The ISA API includes a set of functions to allow you to convert between ISA formats, as well as between ISA formats.
These converters can be found in the ``isatools.convert`` package.

Converting from ISA-Tab to ISA JSON
-----------------------------------

To convert from a directory ``./tabdir/`` containing valid ISA-Tab files (e.g. ``i_investigation.txt``, ``s_...txt``
and ``a_...txt`` files):

.. code-block:: python

   from isatools.convert import isatab2json
   # we run the conversion from ISA-Tab to JSON (by default, the converter will perform validation. IMPORTANT: the converter does not serialise. The writing to file (serialization) needs to be explicitly invoked (see next step).
   isa_json = isatab2json.convert('./tabdir/', use_new_parser=True)

   # we now write to file:
   try:
        with open(output_file_path, 'w') as out_fp:
            json.dump(isa_json, out_fp, indent=4)
   except IOError as e:
        print("something went wrong:", e)

.. hint:: The conversions by default run the ISA validator to check for correctness of the input content. To skip the validation step, set the ``validate_first`` parameter to ``False`` by doing something like ``converter.convert('./my/path/', validate_first=False)``.

.. code-block:: python

   from isatools.convert import isatab2json
   isa_json = isatab2json.convert('./tabdir/',use_new_parser=True, validate_first=False)

    # we now write to file:...(see first block of code)

.. hint:: The conversions by default use a legacy ISA-Tab parser, which has now been replaced with a faster version. To specify using the old parser, set the ``use_new_parser`` parameter to ``False`` by doing something like ``isatab2json.convert('./my/path/', use_new_parser=False)``
 or drop the argument entirely. The older version is invoked by default.

.. code-block:: python

   from isatools.convert import isatab2json
   # we run the conversion from ISA-Tab to JSON (by default, the converter will perform validation. IMPORTANT: the converter does not serialise. The writing to file (serialization) needs to be explicitly invoked (see next step).
   isa_json = isatab2json.convert('./tabdir/')

   # we now write to file: ...(see first block of code)



Converting from ISA JSON to ISA-Tab
-----------------------------------

To convert from a ISA JSON file ``isa.json`` directory to write out ISA-Tab files to a target directory ``./outdir/``:

.. code-block:: python

   from isatools.convert import json2isatab
   with open('isa.json') as file_pointer:
       json2isatab.convert(file_pointer, './outdir/')

To turn off pre-conversion validation, use `validate_first=False`. By default it is set to `validate_first=True`.

.. code-block:: python

   from isatools.convert import json2isatab
   with open('isa.json') as file_pointer:
       json2isatab.convert(file_pointer, './outdir/', validate_first=False)


The ISA API can also convert to and from other formats for import/export to relevant databases and services. For more
on those conversions, please read the sections on `Importing data in ISA formats </importdata>` and
`Exporting data in ISA formats </exportdata>`.