# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "EightDigit-VPC" }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = { Name = "EightDigit-IGW" }
}

# Public Subnets
resource "aws_subnet" "public" {
  count = length(var.public_subnets)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[count.index % length(data.aws_availability_zones.available.names)]
  tags = { Name = "EightDigit-Public-${count.index + 1}-${data.aws_availability_zones.available.names[count.index % length(data.aws_availability_zones.available.names)]}" }
}

# Private subnets removed - not needed for this simple web app architecture

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = { Name = "EightDigit-Public-RT" }
}

# Associate public subnets with route table
resource "aws_route_table_association" "public_assoc" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Private route table removed - not needed without private subnets

# Data for AZs
data "aws_availability_zones" "available" {}
