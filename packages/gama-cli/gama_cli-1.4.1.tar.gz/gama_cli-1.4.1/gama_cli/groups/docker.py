import click

from gama_cli.helpers import call


class Docker:
    def create(self, cli: click.Group):
        @cli.group(help="Docker convenience methods")
        def docker():
            pass

        @docker.command(name="clearlogs")
        def clearlogs():  # type: ignore
            """Clears all the docker logs"""
            command = 'sudo sh -c "truncate -s 0 /var/lib/docker/containers/*/*-json.log"'
            call(command)
