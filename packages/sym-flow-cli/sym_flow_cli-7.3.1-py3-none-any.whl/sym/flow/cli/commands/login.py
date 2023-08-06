import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.login.login_flow import BrowserRedirectFlow
from sym.flow.cli.helpers.tracked_command import TrackedCommand


# Note: This command deliberately does not define `cls=TrackedCommand`, as we track symflow logins when we
# hit the auth/login API (sym_api.verify_login)
@click.command(short_help="Log in to your Sym account")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--port",
    default=11001,
    help="Port to use for the local webserver.",
    show_default=True,
)
@click.option(
    "--org-id",
    prompt="Org ID",
    default=lambda: Config.get_org_slug(),
    help="The ID of the Organization you want to log in to.",
)
def login(options: GlobalOptions, port: int, org_id: str) -> None:
    """Log in to your Sym account to authenticate with the Sym API. This is required to enable privileged actions
    within your Organization such as authoring Sym Flows or installing the Slack App.

    \b
    Example:
        `symflow login --org-id S-0FNWNPZVI4`
    """
    if options.access_token:
        cli_output.fail("SYM_JWT is set, unset SYM_JWT to log in as a regular user")

    org = options.sym_api.get_organization_from_slug(org_id)

    # Save the organization to config so it will be autopopulated the next time `symflow login` is called.
    Config.set_org(org)

    flow = BrowserRedirectFlow(port)
    flow.login(options, org)


@click.command(cls=TrackedCommand, short_help="Log out of your Sym account")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def logout(options: GlobalOptions) -> None:
    if not Config.is_logged_in() and not options.access_token:
        cli_output.fail("You are already logged out!")

    if options.access_token:
        cli_output.fail("You are logged in via SYM_JWT, you must unset SYM_JWT manually")

    if Config.is_logged_in():
        Config.logout()
        cli_output.success("✔️  You successfully logged out!")
