resource "aws_vpc" "mainVpc" {
  cidr_block = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "nimbuskart-vpc"
  }
}


resource "aws_internet_gateway" "mainIgw" {
  vpc_id = aws_vpc.mainVpc.id
  tags = {
    Name = "nimbuskart-igw"
  }
}

resource "aws_subnet" "publicSubnet" {
  vpc_id     = aws_vpc.mainVpc.id
  cidr_block = var.subnet_cidr
  availability_zone = var.availability_zone
  count = length(var.public_subnet_cidrs)
  map_public_ip_on_launch = true
  tags = {
    Name = "nimbuskart-public-subnet"
  }
}

resource "aws_route_table" "publicRouteTable" {
  vpc_id = aws_vpc.mainVpc.id
  tags = {
    Name = "nimbuskart-public-route-table"
  }
}




















