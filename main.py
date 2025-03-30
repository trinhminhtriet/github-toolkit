import logging
import time
from src.config.settings import Settings
from src.database.db_connection import DatabaseConnection
from src.database.models import GithubUser
from src.services.auth_service import AuthService
from src.services.github_repo_scraper import GithubRepoScraper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    db = DatabaseConnection()
    session = db.get_session()
    
    auth = AuthService()
    auth.authenticate()
    
    scraper = GithubRepoScraper(auth.get_driver(), session)
    
    limit = 100
    db_page = 1
    
    try:
        while True:
            db_page += 1
            offset = (db_page - 1) * limit
            logging.info(f"[{db_page}] Start collecting GitHub repositories - Page {db_page}")
            
            github_users = (session.query(GithubUser)
                          .filter(GithubUser.followed_at.is_not(None))
                          .order_by(GithubUser.followed_at.desc())
                          .limit(limit)
                          .offset(offset)
                          .all())
            
            if not github_users:
                logging.info("No more users to collect. Exiting...")
                break

            for user in github_users:
                logging.info(f"[{user.username}] Collect repositories from user: {user.profile_url}")
                scraper.scrape_repos_from_page(user.username)
                time.sleep(2)
    finally:
        auth.close()
        session.close()

if __name__ == "__main__":
    main()