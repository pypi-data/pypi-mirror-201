from typing import List, Optional
import click
import os

from gama_cli.config.gama_gs import Network, Mode, LogLevel, read_gama_gs_config
from gama_cli.helpers import docker_compose_path, get_project_root, docker_bake

from python_on_whales.docker_client import DockerClient
from python_on_whales.utils import ValidPath

DOCKER_GS = docker_compose_path("./gs/docker-compose.yaml")
DOCKER_GS_DEV = docker_compose_path("./gs/docker-compose.dev.yaml")
DOCKER_GS_NETWORK_SHARED = docker_compose_path("./gs/docker-compose.network-shared.yaml")
DOCKER_GS_NETWORK_HOST = docker_compose_path("./gs/docker-compose.network-host.yaml")
DOCKER_GS_NETWORK_VPN = docker_compose_path("./gs/docker-compose.network-vpn.yaml")
DOCKER_GS_WARTHOG_COMBO = docker_compose_path("./gs/docker-compose.warthog-combo.yaml")


class Gs:
    def _get_compose_files(
        self, mode: Optional[Mode] = None, network: Network = Network.SHARED, prod: bool = False
    ) -> List[ValidPath]:
        compose_files: List[ValidPath] = [DOCKER_GS]

        if not prod:
            compose_files.append(DOCKER_GS_DEV)
        if mode == Mode.WARTHOG_COMBO:
            compose_files.append(DOCKER_GS_WARTHOG_COMBO)
        if network == Network.SHARED:
            compose_files.append(DOCKER_GS_NETWORK_SHARED)
        if network == Network.VPN:
            compose_files.append(DOCKER_GS_NETWORK_VPN)
        if network == Network.HOST:
            compose_files.append(DOCKER_GS_NETWORK_HOST)

        return compose_files

    def _get_container_name(self, mode: Mode) -> str:
        return f"gama_gs_{mode.value}"

    def create(self, cli: click.Group):
        @cli.group(help="Commands for the ground-station")
        def gs():
            pass

        config = read_gama_gs_config()

        mode_help = f"The controller active on the gs. Default: {config.mode}"
        network_help = f"The network configuration to run the vessel. Default: {config.network}"
        log_level_help = f"The log level to run the. Default: {config.log_level}"

        @gs.command(name="build")
        @click.option(
            "-m",
            "--mode",
            type=click.Choice(Mode),  # type: ignore
            default=config.mode,
            help=mode_help,
        )
        @click.argument("args", nargs=-1)
        def build(mode: Mode, args: List[str]):
            """Builds the ground-station"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )
            docker.compose.build()

        @gs.command(name="bake")
        @click.option(
            "--version",
            type=str,
            required=True,
            help="The version to bake. Default: latest",
        )
        @click.option(
            "--push",
            type=bool,
            default=False,
            is_flag=True,
            help="Should we push the images to the registry? Default: False",
        )
        @click.argument("services", nargs=-1)
        def bake(version: str, push: bool, services: List[str]):  # type: ignore
            """Bakes the gs docker containers"""
            compose_files = self._get_compose_files()
            docker_bake(
                version=version,
                services=services,
                push=push,
                compose_files=compose_files,
            )

        @gs.command(name="up")
        @click.option(
            "-m",
            "--mode",
            type=click.Choice(Mode),  # type: ignore
            default=config.mode,
            help=mode_help,
        )
        @click.option(
            "-r",
            "--remote-cmd-override",
            type=bool,
            default=config.remote_cmd_override,
            help="Should we override the remote command? Default: False",
        )
        @click.option(
            "-n",
            "--network",
            type=click.Choice(Network),  # type: ignore
            default=config.network,
            help=network_help,
        )
        @click.option(
            "--build",
            type=bool,
            default=False,
            help="Should we rebuild the docker containers? Default: False",
        )
        @click.option(
            "--prod",
            type=bool,
            default=config.prod,
            is_flag=True,
            help=f"Should we start in prod mode? Default: {config.prod}",
        )
        @click.option(
            "--log-level",
            type=click.Choice(LogLevel),  # type: ignore
            default=config.log_level,
            help=log_level_help,
        )
        @click.argument("args", nargs=-1)
        def up(
            mode: Mode,
            remote_cmd_override: bool,
            network: Network,
            build: bool,
            prod: bool,
            log_level: LogLevel,
            args: List[str],
        ):
            """Starts the ground-station"""
            docker = DockerClient(
                compose_files=self._get_compose_files(mode=mode, network=network, prod=prod),
                compose_project_directory=get_project_root(),
            )

            buttons = "True" if mode == Mode.WARTHOG_COMBO else "False"

            gama_gs_command_args = (
                f"mode:={mode.value} buttons:={buttons} remote_cmd_override:={remote_cmd_override}"
            )

            if log_level:
                gama_gs_command_args += f" log_level:={log_level.value}"

            os.environ["GAMA_GS_COMMAND_ARGS"] = gama_gs_command_args
            docker.compose.up(detach=True, build=build)

        @gs.command(name="down")
        @click.option(
            "-m",
            "--mode",
            type=click.Choice(Mode),  # type: ignore
            default=config.mode,
            help=mode_help,
        )
        @click.argument("args", nargs=-1)
        def down(mode: Mode, args: List[str]):
            """Stops the ground-station"""
            docker = DockerClient(
                compose_files=self._get_compose_files(mode),
                compose_project_directory=get_project_root(),
            )
            docker.compose.down()

        @gs.command(name="test")
        def test():
            """Tests the ground-station"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )
            docker.compose.run("gama_gs", "platform ros test".split(" "))
