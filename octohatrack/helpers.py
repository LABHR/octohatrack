import os
import sys
import atexit
import json
from .connection import Connection, Pager
from .exceptions import ResponseError
from functools import wraps


## System Startup tasks

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

# Walk a json endpoint where pagination is link driven
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

# Walk a json endpoint where pagination is integer driven
@memoise
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

# Get the users defined by GitHub as contributors
def get_api_contributors(repo_name):
  progress("Collecting API contributors")
  users = []
  response = get_page_int_json("/repos/%s/contributors" % repo_name)
  for entry in response:
    user = get_user_data(entry)
    if user is not None:
      users.append(user)
  progress_complete()

  return users

# Get all Pull Requests and Issues (PRI) users
def get_pri_contributors(repo_name, limit):
  progress("Collecting all repo contributors")

  pri_count = get_pri_count(repo_name)
  if limit == 0:
    minimum = 1
  else:
    minimum = max(1, pri_count - limit)

  users = []
  for index in range(minimum, pri_count + 1):
    user = get_user("/repos/%s/pulls/%d" % (repo_name, index))
    if user is not None:
      users.append(user)

    user = get_user("/repos/%s/issues/%d" % (repo_name, index))
    if user is not None:
      users.append(user)

    for entry in get_paged_json("/repos/%s/pulls/%d/comments" %
                                (repo_name, index)):
        user = get_user_data(entry)
        if user is not None:
          users.append(user)

    for entry in get_paged_json("/repos/%s/issues/%d/comments" %
                                (repo_name, index)):
        user = get_user_data(entry)
        if user is not None:
          users.append(user)

  progress_complete()

  return users

def unique_users(a, b, w, d):
  f = a + b + w + d

  array = [x for x in f if x is not None]
  p = list({v['user_name']: v for v in array}.values())

  # Special case: wiki contributions
  # Remove item if the display name for a wiki contributor matches another contribution
  # (author display names and github user names don't match)
  f = [x["user_name"] for x in (a + b + d) if x is not None]

  for x in w:
    if x["user_name"] in f:
        if x["user_name"] in p:
            p.remove(x)

  return p


@memoise
def get_data(uri):
  try:
    resp = conn.send("GET", uri)
    return resp.json()
  except ResponseError:
    return None

# Get the number of Pull Requests and Issues
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
    if entry['user'] is None:
      return None
    return {"user_name": entry["user"]["login"],
            "name": get_user_name(entry["user"]["login"])}
  else:
    return {"user_name": entry["login"],
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


def display_results(repo_name, api_contributors, all_contributors):
    print("")

    print("GitHub Contributors:")
    display_users(api_contributors)
    print("")
    
    print("All Contributors:")
    display_users(all_contributors)
    print("")

    print("Repo: %s" % repo_name)
    print("GitHub Contributors: %s" % len(api_contributors))
    print("All Contributors: %s" % len(all_contributors))

def display_users(user_list, array=False): 
  if array: 
    print("\n".join(user_list))
  else:
    for user in sorted(user_list,  key=lambda k: k['user_name'].lower()):
      if user["name"] != user["user_name"]:
        print("%s (%s)" % (user["user_name"], user['name']))
      else:
        print(user["user_name"])
    
def get_user_name(login):
  user = get_data("/users/%s" % login)
  if user is None:
    # Possible ghost user. Return the only data we know; the login
    return login
  if user["name"] is None:
    user["name"] = login
  return user["name"]

