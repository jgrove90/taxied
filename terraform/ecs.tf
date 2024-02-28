resource "aws_ecs_cluster" "data_pipeline" {
  name = "data_pipeline"
}

resource "aws_ecs_task_definition" "data_pipeline" {
  family                   = "data-pipeline"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([{
    name  = var.container_name
    image = "${var.ecr_repo_name}/${var.container_name}:latest"
    portMappings = [{
      containerPort = 80
      hostPort      = 80
      protocol      = "tcp"
    }]
  }])
}

resource "aws_ecs_service" "service" {
  name            = "my-service"
  cluster         = aws_ecs_cluster.data_pipeline.id
  task_definition = aws_ecs_task_definition.data_pipeline.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.private_subnet.id]
    assign_public_ip = false
  }

  desired_count = 1
}