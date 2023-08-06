import os
from importlib.metadata import version
from pathlib import Path
from typing import Tuple

from cement import Controller, ex
from hmd_cli_tools.hmd_cli_tools import load_hmd_env, set_hmd_env, read_manifest
from hmd_cli_tools.prompt_tools import prompt_for_values

from .remotes.github import _get_github_creds, _get_github_org_name
from .remotes import RemoteRepoManager


CONFIG_VALUES = {
    "HMD_REPO_ORG": {
        "prompt": "Prefix all created repositories with Org code, e.g. 'hmd':"
    }
}


VERSION_BANNER = """
hmd repo version: {}
"""


class LocalController(Controller):
    class Meta:
        label = "repo"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Create git repositories"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the repo command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(version("hmd_cli_repo")),
                },
            ),
        )

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="create a git repository",
        arguments=[
            (
                ["-tmp", "--template"],
                {
                    "action": "store",
                    "dest": "template",
                    "required": False,
                    "nargs": "*",
                },
            ),
            (
                ["-y", "--skip"],
                {
                    "action": "store_const",
                    "const": True,
                    "dest": "skip_prompt",
                    "default": False,
                },
            ),
            (
                ["-t", "--project-type"],
                {
                    "action": "store",
                    "dest": "project_type",
                    "required": False,
                },
            ),
        ],
    )
    def create(self):
        load_hmd_env(override=False)
        args = {"skip_prompt": self.app.pargs.skip_prompt}

        templates = self.app.pargs.template
        if templates:
            args.update({"templates": templates})

        if self.app.pargs.project_type != "":
            args.update({"project_type": self.app.pargs.project_type})

        from .hmd_cli_repo import create as do_create

        repo_dir, repo_info = do_create(**args)

        if repo_dir is None:
            return
        remote_mgr = RemoteRepoManager(self.app)

        remote_mgr.create_remote(repo_dir=repo_dir, repo_info=repo_info)

    @ex(
        help="adds technology to a git repository",
        arguments=[],
    )
    def add(self):
        load_hmd_env()
        args = {}

        repo_name = self.app.pargs.repo_name
        args.update({"repo_name": repo_name})

        from .hmd_cli_repo import add as do_add

        do_add(**args)

    @ex(
        help="configures HMD environment variables",
        arguments=[],
    )
    def configure(self):
        load_hmd_env()

        remotes = RemoteRepoManager(self.app)

        questions = remotes.configure()

        results = prompt_for_values({**CONFIG_VALUES, **questions})

        from .hmd_cli_repo import config as do_config

        if results:
            do_config(results)

            for k, v in results.items():
                set_hmd_env(k, str(v))

    @ex(help="pull all available Git repos")
    def pull_all(self):
        load_hmd_env()
        from .hmd_cli_repo import pull_all as do_pull_all

        remotes = RemoteRepoManager(self.app)

        do_pull_all(remotes)

    @ex(help="create remote repository for a project")
    def create_remote(self):
        load_hmd_env()

        repo_dir = os.getcwd()

        manifest = read_manifest()
        repo_name = manifest["name"]
        repo_desc = manifest["description"]

        remotes = RemoteRepoManager(self.app)

        remotes.create_remote(
            repo_dir=repo_dir,
            repo_info={"project_name": repo_name, "description": repo_desc},
        )
