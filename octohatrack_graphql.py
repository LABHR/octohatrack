#!/usr/bin/env python
"""
Quick implementation of octhatrack with GraphQL


USAGE

./octohatrack_graphql.py user/repo


LIMITATIONS

Limitations in the github graphql api means that this will only return the: 
    - last 100 issues
        - last 100 comments per issue
    - last 100 pull requests
        - last 100 comments per pull request
    - last 100 commit comments
"""

import requests
import json
import os
import click

GITHUB_API = "https://api.github.com/graphql"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": "token %s" % GITHUB_TOKEN}

graphql_query = """
query ($owner: String!, $name: String!, $history: Int!) {
  repository(owner: $owner, name: $name) {
    issues(last:$history) {
      nodes {
        author { login avatarUrl } 
        comments (last:$history){ nodes {author {login avatarUrl}}}
      }
    }
    pullRequests(last: $history) {
      edges { node {
          author { avatarUrl login }
          comments (last:$history){ nodes {author {login avatarUrl}}}
      }}
    }
    commitComments(last: $history) {
      edges { node { author { login  avatarUrl }}}
    }
  }
}
"""

def reducejson(j):
    """ 
    Not sure if there's a better way to walk the ... interesting result
    """

    authors = []

    for key in j["data"]["repository"]["commitComments"]["edges"]:
            authors.append(key["node"]["author"])

    for key in j["data"]["repository"]["issues"]["nodes"]:
            authors.append(key["author"])
            for c in key["comments"]["nodes"]:
                    authors.append(c["author"])
            
    for key in j["data"]["repository"]["pullRequests"]["edges"]:
            authors.append(key["node"]["author"])
            for c in key["node"]["comments"]["nodes"]:
                    authors.append(c["author"])

    unique = list({v['login']:v for v in authors if v is not None}.values())
    return unique


@click.command()
@click.argument('repo')
def main(repo):
    owner, name = repo.split("/")
    variables = { "owner": owner, "name": name, "history":100}
    result = requests.post(GITHUB_API, json.dumps({"query": graphql_query, "variables": variables}), headers=HEADERS)

    authors = reducejson(result.json())
    for a in authors:
            print(a)

    print(len(authors))


if __name__ == '__main__':
    main()
