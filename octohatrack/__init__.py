#!/usr/bin/env python

import argparse
import sys
from .helpers import (generate_html, repo_exists, get_code_commentors,
                      get_code_contributors, display_user_name)


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("repo_name", help="githubuser/repo")
  parser.add_argument("-g", "--generate-html", action='store_true',
                      help="Generate output as HTML")
  parser.add_argument("-l", "--limit",
                      help="Limit to the last x Issues/Pull Requests",
                      type=int, default=0)
  parser.add_argument("-c", "--show-contributors", action='store_true',
                      help="Output the code contributors")
  parser.add_argument("-n", "--show-names", action='store_true',
                      help="Show the user's display name")
  parser.add_argument("--no-cache", action='store_false',
                      help='Disable local caching of API results')
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

  non_code_contributors = []
  for user in code_commentors:
    user_name, avatar, name = user
    if user not in code_contributors:
      non_code_contributors.append(user)

  code_contributors = sorted(code_contributors,
                             key=lambda k: k['user_name'].lower())
  non_code_contributors = sorted(non_code_contributors,
                                 key=lambda k: k['user_name'].lower())

  print("\nCode contributions: %d" % len(code_contributors))

  if args.show_contributors:
    for user in code_contributors:
      display_user_name(user, args)

  print("\nNon-code contributions: %d" % len(non_code_contributors))

  for user in non_code_contributors:
    display_user_name(user, args)

  if args.generate_html:
    generate_html(code_contributors, non_code_contributors, args)


if __name__ == "__main__":
  main()
