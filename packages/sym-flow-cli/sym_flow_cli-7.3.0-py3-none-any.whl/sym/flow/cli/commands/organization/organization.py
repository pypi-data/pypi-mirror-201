import click

from sym.flow.cli.commands.organization.organization_configure_mfa import configure_mfa
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.group(name="organization", short_help="Perform operations on your Organization")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def organization(options: GlobalOptions) -> None:
    """Operations on Services"""


organization.add_command(configure_mfa)
