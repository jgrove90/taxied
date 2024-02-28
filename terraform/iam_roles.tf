resource "aws_iam_role" "fargate_role" {
  name = "fargate_s3_access_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "fargate_s3_access_policy" {
  name   = "fargate_s3_access_policy"
  role   = aws_iam_role.fargate_role.id
  policy = data.aws_iam_policy_document.s3_policy.json
}