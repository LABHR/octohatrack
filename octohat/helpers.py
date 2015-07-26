import os
import sys

from connection import Connection, Pager
from exceptions import ResponseError

token = os.environ.get("GITHUB_TOKEN")
conn = Connection(token)
  
def unique(array): 
  seen = set()
  seen_add = seen.add
  return [ x for x in array if not (x in seen or seen_add(x))]

def flatten(array):
  return [item for sublist in array for item in sublist]

def get_code_contributors(repo_name): 
  progress("Collecting contributors")
  users = []
  pager = Pager(conn, "/repos/%s/contributors" % repo_name, params={}, max_pages=0)
  for response in pager:
      progress_advance()
      for entry in response.json():
          users.append(entry["login"])
  progress_complete()
  return unique(users)

def get_code_commentors(repo_name, limit):
  progress("Collecting commentors")
  pri_count = get_pri_count(repo_name)

  if limit == 0:
     minimum = 1
  else: 
    minimum = max(1, pri_count - limit)

  users = []
  for index in range(minimum, pri_count):
      users.append(get_users("/repos/%s/pulls/%d/comments" % (repo_name, index)))
      users.append(get_users("/repos/%s/issues/%d/comments" % (repo_name, index)))
  progress_complete()

  return unique(flatten(users))


def get_data(uri):
    resp = conn.send("GET", uri)
    return resp.json()


def get_pri_count(repo_name):
    prs = get_data("/repos/%s/pulls?state=all" % repo_name)
    pr_count = prs[0]["number"]

    issues = get_data("/repos/%s/issues?state=all" % repo_name)
    issue_count = issues[0]["number"]

    return max(pr_count, issue_count)


def get_users(uri):
    users = []
    try:
        pager = Pager(conn, uri, params={}, max_pages=0)
        for response in pager:
            progress_advance()
            for entry in response.json():
                users.append((entry["user"]["login"], "%s&s=128" % entry["user"]["avatar_url"]))
    except ResponseError, e:
        pass

    return users

def repo_exists(repo_name):
    try:
        repo = conn.send("GET", "/repos/%s" % repo_name)
        return True 
    except ResponseError, e:
        return False

def progress(message):
    sys.stdout.write("%s..." % message)
    sys.stdout.flush()

def progress_advance():
    sys.stdout.write(".")
    sys.stdout.flush()

def progress_complete():
    sys.stdout.write("\n")
