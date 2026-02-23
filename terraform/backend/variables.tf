variable "aws_region" {
  description = "AWS region for backend resources"
  type        = string
  default     = "us-east-1"
}

variable "state_bucket_name" {
  description = "Name of S3 bucket for Terraform state"
  type        = string
  # Must be globally unique - add your name/random string
  default     = "terraform-state-yourname-12345"
}

variable "lock_table_name" {
  description = "Name of DynamoDB table for state locking"
  type        = string
  default     = "terraform-state-locks"
}