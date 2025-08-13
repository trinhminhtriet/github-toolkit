import logging
from infrastructure.database.connection import DatabaseConnection


class GitstarController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_connection = DatabaseConnection()
        self.session = self.db_connection.get_session()

    def collect_user(self):
        from services.gitstar.gitstar_user_scraper import GitstarUserScraper

        try:
            scraper = GitstarUserScraper(self.db_connection)
            self.logger.info("Starting Gitstar user collection...")
            collections = scraper.scrape_all_users(max_pages=100)
            self.logger.info(f"Collected {len(collections)} Gitstar users")
        finally:
            # self.auth_service.close()
            self.session.close()

    def collect_repo(self):
        from services.gitstar.gitstar_repo_scraper import GitstarRepoScraper

        try:
            scraper = GitstarRepoScraper(self.db_connection)
            self.logger.info("Starting Gitstar user collection...")
            collections = scraper.scrape_all_repos(max_pages=1000)
            self.logger.info(f"Collected {len(collections)} Gitstar repositories")
        finally:
            # self.auth_service.close()
            self.session.close()
