####################
Creating ISA objects
####################

The API provides a set of Python objects that you can create ISA content with.

The three main objects that you need to create ISA content are:

- ``Investigation``
- ``Study``
- ``Assay``

...of course!

For example, to create an empty ISA structure consisting of an investigation with one study, you might do something like this:

.. code-block:: python

    from isatools.model.v1 import *
    investigation = Investigation()
    investigation.studies.append(Study())  # add a new Study object to the Investigation

The constructor of each of these objects creates empty content for each of these. If you try and serialize these out to ISA-Tab format, we should see some output into an ``i_investigation.txt`` file. We can do this using the ``isatab`` package.

.. code-block:: python

    from isatools import isatab
    isatab.dump(investigation, 'tmp/')  # dumps out ISA-Tab format of the investigation we made earlier

If all went as expected, you should find an ``i_investigation.txt`` file with the following content in the directory you specified in the ``isatab.dump()`` function::

    ONTOLOGY SOURCE REFERENCE
    Term Source Name
    Term Source File
    Term Source Version
    Term Source Description
    INVESTIGATION
    Investigation Identifier
    Investigation Title
    Investigation Description
    Investigation Submission Date	2016-02-25
    Investigation Public Release Date	2016-02-25
    INVESTIGATION PUBLICATIONS
    Investigation PubMed ID
    Investigation Publication DOI
    Investigation Publication Author List
    Investigation Publication Title
    Investigation Publication Status
    Investigation Publication Status Term Accession Number
    Investigation Publication Status Term Source REF
    INVESTIGATION CONTACTS
    Investigation Person Last Name
    Investigation Person First Name
    Investigation Person Mid Initials
    Investigation Person Email
    Investigation Person Phone
    Investigation Person Fax
    Investigation Person Address
    Investigation Person Affiliation
    Investigation Person Roles
    Investigation Person Roles Term Accession Number
    Investigation Person Roles Term Source REF
    STUDY
    Study Identifier
    Study Title
    Study Description
    Study Submission Date	2016-02-25
    Study Public Release Date	2016-02-25
    Study File Name
    STUDY PUBLICATIONS
    Study PubMed ID
    Study Publication DOI
    Study Publication Author List
    Study Publication Title
    Study Publication Status
    Study Publication Status Term Accession Number
    Study Publication Status Term Source REF
    STUDY FACTORS
    Study Factor Name
    Study Factor Type
    Study Factor Type Term Accession Number
    Study Factor Type Term Source REF

Obviously this isn't enough to create a fully populated ISA investigation, but we would recommend that you have a look
in the ``isatools.model.v1`` package to inspect all the docstring documentation that is included with each of the ISA
model classes.
