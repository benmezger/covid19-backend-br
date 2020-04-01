resource "aws_ecs_cluster" "cluster" {
  name = "${var.project_name}-${var.environment}"

  tags = {
    "covidapp:environment" = var.environment
    "covidapp:project" = var.project_name
    "covidapp:alias" = "cluster"
  }

  depends_on = [var.ecs_instance_role]
}

module "backend" {
  source = "./service"
  region = var.region
  environment = var.environment
  project_name = var.project_name
  vpc_id = var.vpc_id
  alias_name = "backend"
  cluster_id = aws_ecs_cluster.cluster.id
  domain = var.domains["backend"]
  has_service_discovery = false
  log_retention = 7
  task_count = 1
  container_port = 8000
  service_role = var.ecs_service_role
  lb_listener_http = aws_lb_listener.http_listener
  lb_listener_https = aws_lb_listener.https_listener
  task_definition_file = "${path.module}/task-definitions/backend.json"
  health_check_path = "/admin/login/?next=/admin/"
  container_env_vars = {
    environment: var.environment,
    django_debug: "False",
    app_bucket: var.app_bucket,
    django_secret_key: var.backend_secret_key,
    app_domain: var.domains["backend"],
    django_allowed_hosts: "*,",
    database_url: "postgres://${var.database["username"]}:${var.database["password"]}@${var.database["hostname"]}:5432/${var.database["name"]}"
  }
}
