Octohat
=======


.. image:: https://travis-ci.org/glasnt/octohat.svg?branch=master
    :target: https://travis-ci.org/glasnt/octohat
    
It's easy to see your direct `code contributions`_ on GitHub, but what about everything else?

**Octohat** takes a github repo name, and returns a list of every github user that has interacted with a project, but has not committed code. 

Interactions include: 

* raising or commenting on an issue
* raising or commenting on a pull request
* commenting on a commit

"Let's All Build a Hat Rack" (`#LABHR`_) is an original concept by `Leslie Hawthorn`_

Usage
-----
.. code-block:: 

    octohat [-h] [-g] [-l LIMIT] repo_name

    positional arguments:
      repo_name                githubuser/repo

    optional arguments:
      -g, --generate-html      Generate output as HTML
      -l LIMIT, --limit LIMIT  Limit to the last x Issues/Pull Requests


Define an environment variable for "GITHUB_TOKEN" to use an `authentication token`_ (allows for deeper searching)


Dependencies
------------

* requests (may require "pip install pyopenssl ndg-httpsclient pyasn1" (source_))
* simplejson (may require "apt-get install python-dev python-simplejson", as does not install from pip nicely)
* octohub_ (distributed inline under GPLv3 license)

To do
-----
 
* parallel processing
* wiki contributions
* include merge-only contributors as non-code contributors(?)
* work out why simplejson isn't being very simple to install

License
-------

Octohat is distributed under the `MIT license`_.

Octohub is Copyright (c) 2013 Alon Swartz (turnkeylinux), used under the GPLv3 license. 

.. _MIT license: https://github.com/glasnt/octohat/blob/master/LICENSE
.. _#LABHR: https://twitter.com/search?q=%23LABHR&src=typd
.. _Leslie Hawthorn: http://hawthornlandings.org/2015/02/13/a-place-to-hang-your-hat/
.. _code contributions: https://help.github.com/articles/why-are-my-contributions-not-showing-up-on-my-profile/
.. _authentication token: https://help.github.com/articles/creating-an-access-token-for-command-line-use/
.. _octohub: https://github.com/turnkeylinux/octohub
.. _source: http://stackoverflow.com/a/29202163/124019
