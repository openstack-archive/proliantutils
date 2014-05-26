from distutils.core import setup

setup(
    name='ProliantUtils',
    version='0.1.0',
    author='Hewlett Packard',
    packages=['proliantutils', 
              'proliantutils/ilo', 'proliantutils/tests/ilo'],
    license='LICENSE.txt',
    description='A set of libraries for interfacing various devices in '
                'Proliant servers.',
    long_description=open('README.md').read(),
)
