resource "aws_vpc" "mainVpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = merge(var.tags, {
    Name = "nimbuskart-vpc"
  })
}


resource "aws_internet_gateway" "mainIgw" {
  vpc_id = aws_vpc.mainVpc.id
  tags = merge(var.tags, {
    Name = "nimbuskart-igw"
  })
}

resource "aws_subnet" "publicSubnet" {
  vpc_id                  = aws_vpc.mainVpc.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.azs[count.index]
  count                   = length(var.public_subnet_cidrs)
  map_public_ip_on_launch = true
  tags = merge(var.tags, {
    Name = "nimbuskart-public-subnet-${count.index + 1}"
  })
}

resource "aws_route_table" "publicRouteTable" {
  vpc_id = aws_vpc.mainVpc.id
  tags = merge(var.tags, {
    Name = "nimbuskart-public-route-table"
  })
}


resource "aws_route" "publicRoute" {
  route_table_id         = aws_route_table.publicRouteTable.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.mainIgw.id
}

resource "aws_route_table_association" "publicSubnetAssociation" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = aws_subnet.publicSubnet[count.index].id
  route_table_id = aws_route_table.publicRouteTable.id
}


resource "aws_security_group" "mainSecurityGroup" {
  name        = "nimbuskart-security-group"
  description = "Security group for Nimbuskart application"
  vpc_id      = aws_vpc.mainVpc.id
  tags = merge(var.tags, {
    Name = "nimbuskart-security-group"
  })


  ingress {
    description = "Allow HTTP traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTPS traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow SSH traffic"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
















