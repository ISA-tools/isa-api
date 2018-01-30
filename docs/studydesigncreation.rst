###########################################
Study-design-driven creation of ISA content
###########################################

In addition to the basic classes for creating ISA objects (such as ``Investigation``, ``Study``, ``Assay`` described previously),
the ISA API also provides a set of helper Python classes to bootstrap the creation of ISA documents from key parameters obtained from the Design of Experiment (DoE).
The methods allow the creation of the study Treatment plan, the Sample collection Plan and the study assay plan.

The core functions of the ISA-API create mode which are covered in this section are:

- ``InterventionStudyDesign``
- ``Treatment``
- ``TreatmentFactory``
- ``TreatmentSequence``
- ``SampleAssayPlan``
- Assay 'topology modifiers' that support creating experimental graphs with specific characteristics for different technologies, such as ``MSAssayTopologyModifiers`` and ``DNASeqAssayTopologyModifiers``


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

The definition of `intervention design <http://purl.obolibrary.org/obo/OBI_0000115>`_ according to the `Ontology for Biomedical Investigations <http://obi-ontology.org/>`_ is:

.. note::
    "An intervention design is a study design in which a controlled process applied to the subjects (the intervention) serves as the independent variable manipulated by the experimentalist. The treatment (perturbation or intervention) defined can be defined as a combination of values taken by independent variable manipulated by the experimentalists are applied to the recruited subjects assigned (possibly by applying specific methods) to treatment groups. The specificity of intervention design is the fact that independent variables are being manipulated and a response of the biological system is evaluated via response variables as monitored by possibly a series of assays."


Creation of treatments: Treatment, TreatmentFactory, TreatmentSequence
----------------------------------------------------------------------

The ``Treatment`` class is defined as a tuple of factor values (as defined in the ISA model v1) and a treatment type.

To create a treatment object, you need to identify the ``StudyFactor``s and their ``FactorValue``s as the treatment is a specific combination of factor values:

.. code-block:: python

    agent = StudyFactor(name="agent", factor_type="agent value")
    intensity = StudyFactor(name="intensity", factor_type="intensity value")
    duration = StudyFactor(name="duration post exposure", factor_type="duration value")


    treatment = Treatment(treatment_type=INTERVENTIONS['CHEMICAL'],
        factor_values=(
            FactorValue(factor_name=agent, value='ibuprofen'),
            FactorValue(factor_name=intensity, value='low dose'),
            FactorValue(factor_name=duration, value='2 hr')
        ))


For convenience, a few objects are provided with some common:

- ``INTERVENTIONS`` such as chemical, behavioural, surgical, biological, radiological, and
- ``BASE_FACTORS`` representing a perturbation agent, intensity and duration of the treatment

but if these are not suitable for your purposes, you can build your own intervention type and factors.

In the example above we use one of the common interventions but created our own set of ``StudyFactor``s.

Instead of creating individual treatments, you may want to create all the treatments required for a specific design type.

The ``TreatmentFactory`` class provides utility methods to create a set of ``Treatment`` objects. One of the utility methods is that
for creating the set of treatments corresponding to a full factorial design (using method ``compute_full_factorial_design``).
This computes all the combinations of factor values, returning an empty set if one of the factors has no associated values.

An example of using the ``TreatmentFactory`` class is as follows:

.. code-block:: python
    treatment_factory = TreatmentFactory(factors=[agent, intensity, duration])

    treatment_factory.add_factor_value(agent, {'acetyl salicylic acid', 'acetaminophen', 'ibuprofen'})
    treatment_factory.add_factor_value(intensity, {'high dose', 'low dose', 'medium dose'})
    treatment_factory.add_factor_value(duration, {'2 hr', '4 hr'})

    factorial_design_treatments = treatment_factory.compute_full_factorial_design()

The ``factorial_design_treatments`` object will contain the set of 18 treatments that result from performing all the combinations of the 3x3x2 factor values shown above.

A set of treatments may be combined in a ``TreatmentSequence``.

The ``TreatmentSequence`` class provides a way of building is an ordered sequence of treatments, where each
treatment is assigned a rank, or epoch number, with the following properties: the epoch numbers always start with 1 (lowest epoch number),
all epochs should be positive integers, epoch numbers may be repeated (for concomitant treatments),
no value should be missing between the lowest epoch (1) and the highest epoch.


.. code-block:: python
    treatment_sequence = TreatmentSequence(
        ranked_treatments={ (x, (i+1)) for i, x in enumerate(factorial_design_treatments)}
        )


Creation of Sample and Assay Plans
----------------------------------

After you have identified the treatments, to describe your experiment fully you will need to indicate
the sampling plan (i.e. in which way you select the samples) as well as the assay plan (i.e. what
measurements you are taken from the samples). For this purpose, we provide the ``SampleAssayPlan`` class.


Taking into account the specifics of Data Acquisition events dependent on methodology and technology
----------------------------------------------------------------------------------------------------

The Assay 'topology modifiers' functions (such as ``MSAssayTopologyModifiers``  for Mass Spectrometry based assays or  ``DNASeqAssayTopologyModifiers`` for DNA sequence assays) are present to support specific branching or pooling events affecting the underlying experimental graph, which we aim to represent with ISA objects.
Depending on the assay and the technology used to acquire data, the number of 'hinge points' may vary but the basic principle remains the same. Some are common to all: for instance, irrespective of the technique, one may carry out several data acquisition on the same input material (technical replication). On the other hand, when using a technique such as mass spectrometry
an range of setting may be set by the operators, such as the type of injections modes, the type of acquisition modes. When using sequencing technology, different instruments may be used, libraries may be prepared as single or paired ends.
The 'Topology Modifiers' method in the ISA-API allows to specify those in a flexible yet generic way.

We will explain each of these objects and how to use them below.











