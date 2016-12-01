############
Installation
############

**Requires: Python 3.4 or 3.5; additionally Java 1.6+ for validator and SRA conversion**

Installation from the Python Package Index
------------------------------------------

The ISA API is published on the Python Package Index (PyPI) as the `isatools` package ((see `<https://pypi.python.org/pypi/isatools/>`_), and you can use ``pip`` to
install it.


``$ pip install isatools``

Now you're ready to get started!

Installation from sources
-------------------------
The ISA-API source code is hosted on GitHub at: `<https://github.com/ISA-tools/isa-api>`_

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

Now you're ready to get started!

For full instructions on installing and using ``virtualenv`` see `their documentation <https://virtualenv.readthedocs.org>`_.
