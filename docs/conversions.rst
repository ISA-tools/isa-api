###############
ISA Conversions
###############

The ISA API includes a set of functions to allow you to convert between ISA formats, as well as between ISA formats and other formats such as SRA. These converters can be found in the ``isatools.convert`` package.

Converting from ISA tab to ISA JSON
-----------------------------------

To convert from a directory ``./tabdir/`` containing valid ISA tab files (e.g. ``i_investigation.txt``, ``s_...txt`` and ``a_...txt`` files) to a write the target JSON to another directory ``./outdir/``:

.. code-block:: python

   from isatools.convert import isatab2json
   isatab2json.convert('./tabdir/', './outdir/')

Converting from ISA JSON to ISA tab
-----------------------------------

To convert from a ISA JSON file ``isa.json`` directory to write out ISA tab files to a target directory ``./outdir/``:

.. code-block:: python

   from isatools.convert import json2isatab
   json2isatab.convert(open('isa.json')), './outdir/')
