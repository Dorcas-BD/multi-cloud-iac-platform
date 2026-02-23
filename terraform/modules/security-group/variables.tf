variable "name_prefix" {
  description = "Prefix for security group name"
  type        = string
}

variable "description" {
  description = "Security group description"
  type        = string
  default     = "Managed by Terraform"
}

variable "vpc_id" {
  description = "VPC ID where security group will be created"
  type        = string
}

variable "ingress_rules" {
  description = "List of ingress rules"
  type        = list(any)
  default     = []
}

variable "egress_rules" {
  description = "List of egress rules"
  type        = list(any)
  default     = []
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}