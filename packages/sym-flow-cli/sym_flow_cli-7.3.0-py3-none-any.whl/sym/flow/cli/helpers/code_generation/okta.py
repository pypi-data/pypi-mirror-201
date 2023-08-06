import importlib.resources as pkg_resources
from typing import Optional

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation_templates import (  # import the *package* containing the tf files
    flows,
)

from .core import FlowGeneration


class OktaFlowGeneration(FlowGeneration):
    REQUIRES_AWS: bool = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # We just want one newline before we start prompting, not a newline each time we re-prompt.
        click.echo("")

        self.domain_name: str = ""
        while not self.domain_name:
            domain_name: str = click.prompt(
                f'{click.style("What is your Okta domain?", bold=True)} {click.style("(e.g. my-org.okta.com)", dim=True, italic=True)}',
                type=str,
            )

            if domain_name.startswith("http") or domain_name.startswith("www"):
                domain_candidate = domain_name.replace("http://", "").replace("https://", "").replace("www.", "")
                if cli_output.error_confirm(
                    f'Okta domains must be in the format "my-org.okta.com". Use "{domain_candidate}" instead?'
                ):
                    self.domain_name = domain_candidate
            else:
                self.domain_name = domain_name

        # Since we need both quotation marks, and we can't escape them in the f-string (backslashes not allowed), declare the example separately.
        group_id_example = click.style('(e.g. "00g12345abc")', dim=True, italic=True)
        self.group_id: str = click.prompt(
            f'{click.style("What is the Okta group ID you would like to manage with Sym?", bold=True)} {group_id_example}',
            type=str,
        )

        self.aws_region: Optional[str] = self._get_aws_region()

    @property
    def impl_filepath(self) -> str:
        return f"{self.working_directory}/impls/okta_{self.flow_resource_name}_impl.py"

    @classmethod
    def get_flow_tf_filepath(cls, flow_name: str, working_directory: str = ".") -> str:
        return f"{working_directory}/okta_{cls._get_flow_resource_name(flow_name)}.tf"

    def generate(self) -> None:
        """Generate the impl and Terraform files required to configure an Okta Flow."""
        # Generate any core requirements that don't already exist in this directory.
        self._generate_runtime_tf()
        self._generate_secrets_tf()
        self._create_impls_directory()

        # Generate the Okta-specific files.
        self._generate_impl()

        with open(self.flow_tf_filepath, "w") as f:
            okta_tf = pkg_resources.read_text(flows, "okta.tf")
            okta_tf = self._format_template(
                okta_tf,
                replacements={
                    "SYM_TEMPLATE_VAR_OKTA_DOMAIN": self.domain_name,
                    "SYM_TEMPLATE_VAR_OKTA_GROUP_ID": self.group_id,
                },
            )
            f.write(okta_tf)

    def final_instructions(self) -> None:
        cli_output.info(
            "\nAfter running `terraform apply`, set your Okta API Key using the AWS CLI and the following command:"
        )
        cli_output.actionable(
            f'aws secretsmanager put-secret-value --secret-id "sym/{self.flow_name}/okta-api-key" --secret-string "YOUR-OKTA-API-KEY"'
        )
