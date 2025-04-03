import json
import logging
import time
import requests
from bs4 import BeautifulSoup
from typing import List
from core.exceptions import ScraperException
from infrastructure.database.models import GithubRepoModel
from core.entities import GithubRepo
from utils.helpers import convert_to_int


class GitstarRepoScraper:
    def __init__(self, db_connection):
        self.base_url = "https://gitstar-ranking.com/repositories"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
                        repo_stars=convert_to_int(repo_data["repo_stars"]),
                    )
                    session.add(new_repo)
                else:
                    existing_repo.repo_stars = convert_to_int(repo_data["repo_stars"])
                    self.logger.info(f"[{repo_data['repo_url']}] Updated...")
                session.commit()
            except Exception as e:
                session.rollback()
                raise ScraperException(
                    f"Error upserting repo {repo_data['repo_url']}: {str(e)}"
                )

    def get_repos(self, page: int = 1) -> List[GithubRepo]:
        url = f"{self.base_url}?page={page}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            repos = []

            repo_entries = soup.find_all("a", class_="list-group-item paginated_item")
            for entry in repo_entries:
                repo_data = {}

                href = entry["href"]
                if href:
                    if "/" in href:
                        username, repo_name = href.strip("/").split("/")
                    else:
                        username, repo_name = href, None  # or raise an error
                    repo_data["username"] = username
                    repo_data["repo_name"] = repo_name
                    repo_data["repo_url"] = f"https://github.com/{username}/{repo_name}"

                # Extract stars
                stars_span = entry.find("span", class_="stargazers_count")
                if stars_span:
                    stars = stars_span.get_text(strip=True).replace("★", "").strip()
                    repo_data["repo_stars"] = stars

                description_el = entry.find("div", class_="repo-description")
                if description_el:
                    repo_data["repo_intro"] = description_el["title"]

                language_el = entry.find("div", class_="repo-language")
                if language_el:
                    repo_data["repo_lang"] = language_el.span.text.strip()

                if repo_data.get("repo_url"):
                    repos.append(
                        GithubRepo(
                            repo_data["username"],
                            repo_data["repo_url"],
                            repo_data["repo_name"],
                        )
                    )
                    self.upsert_github_repo(repo_data)
                    self.logger.info(
                        json.dumps(repo_data, indent=2, ensure_ascii=False)
                    )

            return repos
        except requests.RequestException as e:
            raise ScraperException(f"Error fetching Gitstar repo page {page}: {str(e)}")

    def scrape_all_repos(self, max_pages: int = 10) -> List[GithubRepo]:
        all_repos = []
        for page in range(1, max_pages + 1):
            self.logger.info(f"Scraping Gitstar repo page {page}...")
            repos = self.get_repos(page)
            all_repos.extend(repos)
            time.sleep(1)  # Rate limiting
        return all_repos
