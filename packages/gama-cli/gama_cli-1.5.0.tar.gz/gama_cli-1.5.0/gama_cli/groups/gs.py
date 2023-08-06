from typing import List, Optional
import click
import os

from gama_cli.config.gama_gs import (
    Network,
    Mode,
    LogLevel,
    read_gama_gs_config,
    GamaGsConfig,
    GAMA_GS_CONFIG_PATH,
    write_gama_gs_config,
)
from gama_cli.helpers import (
    docker_compose_path,
    get_project_root,
    docker_bake,
    maybe_ignore_build,
    maybe_ignore_prod,
)

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

    def __init__(self, cli: click.Group, dev_mode: bool = False):
        @cli.group(help="Commands for the ground-station")
        def gs():
            pass

        @gs.command(name="up")
        @click.option(
            "--build",
            type=bool,
            default=False,
            help="Should we rebuild the docker containers? Default: False",
        )
        @click.argument("args", nargs=-1)
        def up(
            build: bool,
            args: List[str],
        ):
            """Starts the ground-station"""
            config = read_gama_gs_config()
            build = maybe_ignore_build(dev_mode, build)
            prod = maybe_ignore_prod(dev_mode, config.prod)

            docker = DockerClient(
                compose_files=self._get_compose_files(
                    mode=config.mode, network=config.network, prod=prod
                ),
                compose_project_directory=get_project_root(),
            )

            buttons = "True" if config.mode == Mode.WARTHOG_COMBO else "False"

            gama_gs_command_args = f"mode:={config.mode.value} buttons:={buttons} remote_cmd_override:={config.remote_cmd_override}"

            if config.log_level:
                gama_gs_command_args += f" log_level:={config.log_level.value}"

            os.environ["GAMA_GS_COMMAND_ARGS"] = gama_gs_command_args
            docker.compose.up(detach=True, build=build)

        @gs.command(name="down")
        @click.argument("args", nargs=-1)
        def down(args: List[str]):
            """Stops the ground-station"""
            config = read_gama_gs_config()

            docker = DockerClient(
                compose_files=self._get_compose_files(config.mode),
                compose_project_directory=get_project_root(),
            )
            docker.compose.down()

        @gs.command(name="install")
        def install():  # type: ignore
            """Install GAMA on a gs"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )
            try:
                docker.compose.pull()
            except Exception:
                click.echo(
                    click.style(
                        "Failed to pull GAMA files. Have you ran `gama_cli authenticate` ?",
                        fg="yellow",
                    )
                )

        @gs.command(name="configure")
        def configure():  # type: ignore
            """Configure GAMA Ground Station"""
            # Check if the file exists
            if os.path.exists(GAMA_GS_CONFIG_PATH):
                click.echo(
                    click.style(
                        f"GAMA Ground Station config already exists: {GAMA_GS_CONFIG_PATH}",
                        fg="yellow",
                    )
                )
                result = click.prompt(
                    "Do you want to overwrite it?", default="y", type=click.Choice(["y", "n"])
                )
                if result == "n":
                    return

            config = GamaGsConfig(
                mode=click.prompt("Mode", type=click.Choice([mode.value for mode in Mode])),
                network=click.prompt(
                    "Network", type=click.Choice([network.value for network in Network])
                ),
                prod=click.prompt("Prod", type=bool, default=True),
                remote_cmd_override=click.prompt(
                    "Remote Command Override", type=bool, default=False
                ),
                log_level=click.prompt(
                    "Log Level",
                    type=click.Choice([log_level.value for log_level in LogLevel]),
                    default=LogLevel.INFO.value,
                ),
            )
            write_gama_gs_config(config)

        if dev_mode:

            @gs.command(name="build")
            def build():
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

            @gs.command(name="test")
            def test():
                """Tests the ground-station"""
                docker = DockerClient(
                    compose_files=self._get_compose_files(),
                    compose_project_directory=get_project_root(),
                )
                docker.compose.run("gama_gs", "platform ros test".split(" "))
