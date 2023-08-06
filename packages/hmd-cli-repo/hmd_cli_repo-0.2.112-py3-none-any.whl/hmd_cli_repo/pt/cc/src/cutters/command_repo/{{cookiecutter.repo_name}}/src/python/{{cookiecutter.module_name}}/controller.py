import os

from cement import Controller, ex
from importlib.metadata import version
from hmd_cli_tools import get_version

VERSION_BANNER = """
hmd {{ cookiecutter.command }} version: {}
"""

VERSION = version("{{cookiecutter.module_name}}")


class LocalController(Controller):
    class Meta:
        label = "{{ cookiecutter.command }}"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "{{ cookiecutter.description }}"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the {{ cookiecutter.command }} command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(VERSION),
                },
            ),
        )

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="build <...>",
        arguments=[
            (["-n", "--name"], {"action": "store", "dest": "name", "required": False})
        ],
    )
    def build(self):
        args = {}
        # build the args values...

        from .{{cookiecutter.module_name}} import build as do_build

        result = do_build(**args)


    @ex(
        help="publish <...>",
        arguments=[
            (["-n", "--name"], {"action": "store", "dest": "name", "required": False})
        ],
    )
    def publish(self):
        args = {}
        # publish the args values...

        from .{{cookiecutter.module_name}} import publish as do_publish

        result = do_publish(**args)


    @ex(
        help="deploy <...>",
        arguments=[
            (["-n", "--name"], {"action": "store", "dest": "name", "required": False})
        ],
    )
    def deploy(self):
        args = {}
        # deploy the args values...

        from .{{cookiecutter.module_name}} import deploy as do_deploy

        result = do_deploy(**args)
