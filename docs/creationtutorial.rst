########################################
Tutorial: describing a simple experiment
########################################

In this section, we provide a basic example of creating a complete experiment descriptor using the ISA API's model
classes. The descriptor is not complete and realistic, but it demonstrates the range of component classes that you can use to
create ISA content, including things like sample characteristics, ontology annotations and units.

.. Important:: As a pre-requisite to using ISA model please make sure you have read and understood the :doc:`ISA Abstract Model </isamodel>` that the ISA formats are based on.

Firstly, we need to import the ISA API's model classes from the ``isatools`` PyPI package.

.. code-block:: python

    from isatools.model.v1 import *

Next, we build our descriptor encapsulated in a single Python function to simplify the example code. In a real
application or script, you may decompose the function and hook it up to interactive components to solicit feedback
from a user on-the-fly.

Full listing in `createSimpleISA.py <https://github.com/ISA-tools/isa-api/blob/master/isatools/examples/createSimpleISA.py>`_.

