OctoHub Contrib: Gist CLI
=========================

``gist`` is a command line interface for uploading and listing `GitHub Gists`_.

Privacy first
-------------

The interface is prioritized for privacy and aims to eliminate *oops! that
should not be public* moments:

* Requires authentication token by default (anonymous gists can only be deleted
  via a `support request`_).
* All gists are created as ``secret`` by default.

Setup
-----

Once OctoHub is installed, add ``gist`` to your path::

    cd octohub
    ln -s $(pwd)/contrib/gist/gist.py $HOME/bin/gist

Usage
-----

::

    Syntax: gist [-options] [file...fileN]
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


.. _GitHub Gists: https://gist.github.com/
.. _support request: https://help.github.com/articles/cannot-delete-an-anonymous-gist

