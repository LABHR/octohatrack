from octohatrack.code_contrib import *
from octohatrack.contributors_file import *
from octohatrack.wiki import *

from pprint import pprint


repo_name = "LABHR/octohatrack"

c = []

api_contrib = api_contributors(repo_name)
pprint(api_contrib)

c += api_contrib

contrib = pri_contributors(repo_name)
print(contrib)
print(len(contrib))

c += contrib

f = get_contributors_file(repo_name)
print(f)

c += f

w = get_wiki_contributors(repo_name)

print(w)

c += w

pprint(c)

seen = []

for i in c:
  name = i["name"]
  user = i["user_name"]

  if name not in seen:
    seen.append(name) 
    print("%s (%s)" % (user, name))


  

