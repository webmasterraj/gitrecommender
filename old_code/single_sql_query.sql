query = """
        select similar_repos.starred_repo_id
                , similar_repos.repo_name
                , similar_repos.description
                , similar_repos.last_modified
                , similar_repos.language
                , similar_repos.stargazers_count
                , similar_repos.forks_count
                , similar_repos.from_hacker_news
                , similar_repos.hn_added_at
                , similar_repos.hn_submission_time
                , similar_repos.hn_title
                , similar_repos.hn_url
                , sum(similar_users.score) `score`
        from

            (select  other_repos.user_id
                    , other_repos.starred_repo_id
                    , repo.repo_name
                    , repo.description
                    , repo.last_modified
                    , repo.language
                    , repo.stargazers_count
                    , repo.forks_count
                    , repo.from_hacker_news
                    , hn.added_at `hn_added_at`
                    , hn.submission_time `hn_submission_time`
                    , hn.title `hn_title`
                    , hn.url `hn_url`
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
            on repo.repo_name = hn.github_repo_name) similar_repos

        join

            (select  subq.user_id
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
            order by 2 desc) similar_users
        on similar_users.user_id=similar_repos.user_id

        group by similar_repos.starred_repo_id
                , similar_repos.repo_name
                , similar_repos.description
                , similar_repos.last_modified
                , similar_repos.language
                , similar_repos.stargazers_count
                , similar_repos.forks_count
                , similar_repos.from_hacker_news
                , similar_repos.hn_added_at
                , similar_repos.hn_submission_time
                , similar_repos.hn_title
                , similar_repos.hn_url
        order by sum(similar_users.score) desc
""".format(user.id)