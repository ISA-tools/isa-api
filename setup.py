#!/usr/bin/env python

from setuptools import setup

setup(
    name='isatools',
    version='0.2.4',
    packages=['isatools', 'isatools.convert', 'isatools.io', 'isatools.model', 'isatools.sampledata', 
              'isatools.schemas', 'isatools.validate'],
    package_data={'isatools': ['schemas/cedar/*.json',
                               'schemas/isa_model_version_1_0_schemas/core/*.json',
                               'convert/isa_line_commands/bin/lib/*',
                               'convert/isa_line_commands/bin/config.sh',
                               'convert/isa_line_commands/config/*',
                               'convert/isa_line_commands/bin/convert.sh',
                               'convert/isa_line_commands/bin/validate.sh', 
                               'convert/isa_line_commands/import_layer_deps.jar',
                               'convert/resources/sra/*.xsl',
                               'config/json/*.json',
                               'config/json/schemas/*.json',
                               'config/xml/*.xml'],
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
        'biopy-isatab',
        'jsonschema',
        'pandas',
        'networkx',
        'behave',
        'httpretty',
        'sure',
        'lxml',
        'requests',
        'chardet',
        'iso8601'
    ],
    test_suite='tests'
)
