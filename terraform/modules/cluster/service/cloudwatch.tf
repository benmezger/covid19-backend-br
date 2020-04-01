resource "aws_cloudwatch_log_group" "logs" {
  name = "${var.project_name}-${var.alias_name}-${var.environment}"
  retention_in_days = var.log_retention

  tags = {
    "covidapp:environment" = var.environment
    "covidapp:project" = var.project_name
    "covidapp:alias" = var.alias_name
  }
}
