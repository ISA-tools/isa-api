#!/usr/bin/env python

from setuptools import setup

setup(
    name='isatools',
    version='0.9.2-lite',
    packages=['isatools',
              'isatools.convert',
              'isatools.errors',
              'isatools.tests'
              ],
    package_data={'isatools': [
        'resources/schemas/isa_model_version_1_0_schemas/core/*.json',
        'resources/config/xml/*.xml',
        'resources/isatools.ini'],
        '': ['LICENSE.txt', 'README.md']},
    description='Metadata tracking tools help to manage an increasingly '
                'diverse set of life science, environmental and biomedical '
                'experiments',
    author='ISA Infrastructure Team',
    author_email='isatools@googlegroups.com',
    url='https://github.com/ISA-tools/isa-api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],
    install_requires=[
        'numpy',
        'jsonschema',
        'pandas',
        'networkx',
        'lxml',
        'requests',
        'chardet',
        'iso8601',
        'jinja2',
        'bs4',
        'mzml2isa',
        'biopython',
        'progressbar2',
        'deepdiff'
    ],
    test_suite='tests'
)
