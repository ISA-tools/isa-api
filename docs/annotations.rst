######################################################
Quantitative and Qualitative Annotation on ISA objects
######################################################

Let's assume we have an ISA ``Investigation`` object holding one ISA ``Study``

.. code-block:: python

    >>> from isatools.model import *
    >>> from isatools import isajson
    >>> import json

    >>> i = Investigation()
    >>> s = Study(filename="s_study.txt")
    >>> i.studies.append(s)


Ontology Annotations:
---------------------

If using controlled terminologies or ontologies when annotating ISA objects, the first thing to do is to declare all such resources and add them the ``Investigation`` object.

.. code-block:: python

    >>> uo = OntologySource(name="UO",
                            description="Unit Ontology" ,
                            file="http://purl.obolibrary.org/obo/uo.owl")
    >>> obi = OntologySource(name="OBI",
                             description="Ontology for Biomedical Investigation" ,
                             file="http://purl.obolibrary.org/obo/obi.owl")
    >>> uberon = OntologySource(name="UBERON",
                                description="Uber Anatomy Ontology",
                                file="http://purl.obolibrary.org/obo/uberon.owl")

    >>> i.ontology_source_references.append(uo)
    >>> i.ontology_source_references.append(obi)
    >>> i.ontology_source_references.append(uberon)


With this tutorial, we will focus on how to provide annotations on:
 - ISA ``Materials`` objects such as ``Source``, ``Sample``, ``Extract`` and ``LabeledExtract`` via the ISA ``Characteristics`` object.
 - ISA ``Protocol Application`` objects via the ISA ``ParameterValue`` object.
 - ISA ``Material``, ``Assay`` and ``Data File`` Objects via the ISA ``FactorValue`` object.

Annotating ISA objects with Qualitative values:
-----------------------------------------------

So Let's start using ISA ``Characteristics`` to annotate a biological ``Source`` material, which we create using the following calls.

.. code-block:: python

    >>> source = Source(name="Source")
    # here we simply associate our newly created Source to the ISA Study it belongs to.
    >>> s.sources.append(source)


Next, we start qualifying our ``Source``:



.. note:: IMPORTANT: ISA ``Characteristic`` attribute ``category`` **must** be an ``OntologyAnnotation`` object (while the ``value`` attribute is less constrained, taking either ``string`` or ``OntologyAnnotation`` objects), so **DON'T do** :

.. code-block:: python

     >>> c_bad = Characteristic(category="color", value="blue")

This will cause an Error to be thrown!

Instead **DO**:

.. code-block:: python

     >>> c_good = Characteristic(category=OntologyAnnotation(term="color"),
                                 value="blue")
     >>> c_also_good =  Characteristic(category=OntologyAnnotation(term="color"),
                                       value=OntologyAnnotation(term="blue",
                                                                term_source=uberon,
                                                                term_accession=""))



Annotating ISA objects with Quantitative values:
-----------------------------------------------

To report numerical / quantitative values, the process is very similar, except that one must take care when filling the ``value`` attribute of the  ``Characteristic`` object to pass an ``integer`` or a ``float``, but not a ``string``.

So **DO** :

.. code-block:: python

    >>> oa_weight = OntologyAnnotation(term="weight")
    >>> oa_unit1 = OntologyAnnotation(term="kilogram",
                                      term_source=uo)
    >>> c=Characteristic(category=oa_weight,
                         value=74,
                         unit=oa_unit1)
    >>> source.characteristics.append(c)


Alternately, we could also do the following:

.. code-block:: python

    >>> c = Characteristic(category=OntologyAnnotation(term="weight"),
                           value=74,
                           unit=OntologyAnnotation(term="kilogram", term_source=uo))
    >>> source.characteristics.append(c)


But **DON'T DO**:

.. code-block:: python

    >>> c_numericalvalue_nogo = Characteristic(category=OntologyAnnotation(term="weight"),
                                               value="74",
                                               unit=OntologyAnnotation(term="kilogram",
                                                                       term_source=uo))
    >>> c_numericalvalue_nogoeither = Characteristic(category=OntologyAnnotation(term="weight"),
                                                     value=OntologyAnnotation(term="74"),
                                                     unit=OntologyAnnotation(term="kilogram",
                                                                             term_source=uo))

If you are getting error when assigning values for those annotation types, do remember to check all these steps!


.. note:: IMPORTANT: ISA ``Unit`` **must** be described with ``OntologyAnnotation`` objects.




Similar process when using ISA ``ParameterValue`` and ``FactorValue``:
----------------------------------------------------------------------

Here we show how to report an ISA ``ParameterValue`` numerical value:

.. code-block:: python

    >>> p = Protocol(name="myProtocol")
    >>> s.protocols.append(p)
    >>> parameter = ProtocolParameter(parameter_name=OntologyAnnotation(term="myParameter"))
    >>> p.parameters.append(parameter)

    >>> proc = Process(executes_protocol=p)
    >>> proc.inputs.append(source)
    >>> proc.outputs.append(sample)
    >>> s.process_sequence.append(proc)

    >>> u = OntologyAnnotation(term="meter",
                               term_accession="http://example.com/meter",
                               term_source=uo)

    # Now supplying an ISA ```ParameterValue``` quantitative value
    >>> proc.parameter_values.append(ParameterValue(category=parameter,
                                                   value=12,
                                                   unit=u))



Here we show how to report an ISA ```FactorValue``` quantitaive or qualitative values:

.. code-block:: python

    >>> f = StudyFactor(factor_type=OntologyAnnotation(term="dose"), name="dose")
    >>> s.factors.append(f)
    >>> fv = FactorValue(factor_name=f,
                         value=1,
                         unit=OntologyAnnotation(term="mM",
                                                 term_source=uo,
                                                 term_accession="http://purl.org/obolibrary/UO_1241241"))
    >>> sample.factor_values.append(fv)

    >>> chebi =  OntologySource(name="CHEBI",
                                description="Chemical Entity Ontology" ,
                                file="http://purl.obolibrary.org/obo/chebi.owl")

    >>> i.ontology_source_references.append(chebi)
    >>> other_f = StudyFactor(factor_type=OntologyAnnotation(term="chemical entity"),
                              name="drug")
    >>> s.factors.append(other_f)
    >>> other_fv = FactorValue(factor_name=other_f,
                               value=OntologyAnnotation(term="aspirin",
                                                        term_source=chebi,
                                                        term_accession="http://purl.org/obolibrary/CHEBI_15365"))



Commentable ISA Objects:
------------------------

In the ``ISA model``, most ISA objects can be annotated using an ISA `Comment`. All such objects are children of the class ``Commentable``.
To add a ``Comment`` to an ISA object, simple do the following:

.. code-block:: python

    >>> cmt = Comment(name="creation_date", value="YYYY-MM-DD")
    >>> source.comments.append(cmt)

hint:: for ISA ``Comment``, the attributes ``name`` and ``value`` only take ``string`` as input.
