from gama_cli.groups.attach import Attach
from gama_cli.groups.docker import Docker
from gama_cli.groups.git import Git
from gama_cli.groups.gs import Gs
from gama_cli.groups.misc import Misc
from gama_cli.groups.sim import Sim
from gama_cli.groups.vessel import Vessel
from gama_cli.groups.setup import Setup
from gama_cli.helpers import is_dev_version, get_gama_version
from gama_cli.banner import get_banner
import click


def create_developer_mode_cli():
    @click.group(help=get_banner("Developer", get_gama_version()))
    def cli_dev_mode():
        pass

    Sim(cli_dev_mode)
    Docker(cli_dev_mode)
    Git(cli_dev_mode)
    Attach(cli_dev_mode)
    Setup(cli_dev_mode)
    Gs(cli_dev_mode, dev_mode=True)
    Vessel(cli_dev_mode, dev_mode=True)
    Misc(cli_dev_mode, dev_mode=True)
    return cli_dev_mode


def create_basic_mode_cli():
    @click.group(help=get_banner("User", get_gama_version()))
    def cli_user():
        pass

    Misc(cli_user, dev_mode=False)
    Vessel(cli_user, dev_mode=False)
    Gs(cli_user, dev_mode=False)
    return cli_user


def cli():
    if is_dev_version():
        create_developer_mode_cli()()
    else:
        create_basic_mode_cli()()


if __name__ == "__main__":
    cli()
