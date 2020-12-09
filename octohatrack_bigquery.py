"""
Proof of concept using BigQuery to replace API crawling and wiki cloning. 

⚠️ Each call to the githubarchive processes ~150GB of data. The free limit is 1TB/month.

# From https://cloud.google.com/bigquery/docs/reference/libraries#command-line
$ gcloud iam service-accounts create bigquery-sa
$ gcloud projects add-iam-policy-binding glasnt-octohatrack --member="serviceAccount:bigquery-sa@glasnt-octohatrack.iam.gserviceaccount.com" --role="roles/owner"
$ gcloud iam service-accounts keys create ~/bigquery-sa.json --iam-account=bigquery-sa@glasnt-octohatrack.iam.gserviceaccount.com
$ export GOOGLE_APPLICATION_CREDENTIALS="/home/glasnt/bigquery-sa.json"

BigQuery event cache includes "GollumEvent", which is wiki events.
requires: 
 pip install google-cloud-bigquery PyGithub

Note: 
 * includes old/dead usernames in githubarchive, which may cause duplicates
 * if your repo has been renamed, include it in "OLD_REPO" (if not, leave this string empty.)
"""

from google.cloud import bigquery
from octohatrack.contributors_file import contributors_file as contrib_file
from octohatrack.helpers import progress_message
from typing import List
from github import Github


REPO = "LABHR/octohatrack"
OLD_REPO = "glasnt/octohat"
YEARMONTH = "*"  # "*" for all, or use a YYYYMM format for limited results (e.g. 201810)


def api_contributors() -> List[str]:
    repo = Github().get_repo(REPO)
    contribs = repo.get_contributors()
    return [c.login for c in contribs]


def pri_contributors() -> List[str]:
    client = bigquery.Client()

    if OLD_REPO:
        repo_search = f'repo.name in ("{OLD_REPO}", "{REPO}")'
    else:
        repo_search = f'repo.name = "{REPO}"'

    query = f"""
        SELECT
            actor.login
        FROM
            `githubarchive.month.{YEARMONTH}`
        WHERE {repo_search}
        AND type NOT IN ("WatchEvent", "ForkEvent")
        GROUP BY 
        actor.login
        ORDER BY
        LOWER(actor.login) ASC
    """
    query_job = client.query(query)  # Make an API request.

    contribs = []
    for row in query_job:
        contribs.append(row[0])

    return contribs


def file_contributors() -> List[str]:
    return [c["user_name"] for c in contrib_file(REPO)]


def main():
    progress_message("Processing")
    api = api_contributors()
    pri = pri_contributors()
    fil = file_contributors()

    print("\nContributors:\n")
    contribs = sorted(list(set(api + pri + fil)), key=str.casefold)
    print("\n".join(contribs), "\n")

    print(" ", str(len(api)).rjust(5), f"GitHub 'contributors'")
    print(
        "+", str(len(set(pri) - set(api))).rjust(5), f"new contributors seen in events"
    )
    print("+", str(len(fil)).rjust(5), f"contributors named in credit file")
    print("=", str(len(contribs)).rjust(5), f"actual contributors to {REPO}", OLD_REPO)


if __name__ == "__main__":
    main()