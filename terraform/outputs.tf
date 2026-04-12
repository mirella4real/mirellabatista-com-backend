output "api_endpoint" {
  description = "The URL of the API Gateway endpoint"
  value       = "${aws_apigatewayv2_api.visitor_counter.api_endpoint}/count"
}

output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.visitor_counter.function_name
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table"
  value       = aws_dynamodb_table.visitor_counter.name
}