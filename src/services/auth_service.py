import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import logging
from src.config.settings import Settings

class AuthService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=self.options)

    def authenticate(self):
        self.driver.get("https://github.com/login")
        
        if Settings.USE_COOKIE:
            self._load_cookies()
        else:
            self._login_with_credentials()
            self._save_cookies()

    def _load_cookies(self):
        self.logger.info("Using cookies for authentication...")
        with open(Settings.COOKIE_FILEPATH, "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                self.driver.add_cookie({"name": cookie["name"], "value": cookie["value"]})
        time.sleep(5)

    def _login_with_credentials(self):
        self.logger.info("Using username and password for authentication...")
        username_input = self.driver.find_element(By.NAME, "login")
        password_input = self.driver.find_element(By.NAME, "password")
        
        username_input.send_keys(Settings.GITHUB_USERNAME)
        password_input.send_keys(Settings.GITHUB_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(20)

    def _save_cookies(self):
        with open(Settings.COOKIE_FILEPATH, "w") as file:
            json.dump(self.driver.get_cookies(), file)

    def get_driver(self):
        return self.driver

    def close(self):
        self.driver.quit()