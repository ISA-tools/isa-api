# ISA and Repeated Measure Designs

ISA model was built on the foundation work of the MAGE and FUGE object models. Both models had an indicative notion of study design and Experimental Factor.
However, none of these model really tackled provided objects to represetent study timelines and sequential sets of events affecting groups and involving exposures, treatments and interventions.
More sophistocated models such as CDISC SDTM provide such entities under the CDISC Study Design Model (SDM) or the SDTM representation, with the notions of `Arm`, `Epoch`, `Cell`, and Visits clearly identified.

ISA and its Study Factor and associated Factor Values which have correspond to Study Independent Variables and associated variable levels (aka Factor Levels) can be effectively harnessed to represent single exposure. single measurement designs. Such designs represent the overwhelming majority of Study design deposited in majar functional genomics data repositories

However, the model does not work so well to represent explicility and unambiguously situations such as clinical trials or intervention with repeated exposure, and multiple visits where study subjects are followed in a longitudinal fashion. In such studies, it is necessary to track the timeline of treatments, the timelines of sample collections (during visits) and the timeline of measurements and assays.

This is what this section covers.

We will introduce a series a new objects used by the ISA-API create mode to support the reporting of more complex studies.

This work builds on CDISC STDM and while it does not support the full envelop offered by the model, expands the envelop of ISA suffficiently to efficiently represent complex experimemnnts.

This chapter contains 2 main sections, one dedicated to the introduction of the new objects and the second one, shows how to use them.

## ISA Arm, Epoch, Cells and Plans



```{figure} ../_static/images/isa-arms.png
:height: 450px
:name: ISA

an overview of the ISA model for repeated measures
```

```
```




## Practical representations and serialzation



```python
```



