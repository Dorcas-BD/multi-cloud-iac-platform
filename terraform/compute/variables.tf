variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"  
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "iac-platform"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"  # Free tier eligible
}

variable "desired_capacity" {
  description = "Desired number of instances"
  type        = number
  default     = 1
}

variable "min_size" {
  description = "Minimum number of instances"
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Maximum number of instances"
  type        = number
  default     = 3
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed to SSH (use your IP)"
  type        = string
  default     = "0.0.0.0/0"  # Change this to your IP for security
}