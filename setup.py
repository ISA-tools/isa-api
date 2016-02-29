#!/usr/bin/env python

from setuptools import setup

setup(
    name='isatools',
    version='0.1.0',
    packages=['isatools', 'isatools.convert', 'isatools.io', 'isatools.model', 'isatools.sampledata',
              'isatools.schemas', 'isatools.validate'],
    description='ISA-API',
    author='ISA Infrastructure Team',
    author_email='isatools@googlegroups.com',
    url='https://github.com/ISA-tools/isa-api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    install_requires = [
        "biopy-isatab",
        "jsonschema",
        "pandas",
        "networkx",
        "behave",
        "httpretty",
        "sure",
        "lxml",
        "requests",
        "coveralls"
    ],
    test_suite='tests'
)
