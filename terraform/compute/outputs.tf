output "autoscaling_group_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.web.name
}

output "launch_template_id" {
  description = "ID of the launch template"
  value       = aws_launch_template.web.id
}

output "security_group_id" {
  description = "ID of the web security group"
  value       = module.web_sg.security_group_id
}

output "ami_id" {
  description = "AMI ID being used"
  value       = data.aws_ami.amazon_linux.id
}