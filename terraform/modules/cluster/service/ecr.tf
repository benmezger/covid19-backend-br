resource "aws_ecr_repository" "ecr_repo" {
  name = "${var.project_name}-${var.alias_name}/${var.environment}"

  tags = {
    "covidapp:environment" = var.environment
    "covidapp:project" = var.project_name
    "covidapp:alias" = var.alias_name
  }
}
