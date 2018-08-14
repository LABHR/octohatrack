#!/usr/bin/env python

import sys


def _sort_by_name(contributor):
    if contributor.get('name'):
        return contributor['name'].lower()

    return contributor['user_name']


def display_results(repo_name, contributors, api_len):
    """
    Fancy display. 
    """
    print("\n")

    print("All Contributors:")

    # Sort and consolidate on Name
    seen = []
    for user in sorted(contributors, key=_sort_by_name):
        if user.get('name'):
            key = user['name']
        else:
            key = user['user_name']
        if key not in seen:
            seen.append(key)
            if key != user["user_name"]:
                print("%s (%s)" % (user["name"], user['user_name']))
            else:
                print(user["user_name"])

    print("")

    print("Repo: %s" % repo_name)
    print("GitHub Contributors: %s" % api_len)
    print("All Contributors: %s 👏" % len(seen))


def progress():
    """
    Append an dot
    """
    sys.stdout.write(".")
    sys.stdout.flush()


def progress_message(message):
    sys.stdout.write("\n")
    sys.stdout.write("%s..." % message)
    sys.stdout.flush()
