from distutils.core import setup

setup(
    name='isatools_api',
    version='0.0.1',
    packages=['isatools', 'isatools.convert', 'isatools.io', 'isatools.schemas'],
    description='ISA version 0.0.1 API',
    author='ISA Infrastructure Team',
    author_email='isatools@googlegroups.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        ],
    url='https://github.com/ISA-tools/isa-api',
)
