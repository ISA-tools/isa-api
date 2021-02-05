# Creating ISA content

+++
The ISA API provides a set of Python classes that you can use to create
ISA content with.

The three main objects that you need to create ISA content are:

-   `Investigation`
-   `Study`
-   `Assay`

\...of course!

```{admonition}  Important
:class: tip
As a pre-requisite to using ISA model classes, please make sure you have
read and understood the
`ISA Abstract Model </isamodel>`{.interpreted-text role="doc"} that the
ISA formats are based on.
```

***

## Getting started


In `isatools.model`, the class `Investigation` is used as the top level
container for all other ISA content. The `Investigation` Python class
corresponds to the
[Investigation](http://isa-specs.readthedocs.io/en/latest/isamodel.html#investigation)
as defined in the [ISA Model
Specification](http://isa-specs.readthedocs.io/en/latest/isamodel.html).
For example, to create an empty ISA structure consisting of an
investigation with one study, you might use the following code:

```python
from isatools.model import *
investigation = Investigation()
investigation.studies.append(Study())  # adds a new default Study object to investigation
```

This code simply creates one `Investigation` object, and adds a single
`Study` object to it. The constructor of each of these objects creates
empty structures for each of these. We can then inspect the structure by
accessing its instance variables as follows:

* Checking if a `study` exits:
```python
investigation.studies
[<isatools.model.Study object>]
```

* Checking if `assays` are associated to the first `study` object:
```python
investigation.studies[0].assays
[]
```

* Checking if the `Investigation` object has a `title` attribute filled:
```python
investigation.title
''
```

Since we have not set any data in our ISA objects, these are by default
mostly empty at the moment. We can set some instance variables with data
as follows:

```python
investigation.title = "My ISA Investigation"
```
```python
investigation.title
'My ISA Investigation'
```

```python
investigation.studies[0].title = "My ISA Study"
```
```python
investigation.studies[0].title
'My ISA Study'
```

```python
investigation.studies[0].assays.append(Assay())  # adds a new default Assay object to study
```
```python
i.studies[0].assays
[<isatools.model.Assay object>]
```

If you then write these out to ISA-Tab, we can inspect the output
written into an `i_investigation.txt` file. We do this using the
`isatab` module to `dump()` the `Investigation` object we created, as
follows:

```python
from isatools import isatab
isatab.dump(investigation, 'tmp/')  # dump out ISA-Tab  to tmp/
<isatools.model.Investigation object>
```

If all went as expected, you should find an `i_investigation.txt` file
with the standard Investigation sections, one Study section structured
as defined by the [ISA-Tab
Specification](http://isa-specs.readthedocs.io/en/latest/isatab.html).


```{admonition} Hint
:class: tip

Remember that when you `dump()` ISA content, you do it on the
`Investigation` object. This means any `Study` and `Assay` objects and
content must be attached to the `Investigation` for it to be serialized
out.
```

Different classes in `isatools.model` have class constructors and
instance variables that roughly map to the ISA Abstract Model. For full
details of how to instantiate model classes, access and manipulate ISA
data as objects, please inspect the module\'s docstrings.

Obviously this isn\'t enough to create a fully populated ISA
investigation, but we would recommend that you have a look in the
`isatools.model` package to inspect all the docstring documentation that
is included with each of the ISA model classes.
