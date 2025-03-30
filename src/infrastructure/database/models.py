from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class GithubUserModel(Base):
    __tablename__ = "github_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255, collation="utf8mb4_unicode_ci"), unique=True)
    profile_url = Column(String(255, collation="utf8mb4_unicode_ci"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    published_at = Column(DateTime, default=func.now())
    followed_at = Column(DateTime, default=func.now())

class GithubRepoModel(Base):
    __tablename__ = "github_repos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255, collation="utf8mb4_unicode_ci"))
    repo_name = Column(String(255, collation="utf8mb4_unicode_ci"))
    repo_intro = Column(Text(collation="utf8mb4_unicode_ci"))
    repo_url = Column(String(255, collation="utf8mb4_unicode_ci"), unique=True)
    repo_lang = Column(String(255, collation="utf8mb4_unicode_ci"))
    repo_stars = Column(Integer, default=0)
    repo_forks = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    published_at = Column(DateTime, default=func.now())