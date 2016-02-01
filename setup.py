from setuptools import setup

setup(
    name='isatools',
    version='0.0.4',
    packages=['isatools', 'isatools.convert', 'isatools.io', 'isatools.model'],
    description='ISA version 1.0 API',
    author='ISA Infrastructure Team',
    author_email='isa@googlegroups.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3.4',
        ],
    url='http://www.isa-tools.org/',
    test_suite='tests'
)
