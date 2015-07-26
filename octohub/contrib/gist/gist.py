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
OctoHub: Gist CLI

Arguments:
    file...fileN                Files to upload (list gists if none specified)

Options:
    -n --noauth                 Perform actions as an anonymous user
    -p --public                 Set gist as public (default is secret)
    -d --description <str>      Set gist description

Environment:
    OCTOHUB_TOKEN               GitHub personal access token
    OCTOHUB_LOGLEVEL            Log level debugging sent to stderr

Examples:
    export OCTOHUB_TOKEN=...    Set authentication token
    gist                        List user gists
    gist a.txt                  Create secret gist with single file
    gist --public a.txt *.py    Create public gist with multiple files

    gist --noauth               List public gists (limited to first page)
    gist --noauth a.txt         Create anonymous secret gist with single file

    octohub DELETE /gists/:id   Delete a gist
"""

import os
import sys
import getopt
import simplejson as json

from octohub.connection import Connection, Pager

def fatal(e):
    print >> sys.stderr, 'Error: ' + str(e)
    sys.exit(1)

def usage(e=None):
    if e:
        print >> sys.stderr, 'Error: ' + str(e)

    cmd = os.path.basename(sys.argv[0])
    print >> sys.stderr, 'Syntax: %s [-options] [file...fileN]' % cmd
    print >> sys.stderr, __doc__.lstrip()

    sys.exit(1)

def render_gist(gist):
    files = ' '.join(gist.files.keys()).encode('ascii', 'ignore').strip()
    visible = 'pub' if gist.public else 'sec'
    return '[%s] %s %s' % (visible, gist.html_url, files)

def get_gists(token, uri):
    max_pages = 0 if token else 1

    conn = Connection(token)
    pager = Pager(conn, uri, params={}, max_pages=max_pages)
    for response in pager:
        for gist in response.parsed:
            yield gist

def create_gist(token, uri, paths, public=False, description=None):
    data = {}

    data['files'] = {}
    for path in paths:
        name = os.path.basename(path)
        content = file(path, 'r').read()
        data['files'][name] = {'content': content}

    if description:
        data['description'] = description

    data['public'] = public

    conn = Connection(token)
    response = conn.send('POST', uri, params={}, data=json.dumps(data))

    return response.parsed

def main():
    try:
        options = ['help', 'noauth', 'public', 'description=']
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'hnpd:', options)
    except getopt.GetoptError, e:
        usage(e)

    auth = True
    public = False
    description = None
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

        elif opt in ('-n', '--noauth'):
            auth = False

        elif opt in ('-p', '--public'):
            public = True

        elif opt in ('-d', '--description'):
            description = val

    token = os.environ.get('OCTOHUB_TOKEN', None)
    if not token and auth:
        fatal('OCTOHUB_TOKEN is required, override with --noauth')

    if not auth:
        token = None

    uri = '/gists'
    paths = args
    for path in paths:
        if not os.path.exists(path):
            fatal('does not exist: %s' % path)

    if len(paths) == 0:
        for gist in get_gists(token, uri):
            print render_gist(gist)
    else:
        gist = create_gist(token, uri, paths, public, description)
        print render_gist(gist)

if __name__ == '__main__':
   main()
