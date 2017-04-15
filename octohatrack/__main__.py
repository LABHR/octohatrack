#!/usr/bin/env python

import argparse
from argparse import SUPPRESS
import sys
import pkg_resources
from .helpers import *
from .wiki import (get_wiki_contributors)
from .contributors_file import (get_contributors_file)

def main():
 
  # Exit unless we're in python 3
  if not sys.version_info[0] == 3:
    print("octohatrack requires a Python 3 environment.\n\n")
    sys.exit(1)

  version = pkg_resources.require("octohatrack")[0].version

  parser = argparse.ArgumentParser()
  parser.add_argument("repo_name", metavar="username/repo", help="the name of the repo to parse")
  parser.add_argument("--no-cache", action='store_false', help='Disable local caching of API results')
  parser.add_argument("-v", "--version", action='version', version="octohatrack version %s" % version)

  args = parser.parse_args()

  repo_name = args.repo_name

  try:
    if not repo_exists(repo_name):
      print("Repo does not exist: %s" % repo_name)
      sys.exit(1)

    api_contributors = get_api_contributors(repo_name)
    pri_contributors = get_pri_contributors(repo_name, args.limit)
    wiki_contributors = get_wiki_contributors(repo_name)
    file_contributors = get_contributors_file(repo_name)
  except ValueError as e:
    print(e)
    sys.exit(1)

  all_contributors = unique_users(api_contributors, pri_contributors, wiki_contributors, file_contributors)

  display_results(repo_name, api_contributors, all_contributors)

if __name__ == "__main__":
  main()
