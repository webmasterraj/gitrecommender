import os
from github import Github

MAX_REPOS = int(os.environ['GIT_MAX_REPOS'])
MAX_USERS = int(os.environ['GIT_MAX_USERS'])

username = os.environ['GIT_USER']
password = os.environ['GIT_PW']
token = os.environ['GIT_TOKEN']

g = Github(token, per_page=100)
