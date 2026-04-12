variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB visitor counter table"
  type        = string
  default     = "visitor-counter"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "visitor-counter"
}