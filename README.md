# GitHub Repository Recommender

Personalized GitHub repository recommendations based on user interests and starring patterns.

## Overview

This project analyzes GitHub users' starring patterns and repository interactions to create clusters of similar users and repositories, enabling personalized repository recommendations.

## Features

- User profile analysis
- Repository clustering based on user interactions
- Topic-based repository categorization
- Personalized repository recommendations
- PostgreSQL database integration for data persistence

## Tech Stack

- Python 3.x
- Flask web framework
- SQLAlchemy ORM
- PostgreSQL database
- PyGithub (GitHub API wrapper)

## Prerequisites

- Python 3.x
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/webmasterraj/gitrecommender.git
cd gitrecommender
```
2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Start the Flask app:
```bash
python app.py
```
5. Access the app at http://localhost:5000

## Database Models
The application uses three main models:

- **User**: Stores GitHub user information and their relationships
- **Repo**: Manages repository data and metadata
- **Cluster**: Handles grouping of similar repositories and users