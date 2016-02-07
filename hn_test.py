from __future__ import unicode_literals
from hackernews import HackerNews
from mysql import DB

# hn = HackerNews()

def get_new_hn_ids(hn):
    new_hn_ids = hn.new_stories()
    print len(new_hn_ids), "total HN ids"
    return new_hn_ids

def get_hn_items(hn, verbose):
    ids = get_new_hn_ids(hn) 
    items = []
    for i, sid in enumerate(ids):
        items.append(hn.get_item(sid))
        if verbose: 
            print "\t", i, "items"
    print "Got details for", len(items), "HN items" 
    return items

def get_github_items_from_hn(hn, verbose=False):
    all_hn_items = get_hn_items(hn, verbose) 
    hn_github_items = [item for item in all_hn_items
                      if item.url is not None
                      and  'github.com' in item.url
                      and 'gist' not in item.url]
    print(len(hn_github_items), "total github repos", '\n')
    if verbose:
        print '\n\n'.join(item.title+'\n'+item.url for item in hn_github_items)
    return hn_github_items

def add_items_to_database(items):
    db = DB()
#     db.query("SET NAMES utf8;")
    for item in items:
        cmd = """INSERT INTO hacker_news(id, submission_time, title, url) VALUES (%d, '%s', '%s', '%s')""" % (
                item.item_id,
                item.submission_time.strftime("%Y-%m-%d %H:%M"),
                item.title.replace("'", "''"),
                item.url
                )
        print cmd
        db.query(cmd)
    db.commit() 
    return True

if __name__=="__main__":
    hn = HackerNews()
    items = get_github_items_from_hn(hn, verbose=True)
    add_items_to_database(items)




# show_hn_ids = hn.show_stories()
# print len(show_hn_ids), "total Show HN ids"
# 
# show_hn_stories = []
# for sid in show_hn_ids:
#     show_hn_stories.append(hn.get_item(sid))
# 
# show_hn_github_repos = [story for story in stories if 'github.com' in story.url]
# print len(show_hn_github_repos), "Show HN stories from github"
# 
# hn_github_repos = [story for story in stories 
#                    if 'github.com' in story.url 
#                    and 'gist' not in story.url]
# 
# print('\n'.join([item.title for item in show_hn_github_repos 
#        if item in hn_github_repos]))



