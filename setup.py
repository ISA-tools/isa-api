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
    version='0.14.3',
    packages=['isatools',
              'isatools.model',
              'isatools.isatab',
              'isatools.isatab.dump',
              'isatools.isatab.load',
              'isatools.isatab.validate',
              'isatools.isatab.validate.rules',
              'isatools.isajson',
              'isatools.convert',
              'isatools.create',
              'isatools.io',
              'isatools.net',
              'isatools.net.mtbls',
              'isatools.net.mw2isa',
              'isatools.tests',
              'isatools.database',
              'isatools.database.models',
              'isatools.graphQL',
              'isatools.graphQL.utils',
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
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
       # 'Programming Language :: Python :: 3.13',
    ],
    install_requires=[
        'graphene==3.4.3',
        'graphql-core==3.2.6',
        'wheel~=0.43.0',
        'setuptools~=77.0.3',
        'numpy~=2.2.4; python_version >= "3.9"', # or python_version == 3.11 or python_version == 3.12', # or python_version == 3.13'
        'numpy~=2.0.2; python_version < "3.10"',
        'jsonschema~=4.23.0',
        'pandas==2.2.3',
        'openpyxl>=3.1.5',
        'networkx~=3.4.2; python_version >= "3.9"', # or python_version == 3.11 or python_version == 3.12', # or python_version == 3.13',
        'networkx~=3.2; python_version < "3.10"',
        'lxml~=5.3.1',
        'requests~=2.32.3',
        'iso8601~=2.1.0',
        'chardet~=5.2.0',
        'jinja2~=3.1.4',
        'beautifulsoup4~=4.13.3',
        'mzml2isa==1.1.1',
        'biopython~=1.85',
        'progressbar2~=4.4.2',
        'deepdiff~=8.4.2',
        'PyYAML~=6.0.2',
        'bokeh~=3.4.2',
        'certifi==2025.1.31',
        'flake8==7.1.0',
        'ddt==1.7.2',
        'behave==1.2.6',
        'httpretty==1.1.4',
        'sure==2.0.1',
        'coveralls~=4.0.1',
        'rdflib~=7.0.0',
        'SQLAlchemy==1.4.52',
        'python-dateutil~=2.9.0.post0',
        'Flask~=3.1.0',
        'flask_sqlalchemy~=3.0.2'
    ],
    test_suite='tests',
    license_files=("LICENSE.txt")
)
