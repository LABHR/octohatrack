OctoHub: Low level Python and CLI interface to GitHub
=====================================================

OctoHub is a Python package that provides a low level interface to the
full GitHub v3 API:

* `Activity`_
* `Gists`_
* `Git Data`_
* `Issues`_
* `Orgs`_
* `Pull Requests`_
* `Repositories`_
* `Users`_
* `Search`_

OctoHub was developed out of a need to have a one-to-one interface to
the GitHub API based on the excellent `online documentation`_, with the
least amount of abstraction.

OctoHub does do its part by parsing raw json responses into Pythonic
attribute dictionaries, as well providing an optional iterative Pager
for handling pagination.

Also included is a command line interface for quick interaction with
GitHub's API.

Speaking of development, it's really easy to leverage the base code to
develop higher level tools, see `contrib`_ for some examples. We also
love pull requests, see our `gitflow`_ for guidelines and walk through.

Installation
------------

::

    $ git clone https://github.com/turnkeylinux/octohub.git
    $ cd octohub
    $ sudo make install

Dependencies
''''''''''''

* `python-requests`_
* `python-simplejson`_

GitHub Token
------------

OctoHub can be used anonymously, but is much more useful when authenticated.
You can create a revokable access token under ``Personal API Tokens`` in your
`account settings`_.

Usage examples (API)
--------------------

::

    >>> from octohub.connection import Connection
    
    >>> conn = Connection(token)
    >>> uri = '/repos/turnkeylinux/tracker/issues'
    >>> response = conn.send('GET', uri, params={'labels': 'bug'})
    >>> for issue in response.parsed:
    ...:    print issue.title

    >>> from octohub.connection import Pager
    >>> pager = Pager(conn, uri)
    >>> for issue in pager:
    ...:    print issue.title

Usage examples (CLI)
--------------------

::

    # A Personal Access Token from your GitHub account:
    #   Account Settings > Applications > Personal Access Tokens > Create new token
    $ export OCTOHUB_TOKEN=d34db33fd34db33fd34db33fd34db33fd34db33f
    $ export OCTOHUB_LOGLEVEL=INFO
    $ octohub GET /repos/turnkeylinux/tracker/issues labels=feature

    INFO [response]: status: 200 OK
    INFO [response]: x-ratelimit-limit: 5000
    INFO [response]: x-ratelimit-remaining: 4997
    [
     {
      "body": "...
      "title": "...
      ...
    
    
    $ cat repo.json
    {
      "name": "test",
      "description": "My test project",
      "homepage": "http://www.turnkeylinux.org",
    }
    $ octohub POST /user/repos --input=repo.json

    INFO [response]: status: 201 Created
    INFO [response]: x-ratelimit-limit: 5000
    INFO [response]: x-ratelimit-remaining: 4996
    ...

For more example usage::

    $ octohub --help


.. _Activity: http://developer.github.com/v3/activity/
.. _Gists: http://developer.github.com/v3/gists/
.. _Git Data: http://developer.github.com/v3/git/
.. _Issues: http://developer.github.com/v3/issues/
.. _Orgs: http://developer.github.com/v3/orgs/
.. _Pull Requests: http://developer.github.com/v3/pulls/
.. _Repositories: http://developer.github.com/v3/repos/
.. _Users: http://developer.github.com/v3/users/
.. _Search: http://developer.github.com/v3/search/
.. _online documentation: http://developer.github.com/v3/
.. _contrib: https://github.com/turnkeylinux/octohub/tree/master/contrib/
.. _gitflow: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst
.. _python-requests: http://python-requests.org/
.. _python-simplejson: https://github.com/simplejson/simplejson/
.. _account settings: https://github.com/settings/applications

