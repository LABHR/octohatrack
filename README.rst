Octohat
=======

It's easy to see your `code contributions`_, but what about everything else?

**Octohat** takes a github repo name, and returns a list of every github user that has interacted with a project, but has not committed code. 

Interactions include: 

* raising or commenting on an issue
* raising or commenting on a pull request
* commenting on a commit

"Let's All Build a Hat Rack" (#LABHR_) is an original concept by `Leslie Hawthorn`_

Usage
-----

`./octohat.py githubuser/repo`

Define an environment variable for `GITHUB_TOKEN` to use an `authentication token`_ (allows for deeper searching)


Dependencies
------------

* octohub_ by turnkeylinux
* requests
* simplejson

To do
-----
 
* parallel processing
* wiki contributions
* include merge-only contributors as non-code contributors(?)

License
-------


This code is `MIT licensed`_.

.. _MIT licensed: https://github.com/bulletproofnetworks/coco/blob/master/LICENSE
.. _#LABHR: https://twitter.com/search?q=%23LABHR&src=typd
.. _Leslie Hawthorn: http://hawthornlandings.org/2015/02/13/a-place-to-hang-your-hat/
.. _code contributions: https://help.github.com/articles/why-are-my-contributions-not-showing-up-on-my-profile/
.. _authentication token: https://help.github.com/articles/creating-an-access-token-for-command-line-use/
.. _octohub: https://github.com/turnkeylinux/octohub
