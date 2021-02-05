ISA-API installation
====================


```{admonition} IMPORTANT
:class: tip
Requires: Python 3.4, 3.5 or 3.6; additionally Java 1.6+ for SRA and
Biocrates importers
```

***

## Installation from the Python Package Index

The ISA API is published on the Python Package Index (PyPI) as the
[isatools package](https://pypi.python.org/pypi/isatools/), and you can use `pip` to
install it.

```bash
$ pip install isatools
```

Now you're ready to get started!

***

## Installation from sources


The ISA-API source code is hosted on GitHub at:
<https://github.com/ISA-tools/isa-api>

* You can get the source code by running the following `git` command:

```bash
$ git clone https://github.com/ISA-tools/isa-api/
```

* Installation in a virtual environment

We recommend using a virtual environment for your Python projects.
`virtualenv` is a tool for creating isolated Python runtime
environments. It does not install separate copies of Python, but rather
it does provide a clever way to keep different configurations of
environment cleanly separated.

If you are on Mac OS X or Linux, one of the following two commands will
work for you:
```bash
$ sudo easy_install virtualenv
```

or even better:

```bash
$ sudo pip install virtualenv
```

Then, you can create a virtual environment: 

```bash
$ virtualenv venv
```

and activate it: 
```bash
$ source venv/bin/activate
```

Finally, you should install the requirements with:
```bash
$ pip install -r requirements.txt
```

 or if you want to upgrade the requirements already installed.

```bash 
$ pip install --upgrade -r requirements.txt
```


Install into your local Python environment with:

```bash
python setup.py install
```

or open up your favourite IDE to explore the codebase. We use
[JetBrains](https://www.jetbrains.com/pycharm/).

Now you\'re ready to get started!

```{admonition} Tip
:class: tip

For full instructions on installing and using `virtualenv` see [their
documentation](https://virtualenv.readthedocs.org).

`pyenv` is an alternative to virtual, read all about [pyenv here](https://github.com/pyenv/pyenv) or [here](https://realpython.com/intro-to-pyenv/).
```

***
## Running tests

The tests in the ISA-API rely on datasets available in the test branch
of the [ISAdatasets
repository](http://github.com/ISA-tools/ISAdatasets).

Thus, the first step for running the tests is to clone that branch to
the *tests/data* folder from the root of your
*isa-api* source code project:

```bash
git clone -b tests --single-branch http://github.com/ISA-tools/ISAdatasets tests/data
```

After that, you can run the test with the usual command:

```bash
python setup.py test
```
