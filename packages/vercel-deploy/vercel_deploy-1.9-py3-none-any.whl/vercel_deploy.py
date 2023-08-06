#!/usr/bin/env python
#!/usr/bin/env python
import os
import sys

import requests
from dotenv import load_dotenv


def get_token():
    load_dotenv()
    GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
    VERCEL_ACCESS_TOKEN = os.getenv("VERCEL_ACCESS_TOKEN")

    if not GITHUB_ACCESS_TOKEN or not VERCEL_ACCESS_TOKEN:
        print("Please set GITHUB_ACCESS_TOKEN and VERCEL_ACCESS_TOKEN in your .env file")
        sys.exit(1)
    return GITHUB_ACCESS_TOKEN, VERCEL_ACCESS_TOKEN


def get_repo_info(github_repo_url):
    GITHUB_ACCESS_TOKEN, VERCEL_ACCESS_TOKEN = get_token()
    github_api_url = "https://api.github.com/repos/" + "/".join(github_repo_url.split("/")[-2:])
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    response = requests.get(github_api_url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_vercel_project_id(vercel_project_name):
    GITHUB_ACCESS_TOKEN, VERCEL_ACCESS_TOKEN = get_token()
    vercel_api_url = "https://api.vercel.com/v8/projects"
    headers = {
        "Authorization": f"Bearer {VERCEL_ACCESS_TOKEN}",
    }
    response = requests.get(vercel_api_url, headers=headers)
    response.raise_for_status()
    projects = response.json()["projects"]

    for project in projects:
        if project["name"] == vercel_project_name:
            return project["id"]

    return None


def create_vercel_project(vercel_project_name, github_repo_info, vercel_team_id=None):
    GITHUB_ACCESS_TOKEN, VERCEL_ACCESS_TOKEN = get_token()
    project_id = get_vercel_project_id(vercel_project_name)

    if project_id:
        print(f"Vercel project already exists: {vercel_project_name}")
        return {"id": project_id}

    vercel_api_url = "https://api.vercel.com/v9/projects"
    headers = {
        "Authorization": f"Bearer {VERCEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "name": vercel_project_name,
        "gitRepository": {
            "type": "github",
            "repo": f"{github_repo_info['owner']['login']}/{github_repo_info['name']}",
        },
    }
    if vercel_team_id:
        vercel_api_url += f"?teamId={vercel_team_id}"
    response = requests.post(vercel_api_url, json=data, headers=headers)
    print("create_vercel_project, response.json()", response.json())
    response.raise_for_status()
    return response.json()


def get_github_repo_id(github_repo_url):
    GITHUB_ACCESS_TOKEN, VERCEL_ACCESS_TOKEN = get_token()
    github_api_url = "https://api.github.com/repos/" + "/".join(github_repo_url.split("/")[-2:])
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    response = requests.get(github_api_url, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


# https://vercel.com/docs/rest-api/endpoints
def deploy_vercel_project(vercel_project_id, github_repo_info, vercel_team_id=None, ref="main"):
    GITHUB_ACCESS_TOKEN, VERCEL_ACCESS_TOKEN = get_token()
    print("vercel_project_id", vercel_project_id)
    print("github_repo_info", github_repo_info)
    vercel_api_url = "https://api.vercel.com/v13/deployments"
    headers = {
        "Authorization": f"Bearer {VERCEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "name": vercel_project_id,
        "target": "production",
        "gitSource": {
            "type": "github",
            "repoId": github_repo_info["id"],
            "ref": ref,
        },
    }
    if vercel_team_id:
        vercel_api_url += f"?teamId={vercel_team_id}"

    response = requests.post(vercel_api_url, json=data, headers=headers)
    print("deploy_vercel_project, response.json()", response.json())
    response.raise_for_status()
    return response.json()


def main(github_repo_url, vercel_project_name, vercel_team_id):
    github_repo_info = get_repo_info(github_repo_url)
    github_repo_id = get_github_repo_id(github_repo_url)
    github_repo_info["id"] = github_repo_id

    vercel_project = create_vercel_project(vercel_project_name, github_repo_info, vercel_team_id)
    vercel_deployment = deploy_vercel_project(vercel_project["id"], github_repo_info, vercel_team_id)
    response = f"Vercel deployment URL: {vercel_deployment['url']}"
    print(response)
    return response


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python deploy_to_vercel.py <github_repo_url> <vercel_project_name> <vercel_team_id>")
        sys.exit(1)

    github_repo_url = sys.argv[1]
    vercel_project_name = sys.argv[2]
    vercel_team_id = sys.argv[3]
    main(github_repo_url, vercel_project_name, vercel_team_id)
