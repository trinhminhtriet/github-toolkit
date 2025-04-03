import time
import logging
from infrastructure.auth.auth_service import AuthService
from infrastructure.database.connection import DatabaseConnection
from services.github.github_repo_scraper import GithubRepoScraper
from infrastructure.database.models import GithubUserModel


class GitHubRepoController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.auth_service = AuthService()
        self.auth_service.authenticate()

        self.db_connection = DatabaseConnection()

        self.repo_scraper = GithubRepoScraper(
            self.auth_service.get_driver(), self.db_connection
        )
        self.driver = self.auth_service.get_driver()
        self.session = self.db_connection.get_session()

    def collect(self):
        limit = 100
        db_page = 0

        try:
            while True:
                db_page += 1
                offset = (db_page - 1) * limit
                logging.info(
                    f"[{db_page}] Start collecting GitHub repositories - Page {db_page}"
                )

                github_users = (
                    self.session.query(GithubUserModel)
                    .filter(GithubUserModel.followed_at.is_not(None))
                    .order_by(GithubUserModel.repositories_count.desc())
                    .limit(limit)
                    .offset(offset)
                    .all()
                )

                if not github_users:
                    logging.info("No more users to collect. Exiting...")
                    break

                for user in github_users:
                    logging.info(
                        f"[{user.username}] Collect repositories from user: {user.profile_url}"
                    )
                    self.repo_scraper.scrape_repos(user.username)
                    time.sleep(2)
        finally:
            self.auth_service.close()
            self.session.close()
