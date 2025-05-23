import logging
import sys

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
    
    funcs = {
        "hellogithub_collect_repo": hellogithub_collect_repo,
        "gitstar_collect_repo": gitstar_collect_repo,
        "gitstar_collect_user": gitstar_collect_user,
        "github_collect_repo": github_collect_repo,
    }

    if len(sys.argv) < 2:
        print("Usage: python main.py <function_name>")
        print("Available functions:", ", ".join(funcs.keys()))
        sys.exit(1)

    func_name = sys.argv[1]
    func = funcs.get(func_name)
    if func is None:
        print(f"Unknown function: {func_name}")
        print("Available functions:", ", ".join(funcs.keys()))
        sys.exit(1)

    func()
