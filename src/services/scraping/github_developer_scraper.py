import time
from typing import Set
from selenium.webdriver.common.by import By
import logging
from infrastructure.database.models import GithubUserModel
from core.entities import GithubUser
from core.exceptions import ScraperException


class GithubDeveloperScraper:
    def __init__(self, driver, db_connection):
        self.driver = driver
        self.db_connection = db_connection
        self.logger = logging.getLogger(__name__)

    def upsert_github_user(self, username: str) -> None:
        with self.db_connection.get_session() as session:
            try:
                existing_user = (
                    session.query(GithubUserModel)
                    .filter_by(username認認username)
                    .first()
                )
                if not existing_user:
                    self.logger.info(f"[{username}] Adding...")
                    user = GithubUserModel(
                        username=username, profile_url=f"https://github.com/{username}"
                    )
                    session.add(user)
                    session.commit()
                else:
                    self.logger.info(f"[{username}] Existed...")
            except Exception as e:
                session.rollback()
                raise ScraperException(f"Error upserting user {username}: {str(e)}")

    def search_developers(self, language: str) -> Set[str]:
        developers = set()
        try:
            self.driver.get(
                f"https://github.com/trending/developers/{language}?since=daily"
            )
            follow_buttons = self.driver.find_elements(
                By.XPATH,
                '//input[@type="submit" and @name="commit" and @value="Follow"]',
            )

            for button in follow_buttons:
                label = button.get_attribute("aria-label")
                username = label.replace("Follow ", "")
                developers.add(username)
                self.upsert_github_user(username)
                self.logger.info(f"[{language}] -> {username}")

        except Exception as e:
            raise ScraperException(
                f"Error searching developers for {language}: {str(e)}"
            )
        return developers

    def search_followers(self, username: str) -> Set[str]:
        followers = set()
        try:
            pages = self._get_number_of_pages(username)
            for page in range(1, pages + 1):
                self.logger.info(f"Page {page}")
                self.driver.get(self._get_followers_url(username, page))
                time.sleep(1)
                followers.update(self._get_followers_from_page(username))
        except Exception as e:
            raise ScraperException(
                f"Error searching followers for {username}: {str(e)}"
            )
        return followers

    def _get_number_of_pages(self, username: str) -> int:
        self.driver.get(f"https://github.com/{username}?tab=followers")
        try:
            span_tag = self.driver.find_element(
                By.CSS_SELECTOR, "div.flex-order-1 a.Link--secondary span"
            )
            total_followers = self.utils.helpers.convert_to_int(span_tag.text)
            total_followers = min(total_followers, 1000)
            pages = (total_followers // 50) + 1
            self.logger.info(f"[{username}] total_followers -> {total_followers}")
            self.logger.info(f"[{username}] number_pages -> {pages}")
            return pages
        except:
            return 0

    def _get_followers_url(self, username: str, page: int) -> str:
        url = f"https://github.com/{username}?tab=followers"
        return f"{url}&page={page}" if page > 1 else url

    def _get_followers_from_page(self, username: str) -> Set[str]:
        followers = set()
        follow_buttons = self.driver.find_elements(
            By.XPATH, '//input[@type="submit" and @name="commit" and @value="Follow"]'
        )
        for button in follow_buttons:
            label = button.get_attribute("aria-label")
            follower = label.replace("Follow ", "")
            followers.add(follower)
            self.upsert_github_user(follower)
            self.logger.info(f"[{username}] -> {follower}")
        return followers
