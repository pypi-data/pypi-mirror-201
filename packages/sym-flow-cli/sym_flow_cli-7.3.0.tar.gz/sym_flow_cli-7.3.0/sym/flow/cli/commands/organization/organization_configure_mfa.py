import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.constants import SYM_SUPPORT_EMAIL
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand

CONFIRM_TRUE_MESSAGE = (
    "\nWhen this requirement is set to `true`, MFA setup will be enforced across your organization. Users "
    "who do not have MFA set up will be prompted to set it up. When users log in to symflow CLI, "
    "they will be prompted to authenticate using their MFA device."
    "\n\nAre you sure you want to set the MFA requirement to `true`?"
)

CONFIRM_FALSE_MESSAGE = (
    "\nWhen this requirement is set to `false`, any users who already have MFA set up will still be "
    "prompted to use it when logging in to the symflow CLI. However, new users will not need to set "
    f"up MFA. If you would like to reset or remove a user's MFA device, please reach out to us "
    f"at {SYM_SUPPORT_EMAIL}."
    " \n\nAre you sure you want to set the MFA requirement to `false`?"
)


@click.command(cls=TrackedCommand, name="configure-mfa", short_help="Enable or disable MFA for your org")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("enabled", required=True, type=bool)
def configure_mfa(options: GlobalOptions, enabled: bool) -> None:
    if enabled:
        message = CONFIRM_TRUE_MESSAGE
    else:
        message = CONFIRM_FALSE_MESSAGE
    click.confirm(
        message,
        abort=True,
        default=False,
    )
    options.sym_api.configure_mfa(enabled)
    cli_output.success("MFA requirement updated successfully!")
