import os
from typing import List
import click

from gama_cli.config.gama_vessel import Variant, Network, Mode, LogLevel, read_gama_vessel_config
from gama_cli.helpers import call, docker_compose_path, get_project_root, docker_bake
from python_on_whales.docker_client import DockerClient
from python_on_whales.utils import ValidPath


DOCKER_VESSEL = docker_compose_path("vessel/docker-compose.yaml")
DOCKER_VESSEL_GPU = docker_compose_path("vessel/docker-compose.gpu.yaml")
DOCKER_VESSEL_VARIANT_EDUCAT = docker_compose_path("vessel/docker-compose.variant-educat.yaml")
DOCKER_VESSEL_VARIANT_BRAVO = docker_compose_path("vessel/docker-compose.variant-bravo.yaml")
DOCKER_VESSEL_PROD = docker_compose_path("vessel/docker-compose.prod.yaml")
DOCKER_VESSEL_DEV = docker_compose_path("vessel/docker-compose.dev.yaml")
DOCKER_VESSEL_NETWORK_SHARED = docker_compose_path("vessel/docker-compose.network-shared.yaml")
DOCKER_VESSEL_NETWORK_VPN = docker_compose_path("vessel/docker-compose.network-vpn.yaml")
DOCKER_VESSEL_NETWORK_HOST = docker_compose_path("vessel/docker-compose.network-host.yaml")

SERVICES = [
    "gama_ui",
    "gama_chart_tiler",
    "gama_chart_api",
    "gama_vessel",
    "gama_greenstream",
    "gama_docs",
    "lookout",
    "groot",
]


class Vessel:
    def _get_compose_files(
        self,
        network: Network = Network.SHARED,
        gpu: bool = False,
        variant: Variant = Variant.WHISKEY_BRAVO,
        prod: bool = False,
    ) -> List[ValidPath]:
        compose_files: List[ValidPath] = [DOCKER_VESSEL]

        if not prod:
            compose_files.append(DOCKER_VESSEL_DEV)
        if variant == variant.EDUCAT:
            compose_files.append(DOCKER_VESSEL_VARIANT_EDUCAT)
        if variant == variant.WHISKEY_BRAVO:
            compose_files.append(DOCKER_VESSEL_VARIANT_BRAVO)
        if gpu:
            compose_files.append(DOCKER_VESSEL_GPU)
        if network == Network.SHARED:
            compose_files.append(DOCKER_VESSEL_NETWORK_SHARED)
        if network == Network.VPN:
            compose_files.append(DOCKER_VESSEL_NETWORK_VPN)
        if network == Network.HOST:
            compose_files.append(DOCKER_VESSEL_NETWORK_HOST)
        if prod:
            compose_files.append(DOCKER_VESSEL_PROD)

        return compose_files

    def _get_greenstream_config(self, variant: Variant, mode: Mode):
        if mode == Mode.STUBS:
            return "config.stubs.yml"
        if mode == Mode.SIM:
            print("SIM VIDEO STREAMING NO LONGER SUPPORTED")
            return "config.sim.yml"
        if mode == Mode.HW:
            if variant == Variant.WHISKEY_BRAVO:
                return "config.variant.bravo.yml"
            if variant == Variant.EDUCAT:
                return "config.variant.educat.yml"
        raise Exception("Invalid mode/variant combination")

    def create(self, cli: click.Group):
        @cli.group(help="Commands for the vessel")
        def vessel():
            pass

        config = read_gama_vessel_config()
        variant_help = f"The variant to run. Default: {config.variant}"
        mode_help = f"The mode to run the vessel. Default: {config.mode}"
        network_help = f"The network configuration to run the vessel. Default: {config.network}"
        log_level_help = f"The log_level to run. Default: {config.log_level}"

        @vessel.command(name="build")
        @click.option(
            "-v",
            "--variant",
            type=click.Choice(Variant),  # type: ignore
            default=config.variant,
            help=variant_help,
        )
        @click.option(
            "-l",
            "--lookout",
            type=bool,
            default=config.extensions.lookout,
            is_flag=True,
            help="Should we build lookout (requires CUDA)? Default: False",
        )
        @click.option(
            "-g",
            "--groot",
            type=bool,
            default=config.extensions.groot,
            is_flag=True,
            help="Should we build groot? Default: False",
        )
        @click.argument(
            "service",
            required=False,
            type=click.Choice(SERVICES),
        )
        @click.argument("args", nargs=-1)
        def build(variant: Variant, lookout: bool, groot: bool, service: str, args: List[str]):  # type: ignore
            """Builds the vessel"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )

            os.environ["GAMA_VARIANT"] = variant.value

            if service:
                docker.compose.build([service])
                return

            docker.compose.build(["gama_ui", "gama_chart_tiler", "gama_chart_api", "gama_vessel"])

            if lookout:
                docker.compose.build(["lookout"])

            if groot:
                docker.compose.build(["groot"])

        @vessel.command(name="bake")
        @click.option(
            "--variant",
            type=click.Choice(Variant),  # type: ignore
            default=config.variant,
            help=variant_help,
        )
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
        def bake(variant: Variant, version: str, push: bool, services: List[str]):  # type: ignore
            """Bakes the vessel docker containers"""
            compose_files = self._get_compose_files(variant=variant)
            docker_bake(
                version=version,
                services=services,
                push=push,
                compose_files=compose_files,
            )

        @vessel.command(name="up")
        @click.option(
            "-m",
            "--mode",
            type=click.Choice(Mode),  # type: ignore
            default=config.mode,
            help=mode_help,
        )
        @click.option(
            "-v",
            "--variant",
            type=click.Choice(Variant),  # type: ignore
            default=config.variant,
            help=variant_help,
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
            is_flag=True,
            help="Should we rebuild the docker containers? Default: False",
        )
        @click.option(
            "--lookout",
            type=bool,
            default=config.extensions.lookout,
            is_flag=True,
            help=f"Should we start lookout (requires CUDA)? Default: {config.extensions.lookout}",
        )
        @click.option(
            "--groot",
            type=bool,
            default=config.extensions.groot,
            is_flag=True,
            help=f"Should we start groot? Default: {config.extensions.groot}",
        )
        @click.option(
            "--rviz",
            type=bool,
            default=config.extensions.rviz,
            is_flag=True,
            help=f"Should we start rviz? Default: {config.extensions.rviz}",
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
        @click.option(
            "-uu",
            "--ubiquity-user",
            type=str,
            default=config.ubiquity_user,
            help="Ubiquity username. Default: None",
        )
        @click.option(
            "-up",
            "--ubiquity-pass",
            type=str,
            default=config.ubiquity_pass,
            help="Ubiquity password. Default: None",
        )
        @click.option(
            "-uip",
            "--ubiquity-ip",
            type=str,
            default=config.ubiquity_ip,
            help="Ubiquity ip. Default: None",
        )
        @click.argument(
            "service",
            required=False,
            type=click.Choice(SERVICES),
        )
        @click.argument("args", nargs=-1)
        def up(
            mode: Mode,
            network: Network,
            variant: Variant,
            build: bool,
            lookout: bool,
            groot: bool,
            rviz: bool,
            prod: bool,
            log_level: LogLevel,
            ubiquity_user: str,
            ubiquity_pass: str,
            ubiquity_ip: str,
            service: str,
            args: List[str],
        ):
            """Starts the vessel"""
            docker = DockerClient(
                compose_files=self._get_compose_files(
                    gpu=lookout, network=network, variant=variant, prod=prod
                ),
                compose_project_directory=get_project_root(),
            )

            vessel_launch_command_args = f"mode:='{mode.value}' rviz:='{rviz}'"
            if ubiquity_user:
                vessel_launch_command_args += f" ubiquity_user:={ubiquity_user}"
            if ubiquity_pass:
                vessel_launch_command_args += f" ubiquity_pass:='{ubiquity_pass}'"
            if ubiquity_ip:
                vessel_launch_command_args += f" ubiquity_ip:='{ubiquity_ip}'"
            if log_level:
                vessel_launch_command_args += f" log_level:='{log_level.value}'"

            os.environ["GAMA_VARIANT"] = variant.value
            os.environ["GAMA_VESSEL_COMMAND_ARGS"] = vessel_launch_command_args
            os.environ["LOOKOUT_COMMAND_ARGS"] = f"mode:='{mode.value}'"
            os.environ["GREENSTREAM_CONFIG_FILE"] = self._get_greenstream_config(variant, mode)

            services = (
                [service]
                if service
                else [
                    "gama_ui",
                    "gama_chart_tiler",
                    "gama_chart_api",
                    "gama_vessel",
                    "gama_greenstream",
                    "gama_docs",
                ]
            )

            docker.compose.up(
                services,
                detach=True,
                build=build,
            )

            if lookout:
                docker.compose.up(
                    ["lookout"],
                    detach=True,
                    build=build,
                )

            if groot:
                docker.compose.up(["groot"], detach=True, build=build)

        @vessel.command(name="down")
        @click.argument("args", nargs=-1)
        def down(args: List[str]):  # type: ignore
            """Stops the vessel"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )
            docker.compose.down()

        @vessel.command(name="test-ui")
        def test_ui():  # type: ignore
            """Runs test for the ui"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )
            docker.compose.run("gama_ui", ["yarn", "test"])

        @vessel.command(name="test-ros")
        def test_ros():  # type: ignore
            """Runs test for the ros nodes"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )
            docker.compose.run(
                "gama_vessel",
                ["/bin/bash", "-c", "source /home/ros/.profile && platform ros test"],
            )

        @vessel.command(name="test-e2e")
        def test_e2e():  # type: ignore
            """Runs UI e2e tests (assuming all the containers are up)"""
            call("cd ./projects/gama_ui && yarn test:e2e")

        @vessel.command(name="test")
        def test():  # type: ignore
            """Runs test for the all vessel code"""
            call("gama_cli vessel test-ui")
            call("gama_cli vessel test-ros")

        @vessel.command(name="lint-ui")
        @click.argument("args", nargs=-1)
        def lint_ui(args: List[str]):  # type: ignore
            """Runs lints for the ui"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )
            docker.compose.run("gama_ui", ["yarn", "lint", *args])

        @vessel.command(name="type-generate")
        def type_generate():  # type: ignore
            """Generates typescript types for all ros messages"""
            docker = DockerClient(
                compose_files=self._get_compose_files(),
                compose_project_directory=get_project_root(),
            )
            docker.compose.run("gama_vessel", ["npx", "ros-typescript-generator"])
