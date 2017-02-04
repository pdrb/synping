from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


version = '0.4'


setup(
    name='synping',
    version=version,
    description='Ping hosts using tcp syn packets',
    long_description=long_description,
    author='Pedro Buteri Gonring',
    author_email='pedro@bigode.net',
    url='https://github.com/pdrb/synping',
    license='MIT',
    classifiers=[],
    keywords='ping syn tcp packets synping',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    entry_points={
        'console_scripts': ['synping=synping.synping:cli'],
    },
)
