output "input_bucket_name" {
  value       = aws_s3_bucket.input_bucket.id
  description = "Name of S3 input bucket"
}

output "output_bucket_name" {
  value       = aws_s3_bucket.output_bucket.id
  description = "Name of S3 output bucket"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.image_object_detection_table.id
  description = "Name of DynamoDB table"
}
