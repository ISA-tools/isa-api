from distutils.core import setup

setup(
    name='isatools_api',
    version='0.0.1',
    packages=['isatools', 'isatools.io', 'isatools.io.schemas'],
    description='ISA version 1.0 API',
    author='ISA Infrastructure Team',
    author_email='isa@googlegroups.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Library',
        'Programming Language :: Python :: 2.7',
        ],
    url='http://www.isa-tools.org/',
)
