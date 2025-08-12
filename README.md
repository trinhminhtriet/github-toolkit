# 🚀 GitHub toolkit

A Python-based web scraper that collects GitHub developer information, their followers, and repository details using Selenium and stores the data in a MySQL database.

## ✨ Features

- 🔥 Scrapes trending developers across multiple programming languages
- 👥 Collects follower information (up to 1000 per developer)
- 📦 Gathers repository details including name, URL, description, language, stars, and forks
- 🔐 Supports authentication via cookies or username/password
- 🗄️ Stores data in a MySQL database with automatic schema creation
- ⚠️ Includes error handling and logging
- 🧩 Follows clean architecture principles

## 🗂️ Project Structure

```
github-toolkit/
├── config/
│   └── settings.py           # Configuration and environment variables
├── core/
│   ├── entities.py          # Domain entities
│   └── exceptions.py        # Custom exceptions
├── infrastructure/
│   ├── database/           # Database-related code
│   │   ├── connection.py
│   │   └── models.py
│   └── auth/              # Authentication service
│       └── auth_service.py
├── services/
│   └── scraping/          # Scraping services
│       ├── github_developer_scraper.py
│       └── github_repo_scraper.py
├── utils/
│   └── helpers.py         # Utility functions
├── controllers/
│   └── github_scraper_controller.py  # Main controller
├── main.py                # Entry point
└── README.md
```

## 🛠️ Prerequisites

- 🐍 Python 3.8+
- 🗄️ MySQL database
- 🌐 Chrome browser
- 🧰 Chrome WebDriver

## ⚙️ Installation

1. Clone the repository:
```bash
git clone git@github.com:trinhminhtriet/github-toolkit.git
cd github-toolkit
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
GITHUB_USERNAME=your_username
GITHUB_PASSWORD=your_password
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
```

5. Create a `config` directory:
```bash
mkdir config
```

## 📋 Requirements

Create a `requirements.txt` file with:
```
selenium
sqlalchemy
python-dotenv
```

## ▶️ Usage

Run the scraper:
```bash
cd src
python main.py
```

The scraper will:
1. 🔑 Authenticate with GitHub
2. 🌟 Scrape trending developers for specified languages
3. 👥 Collect their followers (up to 1000 per developer)
4. 📦 Scrape their repositories
5. 💾 Store all data in the MySQL database

## ⚙️ Configuration

- Modify `config/settings.py` to change:
  - `LANGUAGES`: List of programming languages to scrape
  - `USE_COOKIE`: Toggle between cookie-based and credential-based authentication
- ⏱️ Adjust sleep times in services if needed for rate limiting

## 🗃️ Database Schema

### github_users
- 🆔 id (PK)
- 👤 username (unique)
- 🔗 profile_url
- 🕒 created_at
- 🕒 updated_at
- 📅 published_at

### github_repos
- 🆔 id (PK)
- 👤 username
- 📦 repo_name
- 📝 repo_intro
- 🔗 repo_url (unique)
- 🏷️ repo_lang
- ⭐ repo_stars
- 🍴 repo_forks
- 🕒 created_at
- 🕒 updated_at
- 📅 published_at

## 🛡️ Error Handling

- ❗ Custom exceptions for authentication, scraping, and database operations
- 📝 Logging configured at INFO level
- 🛑 Graceful shutdown of browser instance

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (create one if needed).

## 🙏 Acknowledgments

- Built with [Selenium](https://www.selenium.dev/), [SQLAlchemy](https://www.sqlalchemy.org/), and [Python](https://www.python.org/).
- Inspired by the need to automate GitHub data collection.