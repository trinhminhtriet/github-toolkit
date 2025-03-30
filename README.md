# GitHub Toolkit

A Python-based tool to scrape GitHub repositories and user data using Selenium, store the information in a MySQL database, and optionally star repositories based on predefined criteria.

## Overview

This project is designed to:
- Authenticate with GitHub using cookies or username/password.
- Scrape repository details (name, URL, description, language, stars, forks) from specified GitHub users.
- Store scraped data in a MySQL database using SQLAlchemy.
- Automatically star repositories with more than 128 stars if not already starred.

The codebase follows clean architecture principles, object-oriented programming (OOP), and a modular folder structure for maintainability and scalability.

## Folder Structure

```
github-toolkit/
├── src/
│   ├── config/           # Configuration settings
│   ├── database/         # Database models and connection logic
│   ├── services/         # Business logic for authentication and scraping
│   ├── utils/            # Helper functions
│   └── main.py           # Entry point of the application
├── config/               # Directory for cookie files
├── .env                  # Environment variables (not tracked in git)
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

## Prerequisites

- Python 3.8+
- MySQL server
- Chrome browser (for Selenium WebDriver)
- ChromeDriver (compatible with your Chrome version)

## Setup

1. **Clone the Repository**
   ```bash
   git clone git@github.com:trinhminhtriet/github-toolkit.git
   cd github-toolkit
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the root directory with the following content:
   ```
   GITHUB_USERNAME=your_github_username
   GITHUB_PASSWORD=your_github_password
   DB_USERNAME=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_HOST=your_mysql_host
   DB_NAME=your_database_name
   ```
   - Ensure the MySQL database (`DB_NAME`) exists before running the script.

4. **Install ChromeDriver**
   - Download ChromeDriver from [here](https://chromedriver.chromium.org/downloads) matching your Chrome version.
   - Add ChromeDriver to your system PATH or place it in a directory accessible to the script.

5. **Create Input Directory**
   ```bash
   mkdir input
   ```
   This directory will store cookie files (e.g., `<username>_cookies.json`) if authentication uses cookies.

## Usage

Run the main script:
```bash
python src/main.py
```

### What It Does
- Authenticates with GitHub using either cookies (if available) or username/password.
- Queries the database for GitHub users with a `followed_at` timestamp.
- Scrapes repositories for each user, storing data in the `github_repos` table.
- Stars repositories with >128 stars if not already starred.
- Logs progress and errors to the console.

### Configuration
- Edit `src/config/settings.py` to modify constants like `USE_COOKIE` (default: `True`) or `COOKIE_FILEPATH`.

## Database Schema

The project uses two tables:
1. **`github_users`**
   - Stores GitHub user profile data (username, profile URL, email, etc.).
2. **`github_repos`**
   - Stores repository data (name, URL, description, stars, forks, etc.).

Both tables are created automatically by SQLAlchemy if they don’t exist.

## Logging

The application logs to the console with the format:
```
%(asctime)s - %(levelname)s - %(message)s
```
Log levels include `INFO` (default) and `ERROR`.

## Features

- **Authentication**: Supports cookie-based or credential-based login.
- **Scraping**: Extracts detailed repository information using Selenium.
- **Database**: Upserts data to avoid duplicates and tracks updates.
- **Starring**: Automatically stars repositories meeting the criteria (>128 stars).

## Troubleshooting

- **Authentication Fails**: Ensure GitHub credentials are correct in `.env` or cookies are valid.
- **Database Errors**: Verify MySQL connection details and database accessibility.
- **Selenium Issues**: Check ChromeDriver version compatibility with your Chrome browser.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (create one if needed).

## Acknowledgments

- Built with [Selenium](https://www.selenium.dev/), [SQLAlchemy](https://www.sqlalchemy.org/), and [Python](https://www.python.org/).
- Inspired by the need to automate GitHub data collection.