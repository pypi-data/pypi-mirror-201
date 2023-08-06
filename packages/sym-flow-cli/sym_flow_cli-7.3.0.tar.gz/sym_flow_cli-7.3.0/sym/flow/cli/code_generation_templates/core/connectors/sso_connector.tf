############ AWS SSO Connector Setup ##############
# Set up a different AWS provider for the SSO connector.
# This is necessary in the typical setup where Sym resources are provisioned in
# a different AWS account than the AWS IAM Identity Center (SSO) instance.
# If you do not do so yet, we recommend using a delegated administration account to manage your SSO instance,
# as described here: https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html
provider "aws" {
  alias  = "sso"
  region = local.aws_region

  # This profile should be configured permissions to read and write IAM Roles in your SSO Management Account,
  # and permissions to read SSO resources.
  profile = "sym-sso-provisioning"
}

# Get the AWS Account ID for the SSO profile.
data "aws_caller_identity" "sso" {
  provider = aws.sso
}

# The AWS IAM Resources that enable Sym to manage SSO Permission Sets
module "sso_connector" {
  source  = "symopsio/sso-connector/aws"
  version = ">= 1.0.0"

  # Provision the SSO connector in the AWS account where your AWS
  # SSO instance lives.
  providers = {
    aws = aws.sso
  }

  environment       = local.environment_name
  runtime_role_arns = [aws_iam_role.sym_runtime_connector_role.arn]
}

# The Integration your Strategy uses to manage SSO Permission Sets
resource "sym_integration" "aws_sso_context" {
  type        = "permission_context"
  name        = "${local.environment_name}-aws-sso-context"
  external_id = module.sso_connector.settings["instance_arn"]
  settings    = module.sso_connector.settings
}
