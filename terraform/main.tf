provider "aws" {
  region = "eu-west-2" 
}

# Stuff that exists already
data "aws_vpc" "c9-vpc" {
    id = "vpc-04423dbb18410aece"
}

data "aws_ecs_cluster" "c9-cluster" {
    cluster_name = "c9-ecs-cluster"
}


# Create ECR repository 

resource "aws_ecr_repository" "dashboard-repo" {
  name                 = "c9-butterflies-dashboard"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}


# # Create task definition 

resource "aws_ecs_task_definition" "dashboard-taskdef" {
    family = "c9-butterflies-dashboard-taskdef"
    requires_compatibilities = ["FARGATE"]
    network_mode = "awsvpc"
    container_definitions = jsonencode([
    {
      "name": "c9-butterflies-dashboard",
      "image": "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-butterflies-dashboard-repo:latest",
      essential = true
      environment = [
        { name = "DB_NAME", value = "${var.DB_NAME}" },
        { name = "DB_USER", value = "${var.DB_USER}" },
        { name = "DB_PASSWORD", value = "${var.DB_PASSWORD}" },
        { name = "DB_PORT", value = "${var.DB_PORT}" },
        { name = "DB_HOST", value = "${var.DB_HOST}" },
        { name = "DB_SCHEMA", value = "${var.DB_SCHEMA}" }
      ]
      portMappings = [
        {
          name          = "c9-butterflies-dashboard-8501-tcp"
          containerPort = 8501
          hostPort      = 8501
          "protocol": "tcp",
          "appProtocol": "http"
        }
      ]
    }])
    cpu = 1024
    memory = 3072
    execution_role_arn = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"

}

resource "aws_ecs_service" "dashboard-service" {
    name = "c9-butterflies-dashboard-service"
    cluster = data.aws_ecs_cluster.c9-cluster.id
    task_definition = "arn:aws:ecs:eu-west-2:129033205317:task-definition/c9-butterflies-dashboard-taskdef:1"
    desired_count = 1
    launch_type = "FARGATE"
    network_configuration {
      subnets = ["subnet-0d0b16e76e68cf51b", "subnet-081c7c419697dec52", "subnet-02a00c7be52b00368"]
      security_groups = ["sg-046ca8117d547057e"]
      assign_public_ip = true
    }
}


# Create a role for the lambda functions

resource "aws_iam_role" "lambda-role" {
  name = "allow-lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Create Lambda function

resource "aws_lambda_function" "data_management_lambda" {
    function_name                  = "c9-butterflies-data-management"
    role                           = aws_iam_role.lambda-role.arn 
    image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-butterflies-data-management:latest"
    package_type = "Image"

    environment {
        variables = {
            AWS_ACCESS_KEY_ID_=var.AWS_ACCESS_KEY_ID_
            AWS_SECRET_ACCESS_KEY_=var.AWS_SECRET_ACCESS_KEY_
            BUCKET_NAME=var.BUCKET_NAME
        }
    }
    timeout = 10
  }


# Create a role for the Eventbridge scheduler

resource "aws_iam_role" "scheduler" {
  name = "cron-scheduler-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = ["scheduler.amazonaws.com"]
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}


# Create the Eventbridge scheduler

resource "aws_scheduler_schedule" "data_management_event" {
  name                = "c9-butterflies-data-management-schedule"
  flexible_time_window {
    mode = "OFF"
  }
  schedule_expression = "cron(15 0 * * ? *)"  
  target {
    arn  = aws_lambda_function.data_management_lambda.arn
    role_arn = aws_iam_role.scheduler.arn 
        }
}


# Terraform Resources for the minute-interval Pipeline

# Lambda function that runs the pipeline every minute

resource "aws_lambda_function" "pipeline-lambda" {
  function_name = "c9-butterflies-pipeline-lambda"
  role = aws_iam_role.lambda-role.arn
  image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-butterflies-pipeline:latest"
  package_type = "Image"
  timeout = 540
  memory_size = 512
  environment {
    variables = {
      AWS_ACCESS_KEY_ID_=var.AWS_ACCESS_KEY_ID_
      AWS_SECRET_ACCESS_KEY_=var.AWS_SECRET_ACCESS_KEY_
      BUCKET_NAME=var.BUCKET_NAME
      DB_HOST=var.DB_HOST
      DB_NAME=var.DB_NAME
      DB_PASSWORD=var.DB_PASSWORD
      DB_PORT=var.DB_PORT
      DB_SCHEMA=var.DB_SCHEMA
      DB_USER=var.DB_USER
    }
  }
}


# EventBridge Schedule that runs the pipeline lambda every minute

resource "aws_scheduler_schedule" "pipeline-event" {
  name                = "c9-butterflies-pipeline-schedule"
  flexible_time_window {
    mode = "OFF"
  }
  schedule_expression = "cron(* * * * ? *)"  
  target {
    arn  = aws_lambda_function.pipeline-lambda.arn
    role_arn = aws_iam_role.scheduler.arn 
        }
}
