from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='octohatrack',
    version='0.5.1',
    description='Non-code contribution groker for GitHub',
    long_description=long_description,
    url='https://github.com/labhr/octohatrack',
    author='Katie McLaughlin',
    author_email='katie@glasnt.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='octohatrack github contributions',
    install_requires=['requests', 'simplejson', 'gitpython'],
    entry_points={
      'console_scripts': [ "octohatrack = octohatrack:main" ]
    },
    packages=find_packages()
)
