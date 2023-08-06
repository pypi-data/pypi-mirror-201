import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.tracked_command import TrackedCommand
from sym.flow.cli.version import __version__


@click.command(cls=TrackedCommand, short_help="Print the version")
def version() -> None:
    cli_output.info(__version__)
