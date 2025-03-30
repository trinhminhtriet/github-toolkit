import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
    GITHUB_PASSWORD = os.getenv("GITHUB_PASSWORD")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    COOKIE_FILEPATH = f"../config/{GITHUB_USERNAME}_cookies.json"
    USE_COOKIE = True
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    LANGUAGES = [
        "python", "javascript", "typescript", "java", "ruby", "php", "go",
        "swift", "kotlin", "rust", "c", "c++", "c#", "shell", "bash", "r", "dart"
    ]