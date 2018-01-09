#!/usr/bin/env python

import requests
import os
import sys
from .memoise import *
from .helpers import *
import time
import math

API = "https://api.github.com/"
USER_LOGIN = "user--login"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

HEADERS = {"Authorization": "token %s" % GITHUB_TOKEN}


def get_json(uri):
    """
    Handle headers and json for us :3
    """
    response = requests.get(API + uri, headers=HEADERS)

    limit = int(response.headers.get('x-ratelimit-remaining'))
    if limit == 0:
        sys.stdout.write("\n")
        message = "You have run out of GitHub request tokens. "

        if int(response.headers.get('x-ratelimit-limit')) == 60:
            message += "Set a GITHUB_TOKEN to increase your limit to 5000/hour. "

        wait_seconds = (int(response.headers.get(
            'x-ratelimit-reset')) - int(time.time()))
        wait_minutes = math.ceil(wait_seconds / 60)
        message += "Try again in ~%d minutes. " % wait_minutes

        if '--wait-for-reset' in sys.argv:
            progress_message(message.replace('Try ', 'Trying '))
            time.sleep(wait_seconds + 1)
            progress_message('Resuming')
            return get_json(uri)
        else:
            raise ValueError(message)

    progress()
    return response.json()


@memoise
def api_walk(uri, per_page=100, key="login"):
    """
    For a GitHub URI, walk all the pages until there's no more content
    """
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

    return list(set(result))


def user_login(r):
    """
    Because dict nesting, this is a special function to return the user_login out of a dict
    """
    if "user" in r:
        if "login" in r["user"]:
            return r["user"]["login"]
    return None


@memoise
def api_get(uri, key=None):
    """
    Simple API endpoint get, return only the keys we care about
    """
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
