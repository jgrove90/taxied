resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/ecs/${var.container_name}"
  retention_in_days = 14
}