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
from .helpers import (progress, progress_advance, get_user_data)

tmp_folder = "tmprepo"


def get_wiki_contributors(repo_name, code, non_code):

    progress("Collecting wiki contributors")

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
        print("No wiki")
        return []
    
    progress_advance()

    # Attempt to clone the repo, catching all gitpython ValueError errors
    try: 
        if os.path.isdir(tmp_folder):
            shutil.rmtree(tmp_folder)

        repo = Repo.clone_from(wiki_url, tmp_folder)
    except ValueError as e:
        print("\nError attempting clone wiki: %s" % str(e))
        return []

    progress_advance()

    wiki_contributors = []
    
    # Go through all the master branch commits and get all the git authors
    for i in list(repo.iter_commits("master")):
        wiki_contributors.append(i.author)

    # Return a unique set of contributors
    wiki = list(set(wiki_contributors))

    if len(wiki) == 0:
        print("\nWiki contributors: 0 (no wiki)")
        return

    github_users=[]

    for x in code: 
        github_users.append(x['name'])
    for x in non_code:
        github_users.append(x['name'])

    new_wiki = []

    # Ignore any users who's author names match an existing listing 
    # as a code or non-coding contribution
    #
    # WARNING: Possibly a lossy process
    for user in wiki: 
        u = str(user)
        if u in github_users:
            continue
        new_wiki.append(get_user_data({"login": u, "avatar_url": ""}))

    return new_wiki
