output "vpc_id" {
  description = "VPC ID."
  value       = module.network.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs."
  value       = module.network.public_subnet_ids
}

output "logs_bucket_name" {
  description = "S3 bucket name for logs."
  value       = aws_s3_bucket.logsBucket.id
}
