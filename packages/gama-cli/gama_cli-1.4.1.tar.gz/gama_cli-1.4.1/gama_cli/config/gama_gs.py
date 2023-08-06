from dataclasses import dataclass
from enum import Enum
from dacite import from_dict, Config
import yaml
import click


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
        with open("config/gama_gs.yml") as stream:
            return from_dict(
                GamaGsConfig, yaml.safe_load(stream), config=Config(cast=[Mode, Network, LogLevel])
            )
    except FileNotFoundError:
        click.echo(click.style("/config/gama_gs.yml not found. Using default values..", fg="yellow"))  # type: ignore
        return GamaGsConfig()
