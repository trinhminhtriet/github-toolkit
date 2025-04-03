import logging
from infrastructure.database.connection import DatabaseConnection


class HelloGitHubController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_connection = DatabaseConnection()
        self.session = self.db_connection.get_session()

    def collect_repo(self, max_pages: int = 1000):
        from services.hellogithub.hellogithub_repo_scraper import HelloGithubRepoScraper
        try:
            scraper = HelloGithubRepoScraper(self.db_connection)
            topics = [
                "all",
                "Z8PipJsHCX",
                "YgDkvUzLAC",
                "D4JBAUo967",
                "yrZkGsUC9M",
                "x3YH09wlKN",
                "0LByh3tjUO",
                "juBLV86qa5",
                "op63PzUDMg",
            ]
            for topic in topics:
                self.logger.info(f"[{topic}] Starting HelloGitHub repo collection for topic...")
                scraper.scrape_all_repos(tid=topic, max_pages=max_pages)
                self.logger.info(f"[{topic}] HelloGitHub repo collection for topic  completed.")
        except Exception as e:
            self.logger.error(f"Error during HelloGitHub repo collection: {e}")
        finally:
            self.session.close()
