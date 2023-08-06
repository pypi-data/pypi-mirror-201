from typing import List
from enum import Enum
from pathlib import Path
import os
import click
from python_on_whales.docker_client import DockerClient
from python_on_whales.utils import ValidPath

from gama_cli.helpers import (
    check_directory_ownership,
    docker_compose_path,
    get_project_root,
    call,
)

DOCKER_ORG = "ghcr.io/greenroom-robotics"

DOCKER_SIM_DEV = docker_compose_path("./sim/docker-compose.dev.yaml")
DOCKER_SIM_STANDALONE = docker_compose_path("./sim/docker-compose.standalone.yaml")

Mode: Enum = Enum("mode", ("dev", "standalone"))

mode_default = "standalone"
mode_help = f"The mode to run the sim. Default: {mode_default}"


class Sim:
    def _get_compose_files(self, mode: str) -> List[ValidPath]:
        if mode == "dev":
            return [DOCKER_SIM_DEV]
        else:
            return [DOCKER_SIM_STANDALONE]

    def __init__(self, cli: click.Group):
        @cli.group(help="Commands for the sim")
        def sim():
            pass

        @sim.command(name="build")
        @click.option(
            "-m",
            "--mode",
            type=click.Choice(list(map(lambda x: x.name, Mode)), case_sensitive=False),
            default=mode_default,
            help=mode_help,
        )
        @click.option(
            "-c",
            "--clean",
            help="Should the ue4 build assets be cleaned?",
            type=bool,
        )
        @click.argument("args", nargs=-1)
        def build(mode: str, clean: bool, args: List[str]):
            """Builds the sim"""
            # If building standalone, we first build the dev sim
            # TODO move this to a multistage build

            # check UE cache dir
            prj_root = get_project_root()
            if not prj_root:
                raise RuntimeError("Could not find project root")

            cache_dir = Path(prj_root / ".cache")
            Path(cache_dir).mkdir(exist_ok=True)

            if not check_directory_ownership(cache_dir):
                raise click.ClickException(
                    "'.cache' directory does not belong to current user/group."
                )

            docker_standalone = DockerClient(
                compose_files=self._get_compose_files("standalone"),
                compose_project_directory=get_project_root(),
            )
            docker_dev = DockerClient(
                compose_files=self._get_compose_files("dev"),
                compose_project_directory=get_project_root(),
            )

            # build ue-dev container
            docker_dev.compose.build()

            if mode == "standalone":
                if clean:
                    clean_command = (
                        """cd "${PROJECTS_HOME}/${PROJECT_NAME}" && ue4 clean && rm -rf dist"""
                    )
                    docker_dev.compose.run("whiskey_ue", ["bash", "-c", clean_command])

                # run UE package command to compile and cook the UE project, making the `dist` directory
                ue_project_package_command = """cd "${PROJECTS_HOME}/${PROJECT_NAME}" && source ${ROS_OVERLAY}/setup.bash && ue4 package Development"""
                docker_dev.compose.run("whiskey_ue", ["bash", "-c", ue_project_package_command])
                docker_standalone.compose.build()

        @sim.command(name="up")
        @click.option(
            "--build",
            type=bool,
            default=False,
            help="Should we rebuild the docker containers? Default: False",
        )
        @click.option(
            "-m",
            "--mode",
            type=click.Choice(list(map(lambda x: x.name, Mode)), case_sensitive=False),
            default=mode_default,
            help=mode_help,
        )
        @click.argument("args", nargs=-1)
        def up(build: bool, mode: str, args: List[str]):
            """Starts the sim"""
            docker = DockerClient(
                compose_files=self._get_compose_files(mode),
                compose_project_directory=get_project_root(),
            )
            docker.compose.up(detach=True, build=build)

        @sim.command(name="down")
        @click.option(
            "-m",
            "--mode",
            type=click.Choice(list(map(lambda x: x.name, Mode)), case_sensitive=False),
            default=mode_default,
            help=mode_help,
        )
        @click.argument("args", nargs=-1)
        def down(mode: str, args: List[str]):
            """Stops the sim"""
            docker = DockerClient(
                compose_files=self._get_compose_files(mode),
                compose_project_directory=get_project_root(),
            )
            docker.compose.down()

        @sim.command(name="base-ue")
        @click.option(
            "--ue-version",
            type=str,
            default="4.27.2",
            help="The release version of Unreal Engine to build",
        )
        @click.option(
            "--memory",
            type=str,
            default=None,
            help="Set maximum memory for the docker build",
        )
        def base_ue(ue_version: str, memory: str):
            """Builds the base Unreal Engine image for development"""

            cuda_ver = "11.8.0"
            ubuntu_ver = "22.04"

            args = ""
            if memory is not None:
                args += f" --memory {memory}"

            # docker org has to be provided as long as we have to build our own cudagl images. requires https://github.com/adamrehn/ue4-docker/pull/276
            call(
                f"ue4-docker build {ue_version} --cuda={cuda_ver} -basetag=ubuntu{ubuntu_ver} -baseorg={DOCKER_ORG} -username={os.environ['GHCR_USERNAME']} -password={os.environ['API_TOKEN_GITHUB']}{args} --opt credential_mode=secrets --exclude ddc",
                env={"UE4DOCKER_TAG_NAMESPACE": DOCKER_ORG},
            )
