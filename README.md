# octohatrack

[![image](https://travis-ci.org/LABHR/octohatrack.svg?branch=master)](https://travis-ci.org/labhr/octohatrack) [![image](https://badge.fury.io/py/octohatrack.svg)](http://badge.fury.io/py/octohatrack)

It's easy to see your direct [code contributions](https://help.github.com/articles/why-are-my-contributions-not-showing-up-on-my-profile/)
on GitHub, but what about everything else?

**Octohatrack** takes a github repo name, and returns a list of every
github user that has interacted with a project, but has not committed
code.

Interactions include:

-   raising or commenting on an issue
-   raising or commenting on a pull request
-   commenting on a commit

"Let's All Build a Hat Rack" ([\#LABHR](https://twitter.com/search?q=%23LABHR&src=typd)) is an
original concept by [Leslie Hawthorn](http://hawthornlandings.org/2015/02/13/a-place-to-hang-your-hat/)

Read more about octohatrack:

-   [A tool for tracking non-code GitHub contributions](https://opensource.com/life/15/10/octohatrack-github-non-code-contribution-tracker) on OpenSource.com
-   Talk ["Build a Better Hat Rack: All Contributions Welcome"](https://www.youtube.com/watch?v=wQxFKxbWcFM) from KiwiPyCon (YouTube video)
-   [Read about the project name change](http://glasnt.com/blog/2015/11/21/goodbye-octohat.html)

## Installation

```
pip install octohatrack
```

## Usage

```
usage: octohatrack.py [-h] [-g] [-l LIMIT] [-c] [-n] repo_name

positional arguments:
  repo_name             githubuser/repo

optional arguments:
  -h, --help            show this help message and exit
  -g, --generate-html   Generate output as HTML
  -l LIMIT, --limit LIMIT
                        Limit to the last x Issues/Pull Requests
  -c, --show-contributors
                        Output the code contributors
  -n, --show-names      Show the user's display name

```

Define an environment variable for "GITHUB\_TOKEN" to use an [authentication token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) (allows for deeper searching)

## Run this repo locally

```
git clone https://github.com/labhr/octohatrack
cd octohatrack
python3 octohatrack.py [arguments]
```

## Run octohatrack in a Docker container

```
git clone https://github.com/labhr/octohatrack
cd octohatrack
docker build -t octohatrack .
docker run -e GITHUB_TOKEN octohatrack [arguments]
```


## To do

-   parallel processing
-   wiki contributions
-   include merge-only contributors as non-code contributors

## Code of Conduct

Octohatrack operates under a [Code of
Conduct](https://github.com/labhr/octohatrack/blob/master/code-of-conduct.md).

## License

Octohatrack is distributed under the [MIT license](https://github.com/labhr/octohatrack/blob/master/LICENSE).

Octohub is Copyright (c) 2013 Alon Swartz (turnkeylinux), used inline under the GPLv3 license.

This project is not affiliated with GitHub.
