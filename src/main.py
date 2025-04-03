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


def github_collect_repo():
    from controllers.github_repo_controller import GitHubRepoController

    ctl = GitHubRepoController()
    ctl.collect()


def hellogithub_collect_repo():
    from controllers.hellogithub_ctl import HelloGitHubController

    ctl = HelloGitHubController()
    ctl.collect_repo(max_pages=1000)


if __name__ == "__main__":
    hellogithub_collect_repo()
