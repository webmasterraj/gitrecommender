from __future__ import unicode_literals
import argparse
import urlparse
from datetime import datetime
from MySQLdb import MySQLError
import hackernews 
from mysql import DB, str_for_mysql, date_for_mysql

# hn = HackerNews()

def get_new_hn_ids(hn):
    new_hn_ids = hn.new_stories()
    print len(new_hn_ids), "total HN ids"
    return new_hn_ids

def get_hn_items(hn, verbose):
    ids = get_new_hn_ids(hn) 
    items = []
    for i, sid in enumerate(ids):
        try:
            items.append(hn.get_item(sid))
        except hackernews.HTTPError as err:
            print 'ERROR:', err 
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
    # if verbose:
#    for item in hn_github_items:
#           print item.title
#           print item.url 
#           print '\n\n'
    return hn_github_items

def add_items_to_database(items, verbose):
    db = DB()
#     db.query("SET NAMES utf8;")
    for item in items:
        url_path = urlparse.urlparse(item.url).path[1:]
        url_path_groups = url_path.split('/')
        github_repo_path = '/'.join(url_path_groups[:2])
        cmd = """
                INSERT INTO hacker_news(id, 
                                        added_at,
                                        submission_time,
                                        title,
                                        url,
                                        github_repo_name) 
                VALUES (%d, '%s', '%s', '%s', '%s', '%s')
              """ % (
                item.item_id,
                date_for_mysql(datetime.now()),
                date_for_mysql(item.submission_time),
                str_for_mysql(item.title),
                str_for_mysql(item.url),
                str_for_mysql(github_repo_path)
                )
        if verbose:
            print cmd
#        db.query(cmd)
        try:
            db.query(cmd)
        except MySQLError as err:
            print "ERROR:", err
            db.conn.rollback()
        else:
            db.commit() 
    return True

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", 
                        help="Verbose output",
                        action="store_true")
    args = parser.parse_args()
    verbose = True if args.verbose else False
    return verbose

if __name__=="__main__":
    hn = hackernews.HackerNews()
    verbose = arg_parser()
    items = get_github_items_from_hn(hn, verbose)
    add_items_to_database(items, verbose)


