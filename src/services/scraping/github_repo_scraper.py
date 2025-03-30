import json
import time
from typing import List
from selenium.webdriver.common.by import By
import logging
from infrastructure.database.models import GithubRepoModel
from core.entities import GithubRepo
from core.exceptions import ScraperException
from utils.helpers import convert_to_int

class GithubRepoScraper:
    def __init__(self, driver, db_connection):
        self.driver = driver
        self.db_connection = db_connection
        self.logger = logging.getLogger(__name__)

    def get_repo_url(self, username: str, page: int) -> str:
        url = f"https://github.com/{username}?tab=repositories&q=&type=&language=&sort=stargazers"
        return f"{url}&page={page}" if page > 1 else url

    def upsert_github_repo(self, repo: dict) -> None:
        with self.db_connection.get_session() as session:
            try:
                existing_repo = session.query(GithubRepoModel).filter_by(repo_url=repo["repo_url"]).first()
                if existing_repo:
                    for key, value in repo.items():
                        setattr(existing_repo, key, value or getattr(existing_repo, key))
                else:
                    new_repo = GithubRepoModel(**{k: v for k, v in repo.items() if v is not None})
                    session.add(new_repo)
                session.commit()
                self.logger.info(f"Upserted repository: {repo.get('repo_url')}")
            except Exception as e:
                session.rollback()
                raise ScraperException(f"Error upserting repository: {str(e)}")

    def scrape_repos(self, username: str) -> List[GithubRepo]:
        repos = []
        self.driver.get(self.get_repo_url(username, 1))
        time.sleep(2)

        try:
            parent_div = self.driver.find_element(By.ID, "user-repositories-list")
            li_tags = parent_div.find_elements(By.TAG_NAME, "li")

            for li in li_tags:
                repo = self._extract_repo_data(li, username)
                repos.append(GithubRepo(repo["username"], repo["repo_url"], repo["repo_name"]))
                self.upsert_github_repo(repo)
                self.logger.info(json.dumps(repo, ensure_ascii=False, indent=2))
        except Exception as e:
            raise ScraperException(f"Error scraping repositories: {str(e)}")
        return repos

    def _extract_repo_data(self, li, username: str) -> dict:
        repo = {
            "username": username,
            "repo_name": li.find_element(By.CSS_SELECTOR, 'a[itemprop="name codeRepository"]').text,
            "repo_url": li.find_element(By.CSS_SELECTOR, 'a[itemprop="name codeRepository"]').get_attribute("href"),
        }
        try:
            repo["repo_intro"] = li.find_element(By.CSS_SELECTOR, 'p[itemprop="description"]').text.strip()
        except:
            repo["repo_intro"] = None
        try:
            repo["repo_lang"] = li.find_element(By.CSS_SELECTOR, 'span[itemprop="programmingLanguage"]').text.strip()
        except:
            repo["repo_lang"] = None
        try:
            repo["repo_stars"] = convert_to_int(li.find_element(By.CSS_SELECTOR, 'a[href*="/stargazers"]').text.strip())
        except:
            repo["repo_stars"] = None
        try:
            repo["repo_forks"] = convert_to_int(li.find_element(By.CSS_SELECTOR, 'a[href*="/forks"]').text.strip())
        except:
            repo["repo_forks"] = None
        return repo