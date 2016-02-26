
<p>Master branch</p> 
[![Build Status](https://travis-ci.org/ISA-tools/isa-api.svg?branch=master)](https://travis-ci.org/ISA-tools/isa-api/)
<p>Develop branch</p> 
[![Build Status](https://travis-ci.org/ISA-tools/isa-api.svg?branch=develop)](https://travis-ci.org/ISA-tools/isa-api/)

# isa-api

[![Build Status](https://travis-ci.org/ISA-tools/isa-api.svg?branch=develop)](https://travis-ci.org/ISA-tools/isa-api) [![Coverage Status](https://coveralls.io/repos/github/ISA-tools/isa-api/badge.svg?branch=develop)](https://coveralls.io/github/ISA-tools/isa-api?branch=develop)

This repository is a python-based ISA-API library, which supports the programmatic creation of ISA objects, multiple ISA serializations (e.g. tabular and JSON representations) and conversions between ISA and other formats (e.g. SRA xml).

It relies on Python 3.4 and we recommand using virtualenv for running/testing the code.

If you are not familiar with virtualenv, read this excellent blogpost by Jamie Matthews (https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/). Make sure your environmental variable are pointing to Python 3.4 before invoking virtualenv.

install all the dependencies by running:

env/bin/pip install -r requirements.txt

source env/bin/activate


# using git and pushing code

 We follow the [GitFlow development workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).

Travis Continuous Integration is set up on both Master and Develop branches of the repo. Prior to push code, always run the tests by invoking the following command

python setup.py test


### Instalation procedure

To install the isa-api, make sure to install the requirements:

`pip install -r requiremens.txt`

To run the tests:

`python setup.py test`

## isatools package

* Install using `pip install -e .` from inside `isa-api` project root (may need to sudo it)

## License

[CPAL License](https://raw.githubusercontent.com/ISA-tools/isa-api/master/LICENSE.txt)

## service

**Note:**

* REST service implementation is available at [isa-rest-api project](https://github.com/ISA-tools/isa-rest-api)
