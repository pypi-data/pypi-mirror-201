import click

from gama_cli.helpers import call


class Git:
    def __init__(self, cli: click.Group):
        @cli.group(help="Git convenience commands")
        def git():
            pass

        @git.command(name="pull")
        def pull():
            """Pulls this repo and all submodules"""
            call("git pull --recurse-submodules=yes")
