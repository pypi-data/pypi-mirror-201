############ AWS IAM Connector Setup ##############
# The iam_connector module creates a new IAM Role with the permissions to add and remove users from IAM Groups.
module "iam_connector" {
  source  = "symopsio/iam-connector/aws"
  version = ">= 1.0.0"

  environment       = local.environment_name
  runtime_role_arns = [aws_iam_role.sym_runtime_connector_role.arn]
}

# The Integration your Strategy uses to manage IAM Groups
resource "sym_integration" "aws_iam_context" {
  type        = "permission_context"
  name        = "${local.environment_name}-aws-iam-context"
  external_id = module.iam_connector.settings.account_id
  settings    = module.iam_connector.settings
}
