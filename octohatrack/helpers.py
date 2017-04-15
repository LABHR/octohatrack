#!/usr/bin/env python

import sys


def display_results(repo_name, contributors, api_len):
    """
    Fancy display. 
    """
    print("\n")

    print("All Contributors:")

    # Sort and consolidate on Name
    seen = []
    for user in sorted(contributors, key=lambda k: k['name'].lower()):
        if user["name"] not in seen:
            seen.append(user["name"])
            if user["name"] != user["user_name"]:
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
