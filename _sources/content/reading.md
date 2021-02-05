# Reading in ISA-Tab or ISA JSON

+++

Using the ISA API you can validate ISA-Tab and ISA JSON files.

***

## Reading ISA-Tab from disk

* To validate ISA-Tab files in a given directory `./tabdir/` against the default reference ISA xml configuration (isaconfig-default_v2015-07-02),  do something like the following, with for instance a folder called `BII-S-3`:

```python
from isatools import isatab
my_json_report = isatab.validate(open(os.path.join('./BII-S-3/', 'i_investigation.txt'))
```

```{admonition}  Tip
:class: tip
The validator will then read the
location of your study and assay table files from the investigation file
in order to validate those.
```

```{admonition}  Tip
:class: tip
 If no path to XML configurations is
provided, the ISA API will automatically select and use the
`isaconfig-default_v2015-07-02` configurations.
```

* To validate ISA-Tab files in a given directory `./tabdir/` against a different, custoom made ISA xml configuration found in a directory
`./my_custom_covid_study_isaconfig_v2021/`, do something like the following, making sure to *point to the investigation file* of your ISA-Tab, and
providing the XML configurations. :

```python
from isatools import isatab
my_json_report = isatab.validate(open(os.path.join('./tabdir/', 'i_investigation.txt')),
								 './my_custom_covid_study_isaconfig_v2021/')
```


This ISA-Tab validator has been tested against the sample data sets:
- [BII-I-1](https://github.com/ISA-tools/ISAdatasets/tree/master/tab/BII-I-1)
- [BII-S-3](https://github.com/ISA-tools/ISAdatasets/tree/master/tab/BII-S-3)
- [BII-S-7](https://github.com/ISA-tools/ISAdatasets/tree/master/tab/BII-S-7)

All of which that are found in the `isatools` package.


```{warning} 
the ISA sample datasets used to test the ISA tools also contains studies which harbour errors.
BII-S-4 and BII-S-5 will fail validation owing to an error in the investigation file (`Publication list` instead of `Publication `*L*`ist`)
```

***

## Reading ISA JSON from disk

To read an ISA JSON file against the ISA JSON version 1.0
specification you can use do so by doing this by doing something like:

```python
from isatools import isajson
my_json_report = isajson.validate(open('isa.json'))
```

The rules we check for in the new validators are documented in [this
working document](https://goo.gl/l0YzZt) in Google spreadsheets. Please
be aware as this is a working document, some of these rules may be
amended as we get more feedback and evolve the ISA API code.

This ISA JSON validator has been tested against [a range of dummy test
data](https://github.com/ISA-tools/ISAdatasets/tree/tests/json) found in
`ISAdatasets` GitHub repository.

The validator will return a JSON-formatted report of warnings and
errors.



