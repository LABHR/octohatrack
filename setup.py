import sys
from codecs import open
from os import path

from setuptools import find_packages, setup

import versioneer

# Exit unless we're in pip3/Python 3
if not sys.version_info[0] == 3:
    print(
        "\noctohatrack requires a Python 3 environment.\n\nTry `pip3 install` instead"
    )
    sys.exit(1)

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "DESCRIPTION.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="octohatrack",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Show _all_ the contributors to a GitHub repository",
    long_description=long_description,
    url="https://github.com/labhr/octohatrack",
    author="Katie McLaughlin",
    author_email="katie@glasnt.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="octohatrack github contributions",
    install_requires=["requests", "gitpython", "requests-cache",],
    entry_points={"console_scripts": ["octohatrack = octohatrack.__main__:main"]},
    packages=find_packages(),
)
