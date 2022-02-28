# Converting between ISA format

The ISA API includes a set of functions to allow you to convert between
ISA formats, as well as between ISA formats. These converters can be
found in the `isatools.convert` package.

---

## Converting from ISA-Tab to ISA JSON

To convert from a directory `./tabdir/` containing valid ISA-Tab files
(e.g. one `i_investigation.txt` file, with at least one `s_...txt` and one `a_...txt` files):

```python
from isatools.convert import isatab2json
isa_json = isatab2json.convert('./tabdir/', validate_first=True, use_new_parser=True)
```


```{admonition} Tip
:class: tip

The conversions by default run the ISA validator to check for correctness of the input content. 
To skip the validation step, set the `validate_first` parameter to `False` by doing something like
`<converter>.convert('./my/path/', validate_first=False)`.
```


```{admonition} Tip
:class: tip

The conversions by default use a legacy ISA-Tab parser, which has now been replaced with a faster version. 
To specify using the new parser, set the `use_new_parser` parameter to `True` by doing something like
`isatab2json.convert('./my/path/', use_new_parser=True)`.
```

---

## Converting from ISA JSON to ISA-Tab

To convert from an ISA JSON file, for example a file named `isa.json`, one needs to provide as argument a target directory where to write out the
ISA-Tab files: in our example, this directory is `./outdir/`, Therefore, the code looks as follows:

```python
from isatools.convert import json2isatab

with open('isa.json') as file_pointer:
    json2isatab.convert(file_pointer, './outdir/')
```

To turn off pre-conversion validation, use
[validate\_first=False]{.title-ref}. By default it is set to
[validate\_first=True]{.title-ref}.

```python
from isatools.convert import json2isatab

with open('isa.json') as file_pointer:
    json2isatab.convert(file_pointer, './outdir/', validate_first=False)
```

```{note}

The ISA API can also convert to and from other formats for import/export
to relevant databases and services. For more on those conversions,
please read the sections on Importing data in ISA formats
and Exporting data in ISA formats.

```
