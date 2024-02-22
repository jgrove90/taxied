variable "aws_region" {
  description = "AWS region for the infrastructure"
  type        = string
  default     = "us-west-2"
}

variable "ecr_repo_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "my_repo"
}