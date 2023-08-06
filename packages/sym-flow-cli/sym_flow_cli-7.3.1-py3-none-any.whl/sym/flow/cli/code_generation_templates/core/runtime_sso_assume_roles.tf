resource "aws_iam_policy" "sso_assume_roles" {
  name = "${local.role_name}_SSOAssumeRoles"
  path = "/sym/"

  description = "This policy allows the Sym Runtime to assume roles in the /sym/ path in your AWS SSO account."
  policy = jsonencode({
    Statement = [{
      Action   = "sts:AssumeRole"
      Effect   = "Allow"
      Resource = ["arn:aws:iam::${data.aws_caller_identity.sso.account_id}:role/sym/*"]
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "attach_assume_roles_sso" {
  policy_arn = aws_iam_policy.sso_assume_roles.arn
  role       = aws_iam_role.sym_runtime_connector_role.name
}
