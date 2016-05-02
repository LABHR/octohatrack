from setuptools import setup, find_packages
from codecs import open
from os import path
import sys
import pypandoc

# Exit unless we're in pip3/Python 3
if not sys.version_info[0] == 3:
    print("\noctohatrack requires a Python 3 environment.\n\nTry `pip3 install` instead")
    sys.exit(1)

# Convert the README.md that works on GitHub to a RST version that works on pypi
long_description = pypandoc.convert('README.md', 'rst')

setup(
    name='octohatrack',
    version='0.5.1',
    description='Show _all_ the contributors to a GitHub repository',
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
    install_requires=[
        'requests', 
        'simplejson', 
        'gitpython'
    ],
    entry_points={
      'console_scripts': [ 
        "octohatrack = octohatrack.__main__:main"
      ]
    },
    packages=find_packages()
)
