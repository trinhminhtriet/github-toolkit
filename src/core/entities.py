from datetime import datetime

class GithubUser:
    def __init__(self, username: str, profile_url: str):
        self.username = username
        self.profile_url = profile_url
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.published_at = datetime.now()

class GithubRepo:
    def __init__(self, username: str, repo_url: str, repo_name: str):
        self.username = username
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.repo_intro = None
        self.repo_lang = None
        self.repo_stars = 0
        self.repo_forks = 0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.published_at = datetime.now()