from pathlib import Path
from typing import Optional, Type

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.errors import NotLoggedInError
from sym.flow.cli.helpers.code_generation.approval_only import ApprovalFlowGeneration
from sym.flow.cli.helpers.code_generation.aws_iam import AWSIAMFlowGeneration
from sym.flow.cli.helpers.code_generation.aws_lambda import AWSLambdaFlowGeneration
from sym.flow.cli.helpers.code_generation.aws_sso import AWSSSOFlowGeneration
from sym.flow.cli.helpers.code_generation.core import FlowGeneration, get_valid_slug
from sym.flow.cli.helpers.code_generation.okta import OktaFlowGeneration
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand
from sym.flow.cli.helpers.utils import get_or_prompt

FLOW_TYPE_OPTIONS = ["okta", "approval-only", "aws-iam", "aws-lambda", "aws-sso"]


@click.command(cls=TrackedCommand, short_help="Generate Terraform to configure a Sym Flow.")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--directory",
    help="The path to the directory created by `symflow init`.",
    default=".",
)
@click.option(
    "--type",
    "type_",
    type=click.Choice(FLOW_TYPE_OPTIONS, case_sensitive=False),
    help="What type of Sym Flow to create.",
)
@click.option(
    "--flow-name",
    help="A unique name for this Sym Flow.",
)
def generate(options: GlobalOptions, directory: str, type_: str, flow_name: Optional[str] = None) -> None:
    """Generates all Terraform required to configure a Sym Flow.

    This command should be run inside the directory created by `symflow init`.
    """
    if not Config.is_logged_in() or not Config.get_org():
        raise NotLoggedInError()

    # If environment.tf and versions.tf are not both present, we can relatively safely assume that
    # the user isn't inside a directory created by `symflow init` because it would have generated them.
    directory_placeholder = "the current directory" if directory == "." else "the directory `" + directory + "`"
    if not Path(f"{directory}/environment.tf").is_file() or not Path(f"{directory}/versions.tf").is_file():
        cli_output.fail(
            "This command must be run inside a directory created by `symflow init`. Please run that command first.",
            hint=f"Hint: {directory_placeholder.capitalize()} must have `environment.tf` and `versions.tf` files.",
        )

    cli_output.info(
        f"\nWelcome to Sym! This command will generate new files required to configure a Sym Flow in {directory_placeholder}.\n",
    )

    if not type_:
        # If they passed in a type_, then we don't need to print this hint
        cli_output.warn(
            "If you don't see the Flow type you're looking for below, check out the docs here for a full list and how to configure them:",
        )
        cli_output.warn(click.style("https://docs.symops.com/docs/integrations-overview\n", bold=True))

    # Prompt for any values that weren't already passed in.
    type_ = get_or_prompt(
        type_,
        click.style("Please select the type of Flow you would like to create", bold=True),
        FLOW_TYPE_OPTIONS,
    )

    if type_ == "okta":
        generator_cls = OktaFlowGeneration
    elif type_ == "approval-only":
        generator_cls = ApprovalFlowGeneration
    elif type_ == "aws-iam":
        generator_cls = AWSIAMFlowGeneration
    elif type_ == "aws-lambda":
        generator_cls = AWSLambdaFlowGeneration
    elif type_ == "aws-sso":
        generator_cls = AWSSSOFlowGeneration
    else:
        # This should never happen, because the user chooses from a given list.
        # If we get here, we've done something wrong.
        cli_output.fail(
            f'Unknown Flow type: "{type_}". Please use `symflow generate --help` to see the list of available Flow types.'
        )

    # If the user used --flow-name to pass in a name, we need to do the same validation we'd do
    # if we were prompting for it.
    if flow_name:
        # This may set the flow_name back to None, if we need to re-prompt.
        flow_name = get_valid_flow_name(candidate=flow_name, generator_cls=generator_cls)

    while not flow_name:
        flow_name_candidate = click.prompt(
            f"{click.style('What would you like to name this Flow?', bold=True)} {click.style('This name should be unique', dim=True, italic=True)}",
            type=str,
        )

        flow_name = get_valid_flow_name(candidate=flow_name_candidate, generator_cls=generator_cls)

    cli_output.info(f'Generating a Sym Flow of type "{type_}" named "{flow_name}"...')

    generator = generator_cls(flow_name=flow_name, directory=directory)
    generator.generate()

    if type_ == "aws-sso":
        cli_output.info(
            f"\nSuccessfully generated your Terraform configuration!"
            f"\nMake sure you are authenticated with both your default AWS credentials and the '{AWSSSOFlowGeneration.SYM_SSO_PROFILE}' profile, then run the following:"
        )
    elif generator_cls.REQUIRES_AWS:
        cli_output.info(
            f"\nSuccessfully generated your Terraform configuration! Make sure you are authenticated to AWS, then run the following to check the configuration:"
        )
    else:
        cli_output.info(
            f"\nSuccessfully generated your Terraform configuration! Run the following to check the configuration:"
        )

    terraform_command = "terraform init && terraform plan"
    if directory != ".":
        terraform_command = f"cd {directory} && " + terraform_command
    cli_output.actionable(terraform_command)

    cli_output.info("\nWhen you are ready to apply your configuration, run the following:")

    cli_output.actionable("terraform apply")

    generator.final_instructions()

    cli_output.info(f"\nAfter everything is configured:")
    cli_output.actionable(f"Run /sym in Slack")
    cli_output.info(f"... to see your new Flow in action!")


def get_valid_flow_name(candidate: str, generator_cls: Type[FlowGeneration]) -> Optional[str]:
    """Interactively validate that a given string:

    - Could be used as a Flow slug
    - Could be used as a sym_flow Terraform resource name
    - Will not conflict with an existing Flow name

    Outputs errors to the command line if not, and prompts the user to confirm
    suggestions or overwrites if necessary.
    """

    flow_name = get_valid_slug(label="Flow name", slug_candidate=candidate)
    if flow_name:
        # No conflicts, we're good to go.
        if not generator_cls.flow_already_exists(flow_name):
            return flow_name

        # There is a conflict, so ask the user whether they want to overwrite. The default is "no".
        if cli_output.error_confirm(
            f'A Flow named "{flow_name}" already exists ({generator_cls.get_flow_tf_filepath(flow_name)}). Would you like to overwrite it?'
        ):
            # There was a conflict, but the user chose to overwrite.
            return flow_name

        # The user did not want to overwrite the existing Flow, so re-prompt.
        return None

    # If the flow_name was never valid, re-prompt.
    return None
