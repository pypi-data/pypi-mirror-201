import importlib.resources as pkg_resources
import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation_templates import (  # import the *package* containing the tf files
    core,
    flows,
)
from sym.flow.cli.errors import CliError
from sym.flow.cli.helpers.version import get_current_version

# Slugs are only allowed to have letters, numbers, and dashes. This regex matches
# all character that are NOT those.
slug_disallowed_pattern = re.compile(r"[^a-zA-Z\d-]+")


class CodeGenerationError(CliError):
    """Generic class for code generation errors."""


class MissingConfig(CodeGenerationError):
    def __init__(self, file_name: str, name: str) -> None:
        super().__init__(f"Could not generate {file_name}. A value for {name} is required, but was not given.")


class FlowGeneration(ABC):
    """Core logic for generating Flow configuration with `symflow generate`."""

    REQUIRES_AWS: bool = False

    def __init__(self, flow_name: str, directory: str = ".") -> None:
        self.flow_name = flow_name
        self.generation_time = datetime.utcnow()
        self.symflow_version = str(get_current_version())
        self.working_directory = directory

        # Subclasses will choose whether they need runtime.tf or not, so we may
        # not need aws_region. Set to None here so it's never undefined.
        self.aws_region: Optional[str] = None

    @property
    def flow_resource_name(self) -> str:
        """The name of the Flow used as a slug may have dashes, but used as a
        file name or Terraform resource should have underscores.
        """
        return self._get_flow_resource_name(self.flow_name)

    @property
    def secrets_tf_filepath(self):
        return f"{self.working_directory}/secrets.tf"

    @property
    def runtime_tf_filepath(self):
        return f"{self.working_directory}/runtime.tf"

    @property
    def environment_tf_filepath(self):
        return f"{self.working_directory}/environment.tf"

    @property
    def flow_tf_filepath(self) -> str:
        """Full path to the main Terraform file that will be generated for this Flow."""
        return self.get_flow_tf_filepath(self.flow_name, self.working_directory)

    @property
    def impls_filepath(self):
        return f"{self.working_directory}/impls"

    @property
    @abstractmethod
    def impl_filepath(self) -> str:
        """Full path to the implementation file that will be generated for this Flow."""

    @classmethod
    def flow_already_exists(cls, flow_name: str, working_directory: str = ".") -> bool:
        """Check if a Flow with the given name already exists.

        For now, we just check the file name that we would generate vs. any files
        that already exist. In the future, we may want to check against the API or
        Terraform state [SYM-4671].

        Args:
            flow_name: The name of the Flow that would be created.
            working_directory: The directory to check for existing files in.
        """
        return Path(cls.get_flow_tf_filepath(flow_name, working_directory)).exists()

    @classmethod
    @abstractmethod
    def get_flow_tf_filepath(cls, flow_name: str, working_directory: str = ".") -> str:
        """Construct the path to this Flow's main Terraform file that will be generated."""

    @classmethod
    def _get_flow_resource_name(cls, flow_name: str) -> str:
        return flow_name.replace("-", "_").lower()

    @abstractmethod
    def generate(self) -> None:
        """Generate all files required to configure this particular type of
        Flow.
        """

    def final_instructions(self) -> None:
        """Optionally output instructions after code generation is complete for
        for the user to follow now or after `terraform apply` (e.g. instructions
        on how to set the value for a new AWS Secretsmanager Secret).
        """

    def _get_aws_region(self) -> Optional[str]:
        """If a runtime.tf file would need to be generated, prompt the user for
        the AWS region to use.
        """

        if not Path(self.runtime_tf_filepath).is_file():
            return click.prompt(
                click.style("What AWS region are your resources in?", bold=True), type=str, default="us-east-1"
            )

    def _generate_runtime_tf(self) -> None:
        """Generate runtime.tf if it does not already exist."""

        if not Path(self.runtime_tf_filepath).is_file():
            if not self.aws_region:
                raise MissingConfig(file_name="runtime.tf", name="aws_region")

            runtime_tf = pkg_resources.read_text(core, "runtime.tf")

            with open(self.runtime_tf_filepath, "w") as f:
                runtime_tf = self._format_template(runtime_tf, {"SYM_TEMPLATE_VAR_AWS_REGION": self.aws_region})
                f.write(runtime_tf)

    def _generate_secrets_tf(self) -> None:
        """Generate secrets.tf if it does not already exist."""

        if not Path(self.secrets_tf_filepath).is_file():
            secrets_tf = pkg_resources.read_text(core, "secrets.tf")

            with open(self.secrets_tf_filepath, "w") as f:
                secrets_tf = self._format_template(secrets_tf)
                f.write(secrets_tf)

    def _generate_impl(self, source_file: str = "impl.txt", replacements: Optional[dict] = None) -> None:
        """Generate the impl file for this Flow."""
        replacements = replacements or {}
        with open(self.impl_filepath, "w") as f:
            # Note: The impl file is stored as a `.txt` resource because PyOxidizer (the tool used to package symflow CLI)
            # Does NOT support reading `.py` files with `importlib.resources`
            # https://github.com/indygreg/PyOxidizer/issues/237
            #
            # However, we don't care about reading the source code, we simply need to pull the text file and write it
            # to the filesystem with a `.py` extension. As a workaround, we have stored `impl.py` as `impl.txt` in the
            # code_generation_templates.flows package so that we can read it with importlib.resources.
            impl_txt = pkg_resources.read_text(flows, source_file)
            impl_txt = self._format_template(impl_txt, replacements)
            f.write(impl_txt)

    def _create_impls_directory(self) -> None:
        """Create the impls directory to contain all Flow impls if it does not
        already exist.
        """

        if not Path(self.impls_filepath).is_dir():
            os.makedirs(self.impls_filepath)

    def _format_template(self, template: str, replacements: Optional[dict] = None) -> str:
        """For each key in `replacements`, replace that value in `template` with
        the value in `replacements`. Always replaces template vars common to all
        Flows (symflow version, generation time, Flow name)
        """
        all_replacements = {
            "SYM_TEMPLATE_VAR_SYMFLOW_VERSION": self.symflow_version,
            "SYM_TEMPLATE_VAR_GENERATION_TIME": self.generation_time.strftime("%Y-%m-%d at %H:%M"),
            "SYM_TEMPLATE_VAR_FLOW_RESOURCE_NAME": self.flow_resource_name,
            "SYM_TEMPLATE_VAR_FLOW_NAME": self.flow_name,
        }

        if replacements:
            all_replacements.update(replacements)

        for key, value in all_replacements.items():
            template = template.replace(key, value)

        return template


def get_valid_slug(label: str, slug_candidate: str) -> Optional[str]:
    """Interactively validate that a given string could be used as a slug and/or as a Terraform
    resource name. Outputs an error message to the command line if not.

    Args:
        label: How to refer to the value the `slug_candidate` will be used for.
        slug_candidate: The string to validate.

    Returns:
        The `slug_candidate` if it's valid or the user confirmed a valid suggestion.
        None otherwise.
    """

    # Look for any disallowed characters in the given slug_candidate.
    if slug_disallowed_pattern.search(slug_candidate):
        # Replace any disallowed characters with dashes and remove any from the start or end.
        formatted_slug_candidate = slug_disallowed_pattern.sub("-", slug_candidate).strip("-")

        # It's possible there was nothing valid to work with, in which case just reject the name outright.
        if not formatted_slug_candidate:
            return None

        # Give the user a chance to accept the newly formatted slug. If they accept, great. If not, return None
        # so we can prompt again for a totally new name.
        if cli_output.error_confirm(
            f'{label} can only contain letters, numbers, and dashes. Use "{formatted_slug_candidate}" instead?'
        ):
            return formatted_slug_candidate

        # Trigger a re-prompt for the slug
        return None

    # The slug will often be used in combination with some other identifying text (e.g. "SLUG-okta-group").
    # Resources like Targets have a slug limit of 55 characters (and -okta-group is 11), so 32 should give us a
    # little bit of wiggle room.
    if len(slug_candidate) > 32:
        cli_output.error(f"{label} cannot be longer than 32 characters. Please enter a shorter name.")

        # Trigger a re-prompt for the Flow name
        return None

    return slug_candidate
