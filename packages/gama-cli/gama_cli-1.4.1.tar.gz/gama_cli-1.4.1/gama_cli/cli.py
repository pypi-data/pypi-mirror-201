from gama_cli.groups.attach import Attach
from gama_cli.groups.docker import Docker
from gama_cli.groups.git import Git
from gama_cli.groups.gs import Gs
from gama_cli.groups.misc import Misc
from gama_cli.groups.sim import Sim
from gama_cli.groups.vessel import Vessel
from gama_cli.groups.setup import Setup

import click


@click.group(help="""GAMA CLI""")
def cli():
    pass


Gs().create(cli)
Sim().create(cli)
Vessel().create(cli)
Docker().create(cli)
Git().create(cli)
Misc().create(cli)
Attach().create(cli)
Setup().create(cli)


if __name__ == "__main__":
    cli()
