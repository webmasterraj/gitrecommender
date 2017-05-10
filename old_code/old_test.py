from github import Github
import json
import git_details

g = git_details.g

for repo in repos:
    repo = g.get_repo(TEST_REPO)
    stargazers = repo.get_stargazers()
    if verbose:
        print repo.stargazers_count, 'stargazers'

users_dict = {}
for user in stargazers:
    print 'Analyzing', user.login
    params = {'sort': 'updated', 'direction': 'desc'}
    starred_repos = user.get_starred(params=params)
#    print 'Got starred_repos object.', starred_repos.totalCount, 'repos'
    users_dict[user.login] = []
    for i, s in enumerate(starred_repos):
        users_dict[user.login].append({'name': s.name, 'id': s.id})
        print '\t', i, s.name
        if i > git_details.MAX_REPOS:
            print 'Too many repos...breaking'
            break
    print len(users_dict[user.login]), 'total starred repos' 
    print g.rate_limiting[0], 'requests remaining.', '\n'

with open('testData.json', 'w') as f:
    f.write(json.dumps(users_dict))

