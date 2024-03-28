resource "aws_iam_role" "fargate_role" {
  name = "fargate_access_role"

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

# resource "aws_iam_role_policy" "fargate_s3_access_policy" {
#   name   = "fargate_s3_access_policy"
#   role   = aws_iam_role.fargate_role.id
#   policy = data.aws_iam_policy_document.s3_policy.json
# }


resource "aws_iam_role_policy_attachment" "fargate_s3_access_policy" {
  role   = aws_iam_role.fargate_role.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "fargate_execution_role_policy" {
  role       = aws_iam_role.fargate_role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}