import json
import os
import re
import shutil
import subprocess
from pathlib import Path
import time
from typing import Dict, List
from tempfile import TemporaryDirectory
import pkg_resources

import yaml
from cement import shell, minimal_logger
from cookiecutter.main import cookiecutter, prompt_for_config
from cookiecutter.replay import load
from git import Repo
from git.cmd import Git

from hmd_cli_tools.hmd_cli_tools import cd, read_manifest
from hmd_cli_tools.prompt_tools import prompt_for_values

from .remotes import RemoteRepoManager
from .loaders.project_type_loader import ProjectTypeLoader
from .loaders.project_template_loader import ProjectTemplateLoader

default_cutter = "default_repo"
user_home = os.path.expanduser("~")
hmd_yml = os.path.join(user_home, ".hmd.yml")
cache_dir = Path(os.environ.get("HMD_HOME", user_home)) / ".cache"

HMD_REPO_HOME = os.environ.get("HMD_REPO_HOME", None)
ORIGINAL_PROMPTS_FILE = ".original_prompts.json"

PRE_CREATE_HOOKS_ENTRY_POINT = "hmd_cli_repo.pre_create"
logger = minimal_logger("hmd-cli-repo")

project_type_loader = ProjectTypeLoader()
project_template_loader = ProjectTemplateLoader()


def get_project_type_context(templates: List[str] = []) -> Dict:
    templates = [default_cutter] + templates

    ctx = {}

    for template in templates:
        cookiecutter_json = (
            project_template_loader.load_project_template(template)
            / "cookiecutter.json"
        )

        with open(cookiecutter_json, "r") as cc:
            cc_ctx = json.load(cc)

            ctx = {**ctx, **cc_ctx}

    return ctx


def _get_default_ctx(repo_name: str):
    prompts_path = Path(os.getcwd()) / "meta-data" / ORIGINAL_PROMPTS_FILE

    if not os.path.exists(prompts_path):
        logger.info(f"Could not find original prompt answers in {str(prompts_path)}")
        return {"project_name": repo_name}

    with open(prompts_path, "r") as cc:
        return json.load(cc)


def _setup_git(repo_dir: str):
    r = Repo.init(repo_dir)

    for f in os.listdir(repo_dir):
        if f == ".git":
            continue
        r.index.add(f)

    cmd = ["git", "commit", "-m", "feat: :tada: generate initial repo structure"]

    process = subprocess.run(
        cmd, stdout=subprocess.PIPE, universal_newlines=True, cwd=repo_dir
    )
    print(process.stdout)
    r.git.branch("-M", "main")

    return r


def _check_local_repo_status(repo_url: str, pull: bool = True):
    repo_name = repo_url.split("/")[-1].removesuffix(".git")
    if HMD_REPO_HOME is None:
        raise Exception("Missing HMD_REPO_HOME environment variable")

    print(f" Checking for {repo_name} in {HMD_REPO_HOME}")
    repo_path = Path(HMD_REPO_HOME, repo_name)
    repo_exists = os.path.isdir(repo_path)
    print(f"Exists: {repo_exists}")

    try:
        if repo_exists:
            repo = Repo(repo_path)
            if repo.is_dirty(untracked_files=False):
                print(f"{repo_name} has local changes, cannot pull")
                diff = repo.git.diff(repo.head.commit.tree)
                print(diff)
            else:
                if pull:
                    print(f"Pulling {repo_name} from {repo.active_branch}")
                    print(repo.remotes.origin.pull())
        else:
            with cd(HMD_REPO_HOME):
                print(f"Cloning {repo_name}")
                Repo.clone_from(repo_url, repo_path)
    except Exception as e:
        logger.error(e)
        logger.warning(f"Could not update {repo_name}, skipping")


def _prompt_for_project_type() -> str:
    categories = project_type_loader.list_project_type_categories()
    questions = {
        "category": {
            "type": "list",
            "message": "Choose a Project Type Category:",
            "choices": categories,
        },
        "project_type": {
            "type": "list",
            "message": "Choose a Project Type:",
            "choices": lambda results: project_type_loader.list_project_types(
                category=results["category"]
            ),
        },
    }

    answers = prompt_for_values(questions)
    project_type = answers.get("project_type")

    return project_type


def run_cookiecutter(
    cutter: str,
    context: Dict,
    skip_prompt: bool = False,
    overwrite: bool = False,
    extra_ctx: Dict = {},
):
    output_dir = os.getcwd()
    cookiecutterrc = (
        Path(os.environ.get("HMD_HOME", user_home)) / ".config" / ".hmdreporc"
    )

    with open(cookiecutterrc, "r") as cc:
        defaults = yaml.safe_load(cc)
        defaults = defaults.get("default_context", {})
    with TemporaryDirectory() as tmp:
        cutter_name = f"hmd_cli_repo"
        cutter_path = Path(tmp) / cutter_name
        shutil.copytree(cutter, cutter_path)

        with open(cutter_path / "cookiecutter.json", "w") as cc:
            json.dump(context, cc)

        result = cookiecutter(
            str(cutter_path),
            no_input=skip_prompt,
            overwrite_if_exists=overwrite,
            extra_context=extra_ctx,
            output_dir=output_dir,
            config_file=str(cookiecutterrc),
        )

        return (
            result,
            load(os.path.join(user_home, ".cookiecutter_replay"), cutter_name)[
                "cookiecutter"
            ],
        )


def _run_pre_create_hooks(ctx: Dict):
    hooks = pkg_resources.iter_entry_points(PRE_CREATE_HOOKS_ENTRY_POINT)

    project_name = ctx["project_name"]

    for hook in hooks:
        h = hook.load()
        h(project_name)


def create(
    project_type: str = None,
    templates: List[str] = list(),
    skip_prompt: bool = False,
):
    if project_type is None:
        project_type = _prompt_for_project_type()

    if project_type is None:
        return None, None

    project_type_config = project_type_loader.load_project_type(project_type)
    templates = (
        list(map(lambda t: t["name"], project_type_config.get("templates", [])))
        + templates
    )

    templates = [default_cutter] + templates

    template_ctx = get_project_type_context(templates)
    ctx_values = {}
    for k, v in template_ctx.items():
        s = re.search("\{[A-Z_]+\}", v)

        if s is not None:
            ctx_values[k] = v.format(**os.environ)
    overwrite = False
    templates = [
        project_template_loader.load_project_template(template)
        for template in templates
    ]
    cookiecutterrc = (
        Path(os.environ.get("HMD_HOME", user_home)) / ".config" / ".hmdreporc"
    )

    with open(cookiecutterrc, "r") as cc:
        defaults = yaml.safe_load(cc)
        defaults = defaults.get("default_context", {})

    ctx = prompt_for_config(
        {"cookiecutter": {**template_ctx, **defaults, **ctx_values}}
    )
    _run_pre_create_hooks(ctx)
    skip_prompt = True
    for template in templates:
        result, ctx_values = run_cookiecutter(
            cutter=template,
            context=template_ctx,
            skip_prompt=skip_prompt,
            overwrite=overwrite,
            extra_ctx={**ctx_values, **ctx},
        )
        skip_prompt = True
        overwrite = True

    cache_path = Path(result) / "meta-data"

    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    with open(cache_path / ORIGINAL_PROMPTS_FILE, "w") as cc:
        json.dump(ctx_values, cc, indent=2)

    with cd(result):
        manifest = read_manifest()

        manifest["project_type"] = {"name": project_type}

        with open(Path("./meta-data/manifest.json"), "w") as mf:
            json.dump(manifest, mf, indent=2)

    _setup_git(result)

    return result, ctx_values


def add(repo_name: str = None):
    default_ctx = _get_default_ctx(repo_name)

    if repo_name is not None:
        default_ctx["project_name"] = repo_name
        default_ctx["repo_name"] = repo_name

    project_type = _prompt_for_project_type()
    project_type_config = project_type_loader.load_project_type(project_type)
    templates = list(map(lambda t: t["name"], project_type_config.get("templates", [])))

    template_ctx = get_project_type_context(templates)

    templates = [
        project_template_loader.load_project_template(template)
        for template in templates
    ]
    new_ctx = {}

    for k, v in template_ctx.items():
        if k not in default_ctx:
            new_ctx[k] = v
        else:
            new_ctx[k] = default_ctx[k]

    if new_ctx:
        logger.info(f"Found additional prompts in new type {project_type}")
        new_ctx = prompt_for_config({"cookiecutter": new_ctx})
        print(new_ctx)

    ctx = {**template_ctx, **default_ctx}

    repo_path = os.getcwd()
    repo = Repo(os.getcwd())

    branch_name = f"add-{project_type.replace(' ', '-')}-{time.time()}"
    repo.git.checkout("HEAD", b=branch_name)

    with TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            for template in templates:
                run_cookiecutter(
                    cutter=template,
                    context=ctx,
                    skip_prompt=True,
                    overwrite=True,
                    extra_ctx=ctx,
                )

            shutil.copytree(repo_name, repo_path, dirs_exist_ok=True)

    for f in os.listdir(repo_path):
        if f == ".git":
            continue
        repo.index.add(f)

    cmd = ["git", "commit", "-m", f"feat: added {project_type} project type"]

    process = subprocess.run(
        cmd, stdout=subprocess.PIPE, universal_newlines=True, cwd=os.getcwd()
    )
    print(process.stdout)

    checkout_cmd = ["git", "checkout", "main"]

    process = subprocess.run(
        checkout_cmd, stdout=subprocess.PIPE, universal_newlines=True, cwd=os.getcwd()
    )
    print(process.stdout)

    diff_cmd = ["git", "diff", f"main..{branch_name}"]

    process = subprocess.run(
        diff_cmd, stdout=subprocess.PIPE, universal_newlines=True, cwd=os.getcwd()
    )
    print(process.stdout)

    print(
        f"""
To view changed files run:

    git diff main..{branch_name}

And to merge in changes:

    git merge {branch_name}
"""
    )

    return True


def config(config_vars: Dict):
    cfg = {}

    author_name = os.environ.get("HMD_AUTHOR_NAME")
    author_email = os.environ.get("HMD_AUTHOR_EMAIL")

    if author_name:
        cfg.update({"_author": author_name})

    if author_email:
        cfg.update({"_author_email": author_email})

    cookiecutterrc = (
        Path(os.environ.get("HMD_HOME", user_home)) / ".config" / ".hmdreporc"
    )

    if not os.path.exists(cookiecutterrc.parent):
        os.makedirs(cookiecutterrc.parent)

    with open(cookiecutterrc, "w") as f:
        yaml.dump({"default_context": cfg}, f)

    logger.warning(
        """
Should we configure your Git environment to automatically use pre-commit hooks in all future repos?

NOTICE: This requires pre-commit to be installed, and we will configure Git globally.

This should only be done if you do not have custom Git configuration already.
    """
    )
    configure_git = shell.Prompt(
        "Configure Git and pre-commit:", options=["yes", "no"], default="no"
    )
    git_cfg = configure_git.prompt()

    if git_cfg == "yes":
        templateDir = os.path.join(user_home, ".hmd", ".git-templatedir")
        CONFIG_CMDS = [
            ["pre-commit", "init-templatedir", templateDir],
            ["pre-commit", "init-templatedir", "-t", "commit-msg", templateDir],
        ]
        if not os.path.exists(templateDir):
            os.makedirs(templateDir)

        g = Git()
        if author_name:
            g.execute(["git", "config", "--global", "user.name", author_name])
        if author_email:
            g.execute(["git", "config", "--global", "user.email", author_email])

        g.execute(["git", "config", "--global", "init.templateDir", templateDir])

        for cmd in CONFIG_CMDS:
            process = subprocess.run(
                cmd, stdout=subprocess.PIPE, universal_newlines=True
            )
            print(process.stdout)

    return True


def pull_all(remote_mgr: RemoteRepoManager):

    repos = remote_mgr.list_remote_repos()
    print(f"Pulling all repos...")

    for repo in repos:
        _check_local_repo_status(repo)

    print("Pull complete")
    return True
