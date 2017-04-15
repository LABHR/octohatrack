#!/usr/bin/env python

from .api_helpers import *

"""
Given a repo name, get the "contributors" from the contribution counter
"""
def api_contributors(repo_name):
  contribs = api_walk(repo_name + "/contributors")
  return [user_data(c) for c in contribs]

"""
Since Pull Requests and Issues are so similar in structure, do them together
"""
def pr_contributors(repo_name, _type="pulls"):
  contribs = []

  _count= api_get("%s/%s?state=all&page=1&per_page=1" % (repo_name, _type), "number")

  for i in range(1, _count + 1):
    uri_stub = "/".join([repo_name, _type, str(i)])

    start = api_get(uri_stub, key=USER_LOGIN)
    if start:
      contribs.append(start)
    else:
      break

    users = api_walk(uri_stub + "/comments", key=USER_LOGIN)
    if users:
      contribs += users

  return contribs

"""
Given a repo name, get all the contributors to all the PR/Issues
"""
def pri_contributors(repo_name):
  pr = pr_contributors(repo_name, "pulls")
  i = pr_contributors(repo_name, "issues")
  
  contribs = list(set(pr + i))
  return [user_data(c) for c in contribs]

"""
from a user_name string, return a user_name/name dict
"""
def user_data(username):
  name = api_get("users/%s" % username, "name")
  return {"user_name": username, "name": name}
