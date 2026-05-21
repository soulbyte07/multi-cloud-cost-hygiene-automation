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

variable "vpc_cidr" {
  description = "VPC CIDR block."
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





















