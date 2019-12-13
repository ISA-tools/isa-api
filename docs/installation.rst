############
Installation
############

**Requires: Python 3.4+, tested on 3.4, 3.5, 3.6 and 3.7; additionally Java 1.6+ for INSDC SRA (Sequence Read Archive) and Biocrates &trade; importers**

Installation from the Python Package Index
------------------------------------------

The ISA API is published on the Python Package Index (PyPI) as the `isatools` package ((see `<https://pypi.python.org/pypi/isatools/>`_), and you can use ``pip`` to install it.

``$ pip install isatools``

This command will install the latest version posted on PyPI. If you need to install a specific version of the isatools module, use the following:

``$ pip install isatools==10.4 ``

To upgrade from an earlier installation of the isatools package, do:

``$ pip install --upgrade isatools``

Now you're ready to get started!

Installation from sources
-------------------------
The ISA-API source code is hosted on GitHub at: `<https://github.com/ISA-tools/isa-api>`_ You can get the source code by running the following `git` command:

``$ git clone https://github.com/ISA-tools/isa-api/``

We recommend using a virtual environment for your Python projects. ``virtualenv`` is a tool for creating isolated
Python runtime environments. It does not install separate copies of Python, but rather it does provide a clever way
to keep different configurations of environment cleanly separated.

If you are on Mac OS X or Linux, one of the following two commands will work for you:

``$ sudo easy_install virtualenv``

or even better:

``$ sudo pip install virtualenv``

Then, you can create a virtual environament:
``$ virtualenv venv``

and activate it:
``$ source venv/bin/activate``

Finally, you should install the requirements with:
``$ pip install -r requirements.txt``
  or
``$ pip install --upgrade -r requirements.txt``
if you want to upgrade the requirements already installed.

Install into your local Python environment with:

``python setup.py install``

or open up your favourite IDE to explore the codebase. We use JetBrains' `https://www.jetbrains.com/pycharm/ <https://www.jetbrains.com/pycharm/>`_.

Now you're ready to get started!

For full instructions on installing and using ``virtualenv`` see `their documentation <https://virtualenv.readthedocs.org>`_.
Alternative to ``virtualenv``, ``pyenv`` is also great to manage virtual environments. For full instructions on installing and using ``pyenv`` see `their documentation <https://github.com/pyenv/pyenv>`_.

Running tests
-------------

The tests in the ISA-API rely on datasets available in the test branch of the `ISAdatasets repository <http://github.com/ISA-tools/ISAdatasets>`_.

Thus, the first step for running the tests is to clone that branch to the `tests/data` folder from the root of your `isa-api` source code project:

``git clone -b tests --single-branch http://github.com/ISA-tools/ISAdatasets tests/data``

After that, you can run the test with the usual command:

``python setup.py test``
