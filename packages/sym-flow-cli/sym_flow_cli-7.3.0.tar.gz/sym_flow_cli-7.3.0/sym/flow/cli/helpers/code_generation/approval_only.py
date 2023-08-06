import importlib.resources as pkg_resources

from sym.flow.cli.code_generation_templates import (  # import the *package* containing the tf files
    flows,
)

from .core import FlowGeneration


class ApprovalFlowGeneration(FlowGeneration):
    @property
    def impl_filepath(self) -> str:
        return f"{self.working_directory}/impls/approval_{self.flow_resource_name}_impl.py"

    @classmethod
    def get_flow_tf_filepath(cls, flow_name: str, working_directory: str = ".") -> str:
        return f"{working_directory}/approval_{cls._get_flow_resource_name(flow_name)}.tf"

    def generate(self) -> None:
        """Generate the impl and Terraform files required to configure an Approval-Only Flow."""
        # Generate any core requirements that don't already exist in this directory.
        self._create_impls_directory()

        # Generate the Approval-Only-specific files.
        self._generate_impl(
            source_file="approval_impl.txt",
            replacements={"SYM_TEMPLATE_VAR_IMPL_PATH": f"approval_{self.flow_resource_name}_impl.py"},
        )

        with open(self.flow_tf_filepath, "w") as f:
            approval_tf = pkg_resources.read_text(flows, "approval_only.tf")
            approval_tf = self._format_template(approval_tf)
            f.write(approval_tf)
