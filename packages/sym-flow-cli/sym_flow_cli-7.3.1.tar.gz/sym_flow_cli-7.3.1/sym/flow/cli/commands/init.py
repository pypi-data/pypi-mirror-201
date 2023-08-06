import importlib.resources as pkg_resources
import os
from datetime import datetime
from typing import Optional, cast

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation_templates import (
    core,  # import the *package* containing the tf files
)
from sym.flow.cli.errors import NotLoggedInError
from sym.flow.cli.helpers.code_generation.core import get_valid_slug
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand
from sym.flow.cli.helpers.version import get_current_version


@click.command(cls=TrackedCommand, short_help="Generate starter Terraform code")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--directory",
    help="The path to the directory where Terraform will be generated.",
)
@click.option(
    "--slack-workspace-id", "--workspace-id", help="The ID of the Slack workspace where you installed the Sym App."
)
@click.option(
    "--environment",
    help="A name describing the environment where your Flows will be deployed (e.g. prod, staging, sandbox).",
)
def init(
    options: GlobalOptions,
    directory: Optional[str] = None,
    slack_workspace_id: Optional[str] = None,
    environment: Optional[str] = None,
) -> None:
    """Generates the common Terraform configuration required to start building any Sym Flow.

    After running this command, run `symflow generate` inside the created directory to generate
    the code for your first Sym Flow.
    """
    if not Config.is_logged_in() or not (org := Config.get_org()):
        raise NotLoggedInError()

    cli_output.info(
        "\nWelcome to Sym! This command will generate a new directory containing the Terraform files needed "
        "to start building your first Sym Flow.\n",
    )

    if directory:
        directory = _get_valid_directory_path(directory=directory)

    while not directory:
        directory = click.prompt(
            click.style("What should we name the directory?", bold=True), type=str, prompt_suffix=""
        )
        directory = _get_valid_directory_path(directory=directory)

    if not slack_workspace_id:
        slack_workspace_id = cast(
            str,
            click.prompt(
                f"{click.style('Slack Workspace ID', bold=True)} {click.style('(You can find this in Slack by running /sym whoami)', dim=True, italic=True)}",
                type=str,
            ),
        )

    if environment:
        environment = get_valid_slug(label="Environment Name", slug_candidate=environment)

    while not environment:
        environment_candidate = cast(
            str,
            click.prompt(
                f"{click.style('Environment Name', bold=True)} {click.style('This is where your Sym Flows will be deployed (e.g. prod, staging, sandbox)', dim=True, italic=True)}",
                type=str,
                default="prod",
            ),
        )

        environment = get_valid_slug(label="Environment Name", slug_candidate=environment_candidate)

    # Create the directory
    os.makedirs(directory)

    # These files don't need any values substituted in them, and can just be copied over as-is.
    static_files = ["versions.tf", "README.md"]

    for output_file in static_files:
        template = pkg_resources.read_text(core, output_file)
        with open(f"{directory}/{output_file}", "w") as f:
            f.write(template)

    # Create the environment.tf file with Org ID, environment name, and workspace ID filled in
    environment_tf = pkg_resources.read_text(core, "environment.tf")
    with open(f"{directory}/environment.tf", "w") as f:
        environment_tf = environment_tf.replace("SYM_TEMPLATE_VAR_SYMFLOW_VERSION", str(get_current_version()))
        environment_tf = environment_tf.replace(
            "SYM_TEMPLATE_VAR_GENERATION_TIME", datetime.utcnow().strftime("%Y-%m-%d at %H:%M")
        )
        environment_tf = environment_tf.replace("SYM_TEMPLATE_VAR_ORG_ID", org.slug)
        environment_tf = environment_tf.replace("SYM_TEMPLATE_VAR_SLACK_WORKSPACE_ID", slack_workspace_id.upper())
        environment_tf = environment_tf.replace("SYM_TEMPLATE_VAR_ENVIRONMENT_NAME", environment)

        f.write(environment_tf)

    cli_output.info(
        "\nSuccessfully generated your Sym Terraform configuration! Run the following to add your first Flow:"
    )
    cli_output.actionable(f"cd {directory} && symflow generate")


def _get_valid_directory_path(directory: str) -> Optional[str]:
    """Checks if the directory path exists and returns None if it exists and the path if not.
    Also outputs an error message to the command line if it exists.

    Args:
        directory: The path to a directory.

    Returns:
        None if the directory exists, directory otherwise.
    """
    if os.path.exists(directory):
        cli_output.error(
            f"Looks like the directory '{directory}' already exists! Please provide the name for a new directory."
        )
        return None
    else:
        return directory
