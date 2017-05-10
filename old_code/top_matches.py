from __future__ import division
from collections import Counter
import json
import git_details

g = git_details.g

users_dict = json.loads(open('testData.json', 'r').read())
    
all_repos = []
for user in users_dict:
    for r in users_dict[user]:
        all_repos.append((r['name'], r['id']))

summary = Counter(all_repos)
top_matches = [{'name': s[0][0], 'id': s[0][1], 'count': s[1]} for s in summary.most_common()[:100]]

for match in top_matches:
    match_repo = g.get_repo(match['id'])
    print 'Got details for', match['name']
    match['total_stars'] = match_repo.stargazers_count   
    match['normalized_count'] = match['count'] / match['total_stars']

top_matches = sorted(top_matches, key=lambda x: x['normalized_count'], reverse=True)
print top_matches
