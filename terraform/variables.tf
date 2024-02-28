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

variable "private_subnet_cidrs" {
  type        = string
  description = "Private Subnet CIDR values"
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  type        = string
  description = "Availability Zone"
  default     = "us-west-2a"
}

variable "container_name" {
  type        = string
  description = "Name of the container"
  default     = "taxied"
}

variable "s3_bucket_name" {
  type        = string
  description = "Name of the S3 bucket"
  default     = "deltalake-taxied-1337"
}