import os
from typing import Dict, List, Tuple

from cement import App, shell
from git import Repo
from git.cmd import Git
from github import Github
from github.AuthenticatedUser import AuthenticatedUser
from github.Organization import Organization
from github.Repository import Repository

from . import RemoteRepositoryFactory


def _check_git_creds(gh_username: str, gh_token: str):
    if gh_username is None or gh_token is None:
        raise Exception(
            "Missing GitHub username and/or PAT. Please run hmd repo config."
        )


def _list_repos(gh_token: str, org_name: str) -> List[Repository]:
    if gh_token is None:
        raise Exception(
            "Access token not passed in. Check if it is set as HMD_GH_PASSWORD or run hmd repo config."
        )

    _, hmd = _get_github_info(gh_token, org_name)
    return hmd.get_repos()


def _get_github_info(
    gh_token: str, org_name: str
) -> Tuple[AuthenticatedUser, Organization]:
    gh = Github(gh_token.strip())
    gh_user = gh.get_user()
    hmd = list(filter(lambda org: org.login == org_name, gh_user.get_orgs()))[0]
    return gh_user, hmd


def _get_github_creds(app: App) -> Tuple[str, str]:
    gh_token = None
    gh_username = None

    try:
        gh_username = app.config.get("github", "username")
    except:
        pass

    if gh_username is None:
        gh_username = os.environ.get("HMD_GH_USERNAME")

    if gh_username is None:
        p = shell.Prompt(
            text="Please enter your GitHub username. You can set HMD_GH_USERNAME to avoid this prompt:"
        )
        gh_username = p.prompt()

    try:
        gh_token = app.config.get("github", "password")
    except:
        pass

    if gh_token is None:
        gh_token = os.environ.get("HMD_GH_PASSWORD")

        if gh_token is not None and os.path.exists(gh_token):
            with open(gh_token, "r") as pat:
                gh_token = pat.read()

    if gh_token is None:
        ghpat = os.path.join(os.path.expanduser("~"), ".ghpat")
        if os.path.exists(ghpat):
            with open(ghpat, "r") as pat:
                gh_token = pat.read()

    if gh_token is None:
        p = shell.Prompt(
            text="Please enter your GitHub PAT. You can set HMD_GH_PASSWORD to avoid this prompt."
        )
        gh_token = p.prompt()

    return gh_username, gh_token.strip()


def _get_github_org_name():
    org_name = os.environ.get("HMD_GH_ORG_NAME")

    if org_name is None:
        p = shell.Prompt(
            f"Enter GitHub Organization Name [{org_name}]:", default=org_name
        )
        org_name = p.prompt()

    return org_name


def create_github_repo(app: App, repo_dir: str, repo_info: Dict) -> str:
    gh_username, gh_token = _get_github_creds(app)

    repo_name = repo_info.get("project_name", repo_dir.split(os.sep)[-1])

    org_name = _get_github_org_name()

    gh_user, org = _get_github_info(gh_token=gh_token, org_name=org_name)

    assert org is not None, "Could not find GitHub organization to create repository."

    p = shell.Prompt(
        f"Create Public/Private Repo [private]: ",
        default="private",
        options=["private", "public"],
        numbered=True,
    )
    private = p.prompt()
    org.create_repo(
        repo_name,
        description=repo_info.get("description", repo_name),
        private=private == "private",
    )

    r = Repo(repo_dir)

    gh_url = f"git@github.com:{org_name}/{repo_name}.git"
    if "origin" in r.remotes and r.remotes.origin.exists():
        r.remotes.origin.set_url(gh_url, r.remotes.origin.url)
    else:
        r.create_remote("origin", gh_url)

    if "github" in r.remotes and r.remotes.github.exists():
        r.remotes.github.set_url(gh_url, r.remotes.github.url)
    else:
        r.create_remote("github", gh_url)

    r.git.push("--set-upstream", "origin", "main")

    return gh_url


class GitHubRemote(RemoteRepositoryFactory):
    def __init__(self, app: App) -> None:
        super().__init__(app)

    def create_remote_repo(self, repo_dir: str, repo_info: Dict) -> str:
        return create_github_repo(self.app, repo_dir, repo_info)

    def list_remote_repos(self) -> List[str]:
        gh_username, gh_token = _get_github_creds(self.app)
        org_name = _get_github_org_name()
        return list(map(lambda repo: repo.ssh_url, _list_repos(gh_token, org_name)))

    def configure(self) -> Dict:

        return {
            "HMD_GH_USERNAME": {"prompt": "Enter your Github username:"},
            "HMD_GH_PASSWORD": {"prompt": "Enter filepath to your Github PAT file:"},
            "HMD_GH_ORG_NAME": {"prompt": "Enter Github Organization name:"},
        }
