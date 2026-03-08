output "s3_bucket_name" {
  description = "Name of the S3 bucket for Terraform state"
  value       = aws_s3_bucket.terraform_state.id
}

output "dynamodb_table_name" {
  description = "Name of DynamoDB table for state locking"
  value       = aws_dynamodb_table.terraform_locks.id
}

output "backend_config" {
  description = "Backend configuration for other Terraform projects"
  value       = <<-EOT
    terraform {
      backend "s3" {
        bucket         = "${aws_s3_bucket.terraform_state.id}"
        key            = "path/to/your/statefile.tfstate"
        region         = "${var.aws_region}"
        dynamodb_table = "${aws_dynamodb_table.terraform_locks.id}"
        encrypt        = true
      }
    }
  EOT
}