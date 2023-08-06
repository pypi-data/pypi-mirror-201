import click

from gama_cli.helpers import call


class Misc:
    def create(self, cli: click.Group):
        @cli.command(name="lint")
        def lint():
            """Lints all the things"""
            call("pre-commit run --all")
            call("gama_cli vessel lint-ui")

        @cli.command(name="test")
        def test():
            """Tests all the things"""
            call("gama_cli lint")
            call("gama_cli gs test")
            call("gama_cli vessel test-ui")
            call("gama_cli vessel test-ros")

        @cli.command(name="test-e2e")
        def test_e2e():
            """Brings up all containers and runs the e2e tests"""
            call("gama_cli gs up")
            call("gama_cli vessel up --mode stubs")
            call("gama_cli vessel test-e2e")
