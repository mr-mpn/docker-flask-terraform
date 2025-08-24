# Output important resource information
output "ecr_repository_url" {
  description = "ECR repository URL for the Flask app"
  value       = aws_ecr_repository.flask_app.repository_url
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.flask_cluster.name
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.eight_digit.name
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

# Private subnet outputs removed - simplified architecture