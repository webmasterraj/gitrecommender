import os
from github import Github

MAX_REPOS = int(os.environ['GIT_MAX_REPOS'])
MAX_USERS = int(os.environ['GIT_MAX_USERS'])

username = os.environ['GIT_USER']
password = os.environ['GIT_PW']
token = os.environ['GIT_TOKEN']
PER_PAGE = os.environ['GIT_PER_PAGE'] # Setting per_page to max 100

g = Github(token, per_page=PER_PAGE)
