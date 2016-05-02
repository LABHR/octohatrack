#!/usr/bin/env python

import argparse
from argparse import SUPPRESS
import sys
import pkg_resources
from .helpers import (repo_exists, get_api_contributors, get_pri_contributors, unique_users, display_results)
from .wiki import (get_wiki_contributors)
from .contributors_file import (get_contributors_file)

def main():
 
  print("NOOTNOOOT")
  # Exit unless we're in python 3
  if not sys.version_info[0] == 3:
    print("octohatrack requires a Python 3 environment.\n\n")
    sys.exit(1)

  version = pkg_resources.require("octohatrack")[0].version

  parser = argparse.ArgumentParser()
  parser.add_argument("repo_name", metavar="username/repo", help="the name of the repo to parse")
  parser.add_argument("--no-cache", action='store_false', help='Disable local caching of API results')
  parser.add_argument("-v", "--version", action='version', version="octohatrack version %s" % version)
  parser.add_argument("-l", "--limit", metavar=10, help="Limit to the last x Issues/Pull Requests", type=int, default=0)

  # Deprecated flags
  parser.add_argument("-c", "--show-contributors", action="store_true", help=SUPPRESS)
  parser.add_argument("-n", "--show-names", action="store_true", help=SUPPRESS)
  parser.add_argument("-g", "--generate-html", action="store_true", help=SUPPRESS)
  parser.add_argument("-w", "--wiki", action="store_true", help=SUPPRESS)

  args = parser.parse_args()

  # Deprecation warnings
  if args.show_contributors:
    print("The --show-contributors (-c) flag is deprecated. Ignoring.")

  if args.show_names:
    print("The --show-contributors (-n) flag is deprecated. Ignoring.")
  
  if args.generate_html:
    print("The --generate-html (-g) flag is deprecated. Ignoring.")

  if args.wiki:
    print("The --wiki (-w) flag is deprecated. Ignoring.")
  
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
