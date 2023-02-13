#!/usr/bin/env python
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name)).read()


setup(
    name='isatools',
    version='0.14.0',
    packages=['isatools',
              'isatools.model',
              'isatools.isatab',
              'isatools.isajson',
              'isatools.convert',
              'isatools.create',
              'isatools.io',
              'isatools.net',
              'isatools.tests',
              'isatools.database',
              'isatools.graphQL'
              ],
    package_data={'isatools': [
        'resources/schemas/cedar/*.json',
        'resources/schemas/isa_model_version_1_0_schemas/core/*.json',
        'resources/schemas/configs/*.json',
        'resources/schemas/configs/schemas/*.json',
        'resources/config/json/default/*.json',
        'resources/config/json/default/schemas/*.json',
        'resources/config/json/sra/*.json',
        'resources/config/json/sra/schemas/*.json',
        'resources/config/xml/*.xml',
        'resources/config/yaml/*.yml',
        'resources/sra_schemas/*.xsd',
        'resources/sra_templates/*.xml',
        'resources/tab_templates/*.txt',
        'net/resources/biocrates/*',
        'net/resources/sra/*.xsl',
        'net/resources/sra/*.xml',
        'resources/isatools.ini'],
        '': ['LICENSE.txt', 'README.md']},
    description='Metadata tracking tools help to manage an increasingly diverse set of life science, '
                'environmental and biomedical experiments',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='ISA Infrastructure Team',
    author_email='isatools@googlegroups.com',
    url='https://github.com/ISA-tools/isa-api',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'graphene==3.1.1',
        'graphql-core==3.2.3',
        'wheel~=0.36.2',
        'setuptools~=57.1.0',
        'numpy~=1.23.3',
        'jsonschema~=3.2.0',
        'pandas==1.5.0',
        'openpyxl>=2.5.0',
        'networkx~=2.5.1',
        'lxml~=4.9.1',
        'requests~=2.25.1',
        'iso8601~=0.1.14',
        'chardet~=4.0.0',
        'jinja2~=3.0.1',
        'beautifulsoup4~=4.9.3',
        'mzml2isa==1.1.1',
        'biopython~=1.79',
        'progressbar2~=3.53.1',
        'deepdiff~=5.5.0',
        'PyYAML~=5.4.1',
        'bokeh~=2.3.2',
        'certifi==2021.5.30',
        'flake8==3.9.2',
        'ddt==1.4.2',
        'behave==1.2.6',
        'httpretty==1.1.3',
        'sure==2.0.0',
        'coveralls~=3.1.0',
        'rdflib~=6.0.2',
        'Flask~=2.2.2',
        'flask_sqlalchemy~=3.0.2'
    ],
    test_suite='tests'
)
