from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import DATABASE

Base = declarative_base()

app = Flask(__name__)
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    user_name = Column('user_name', String)
    email = Column('email', String, nullable=True)
    url = Column('url', String, nullable=True)
    location = Column('location', String, nullable=True)
    fullname = Column('fullname', String, nullable=True)
    created_at = Column('created_at', DateTime, nullable=True)
    random = Column('random', String, nullable=True)
    num_stars = Column('num_stars', Integer, nullable=True)


class Repos(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True)
    repo_id = Column('repo_id', Integer)
    repo_name = Column('repo_name', String)
    owner_id = Column('owner_id', Integer)
    owner_name = Column('owner_name', String)
    name = Column('name', String, nullable=True)
    num_forks = Column('num_forks', Integer, nullable=True)
    num_stargazers = Column('num_stargazers', Integer, nullable=True)
    topics = Column('topics', ARRAY(String), nullable=True)


class Stars(Base):
    __tablename__ = "stars"

    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    repo_id = Column('repo_id', Integer)
    starred_at = Column('starred_at', DateTime)


class Clusters(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True)
    cluster_id = Column('cluster_id', String)
    seed = Column('seed', String)
    repo_id = Column('repo_id', Integer, nullable=True)
    created = Column('created', String, nullable=True)


class ClusterMembership(Base):
    __tablename__ = "user_cluster_rel"

    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    cluster_id = Column('cluster_id', String)
