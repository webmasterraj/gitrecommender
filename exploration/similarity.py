def similar_users_query(user): 
    # Pass user object, return query to get users who starred same things as them
    query = """
    select  subq.user_id
            , sum(1/log(subq.stargazers_count+1)) `score`
            , count(*) `count`
    from
        (select  others.user_id
                , others.starred_repo_id
                , repo.repo_name
                , repo.description
                , repo.last_modified
                , repo.language
                , repo.stargazers_count
                , repo.forks_count
                , repo.from_hacker_news
        from
            (select user_id
                    , starred_repo_id
            from github_user_starred_repos
            where user_id != {0}) others
        join
            (select  starred_repo_id
            from github_user_starred_repos
            where user_id = {0}) usr
        on others.starred_repo_id=usr.starred_repo_id
        join
            (select id
                    , repo_name
                    , description
                    , last_modified
                    , language
                    , stargazers_count
                    , forks_count
                    , from_hacker_news
            from github_repos) repo
        on others.starred_repo_id=repo.id) subq
    group by subq.user_id
    order by 2 desc
    """.format(user.id)
    return query


def similar_repos_query(user): 
    # Pass user object, return query to get users who starred same things as them
    query = """
    select  other_repos.user_id
            , other_repos.starred_repo_id
            , repo.repo_name
            , repo.description
            , repo.last_modified
            , repo.language
            , repo.stargazers_count
            , repo.forks_count
            , repo.from_hacker_news
            , hn.added_at
            , hn.submission_time
            , hn.title
            , hn.url
    from
        (select user_id
                , starred_repo_id
        from github_user_starred_repos
        where user_id != {0}) other_repos
    join
        (select distinct(others.user_id) `user_id`
        from
            (select user_id
                     , starred_repo_id
            from github_user_starred_repos
            where user_id != {0}) others
        join
            (select starred_repo_id
            from github_user_starred_repos
            where user_id = {0}) usr
        on others.starred_repo_id = usr.starred_repo_id) others
    on other_repos.user_id=others.user_id
    join
         (select id
            , repo_name
            , description
            , last_modified
            , language
            , stargazers_count
            , forks_count
            , from_hacker_news
        from github_repos) repo
    on other_repos.starred_repo_id=repo.id
    join
        (select added_at
                , submission_time
                , title
                , url
                , github_repo_name
        from hacker_news) hn
    on repo.repo_name = hn.github_repo_name
    """.format(user.id)
    return query
