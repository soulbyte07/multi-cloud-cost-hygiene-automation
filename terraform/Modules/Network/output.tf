output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.mainVpc.id
}

output "public_subnet_ids" {
  description = "The IDs of the public subnets"
  value       = aws_subnet.publicSubnet[*].id
}

output "security_group_id" {
  description = "The ID of the security group"
  value       = aws_security_group.mainSecurityGroup.id
}
