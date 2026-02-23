# This file creates the S3 bucket and DynamoDB table for Terraform state

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "IaC-Platform"
      ManagedBy   = "Terraform"
      Environment = "backend"
    }
  }
}

# S3 Bucket for Terraform State
resource "aws_s3_bucket" "terraform_state" {
  bucket = var.state_bucket_name
  
  # Prevent accidental deletion
  lifecycle {
    prevent_destroy = true
  }
}

# Enable versioning (keep history of state files)
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable encryption at rest
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# DynamoDB Table for State Locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = var.lock_table_name
  billing_mode = "PAY_PER_REQUEST"  # Only pay for what you use
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
  
  # Prevent accidental deletion
  lifecycle {
    prevent_destroy = true
  }
}