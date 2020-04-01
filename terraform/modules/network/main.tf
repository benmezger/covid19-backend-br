resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = "true"

  tags = {
    Name = "${var.project_name}-${var.environment}-vpc"
    "covidapp:environment" = var.environment
    "covidapp:project" = var.project_name
    "covidapp:alias" = "network"
  }
}
