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

resource "aws_lambda_function" "report_lambda" {
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



# Create Eventbridge schedular