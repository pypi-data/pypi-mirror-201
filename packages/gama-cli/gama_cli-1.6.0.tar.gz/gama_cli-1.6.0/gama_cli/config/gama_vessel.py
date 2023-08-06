from dataclasses import dataclass
from enum import Enum
from dacite import from_dict, Config
import yaml
import click
from typing import Optional
import os
from pathlib import Path
from gama_cli.helpers import dacite_to_dict

GAMA_VESSEL_CONFIG_PATH = ".gama/gama_vessel.yml"


class Mode(str, Enum):
    SIMULATOR = "simulator"
    HARDWARE = "hardware"
    STUBS = "stubs"


class Network(str, Enum):
    SHARED = "shared"
    VPN = "vpn"
    HOST = "host"


class Variant(str, Enum):
    WHISKEY_BRAVO = "whiskey_bravo"
    EDUCAT = "educat"


class LogLevel(str, Enum):
    INFO = "info"
    DEBUG = "debug"


@dataclass
class GamaVesselConfigExtensions:
    lookout: bool = False
    rviz: bool = False
    groot: bool = False


@dataclass
class GamaVesselConfig:
    variant: Variant = Variant.WHISKEY_BRAVO
    mode: Mode = Mode.SIMULATOR
    extensions: GamaVesselConfigExtensions = GamaVesselConfigExtensions()
    network: Network = Network.SHARED
    prod: bool = False
    log_level: LogLevel = LogLevel.INFO
    ubiquity_user: Optional[str] = None
    ubiquity_pass: Optional[str] = None
    ubiquity_ip: Optional[str] = None


def read_gama_vessel_config():
    try:
        with open(GAMA_VESSEL_CONFIG_PATH) as stream:
            return from_dict(
                GamaVesselConfig,
                yaml.safe_load(stream),
                config=Config(cast=[Mode, Network, Variant, LogLevel]),
            )
    except FileNotFoundError:
        click.echo(click.style(f"{GAMA_VESSEL_CONFIG_PATH} not found. Using default values...", fg="yellow"))  # type: ignore
        return GamaVesselConfig()


def write_gama_vessel_config(config: GamaVesselConfig):
    # Make the config dir if it doesn't exist
    os.makedirs(Path(GAMA_VESSEL_CONFIG_PATH).parent, exist_ok=True)

    with open(GAMA_VESSEL_CONFIG_PATH, "w") as stream:
        click.echo(click.style(f"Writing {GAMA_VESSEL_CONFIG_PATH}...", fg="green"))  # type: ignore
        yaml.dump(dacite_to_dict(config), stream)
