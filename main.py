import logging
from src.controllers.github_repo_controller import GitHubRepoController

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    ctl = GitHubRepoController()
    ctl.collect()


if __name__ == "__main__":
    main()
