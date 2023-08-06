from abc import abstractmethod
import os
from typing import Dict, List
import pkg_resources

from cement import App, minimal_logger, shell

logger = minimal_logger("hmd_cli_repo")

REMOTE_ENTRY_POINT = "hmd_cli_repo.remotes"
REMOTE_HOOKS_ENTRY_POINT = "hmd_cli_repo.post_remote"


class RemoteRepoManager:
    def __init__(self, app: App):
        self.app = app
        self.all_remotes: List[str] = []
        self.remotes: List[RemoteRepositoryFactory] = []
        self.post_remote_hooks: List = []

        entrypoints = pkg_resources.iter_entry_points(REMOTE_ENTRY_POINT)

        for entrypoint in entrypoints:
            logger.debug(f"Checking if {entrypoint.name} is enabled...")
            self.all_remotes.append(str(entrypoint.name))
            if self._check_enabled(str(entrypoint.name)):
                logger.info(f"Loading remote repo extension {entrypoint.name}...")
                self.remotes.append(entrypoint.load()(self.app))

        hooks = pkg_resources.iter_entry_points(REMOTE_HOOKS_ENTRY_POINT)

        for hook in hooks:
            self.post_remote_hooks.append(hook.load())

    def _check_enabled(self, remote: str) -> bool:
        env_var = f"HMD_REPO_REMOTE_{remote.upper()}_ENABLED"
        return os.environ.get(env_var, "False").lower() == "true"

    def create_remote(self, repo_dir: str, repo_info: Dict) -> List[str]:
        result = []

        if len(self.remotes) == 0:
            print("Not creating remote repositories because none were found enabled.")
            return

        for remote in self.remotes:
            result.append(remote.create_remote_repo(repo_dir, repo_info))

        for hook in self.post_remote_hooks:
            hook(repo_dir, result[0])

        return result

    def list_remote_repos(self) -> List[str]:
        result = []

        if len(self.remotes) == 0:
            print("No list remote repositories because none were found enabled.")
            return result

        for remote in self.remotes:
            result.extend(remote.list_remote_repos())

        return result

    def configure(self) -> Dict:
        config_vars = {}

        for remote in self.all_remotes:
            enabled = self._check_enabled(remote)
            config_vars[f"HMD_REPO_REMOTE_{remote.upper()}_ENABLED"] = {
                "hidden": True,
                "default": enabled,
            }
            if enabled:
                entrypoints = pkg_resources.iter_entry_points(
                    REMOTE_ENTRY_POINT, remote
                )

                for entrypoint in entrypoints:
                    factory = entrypoint.load()

                    r: RemoteRepositoryFactory = factory(self.app)
                    results = r.configure()
                    config_vars = {**config_vars, **results}

        return config_vars


class RemoteRepositoryFactory:
    def __init__(self, app: App) -> None:
        self.app = app

    @abstractmethod
    def create_remote_repo(self, repo_dir: str, repo_info: Dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def list_remote_repos(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def configure(self) -> Dict:
        raise NotImplementedError
