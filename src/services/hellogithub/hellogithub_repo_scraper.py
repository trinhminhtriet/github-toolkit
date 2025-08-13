import logging
import requests
from core.exceptions import ScraperException
import json
import time

from infrastructure.database.models import GithubRepoModel
from utils.helpers import convert_to_int

class HelloGithubRepoScraper:
    def __init__(self, db_connection):
        self.base_url = "https://abroad.hellogithub.com/v1/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.db_connection = db_connection
        self.logger = logging.getLogger(__name__)

    def upsert_github_repo(self, repo_data: dict) -> None:
        with self.db_connection.get_session() as session:
            try:
                existing_repo = (
                    session.query(GithubRepoModel)
                    .filter_by(repo_url=repo_data["repo_url"])
                    .first()
                )
                if not existing_repo:
                    self.logger.info(
                        f"[{repo_data['repo_url']}] Adding to github_repos..."
                    )
                    new_repo = GithubRepoModel(
                        username=repo_data["username"],
                        repo_name=repo_data["repo_name"],
                        repo_url=repo_data["repo_url"],
                    )
                    session.add(new_repo)
                    session.commit()
            except Exception as e:
                session.rollback()
                raise ScraperException(
                    f"Error upserting repo {repo_data['repo_url']}: {str(e)}"
                )

    def _fetch_page(self, tid: str = "all", page: int = 1) -> dict:
        """Fetch a single page of repositories from HelloGitHub API."""
        params = {
            "sort_by": "featured",
            "page": page,
            "rank_by": "newest",
            "tid": tid, # "YgDkvUzLAC"
        }
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch page {page}: {e}")
            raise ScraperException(f"API request failed: {e}")

    def _normalize_repo_data(self, repo_data):
        """Normalize HelloGitHub API data to match our GithubRepo entity."""
        return {
            "username": repo_data.get("author", "unknown"),
            "repo_name": repo_data.get("name", ""),
            "repo_url": f"https://github.com/{repo_data.get('author', '')}/{repo_data.get('name', '')}",
            "repo_intro": repo_data.get("summary_en", ""),
            "repo_lang": repo_data.get("primary_lang", ""),
        }

    def scrape_all_repos(self, tid: str = "all", max_pages:int =100):
        """Scrape all repositories from HelloGitHub, optionally up to max_pages."""
        page = 1
        while True:
            if max_pages and page > max_pages:
                self.logger.info(f"Reached max pages limit of {max_pages}")
                break

            self.logger.info(f"Scraping HelloGitHub page {page}")
            try:
                data = self._fetch_page(tid=tid, page=page)
                
                # Check if there are repositories in the response
                repos = data.get("data", [])
                if not repos:
                    self.logger.info("No more repositories found. Stopping.")
                    break

                # Process each repository
                for repo in repos:
                    normalized_repo = self._normalize_repo_data(repo)
                    self.upsert_github_repo(normalized_repo)
                    
                    repo_json = json.dumps(normalized_repo, ensure_ascii=False, indent=2)
                    self.logger.info(f"Processed repository: {repo_json}")

                if data.get("has_more") is False:
                    self.logger.info(f"[{page}] No more pages to scrape.")
                    break
                page += 1
                time.sleep(1)  # Rate limiting

            except ScraperException as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error on page {page}: {e}")
                break

        self.logger.info("HelloGitHub repository scraping completed")
