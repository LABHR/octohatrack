#!/usr/bin/env python

import argparse
from argparse import SUPPRESS
import sys
import pkg_resources
from octohatrack.code_contrib import *
from octohatrack.contributors_file import *
from octohatrack.wiki import *
from octohatrack.helpers import *


def main():

    # Exit unless we're in python 3
    if not sys.version_info[0] == 3:
        print("octohatrack requires a Python 3 environment.\n\n")
        sys.exit(1)

    version = pkg_resources.require("octohatrack")[0].version

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo_name", metavar="username/repo", help="the name of the repo to parse"
    )
    parser.add_argument(
        "--no-cache", action="store_false", help="Disable local caching of API results"
    )
    parser.add_argument(
        "--wait-for-reset",
        action="store_true",
        help="Enable waiting for rate limit reset " "rather than erroring",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="octohatrack version %s" % version
    )

    args = parser.parse_args()
    repo_name = args.repo_name

    progress_message("Checking repo exists")
    repo = get_json("repos/%s" % repo_name)

    progress_message("Getting API Contributors")
    api = api_contributors(repo_name)
    progress_message("Getting Issue and Pull Request Contributors")
    pri = pri_contributors(repo_name)
    progress_message("Getting File Contributors")
    fil = contributors_file(repo_name)
    progress_message("Getting Wiki Contributors")
    wik = wiki_contributors(repo_name)

    contributors = api + pri + fil + wik

    display_results(repo_name, contributors, len(api))

if __name__ == "__main__":
    main()