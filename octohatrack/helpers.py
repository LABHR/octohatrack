import os
import sys
import atexit
import json
from .connection import Connection, Pager
from .exceptions import ResponseError
from functools import wraps

if "--no-cache" not in sys.argv:
  # Always run on start import
  cache_file = "cache_file.json"
  cache = {}

  if os.path.isfile(cache_file):
    with open(cache_file, "r") as f:
      try:
        cache = json.load(f)
      except ValueError:
        pass

  # Always run on exit
  def save_cache():
    with open(cache_file, 'w') as f:
      json.dump(cache, f)

  atexit.register(save_cache)

  def memoise(wrapped):

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
      key = args[0]
      if key not in cache:
        cache[key] = wrapped(*args, **kwargs)
      return cache[key]

    return wrapper

else:
  # Disable memoisation, force all calls to happen regardless
  def memoise(wrapped):

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
      return wrapped(*args, **kwargs)

    return wrapper

token = os.environ.get("GITHUB_TOKEN")
debug = os.environ.get("DEBUG")


if token is None:
  print("Warning: No GITHUB_TOKEN found - Unauthenticated "
        "requests are rate limited to 60 requests per hour.")
else:
  if debug:
    print("GITHUB_TOKEN found of length %d" % len(token))

conn = Connection(token)


def unique(array):
  array = [x for x in array if x is not None]
  return list({v['user_name']: v for v in array}.values())


def flatten(array):
  return [item for sublist in array for item in sublist]


@memoise
def get_paged_json(uri):
  json = []
  try:
    pager = Pager(conn, uri, params={}, max_pages=0)
    for response in pager:
      progress_advance()
      json += response.json()
  except ResponseError:
    pass

  return json

#@memoise
def get_page_int_json(uri):
   json = []
   page = 1
   while True:
      progress_advance()
      response = get_data("%s?page=%d" % (uri, page))
      if len(response) == 0:
         break
      else:
         page = page + 1
         json += response
   return json


def get_code_contributors(repo_name):
  progress("Collecting contributors")
  users = []
  response = get_page_int_json("/repos/%s/contributors" % repo_name)
  for entry in response:
    users.append(get_user_data(entry))
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
  for index in range(minimum, pri_count + 1):
    users.append(get_user("/repos/%s/pulls/%d" % (repo_name, index)))
    users.append(get_user("/repos/%s/issues/%d" % (repo_name, index)))

    for entry in get_paged_json("/repos/%s/pulls/%d/comments" %
                                (repo_name, index)):
      users.append(get_user_data(entry))

    for entry in get_paged_json("/repos/%s/issues/%d/comments" %
                                (repo_name, index)):
      users.append(get_user_data(entry))

  progress_complete()

  return unique(users)


@memoise
def get_data(uri):
  try:
    resp = conn.send("GET", uri)
    return resp.json()
  except ResponseError:
    return None


def get_pri_count(repo_name):
  prs = get_data("/repos/%s/pulls?state=all" % repo_name)
  issues = get_data("/repos/%s/issues?state=all" % repo_name)

  if not prs:
    pr_count = 0
  else:
    pr_count = prs[0]["number"]

  if not issues:
    issue_count = 0
  else:
    issue_count = issues[0]["number"]

  return max(pr_count, issue_count)


def get_user_data(entry):
  if "user" in entry.keys():
    return {"user_name": entry["user"]["login"],
            "avatar": "%s&s=128" % entry["user"]["avatar_url"],
            "name": get_user_name(entry["user"]["login"])}
  else:
    return {"user_name": entry["login"],
            "avatar": "%s&s=128" % entry["avatar_url"],
            "name": get_user_name(entry["login"])}


@memoise
def get_user(uri):
  progress_advance()
  entry = get_data(uri)
  if entry is not None:
    return get_user_data(entry)


@memoise
def repo_exists(repo_name):
  try:
    conn.send("GET", "/repos/%s" % repo_name)
    return True
  except ResponseError:
    return False


def progress(message):
  sys.stdout.write("%s..." % message)
  sys.stdout.flush()


def progress_advance():
  sys.stdout.write(".")
  sys.stdout.flush()


def progress_complete():
  sys.stdout.write("\n")


def get_user_name(login):
  user = get_data("/users/%s" % login)
  if user["name"] is None:
    user["name"] = login
  return user["name"]

def consolidate(contributors, commentors):
  non_code_contributors = []
  for user in commentors:
    user_name, avatar, name = user
    if user not in contributors:
        non_code_contributors.append(user)

  return non_code_contributors

def display_users(user_list, title, array=False): 
  print("\n%s: %d" % (title, len(user_list)))
  if array: 
    print("\n".join(user_list))
  else:
    for user in sorted(user_list,  key=lambda k: k['user_name'].lower()):
      if user["name"] != user["user_name"]:
        print("%s (%s)" % (user["user_name"], user['name']))
      else:
        print(user["user_name"])
    
