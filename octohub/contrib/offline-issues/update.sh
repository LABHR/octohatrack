#!/bin/bash -e
# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of octohub/contrib
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

fatal() {
    echo "fatal: $@" 1>&2
    exit 1
}

ISSUES_URI=/repos/turnkeylinux/tracker/issues
ISSUES_DIR=$(dirname $(readlink -f $0))

which octohub >/dev/null || fatal "octohub not in path"
which octohub-parse-issues >/dev/null || fatal "octohub-parse-issues not in path"

mkdir -p $ISSUES_DIR/.raw
octohub --max-pages=0 GET $ISSUES_URI state=open > $ISSUES_DIR/.raw/open.json
octohub --max-pages=0 GET $ISSUES_URI state=closed > $ISSUES_DIR/.raw/closed.json

octohub-parse-issues $ISSUES_DIR/.raw/open.json .
octohub-parse-issues --noinit $ISSUES_DIR/.raw/closed.json .

if [ -d $ISSUES_DIR/.git ]; then
    cd $ISSUES_DIR
    git add -A .
    git commit -m "autocommit"
fi

