#!/usr/bin/env python

import os
import getopt
import sys

from octohub.connection import Connection, Pager
from octohub.exceptions import ResponseError

token = os.environ.get("GITHUB_TOKEN")
conn = Connection(token)

if len(sys.argv) == 1:
    print "Usage: ./octohat.py githubuser/repo"
    sys.exit(1)

repo_name = sys.argv[1]


def get_repo_uri(uri_ending):
    return "/repos/%s/%s" % (repo_name, uri_ending)


def get_data(uri):
    resp = conn.send("GET", get_repo_uri(uri))
    return resp.json()


def get_pri_count():
    prs = get_data("pulls?state=all")
    pr_count = prs[0]["number"]

    issues = get_data("issues?state=all")
    issue_count = issues[0]["number"]

    return max(pr_count, issue_count)


def get_users(uri):
    try:
        pager = Pager(conn, uri, params={}, max_pages=0)
        for response in pager:
            progress_advance()
            for comm in response.json():
                commentor = comm["user"]["login"]
                if commentor not in commentors:
                    commentors.append(commentor)
                    userdata[commentor] = {'user': commentor,
                                           'avatar': "%s&s=128" % comm["user"]["avatar_url"],
                                           'page': comm["user"]["html_url"]}
    except ResponseError, e:
        pass


def test_repo_exists():
    try:
        repo = conn.send("GET", "/repos/%s" % repo_name)
        if repo.json()["has_wiki"] == "true":
            has_wiki = True
    except ResponseError, e:
        print "Repo %s does not exist." % repo_name
        sys.exit(1)


def progress(message):
    sys.stdout.write("%s..." % message)
    sys.stdout.flush()


def progress_advance():
    sys.stdout.write(".")
    sys.stdout.flush()


def progress_complete():
    sys.stdout.write("\n")

userdata = {}
noncode_userdata = {}
contributors = []
non_code = []
commentors = []
has_wiki = False


def main():
    conn = Connection(token)

    test_repo_exists()

    progress("Collecting contributors")
    pager = Pager(conn, get_repo_uri("contributors"), params={}, max_pages=0)
    for response in pager:
        progress_advance()
        for contrib in response.json():
            contributor = contrib["login"]
            if contributor not in contributors:
                contributors.append(contributor)
    progress_complete()

    progress("Collecting commentors")
    pri_count = get_pri_count()
    for index in range(1, pri_count):
        get_users("/repos/%s/pulls/%d/comments" % (repo_name, index))
        get_users("/repos/%s/issues/%d/comments" % (repo_name, index))
    progress_complete()

    for commentor in commentors:
        if commentor not in contributors:
            if commentor not in non_code:
                non_code.append(commentor)
                noncode_userdata[commentor] = userdata[commentor]

    non_code.sort()
    print "\n"
    print "Non-code contributions: %d" % len(non_code)
    print ", ".join(non_code)

    generate = []
    generate.append("<h1>Non-code contributions for %s</h1>" % repo_name)

    for user, data in noncode_userdata.iteritems():
        involves = "https://github.com/%s/issues?q=involves:%s" % (
            repo_name, data["user"])
        generate.append(
            "<a href=\"%s\"><img src=\"%s\" width=\"128\"></a>" % (involves, data["avatar"]))

    html_file = "%s_contrib.html" % repo_name.replace("/", "_")
    f = open(html_file, "w")
    f.write("\n".join(generate))

    print "Generated HTML representation, saved to %s" % html_file
    if has_wiki:
        print "Note: does not include wiki contributions."  # TODO
