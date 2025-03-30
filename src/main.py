import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def collect_user():
    from controllers.github_repo_controller import GitHubRepoController
    ctl = GitHubRepoController()
    ctl.collect()

def collect_repo():
    from controllers.github_repo_controller import GitHubRepoController
    ctl = GitHubRepoController()
    ctl.collect()

if __name__ == "__main__":
    collect_repo()