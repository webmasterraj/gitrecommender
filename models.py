from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRCK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    user_name = db.Column(db.String())
    email = db.Column(db.String(), nullable=True)
    url = db.Column(db.String(), nullable=True)
    location = db.Column(db.String(), nullable=True)
    fullname = db.Column(db.String(), nullable=True)
    created = db.Column(db.DateTime(), nullable=True)
    num_stars = db.Column(db.Integer(), nullable=True)
    clusters = db.relationship('Cluster', secondary=cluster_membership,
            backref='users')
    stars = db.relationship('Repo', secondary=starred)

    def __init__(self, user_id, user_name, email=None, url=None, location=None, 
            fullname=None, created=None, num_stars=None):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.location = location
        self.fullname = fullname
        self.created = created
        self.num_stars = num_stars


class Repo(db.Model):
    __tablename__ = "repos"

    id = db.Column(db.Integer(), primary_key=True)
    repo_id = db.Column(db.Integer())
    repo_name = db.Column(db.String())
    owner_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    owner = db.relationship('User', backref='repos')
    num_forks = db.Column(db.Integer(), nullable=True)
    num_stargazers = db.Column(db.Integer(), nullable=True)
    topics = db.Column(db.ARRAY(db.String()), nullable=True)
    stargazers = db.relationship('User', secondary=starred)

    def __init__(self, repo_id, repo_name, owner_id, owner_name,
            num_forks=None, num_stargazers=None, topics=None):
        self.repo_id = repo_id
        self.repo_name = repo_name
        self.owner_id = owner_id
        self.num_forks = num_forks
        self.num_stargazers = num_stargazers
        self.topics = topics


class Cluster(db.Model):
    __tablename__ = "clusters"

    id = db.Column(db.Integer(), primary_key=True)
    cluster_hash= db.Column(db.String())
    seed = db.Column(db.String())
    repo_id = db.Column(db.Integer(), db.ForeignKey('repos.id'), nullable=True)
    repo = db.relationship('Repo', uselist=False)
    created = db.Column(db.DateTime())
    
    def __init__(self, cluster_id, seed, repo_id, created):
        self.cluster_id = cluster_id
        self.seed = seed
        self.repo_id = repo_id
        self.created = created


cluster_membership = db.Table('user_cluster_rel',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('cluster_id', db.Integer, db.ForeignKey('repos.id')),
)


#class Star(db.Model):
#    __tablename__ = "stars"
#
#    id = db.Column(db.Integer(), primary_key=True)
#    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
#    repo_id = db.Column(db.Integer(), db.ForeignKey('repos.id'))
#    starred_at = db.Column(db.DateTime())
#
#    def __init__(self, user_id, repo_id, starred_at):
#        self.user_id = user_id
#        self.repo_id = repo_id
#        self.starred_at = starred_at


starred = db.Table('stars',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('cluster_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('starred_at', db.DateTime),
)
