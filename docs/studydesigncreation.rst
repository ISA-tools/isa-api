############################################
Study-design-driven creation of ISA content
###########################################

In addition to the basic classes for creating ISA objects (such as ``Investigation``, ``Study``, ``Assay`` described previously),
the ISA API also provides a set of Python classes that you can use to create ISA content based on on the experiment, or study,  design.

Some of the objects we cover for this are:

- ``InterventionStudyDesign``
- ``Treatment``
- ``TreatmentFactory``
- ``TreatmentSequence``
- ``SampleAssayPlan``
- and what we call 'topology modifiers', which are different ways of modifying the topology (or shape) of the graph representing the experiment, such as
specific modifiers for mass spectrometry assays (```MSAssayTopologyModifiers```) or for DNA sequence assays  (```DNASeqAssayTopologyModifiers```)

We will explain each of these objects and how to use them below.

Getting started
---------------

The package containing all the classes for study-design-based creation of ISA content is ``isatools.create..model``.

To use this package, include the following import statement in your code, which includes all the objects available in the package

.. code-block:: python

    >>> from isatools.create.models import *


Alternatively, you can include specific classes and objects that you are interested in. For example

.. code-block:: python

    >>> from isatools.create.models import *

    from isatools.create.models import (InterventionStudyDesign, Treatment,
                                    Characteristic, TreatmentFactory,
                                    TreatmentSequence, AssayType,
                                    SampleAssayPlan, INTERVENTIONS,
                                    BASE_FACTORS_ as BASE_FACTORS,
                                    IsaModelObjectFactory,
                                    MSAssayTopologyModifiers,
                                    DNASeqAssayTopologyModifiers)



Currently, we only support intervention designs by creating objects of the class ```InterventionStudyDesign``` (see code snippet below). We will soon also support
observation designs.

.. code-block:: python

>>> study_design = InterventionStudyDesign()

The definition of `intervention design http://purl.obolibrary.org/obo/OBI_0000115`_ according to the `Ontology for Biomedical Investigations http://obi-ontology.org/`_ is:

.. note::
    "An intervention design is a study design in which a controlled process applied to the subjects (the intervention) serves as the independent variable manipulated by the experimentalist. The treatment (perturbation or intervention) defined can be defined as a combination of values taken by independent variable manipulated by the experimentalists are applied to the recruited subjects assigned (possibly by applying specific methods) to treatment groups. The specificity of intervention design is the fact that independent variables are being manipulated and a response of the biological system is evaluated via response variables as monitored by possibly a series of assays."


Creation of treatments: Treatment, TreatmentSequence, TreatmentFactory
---------------------------------------------------------------------

The ```Treatment``` class is defined as a tuple of factor values (as defined in the ISA
    model v1) and a treatment type











