#!/usr/bin/env python

from setuptools import setup

setup(
    name='isatools',
    version='0.9.3-lite_test',
    packages=['isatools',
              'isatools.errors'
              ],
    package_data={'isatools': [],
        '': ['LICENSE.txt', 'README.md']},
    description='Metadata tracking tools help to manage an increasingly '
                'diverse set of life science, environmental and biomedical '
                'experiments',
    author='ISA Infrastructure Team',
    author_email='isatools@googlegroups.com',
    url='https://github.com/ISA-tools/isa-api',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    install_requires=[
        'numpy',
        'jsonschema',
        'pandas',
        'networkx',
        'six'
    ],
    test_suite='tests'
)
