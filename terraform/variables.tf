variable "AWS_ACCESS_KEY_ID_" {
    description = "AWS access key ID"
    type        = string
}

variable "AWS_SECRET_ACCESS_KEY_" {
    description = "AWS secret access key"
    type        = string
}

variable "BUCKET_NAME" {
    description = "bucket name"
    type        = string
}

variable "DB_HOST" {
    description = "DB host name"
    type = string 
}

variable "DB_NAME" {
    description = "Name of database"
    type = string
}

variable "DB_PASSWORD" {
    description = "Password to access database"
    type = string 
}

variable "DB_USER" {
    description = "Specific user of the database"
    type = string 
}

variable "DB_PORT" {
    description = "Port to access database"
    type = number
}

variable "DB_SCHEMA" {
    description = "Relevant database schema"
    type = string
}