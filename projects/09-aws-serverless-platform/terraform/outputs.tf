output "api_endpoint" {
  value       = aws_apigatewayv2_api.http.api_endpoint
  description = "HTTP API endpoint"
}

output "dynamodb_table" {
  value       = aws_dynamodb_table.messages.name
  description = "Created DynamoDB table"
}
