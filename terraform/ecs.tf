resource "aws_ecs_cluster" "data_pipeline" {
  name = "data_pipeline"
}

resource "aws_ecs_task_definition" "data_pipeline" {
  family                   = "data_pipeline_task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.fargate_role.arn
  task_role_arn            = aws_iam_role.fargate_role.arn


  container_definitions = jsonencode([{
    name  = var.container_name
    image = "<aws_id>.dkr.ecr.us-west-2.amazonaws.com/${var.container_name}:latest"
    portMappings = [{
      containerPort = 80
      hostPort      = 80
      protocol      = "tcp"
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.log_group.name
        "awslogs-region"        = "us-west-2"
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "service" {
  name            = "container-service"
  cluster         = aws_ecs_cluster.data_pipeline.id
  task_definition = aws_ecs_task_definition.data_pipeline.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.private_subnet.id]
    security_groups  = [aws_security_group.main.id]
    assign_public_ip = false
  }


  desired_count = 1
}