import importlib.resources as pkg_resources
import re
from typing import Optional

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation_templates import (  # import the *package* containing the tf files
    flows,
)

from .aws import AWSFlowGeneration


class AWSIAMFlowGeneration(AWSFlowGeneration):
    REQUIRES_AWS: bool = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.role_name: str = ""

        while not self.role_name:
            role_name = click.prompt(
                click.style("\nWhat is the AWS managed role you would like to provision?", bold=True),
                type=str,
                default="PowerUserAccess",
                prompt_suffix=click.style(
                    "\nYou can specify any AWS Managed Policy, but we’d suggest starting with one of the job "
                    "function-aligned policies listed at "
                    "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html",
                    fg="cyan",
                ),
            )
            if not self.is_valid_aws_role_name(role_name):
                cli_output.warn(
                    "The role name must only contain letters, numbers, or underscores, and must "
                    "start with a capital letter. For example, AmazonElasticMapReduceforEC2Role"
                )
            else:
                self.role_name = role_name

        self.aws_region: Optional[str] = self._get_aws_region()

    @property
    def impl_filepath(self):
        return f"{self.working_directory}/impls/aws_iam_{self.flow_resource_name}_impl.py"

    @classmethod
    def get_flow_tf_filepath(cls, flow_name: str, working_directory: str = ".") -> str:
        return f"{working_directory}/aws_iam_{cls._get_flow_resource_name(flow_name)}.tf"

    def is_valid_aws_role_name(self, string):
        # Matches PascalCase, plus underscores b/c of AWS role naming
        return bool(re.match(r"([A-Z]+[a-z0-9_]+)+", string))

    def generate(self) -> None:
        """Generate the impl and Terraform files required to configure an AWS IAM Flow."""
        # Generate any core requirements that don't already exist in this directory.
        self._generate_runtime_tf()
        self._create_impls_directory()
        self._add_runtime_id_to_environment()
        self._append_connector_module("iam_connector")

        # Generate the AWS IAM specific files.
        self._generate_impl()

        with open(self.flow_tf_filepath, "w") as f:
            aws_iam_tf = pkg_resources.read_text(flows, "aws_iam.tf")
            aws_iam_tf = self._format_template(
                aws_iam_tf,
                {
                    "SYM_TEMPLATE_VAR_IAM_ROLE_NAME": self.role_name,
                    "SYM_TEMPLATE_VAR_IAM_ROLE_ARN": f"arn:aws:iam::aws:policy/{self.role_name}",
                },
            )
            f.write(aws_iam_tf)
