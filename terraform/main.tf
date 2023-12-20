provider "aws" {
  region = "eu-west-2" 
}

# Create ECR repository 



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
    function_name                  = "c9-butterflies-data-management-terraform"
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
  name                = "c9-butterflies-data-management-schedule-terraform"
  flexible_time_window {
    mode = "OFF"
  }
  schedule_expression = "cron(15 0 * * ? *)"  
  target {
    arn  = aws_lambda_function.data_management_lambda.arn
    role_arn = aws_iam_role.scheduler.arn 
        }
}
