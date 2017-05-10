from mysql import DB, str_for_mysql, date_for_mysql
from github import Github, GithubException
import git_details
import hashlib
from datetime import datetime
from MySQLdb import MySQLError


def repos_to_update():
    db = DB()
    last_job_time = db.query("""
                            SELECT max(added_at) 
                            from github_user_starred_repos
                            """
                     ).fetchone()[0]  
    last_job_time = '2016-02-21'
    repos_raw = db.query("""
                            SELECT id 
                            from github_repos   
                            where added_at > '%s' 
                            """ % last_job_time 
                            ).fetchall() 
    repos = list(zip(*repos_raw)[0]) if repos_raw else []
    db.close()
    return repos


def add_users(repos):
    g = git_details.g
    print "Adding users for %d repos" % len(repos)
    for repo_id in repos:
        repo = g.get_repo(repo_id)
        print "Processing repo:", repo.name 
        add_users_who_starred_repo(repo)
        print


def add_users_who_starred_repo(repo):
    db = DB()
    stargazers = repo.get_stargazers_with_dates()
    for i, s in enumerate(stargazers): 
        print "\tAdding user {0}: {1}".format(i, s.user.login)
        insert_user_repo_relationship(db, repo, s.user, s.starred_at)
        insert_user(db, s.user)
        add_users_other_stars(db, s.user)
        if i > git_details.MAX_USERS:
            print "**WARNING: More than %d users" % git_details.MAX_REPOS
            break
    print "\t\tAdded {0} starred repos".format(i)
    db.close()


def add_users_other_stars(db, user):
    stars = user.get_starred()
    print "\t\tAdding user's other repos"
    for i, starred_repo in enumerate(stars):
        insert_user_repo_relationship(db, starred_repo, user, None)
        # print "\t\t{0} starred repos".format(i)
        if i > git_details.MAX_REPOS: 
            print "**WARNING: MORE than %d starred repos" % git_details.MAX_REPOS
            break
    print "\t\tAdded {0} starred repos".format(i)


def insert_user_repo_relationship(db, repo, user, date):
    hash_object = hashlib.md5(user.login+repo.full_name)
    query = """
            INSERT INTO github_user_starred_repos(
                        record_id,
                        added_at,
                        user_id,
                        starred_repo_id,
                        starred_at)
            VALUES ('{0}', '{1}', {2}, {3}, '{4}')
            """.format(
                hash_object.hexdigest(),
                date_for_mysql(datetime.now()),
                user.id,
                repo.id,
                date_for_mysql(date) if date else "NULL")
    try:
        # print "\t\tAdding user_repo_relationship to db"
        # print query
        db.query(query)
    except MySQLError as err:
        print "***ERROR***", err
        return False
    else:
        db.commit() 
    return True 

           
def insert_user(db, user):
    query = """
            INSERT INTO github_users(
                        added_at,
                        id,
                        username,
                        full_name,
                        email,
                        location,
                        created_at,
                        public_repos_count,
                        private_repos_count,
                        followers_count,
                        contributions_count)
            VALUES ('%s', %d, '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d)
            """ % (
                date_for_mysql(datetime.now()),
                user.id,
                str_for_mysql(user.login),
                str_for_mysql(user.name),
                str_for_mysql(user.email),
                str_for_mysql(user.location),
                date_for_mysql(user.created_at),
                user.public_repos if user.public_repos else 0,
                user.total_private_repos if user.total_private_repos else 0,
                user.followers if user.followers else 0,
                user.contributions if user.contributions else 0) 
    try:
        # print "\t\tAdding user to db"
        # print query
        db.query(query)
    except MySQLError as err:
        print "***ERROR***:", err
        return False
    else:
        db.commit() 
    return True 


if __name__=="__main__":
    repos = repos_to_update()
    add_users(repos)

