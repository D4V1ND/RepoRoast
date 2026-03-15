import requests
import os
import shutil
from git import Repo


def fetch_repo_contents(repo_url): 
    api_url = repo_url.replace("github.com", "api.github.com/repos")
    response = requests.get(api_url)
    return response.json()

