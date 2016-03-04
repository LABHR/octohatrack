#!/usr/bin/env python

import argparse
import sys
import pkg_resources
from .helpers import (repo_exists, get_code_commentors,
                      get_code_contributors, consolidate, display_users)

def main():
  version = pkg_resources.require("octohatrack")[0].version

  parser = argparse.ArgumentParser()
  parser.add_argument("repo_name", help="githubuser/repo")
  parser.add_argument("-l", "--limit",
                      help="Limit to the last x Issues/Pull Requests",
                      type=int, default=0)
  parser.add_argument("--no-cache", action='store_false',
                      help='Disable local caching of API results')
  parser.add_argument("-v", "--version", action='version',
                      version="octohatrack version %s" % version)

  args = parser.parse_args()

  repo_name = args.repo_name

  try:
    if not repo_exists(repo_name):
      print("Repo does not exist: %s" % repo_name)
      sys.exit(1)

    code_contributors = get_code_contributors(repo_name)
    code_commentors = get_code_commentors(repo_name, args.limit)
  except ValueError as e:
    print(e)
    sys.exit(1)

  non_code_contributors = consolidate(code_contributors, code_commentors)

  display_users(code_contributors, "Code contributors")
  display_users(non_code_contributors, "Non-coding contributors")


if __name__ == "__main__":
  main()
