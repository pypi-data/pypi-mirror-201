resource "sym_runtime" "SYM_TEMPLATE_VAR_ENVIRONMENT_NAME" {
  name = "SYM_TEMPLATE_VAR_ENVIRONMENT_NAME"

  # This tells the Sym Runtime to assume the IAM Role declared in runtime.tf
  # when executing AWS-related Access Strategies. It will be passed into the sym_environment
  # declared in the environment.tf file.
  context_id = sym_integration.runtime_context.id
}
