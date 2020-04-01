resource "aws_s3_bucket" "app_bucket" {
  bucket = "${var.project_name}-${var.environment}"
  acl = "public-read"

  tags = {
    "covidapp:environment" = var.environment
    "covidapp:project" = var.project_name
    "covidapp:alias" = "app"
  }
}
