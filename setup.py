#!/usr/bin/env python

from setuptools import setup

setup(
    name='isatools',
    version='0.1',
    packages=['isatools', 'isatools.convert', 'isatools.io', 'isatools.model', 'isatools.sampledata',
              'isatools.schemas', 'isatools.validate'],
    description='ISA version 1.0 API',
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
)
