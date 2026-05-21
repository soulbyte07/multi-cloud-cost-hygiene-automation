terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    apigateway     = "http://localhost:4566"
    cloudformation = "http://localhost:4566"
    cloudwatch     = "http://localhost:4566"
    dynamodb       = "http://localhost:4566"
    ec2            = "http://localhost:4566"
    iam            = "http://localhost:4566"
    kms            = "http://localhost:4566"
    lambda         = "http://localhost:4566"
    logs           = "http://localhost:4566"
    s3             = "http://localhost:4566"
    sns            = "http://localhost:4566"
    sqs            = "http://localhost:4566"
    sts            = "http://localhost:4566"
  }
}

locals {
  tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "ec2Instance" {
  count         = var.instance_count
  ami           = var.ami_id
  instance_type = var.instance_type

  subnet_id                   = module.network.public_subnet_ids[count.index]
  vpc_security_group_ids      = [module.network.security_group_id]
  associate_public_ip_address = true

  tags = merge(local.tags, {
    Name = "nimbuskart-ec2_instance-${count.index + 1}"
    Tier = "ec2_instance"
  })
}


resource "aws_s3_bucket" "logsBucket" {
  bucket = aws_s3_bucket.logsBucket.id

  tags = merge(local.tags, {
    Name = "nimbuskart-logs-bucket"
    Tier = "logs_bucket"
  })
}

resource "aws_s3_bucket_versioning" "logsBucketVersioning" {
  bucket = aws_s3_bucket.logsBucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "logsBucketLifecycle" {
  bucket = aws_s3_bucket.logsBucket.id

  rule {
    id     = "ExpireOldVersions"
    status = "Enabled"

    noncurrent_version_expiration {
      days = 30
    }
  }
}

resource "aws_ebs_volume" "ebsVolume" {
  count             = var.instance_count
  availability_zone = element(var.azs, count.index)
  size              = 20
  type              = "gp2"

  tags = merge(local.tags, {
    Name = "nimbuskart-ebs_volume-${count.index + 1}"
    Tier = "ebs_volume"
  })
}

module "network" {
  source = "./Modules/Network"

  vpc_cidr            = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
  azs                 = var.azs
  ssh_cidr            = var.ssh_cidr
  tags                = local.tags
}



















