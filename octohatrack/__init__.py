#!/usr/bin/env python

import argparse
import sys
import pkg_resources
from .helpers import (repo_exists, get_code_commentors,
                      get_code_contributors, consolidate, display_users)
from .wiki import (get_wiki_contributors)

def main():
  version = pkg_resources.require("octohatrack")[0].version

  parser = argparse.ArgumentParser()
  parser.add_argument("repo_name", help="githubuser/repo")
  parser.add_argument("-l", "--limit",
                      help="Limit to the last x Issues/Pull Requests",
                      type=int, default=0)
  parser.add_argument("--no-cache", action='store_false',
                      help='Disable local caching of API results')
  parser.add_argument("-w", "--wiki", action='store_true',
                      help="Experimental: Show wiki contributions, if available")
  parser.add_argument("-v", "--version", action='version',
                      version="octohatrack version %s" % version)

  # Deprecated
  parser.add_argument("-c", "--show-contributors", action='store_true',
                      help="DEPRECATED - Output the code contributors")
  parser.add_argument("-n", "--show-names", action='store_true',
                      help="DEPRECATED - Show the user's display name")
  parser.add_argument("-g", "--generate-html", action='store_true',
                      help="DEPRECATED - Generate output as HTML")

  args = parser.parse_args()

  if args.show_contributors:
    print("The --show-contributors (-c) flag is deprecated. Ignoring.")

  if args.show_names:
    print("The --show-contributors (-n) flag is deprecated. Ignoring.")
  
  if args.generate_html:
    print("The --generate-html (-g) flag is deprecated. Ignoring.")
  
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

  if args.wiki:
    wiki_contributors = get_wiki_contributors(repo_name, code_contributors, non_code_contributors)

  display_users(code_contributors, "Code contributors")
  display_users(non_code_contributors, "Non-coding contributors")

  if args.wiki:
    display_users(wiki_contributors, "Wiki contributors")

if __name__ == "__main__":
  main()
