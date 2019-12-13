####################
Creating ISA content
####################

The ISA API provides a set of Python classes that you can use to create ISA content with.

The three main objects that you need to create ISA content are:

- ``Investigation``
- ``Study``
- ``Assay``

...of course!

.. Important:: As a pre-requisite to using ISA model classes, please make sure you have read and understood the :doc:`ISA Abstract Model </isamodel>` that the ISA formats are based on.

Getting started
---------------

In ``isatools.model``, the class ``Investigation`` is used as the top level container for all other ISA content.
The ``Investigation`` Python class corresponds to the
`Investigation <http://isa-specs.readthedocs.io/en/latest/isamodel.html#investigation>`_ as defined in the
`ISA Model Specification <http://isa-specs.readthedocs.io/en/latest/isamodel.html>`_. For example, to create an empty
ISA structure consisting of an ``Investigation`` with one ``Study``, you might use the following code:

.. code-block:: python

    >>> from isatools.model import *
    >>> investigation = Investigation()
    >>> investigation.studies.append(Study())  # adds a new default Study object to investigation

This code simply creates one ``Investigation`` object, and adds a single ``Study`` object to it. The constructor of
each of these objects creates empty structures for each of these. We can then inspect the structure by accessing
its instance variables as follows:

.. code-block:: python

    >>> investigation.studies
    [<isatools.model.Study object>] # returns an array of ISA Study Objects

    >>> investigation.studies[0].assays
    [] # returns an empty array, meaning the that first ISA Study object associated with the ISA Investigation has no ISA Assay declared yet.

    >>> investigation.title
    '' # returns an empty string, meaning that the attribute `title` of the ISA Investigation object has not been filled.

Since we have not set any data in our ISA objects, these are by default mostly empty at the moment.
We can set some instance variables with data as follows:

.. code-block:: python

    >>> investigation.title = "My ISA Investigation" # setting a value for the attribute `title`
    >>> investigation.title # call to retrieve the Investigation `title` attribute value.
    'My ISA Investigation'

    >>> investigation.studies[0].title = "My ISA Study"
    >>> investigation.studies[0].title
    'My ISA Study'

    >>> investigation.studies[0].assays.append(Assay())  # adds a new default ISA Assay object to study
    >>> i.studies[0].assays
    [<isatools.model.Assay object>]

.. hint:: IMPORTANT: Note how, in the command above, we took care to supply the `append()` command with the Object type
 expected by the association list. However, be aware that in Python, the append() function will add to a list any item passed as argument.
So it is **critical** to check against the ISA model that types of Objects required in order to avoid serialization errors.


Writing to file as ISA-Tab
--------------------------

If you then write these out to ISA-Tab, we can inspect the output written into an ``i_investigation.txt`` file. We
do this using the ``isatab`` module to ``dump()`` the ``Investigation`` object we created, as follows:

.. code-block:: python

    >>> from isatools import isatab
    >>> isatab.dump(investigation, 'tmp/')  # dump out ISA-Tab  to tmp/ directory
    <isatools.model.Investigation object>

If all went as expected, you should find an ``i_investigation.txt`` file with the standard Investigation sections,
one Study section structured as defined by the
`ISA-Tab Specification <http://isa-specs.readthedocs.io/en/latest/isatab.html>`_.

.. hint:: Remember that when you ``dump()`` ISA content, you do it on the ``Investigation`` object. This means any
   ``Study`` and ``Assay`` objects and content must be attached to the ``Investigation`` for it to be serialized out.

Different classes in ``isatools.model`` have class constructors and instance variables that roughly map to the
ISA Abstract Model. For full details on how to instantiate model classes, access and manipulate ISA data as objects,
please inspect the module's docstrings.

Obviously, this isn't enough to create a fully populated ISA investigation, but we would recommend that you have a look
in the ``isatools.model`` package to inspect all the docstring documentation that is included with each of the ISA
model classes.

A more detailed discussion about `serializing` (i.e. writing to file) ISA objects in Tab or JSON formats is available in this section