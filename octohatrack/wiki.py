#############################################################
#
#                         WARNING
#
#   This module is extremely experimental.
#
#   May contain traces of: 
#    * checking for specific strings on web pages to check
#      for the existance of a wiki on a GitHub repo
#    * locally cloning a wiki repo to check the commit 
#      history
#    * local file system manipulation
#    * peanuts, or other tree nuts
#    
#############################################################


from git import Repo
import os
import shutil
import sys
import requests

tmp_folder = "tmprepo"

def get_wiki_contributors(repo_name):

    # Confirm git is available before continuing
    if not shutil.which("git"):
        print("Cannot find local 'git' installation. Skipping wiki contributions")
        return[]

    wiki_url = "https://github.com/%s.wiki" % repo_name

    # There is no way to check if a repo has a wiki via the api
    # 
    # The `has_wiki` is just a flag that reflects the settings checkbox
    # if a wiki is *enabled*, but it can be empty, and thus not cloneable
    #
    # So, check that there is the special string on the assumed wiki page
    # as a replacement for an API check
    resp = requests.get("https://github.com/%s/wiki" % repo_name)
    if "Clone this wiki locally" not in resp.text:
        return []

    # Attempt to clone the repo, catching all gitpython ValueError errors
    try: 
        if os.path.isdir(tmp_folder):
            shutil.rmtree(tmp_folder)

        repo = Repo.clone_from(wiki_url, tmp_folder)
    except ValueError as e:
        print("\nError attempting clone wiki: %s" % str(e))
        return []

    wiki_contributors = []
    
    # Go through all the master branch commits and get all the git authors
    for i in list(repo.iter_commits("master")):
        wiki_contributors.append(str(i.author))

    # Return a unique set of contributors
    contribs = list(set(wiki_contributors))

    return [ {"user_name": None, "name": c} for c in contribs ]
