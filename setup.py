#!/usr/bin/env python

from setuptools import setup

with open("requirements.txt") as r:
    install_requires = r.read().splitlines()

with open("requirements-tests.txt") as r:
    tests_require = r.read().splitlines()

setup(
    name='isatools',
    version='0.3.2',
    packages=['isatools', 'isatools.convert', 'isatools.io', 'isatools.model', 'isatools.sampledata'],
    package_data={'isatools': ['schemas/cedar/*.json',
                               'schemas/isa_model_version_1_0_schemas/core/*.json',
                               'schemas/configs/*.json',
                               'schemas/configs/schemas/*.json',
                               'convert/isa_line_commands/bin/lib/*',
                               'convert/isa_line_commands/bin/config.sh',
                               'convert/isa_line_commands/config/*',
                               'convert/isa_line_commands/bin/convert.sh',
                               'convert/isa_line_commands/bin/validate.sh',
                               'convert/isa_line_commands/import_layer_deps.jar',
                               'convert/isa_line_commands/bin/batch_sra2isatab.sh',
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
                               'sampledata/BII-I-1.json',
                               'sampledata/BII-S-3.json',
                               'sampledata/BII-S-7.json'],
                  '': ['LICENSE.txt', 'README.md', 'requirements.txt', 'requirements-tests.txt']},
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
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests'
)
