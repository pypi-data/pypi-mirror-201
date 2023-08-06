import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.errors import SymAPIRequestError
from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand


@click.command(cls=TrackedCommand, short_help="Check your stored auth token")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def status(options: GlobalOptions) -> None:
    """Check if you have an existing session that is still valid."""
    if options.access_token:
        check_status_by_sym_jwt(options.sym_api)
    else:
        check_status_by_config(options.sym_api)


def check_status_by_sym_jwt(api: SymAPI):
    """Validate that the environment variable SYM_JWT contains a valid JWT."""
    try:
        user_data = api.verify_login()
    except SymAPIRequestError:
        cli_output.fail("A server error has occurred, Please try again later.")

    if user_data.get("error") and user_data.get("message"):
        if user_data.get("code") == "Authentication:INVALID_JWT":
            # This specific error message is very generic, and the Bot Token has probably just expired.
            cli_output.fail(
                "Status check failed!",
                f"  {user_data['message']} Use `symflow tokens list` to make sure your token is still valid.",
            )
        else:
            cli_output.fail("Status check failed!", f"  {user_data['message']}")
    elif user_data.get("error"):
        # All Sym API errors should have a message field, but just in case...
        cli_output.fail(
            "Status check failed!",
            "   Please check the Sym documentation on Bot Users and Tokens at https://docs.symops.com/docs/using-bot-tokens",
        )

    org = user_data["organization"]
    username = user_data["username"]

    cli_output.success("✔️  Status check succeeded!")
    click.echo(
        f"   You are logged in to {click.style(org, bold=True)} as {click.style(username, bold=True)} via SYM_JWT."
    )


def check_status_by_config(api: SymAPI):
    """Validate that the User's auth token stored in config.yml is a valid JWT."""
    if not Config.is_logged_in():
        # If the User doesn't even have an auth token set, they are definitely not logged in.
        cli_output.fail("You are not currently logged in", "   Try running `symflow login`")

    email = Config.get_email()

    try:
        # Check the User's session with the Sym API. This will validate that the JWT is still valid,
        # and matches the email address that the User is logged in with.
        user_data = api.verify_login(email)
    except SymAPIRequestError:
        cli_output.fail("A server error has occurred, Please try again later.")

    if user_data.get("error") and user_data.get("message"):
        if user_data.get("code") == "Authentication:INVALID_JWT":
            # This specific error message is very generic, and the User probably just needs to log in again.
            cli_output.fail("Status check failed!", f"  {user_data['message']} Try running `symflow login`.")
        else:
            cli_output.fail("Status check failed!", f"  {user_data['message']}")
    elif user_data.get("error"):
        # All Sym API errors should have a message field, but just in case...
        cli_output.fail("Status check failed!", "   Try running `symflow login`.")

    org = user_data["organization"]
    username = user_data["username"]
    role = user_data["role"]

    cli_output.success("✔️  Status check succeeded!")
    # Not using cli_output here due to the complexity of the styling
    click.echo(
        f"   You are logged in to {click.style(org, bold=True)} as {click.style(username, bold=True)} (role: {click.style(role, bold=True)})."
    )
