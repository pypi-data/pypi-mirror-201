import importlib.resources as pkg_resources
import os
from pathlib import Path
from typing import Optional

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation_templates import (  # import the *package* containing the tf files
    flows,
)

from .aws import AWSFlowGeneration


class AWSLambdaFlowGeneration(AWSFlowGeneration):
    REQUIRES_AWS: bool = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.aws_region: Optional[str] = self._get_aws_region()

    @property
    def impl_filepath(self) -> str:
        return f"{self.working_directory}/impls/aws_lambda_{self.flow_resource_name}_impl.py"

    @property
    def lambda_src_directory(self) -> str:
        return f"{self.working_directory}/{self.flow_resource_name}_lambda_src"

    @classmethod
    def get_flow_tf_filepath(cls, flow_name: str, working_directory: str = ".") -> str:
        return f"{working_directory}/aws_lambda_{cls._get_flow_resource_name(flow_name)}.tf"

    def generate(self) -> None:
        """Generate the impl and Terraform files required to configure an AWS Lambda Flow."""
        if Path(self.lambda_src_directory).exists():
            cli_output.fail(
                f"The directory or file {self.lambda_src_directory} already exists.",
                hint=f"Please try again with a unique Flow name.",
            )

        # Generate any core requirements that don't already exist in this directory.
        self._generate_runtime_tf()
        self._create_impls_directory()
        self._add_runtime_id_to_environment()

        # Generate the AWS Lambda specific files.
        self._generate_impl(source_file="lambda_impl.txt")

        with open(self.flow_tf_filepath, "w") as f:
            aws_lambda_tf = pkg_resources.read_text(flows, "aws_lambda.tf")
            aws_lambda_tf = self._format_template(aws_lambda_tf)
            f.write(aws_lambda_tf)

        os.makedirs(self.lambda_src_directory)
        with open(f"{self.lambda_src_directory}/handler.py", "w") as f:
            # Note: The handler file is stored as a `.txt` resource because PyOxidizer (the tool used to package symflow CLI)
            # Does NOT support reading `.py` files with `importlib.resources`
            # https://github.com/indygreg/PyOxidizer/issues/237
            aws_lambda_handler = pkg_resources.read_text(flows, "lambda_handler.txt")
            aws_lambda_handler = self._format_template(
                aws_lambda_handler,
                {
                    "SYM_TEMPLATE_VAR_LAMBDA_SOURCE_DIRECTORY": f"{self.flow_resource_name}_lambda_src",
                },
            )
            f.write(aws_lambda_handler)
