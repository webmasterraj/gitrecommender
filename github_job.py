from mysql import DB, str_for_mysql, date_for_mysql
from github import Github, GithubException
import git_details
import urlparse
import json
from datetime import datetime
from MySQLdb import MySQLError

def get_hn_repos():
    db = DB()
    last_job_time = db.query("""
                            SELECT max(added_at) 
                            from github_repos 
                            where from_hacker_news=1
                            """
                     ).fetchone()[0]  
    last_job_time = None
    if not last_job_time:
        last_job_time = '1970-01-01' 

    hn_repos_raw = db.query("""
                            SELECT github_repo_name 
                            from hacker_news   
                            where added_at > '%s' 
                            """ % last_job_time
                            ).fetchall()   
    hn_repos = list(zip(*hn_repos_raw)[0])
    db.close()
    return hn_repos


def add_repo_to_db(db, repo, from_hacker_news=False):
    hn_flag = 1 if from_hacker_news else 0
    query = """
            INSERT INTO github_repos(
                        added_at,
                        id,
                        repo_name,
                        description,
                        author_id,
                        author_name,
                        created_at,
                        last_modified,
                        language,
                        stargazers_count,
                        forks_count,
                        from_hacker_news)
            VALUES ('%s', %d, '%s', '%s', %d, '%s', '%s', '%s', '%s', %d, %d, %d)
            """ % (
                date_for_mysql(datetime.now()),
                repo.id,
                str_for_mysql(repo.full_name),
                str_for_mysql(repo.description),
                repo.owner.id,
                str_for_mysql(repo.owner.name),
                date_for_mysql(repo.created_at),
                date_for_mysql(repo.updated_at),
                str_for_mysql(repo.language),
                repo.stargazers_count,
                repo.forks_count,
                hn_flag)
    # print '\t' + query
    try:
        db.query(query)
    except MySQLError as err:
        # for primary key collisions
        print "ERROR: ", err 
    else:
        db.commit()
    return True


def get_details_for_repos(repo_names, from_hacker_news=False):
    g = git_details.g
    db = DB()
    for r in repo_names:
        repo = g.get_repo(r)
        try: 
            name = repo.name
        except Exception as err:
            print "ERROR: ", err
        else:
            if repo.id:
                print "\tAdding details for", repo.name
                print "\t\t", repo.description
                print
                add_repo_to_db(db, repo, from_hacker_news) 
    db.close() 
            

if __name__=="__main__":
    repos = get_hn_repos()
    print "Adding details for", len(repos), "repos..."
    get_details_for_repos(repos, from_hacker_news=True)





