#!/usr/bin/env python
# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of octohub/contrib.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

"""
OctoHub: List all open pull requests for a given owner[/repo]

Arguments:
    owner[/repo]                owner := github organization or username
                                repo  := if not set all repos will be queried

Options:
    -n --noauth                 Perform actions as an anonymous user

Environment:
    OCTOHUB_TOKEN               GitHub personal access token
    OCTOHUB_LOGLEVEL            Log level debugging sent to stderr

"""

import os
import sys
import getopt

from octohub.connection import Connection, Pager
from octohub.exceptions import ResponseError

def fatal(e):
    print >> sys.stderr, 'Error: ' + str(e)
    sys.exit(1)

def usage(e=None):
    if e:
        print >> sys.stderr, 'Error: ' + str(e)

    cmd = os.path.basename(sys.argv[0])
    print >> sys.stderr, 'Syntax: %s [-options] owner[/repo]' % cmd
    print >> sys.stderr, __doc__.lstrip()

    sys.exit(1)

def get_repos(conn, uri, issues_min=1, forks_min=1):
    repos = []
    pager = Pager(conn, uri, params={}, max_pages=0)
    for response in pager:
        for repo in response.parsed:
            if int(repo.open_issues_count) >= issues_min and \
               int(repo.forks_count) >= forks_min:
                repos.append(repo.name)

    return repos

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'hn', ['help', 'noauth'])
    except getopt.GetoptError, e:
        usage(e)

    auth = True
    repos = []
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

        elif opt in ('-n', '--noauth'):
            auth = False

    token = os.environ.get('OCTOHUB_TOKEN', None)
    if not token and auth:
        fatal('OCTOHUB_TOKEN is required, override with --noauth')

    if not auth:
        token = None

    if not len(args) == 1:
        usage()

    conn = Connection(token)

    if '/' in args[0]:
        owner = args[0].split('/')[0]
        repos.append(args[0].split('/')[1])
    else:
        owner = args[0]
        try:
            repos = get_repos(conn, '/orgs/%s/repos' % owner)
        except ResponseError, e:
            repos = get_repos(conn, '/users/%s/repos' % owner)

    for repo in repos:
        response = conn.send('GET', '/repos/%s/%s/pulls' % (owner, repo))
        if response.parsed:
            print '%s/%s\n' % (owner, repo)
            for pull in response.parsed:
                print '  [%s] %s' % (pull.head.user.login, pull.title)
                print '  %s' % pull.html_url
                print


if __name__ == '__main__':
   main()
