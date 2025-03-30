import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def gitstar_collect_user():
    from controllers.gitstar_controller import GitstarController

    ctl = GitstarController()
    ctl.collect_user()


def gitstar_collect_repo():
    from controllers.gitstar_controller import GitstarController

    ctl = GitstarController()
    ctl.collect_repo()


def collect_repo():
    from controllers.github_repo_controller import GitHubRepoController

    ctl = GitHubRepoController()
    ctl.collect()


if __name__ == "__main__":
    collect_repo()
