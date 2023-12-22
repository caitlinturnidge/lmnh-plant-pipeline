To create cloud resources

## Requirements

Add these environment variables to a `terraform.tfvars` file

- BUCKET_NAME
- AWS_ACCESS_KEY_ID_
- AWS_SECRET_ACCESS_KEY_
- DB_HOST
- DB_NAME
- DB_PASSWORD
- DB_PORT
- DB_SCHEMA
- DB_USER

## Running main.tf

- Run `terraform init`
- Run `terraform apply` to create all cloud resources
- Run `terraform destroy` to delete all cloud resources

## Assumptions

- The ECR images for daily pipeline, minute pipeline and the dashboard already exist. 