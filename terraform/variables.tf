variable "region" {
  description = "AWS region (LocalStack default)."
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project tag value."
  type        = string
  default     = "NimbusKart"
}

variable "environment" {
  description = "Environment tag value."
  type        = string
  default     = "dev"
}

variable "owner" {
  description = "Owner tag value."
  type        = string
  default     = "cost-hygiene"
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks."
  type        = list(string)
  default     = ["10.20.1.0/24", "10.20.2.0/24"]
}


variable "azs" {
  description = "Availability zones for subnets and resources."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "ssh_cidr" {
  description = "CIDR allowed for SSH (port 22)."
  type        = string
  default     = "0.0.0.0/0"
}


variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.micro"
}

variable "instance_count" {
  description = "Number of web tier instances."
  type        = number
  default     = 2
}

variable "ami_id" {
  description = "AMI ID for EC2 instances (LocalStack placeholder)."
  type        = string
  default     = "ami-12345678"
}

variable "log_bucket_name" {
  description = "Name of the S3 bucket for logs."
  type        = string
  default     = "nimbuskart-logs-bucket"
}

variable "ebs_volume_size" {
  description = "Size of EBS volumes in GB."
  type        = number
  default     = 2
}

















