from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='octohat',
    version='0.1.3',
    description='Non-code contribution groker for GitHub',
    long_description=long_description,
    url='https://github.com/glasnt/octohat',
    author='Katie McLaughlin',
    author_email='katie@glasnt.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
    ],
    keywords='octohat github contributions non-code',
    install_requires=['requests', 'simplejson'],
    entry_points={
      'console_scripts': [ "octohat = octohat:main" ]
    },
    packages=find_packages()
)
