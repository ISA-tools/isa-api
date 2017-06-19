#!/usr/bin/env python

from setuptools import setup

setup(
    name='isatools',
    version='0.8.1',
    packages=['isatools', 'isatools.convert', 'isatools.io', 'isatools.model'],
    package_data={'isatools': ['schemas/cedar/*.json',
                               'schemas/isa_model_version_1_0_schemas/core/*.json',
                               'schemas/configs/*.json',
                               'schemas/configs/schemas/*.json',
                               'convert/resources/biocrates/*',
                               'convert/resources/sra/*.xsl',
                               'convert/resources/sra/*.xml',
                               'config/json/default/*.json',
                               'config/json/default/schemas/*.json',
                               'config/json/sra/*.json',
                               'config/json/sra/schemas/*.json',
                               'config/xml/*.xml',
                               'resources/sra_schemas/*.xsd',
                               'resources/sra_templates/*.xml',
                               'resources/tab_templates/*.txt'],
                  '': ['LICENSE.txt', 'README.md']},
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
        'progressbar2'
    ],
    test_suite='tests'
)
