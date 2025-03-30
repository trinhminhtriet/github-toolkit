import time
import logging
from config.settings import Settings
from infrastructure.auth.auth_service import AuthService
from infrastructure.database.connection import DatabaseConnection
from services.scraping.github_developer_scraper import GithubDeveloperScraper
from services.scraping.github_repo_scraper import GithubRepoScraper

class GithubScraperController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.auth_service = AuthService()
        self.db_connection = DatabaseConnection()
        self.dev_scraper = GithubDeveloperScraper(self.auth_service.get_driver(), self.db_connection)
        self.repo_scraper = GithubRepoScraper(self.auth_service.get_driver(), self.db_connection)

    def collect(self) -> None:
        try:
            self.auth_service.authenticate()
            self.logger.info("Start collecting developers...")
            
            for language in Settings.LANGUAGES:
                self.logger.info(f"Exploring [{language}] developers")
                developers = self.dev_scraper.search_developers(language)
                self.logger.info(f"Total developers: {len(developers)}")
                
                for developer in developers:
                    # Scrape followers
                    followers = self.dev_scraper.search_followers(developer)
                    self.logger.info(f"Total followers: {len(followers)}")
                    
                    # Scrape repositories
                    repos = self.repo_scraper.scrape_repos(developer)
                    self.logger.info(f"Total repositories: {len(repos)}")
                    
                    self.logger.info("=====================================")
                    time.sleep(1)
                self.logger.info("=====================================")
                
        except Exception as e:
            self.logger.error(f"Error in collection process: {str(e)}")
        finally:
            self.auth_service.close()