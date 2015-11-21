Octohatrack
=======

.. image:: https://travis-ci.org/labhr/octohatrack.svg?branch=master
    :target: https://travis-ci.org/labhr/octohatrack
    
.. image:: https://badge.fury.io/py/octohatrack.svg
    :target: http://badge.fury.io/py/octohatrack
    
    
It's easy to see your direct `code contributions`_ on GitHub, but what about everything else?

**Octohatrack** takes a github repo name, and returns a list of every github user that has interacted with a project, but has not committed code. 

Interactions include: 

* raising or commenting on an issue
* raising or commenting on a pull request
* commenting on a commit

"Let's All Build a Hat Rack" (`#LABHR`_) is an original concept by `Leslie Hawthorn`_

Read more about Octohatrack: 

-  `A tool for tracking non-code GitHub
   contributions <https://opensource.com/life/15/10/octohatrack-github-non-code-contribution-tracker>`__
   on OpenSource.com
-  Talk `"Build a Better Hat Rack: All Contributions
   Welcome" <https://www.youtube.com/watch?v=wQxFKxbWcFM>`__ from
   KiwiPyCon (YouTube video)

Installation
------------
.. code-block:: 

    pip install octohatrack

Usage
-----
.. code-block:: 

    octohatrack [-h] [-g] [-l LIMIT] repo_name

    positional arguments:
      repo_name                githubuser/repo

    optional arguments:
      -g, --generate-html      Generate output as HTML
      -l LIMIT, --limit LIMIT  Limit to the last x Issues/Pull Requests


Define an environment variable for "GITHUB_TOKEN" to use an `authentication token`_ (allows for deeper searching)

Run this repo locally
---------------------

.. code-block::
    git clone https://github.com/labhr/octohatrack
    cd octohatrack
    python3 octohatrack.py [arguments]


To do
-----
 
* parallel processing
* wiki contributions
* include merge-only contributors as non-code contributors


Code of Conduct
---------------

Octohatrack operates under a `Code of Conduct`_.


License
-------

Octohatrack is distributed under the `MIT license`_.

Octohub is Copyright (c) 2013 Alon Swartz (turnkeylinux), used inline under the GPLv3 license. 

.. _MIT license: https://github.com/labhr/octohatrack/blob/master/LICENSE
.. _#LABHR: https://twitter.com/search?q=%23LABHR&src=typd
.. _Leslie Hawthorn: http://hawthornlandings.org/2015/02/13/a-place-to-hang-your-hat/
.. _code contributions: https://help.github.com/articles/why-are-my-contributions-not-showing-up-on-my-profile/
.. _authentication token: https://help.github.com/articles/creating-an-access-token-for-command-line-use/
.. _octohub: https://github.com/turnkeylinux/octohub
.. _source: http://stackoverflow.com/a/29202163/124019
.. _Code of Conduct: https://github.com/labhr/octohatrack/blob/master/code-of-conduct.md
