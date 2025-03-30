import json
import time
from selenium.webdriver.common.by import By
import logging
from src.database.models import GithubRepo
from src.utils.helpers import convert_to_int

class GithubRepoScraper:
    def __init__(self, driver, session):
        self.driver = driver
        self.session = session
        self.logger = logging.getLogger(__name__)

    def get_repo_url(self, username, page):
        url = f"https://github.com/{username}?tab=repositories&q=&type=&language=&sort=stargazers"
        return f"{url}&page={page}" if page > 1 else url

    def upsert_github_repo(self, repo):
        try:
            existing_repo = self.session.query(GithubRepo).filter_by(repo_url=repo['repo_url']).first()
            if existing_repo:
                for key, value in repo.items():
                    setattr(existing_repo, key, value or getattr(existing_repo, key))
                # existing_repo.updated_at = func.now()
            else:
                new_repo = GithubRepo(**{k: v for k, v in repo.items() if v is not None})
                self.session.add(new_repo)
            self.session.commit()
            self.logger.info(f"Upserted repository: {repo.get('repo_url')}")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error while upserting repository: {e}")

    def scrape_repos_from_page(self, username):
        repos = []
        self.driver.get(self.get_repo_url(username, 1))
        time.sleep(2)

        try:
            parent_div = self.driver.find_element(By.ID, 'user-repositories-list')
            li_tags = parent_div.find_elements(By.TAG_NAME, 'li')

            for li in li_tags:
                repo = self._extract_repo_data(li, username)
                repos.append(repo)
                self.upsert_github_repo(repo)
                self.logger.info(json.dumps(repo, ensure_ascii=False, indent=2))
                self.logger.info("=====================================")
        except Exception as e:
            self.logger.error(f"Error scraping repositories: {e}")

        return repos

    def _extract_repo_data(self, li, username):
        repo = {
            'username': username,
            'repo_name': li.find_element(By.CSS_SELECTOR, 'a[itemprop="name codeRepository"]').text,
            'repo_url': li.find_element(By.CSS_SELECTOR, 'a[itemprop="name codeRepository"]').get_attribute('href')
        }

        try:
            repo['repo_intro'] = li.find_element(By.CSS_SELECTOR, 'p[itemprop="description"]').text.strip()
        except:
            repo['repo_intro'] = None

        try:
            repo['repo_lang'] = li.find_element(By.CSS_SELECTOR, 'span[itemprop="programmingLanguage"]').text.strip()
        except:
            repo['repo_lang'] = None

        try:
            repo['repo_stars'] = convert_to_int(li.find_element(By.CSS_SELECTOR, 'a[href*="/stargazers"]').text.strip())
        except:
            repo['repo_stars'] = None

        try:
            repo['repo_forks'] = convert_to_int(li.find_element(By.CSS_SELECTOR, 'a[href*="/forks"]').text.strip())
        except:
            repo['repo_forks'] = None

        self._handle_starring(li, repo)
        return repo

    def _handle_starring(self, li, repo):
        try:
            starring_container = li.find_element(By.CSS_SELECTOR, 'div.starring-container')
            repo_starred = " on " in starring_container.get_attribute("class")
            div_tag = starring_container.find_element(By.CSS_SELECTOR, 'div.starred' if repo_starred else 'div.unstarred')

            if not repo_starred and repo['repo_stars'] and repo['repo_stars'] > 128:
                star_button = div_tag.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                self.logger.info(f"{repo['repo_url']} - {star_button.get_attribute('aria-label')}")
                star_button.click()
                self.logger.info(f"Starred repository: {repo['repo_url']}")
                time.sleep(1)
            else:
                self.logger.info(f"Skip starring repository: {repo['repo_url']}")
        except Exception as e:
            self.logger.error(f"Error while starring repository: {e}")
            