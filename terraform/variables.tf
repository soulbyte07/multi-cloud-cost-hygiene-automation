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
