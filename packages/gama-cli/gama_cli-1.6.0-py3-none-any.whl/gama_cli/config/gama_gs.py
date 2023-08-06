from dataclasses import dataclass
from enum import Enum
from dacite import from_dict, Config
import yaml
import click
from gama_cli.helpers import dacite_to_dict

GAMA_GS_CONFIG_PATH = ".gama/gama_gs.yml"


class Mode(str, Enum):
    NONE = "none"
    XBOX = "xbox"
    THRUSTMASTER = "thrustmaster"
    THRUSTMASTER_COMBO = "thrustmaster_combo"
    WARTHOG = "warthog"
    WARTHOG_COMBO = "warthog_combo"


class Network(str, Enum):
    SHARED = "shared"
    VPN = "vpn"
    HOST = "host"


class LogLevel(str, Enum):
    INFO = "info"
    DEBUG = "debug"


@dataclass
class GamaGsConfig:
    mode: Mode = Mode.NONE
    network: Network = Network.SHARED
    prod: bool = False
    log_level: LogLevel = LogLevel.INFO
    remote_cmd_override: bool = False


def read_gama_gs_config():
    try:
        with open(GAMA_GS_CONFIG_PATH) as stream:
            return from_dict(
                GamaGsConfig, yaml.safe_load(stream), config=Config(cast=[Mode, Network, LogLevel])
            )
    except FileNotFoundError:
        click.echo(click.style(f"{GAMA_GS_CONFIG_PATH} not found. Using default values..", fg="yellow"))  # type: ignore
        return GamaGsConfig()


def write_gama_gs_config(config: GamaGsConfig):
    with open(GAMA_GS_CONFIG_PATH, "w") as stream:
        click.echo(click.style(f"Writing {GAMA_GS_CONFIG_PATH}...", fg="green"))  # type: ignore
        yaml.dump(dacite_to_dict(config), stream)
