#!/usr/bin/env python

import requests
import os
from .memoise import *

API = "https://api.github.com/"
USER_LOGIN = "user--login"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

if GITHUB_TOKEN:
  print("GITHUB_TOKEN in use")
else:
  print("NO GITHUB_TOKEN")

HEADERS = {"Authorization": "token %s" % GITHUB_TOKEN}

"""
Handle headers and json for us :3
"""
def get_json(uri):
  response = requests.get(API + uri, headers=HEADERS)
  return response.json()

"""
For a GitHub URI, walk all the pages until there's no more content
"""
@memoise
def api_walk(uri, per_page = 100, key = "login"): 
  page = 1
  result = []

  while True: 
    response = get_json(uri + "?page=%d&per_page=%d" % (page, per_page))
    if len(response) == 0:
      break
    else: 
      page += 1
      for r in response:
        if key == USER_LOGIN:
          result.append(user_login(r))
        else:
          result.append(r[key])

  return result

"""
Because dict nesting, this is a special function to return the user_login out of a dict
"""
def user_login(r):
    if "user" in r:
      if "login" in r["user"]:
        return r["user"]["login"]
    return None

"""
Simple API endpoint get, return only the keys we care about
"""
@memoise
def api_get(uri, key=None):
    print(uri)
    response = get_json(uri)

    if response:
      if type(response) == list:
        r = response[0]
      elif type(response) == dict:
        r = response

      if type(r) == dict:
        # Special nested value we care about
        if key == USER_LOGIN:
          return user_login(r)
        if key in r:
          return r[key]

