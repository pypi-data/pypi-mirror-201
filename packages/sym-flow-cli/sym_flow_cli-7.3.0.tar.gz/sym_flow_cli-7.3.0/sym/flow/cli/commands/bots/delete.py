import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.errors import SymAPIRequestError, UnknownBotError
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand
from sym.flow.cli.models import ServiceType


@click.command(cls=TrackedCommand, name="delete", short_help="Delete a Sym Bot User")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("username")
@click.option(
    "--force",
    is_flag=True,
    help="Delete the service immediately",
)
def bots_delete(options: GlobalOptions, username: str, force: bool) -> None:
    """
    Deletes a Bot User with the given username and revokes all their tokens.
    """

    # Prompt user to confirm
    if not force:
        click.confirm(
            "WARNING: This is a destructive action. \nAre you sure you want to continue?",
            abort=True,
            default=False,
        )

    payload = {
        "users": [
            {
                "identity": {
                    "service_type": ServiceType.SYM.type_name,
                    "matcher": {"username": username},
                },
            }
        ]
    }

    try:
        options.sym_api.delete_user(payload)
    except SymAPIRequestError as e:
        if e.response_code == 404:
            raise UnknownBotError(username)
    cli_output.success(f"Successfully deleted bot user {username}!")
