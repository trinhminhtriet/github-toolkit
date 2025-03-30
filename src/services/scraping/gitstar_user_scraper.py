import logging
import time
import requests
from bs4 import BeautifulSoup
from typing import List
from core.exceptions import ScraperException
from infrastructure.database.models import GithubUserModel
from core.entities import GithubUser
from utils.helpers import convert_to_int


class GitstarUserScraper:
    def __init__(self, db_connection):
        self.base_url = "https://gitstar-ranking.com/users"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.db_connection = db_connection
        self.logger = logging.getLogger(__name__)

    def upsert_github_user(self, user_data: dict) -> None:
        with self.db_connection.get_session() as session:
            try:
                existing_user = (
                    session.query(GithubUserModel)
                    .filter_by(username=user_data["username"])
                    .first()
                )
                if not existing_user:
                    self.logger.info(
                        f"[{user_data['username']}] Adding to github_users..."
                    )
                    new_user = GithubUserModel(
                        username=user_data["username"],
                        profile_url=f"https://github.com/{user_data['username']}",
                        stars=convert_to_int(user_data["stars"]),
                        avatar_url=user_data.get("avatar_url"),
                    )
                    session.add(new_user)
                else:
                    existing_user.stars = convert_to_int(user_data["stars"])
                    existing_user.avatar_url = user_data.get("avatar_url")
                    self.logger.info(f"[{user_data['username']}] Updated...")
                session.commit()
            except Exception as e:
                session.rollback()
                raise ScraperException(
                    f"Error upserting user {user_data['username']}: {str(e)}"
                )

    def get_users(self, page: int = 1) -> List[GithubUser]:
        url = f"{self.base_url}?page={page}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            users = []

            user_entries = soup.find_all("a", class_="list-group-item paginated_item")
            for entry in user_entries:
                user_data = {}

                name_span = entry.find("span", class_="name")
                if name_span:
                    username_span = name_span.find("span", class_="hidden-xs hidden-sm")
                    if username_span:
                        user_data["username"] = username_span.get_text(strip=True)

                stars_span = entry.find("span", class_="stargazers_count")
                if stars_span:
                    stars = stars_span.get_text(strip=True).replace("★", "").strip()
                    user_data["stars"] = stars

                avatar_img = entry.find("img", class_="avatar_image_big")
                if avatar_img and "src" in avatar_img.attrs:
                    user_data["avatar_url"] = avatar_img["src"]

                if not user_data["profile_url"]:
                    user_data["profile_url"] = (
                        f"https://github.com/{user_data['username']}"
                    )

                if user_data.get("username"):
                    users.append(
                        GithubUser(user_data["username"], user_data["profile_url"])
                    )
                    self.upsert_github_user(user_data)
                    self.logger.info(
                        f"Added {user_data['username']} with {user_data['stars']} stars"
                    )

            return users
        except requests.RequestException as e:
            raise ScraperException(f"Error fetching Gitstar page {page}: {str(e)}")

    def scrape_all_users(self, max_pages: int = 10) -> List[GithubUser]:
        all_users = []
        for page in range(1, max_pages + 1):
            self.logger.info(f"Scraping Gitstar page {page}...")
            users = self.get_users(page)
            all_users.extend(users)
            time.sleep(1)  # Rate limiting
        return all_users
