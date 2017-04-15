#############################################################
#
#                         WARNING
#
#   This module is extremely experimental.
#
#   May contain traces of: 
#    * using the GitHub API to pull content of a repo
#    * string parsing
#    * gluten
#    
#############################################################

import base64
import re
import hashlib
from .api_helpers import *


def get_contributors_file(repo_name):

    response = get_json("repos/%s/contents/CONTRIBUTORS" % repo_name)


    if response is None:
        print("No CONTRIBUTORS file")
        return []

    if "message" in response.keys():
        print(response)
        print("No CONTRIBUTORS file")
        return []

    results = []

    content = base64.b64decode(response["content"]).decode("utf-8", "ignore")

    for line in content.splitlines():
        if not line.startswith("#"):
            if line.strip() is not "":
                if "<" in line:
                    name, alias = line.strip(">").split("<")
                    if ":" in alias:
                        service, user_name = alias.split(":@")
                        if service == "twitter":
                            user_name += " (twitter)"
                    elif "@" in alias:
                        user_name = alias
                    else:
                        log.debug("Invalid contributor line type: %s. Returning plain" % line)
                    
                    results.append({'name': name.strip(), 'user_name': user_name})

    return results

