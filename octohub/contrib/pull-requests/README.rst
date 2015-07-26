OctoHub Contrib: List all open pull requests
============================================

When you have just a few repositories, tracking pull requests is a simple task,
and you probably don't even think of it as such. But, this changes when you
have to track pull requests across user accounts and organizations, with an
ever growing amount of repositories.

For example, the `turnkeylinux-apps`_ organization has over 100 repositories,
not to mention the ever growing repo count in the `turnkeylinux`_ organization
and personal accounts. Getting a high level overview of open pull requests is
impractical to do manual, so this command line interface was born.

Usage
-----

::

    Syntax: list.py [-options] owner[/repo]
    OctoHub: List all open pull requests for a given owner[/repo]

    Arguments:
        owner[/repo]                owner := github organization or username
                                    repo  := if not set all repos will be queried

    Options:
        -n --noauth                 Perform actions as an anonymous user

    Environment:
        OCTOHUB_TOKEN               GitHub personal access token
        OCTOHUB_LOGLEVEL            Log level debugging sent to stderr


.. _turnkeylinux: https://github.com/turnkeylinux
.. _turnkeylinux-apps: https://github.com/turnkeylinux-apps

