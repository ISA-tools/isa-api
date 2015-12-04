from distutils.core import setup

setup(
    name='isatools',
    version='0.0.2',
    packages=['isatools', 'isatools.convert', 'isatools.io', 'isatools.model'],
    description='ISA version 1.0 API',
    author='ISA Infrastructure Team',
    author_email='isa@googlegroups.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Library',
        'Programming Language :: Python :: 3.5',
        ],
    url='http://www.isa-tools.org/',
)
