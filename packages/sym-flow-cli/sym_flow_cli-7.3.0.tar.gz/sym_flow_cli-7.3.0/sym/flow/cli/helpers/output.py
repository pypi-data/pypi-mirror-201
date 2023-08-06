"""CLI Helpers"""

import sys
from typing import Optional

import click


def success(message: str, newline=True):
    click.secho(message, fg="green", nl=newline)


def warn(message: str):
    click.secho(message, fg="yellow")


def info(message: str, bold=False):
    click.secho(message, bold=bold)


def actionable(message: str):
    """Print a message that we want the user to act on."""
    click.secho(message, bold=True, fg="cyan")


def error(message: str, color="red"):
    click.secho(message, fg=color, err=True)


# This function is for errors that are followed by program exit
def fail(
    message: str = "Something went wrong",
    hint: Optional[str] = "Please check the Sym documentation at https://docs.symops.com/",
):
    """Raise a usage error with a useful message"""
    click.secho(f"✖ {message}", fg="red", bold=True, err=True)

    if hint:
        click.secho(f"{hint}", fg="cyan")

    sys.exit(1)


def error_confirm(message: str, default: bool = False, **kwargs) -> bool:
    """Output an error message to the user and ask for confirmation.

    Example usage of this might be to accept a suggested fix for the error, or to
    continue anyway.

    Args:
        message: Full error + confirmation message to display to the user.

    Returns:
        Boolean indicating the user's response to the confirmation prompt.
    """

    return click.confirm(click.style(message, fg="red"), default=default, **kwargs)
