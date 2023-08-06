import importlib.resources as pkg_resources
from abc import ABC
from pathlib import Path

import hcl2

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation_templates import (  # import the *package* containing the tf files
    core,
)
from sym.flow.cli.code_generation_templates.core import connectors
from sym.flow.cli.helpers.code_generation.core import FlowGeneration
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.terraform import (
    get_terraform_local_variable,
    get_terraform_module,
    get_terraform_resource,
)


class AWSFlowGeneration(FlowGeneration, ABC):
    """A superclass containing common utility methods needed for generating AWS-strategies"""

    REQUIRES_AWS: bool = True

    @property
    def connectors_tf_filepath(self) -> str:
        return f"{self.working_directory}/connectors.tf"

    def _append_connector_module(self, module_name: str):
        """
        Creates a `connectors.tf` if it does not yet exist, then appends the given connector module to the
        end of the file if the module does not already exist.
        Args:
            module_name: The name of the module (e.g. "iam_connector"). Should match the template file name as well.
        """
        # Create connectors.tf if it does not yet exist.
        if not Path(self.connectors_tf_filepath).is_file():
            base_connectors_tf = pkg_resources.read_text(connectors, "connectors.tf")
            with open(self.connectors_tf_filepath, "w") as f:
                base_connectors_tf = self._format_template(base_connectors_tf)
                f.write(base_connectors_tf)

        # Open connectors.tf in Read + Append mode
        with open(self.connectors_tf_filepath, "a+") as f:
            # Ensure that we read from the beginning of the file. "a+" can have different behavior
            # depending on the OS.
            f.seek(0)
            connectors_tf = hcl2.load(f)

            # If the module does not already exist in connectors.tf, append it.
            if not get_terraform_module(connectors_tf, module_name):
                module_contents = pkg_resources.read_text(connectors, f"{module_name}.tf")
                f.write("\n")
                f.write(module_contents)

    def _append_sym_runtime(self, environment_name: str):
        """Parses the runtime.tf file and adds a sym_runtime resource to the end if it does not yet exist."""
        sym_runtime = pkg_resources.read_text(core, "sym_runtime.tf")
        sym_runtime = self._format_template(sym_runtime, {"SYM_TEMPLATE_VAR_ENVIRONMENT_NAME": environment_name})

        # Open the file in Read + Append mode
        with open(self.runtime_tf_filepath, "a+") as f:
            # Ensure that we read from the beginning of the file. "a+" can have different behavior
            # depending on the OS.
            f.seek(0)
            # Parse the existing runtime.tf file into a dict
            runtime_tf = hcl2.load(f)

            # Check to see if a sym_runtime resource is already defined, and append one if not.
            if not get_terraform_resource(runtime_tf, "sym_runtime", environment_name):
                # Append a sym_runtime resource
                f.write("\n")
                f.write(sym_runtime)

    def _add_runtime_id_to_environment(self):
        # Parse the environment.tf file to see if we need to append a sym_runtime
        with open(self.environment_tf_filepath, "r") as f:
            environment_tf = hcl2.load(f)

        if not (sym_environment := get_terraform_resource(environment_tf, "sym_environment", "this")):
            cli_output.fail(
                "The sym_environment.this resource is missing in environment.tf",
                hint=f"To manually configure this resource, check out https://docs.symops.com/docs/aws",
            )

        if not (environment_name := get_terraform_local_variable(environment_tf, "environment_name")):
            cli_output.fail(
                "The environment_name local variable is missing in environment.tf",
                hint=f"To manually configure this resource, check out https://docs.symops.com/docs/aws",
            )

        if not isinstance(environment_name, str):
            cli_output.fail(
                "The environment_name local variable in environment.tf must be a string.",
                hint=f"To manually configure this resource, check out https://docs.symops.com/docs/aws",
            )

        if not (slack_integration := get_terraform_resource(environment_tf, "sym_integration", "slack")):
            cli_output.fail(
                'The sym_integration resource of type "slack" is missing in environment.tf',
                hint=f"To manually configure this resource, check out https://docs.symops.com/docs/aws",
            )

        slack_workspace_id = slack_integration["external_id"]

        if slack_error_logger := get_terraform_resource(environment_tf, "sym_error_logger", "slack"):
            error_logger_destination = slack_error_logger["destination"]
        else:
            error_logger_destination = "#sym-errors"

        if not sym_environment.get("runtime_id"):
            # Add a sym_runtime resource
            self._append_sym_runtime(environment_name)

            # Add the runtime_id to the sym_environment
            with open(self.environment_tf_filepath, "w") as f:
                # Replace `environment.tf` with `environment_with_runtime.tf`, which contains runtime_id line
                environment_tf = pkg_resources.read_text(core, "environment_with_runtime.tf")
                environment_tf = self._format_template(
                    environment_tf,
                    {
                        "SYM_TEMPLATE_VAR_ENVIRONMENT_NAME": environment_name,
                        "SYM_TEMPLATE_VAR_SLACK_WORKSPACE_ID": slack_workspace_id,
                        "SYM_TEMPLATE_VAR_ERROR_LOGGER_DESTINATION_ID": error_logger_destination,
                        "SYM_TEMPLATE_VAR_SYM_ORG_SLUG": Config.get_org().slug,
                    },
                )
                f.write(environment_tf)
