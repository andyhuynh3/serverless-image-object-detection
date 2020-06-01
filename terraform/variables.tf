variable "aws_region" {
  default     = "us-west-2"
  type        = string
  description = "Name of AWS region to deploy resources to"
}

variable "aws_profile" {
  default     = "default"
  type        = string
  description = "Name of AWS profile used to deploy resources"
}

variable "dynamodb_table_name" {
  type        = string
  description = "Name of the DynamoDB table"
}

variable "dynamodb_table_billing_mode" {
  default     = "PAY_PER_REQUEST"
  type        = string
  description = "Billing method for DynamoDB table (PROVISIONED vs PAY_PER_REQUEST)"
}

variable "s3_input_bucket_name" {
  type        = string
  description = "Name of the S3 input bucket for images"
}

variable "s3_input_bucket_cors_allowed_origins" {
  default     = ["*"]
  type        = list(string)
  description = "S3 input bucket CORS allowed origins"
}

variable "s3_input_bucket_cors_allowed_methods" {
  default     = ["GET", "PUT", "POST", "HEAD", "DELETE"]
  type        = list(string)
  description = "S3 input bucket CORS allowed methods"
}

variable "s3_input_bucket_cors_max_age_seconds" {
  default     = 3000
  type        = number
  description = "S3 input bucket CORS max age in seconds"
}

variable "s3_input_bucket_cors_allowed_headers" {
  default     = ["*"]
  type        = list(string)
  description = "S3 input bucket CORS allowed headers"
}

variable "s3_input_bucket_force_destroy" {
  default     = true
  type        = bool
  description = "Whether or not to force destroy bucket"
}

variable "s3_output_bucket_name" {
  type        = string
  description = "Name of the S3 output bucket for images"
}

variable "s3_output_bucket_cors_allowed_origins" {
  default     = ["*"]
  type        = list(string)
  description = "S3 output bucket CORS allowed origins"
}

variable "s3_output_bucket_cors_allowed_methods" {
  default     = ["GET", "PUT", "POST", "HEAD", "DELETE"]
  type        = list(string)
  description = "S3 output bucket CORS allowed methods"
}

variable "s3_output_bucket_cors_max_age_seconds" {
  default     = 3000
  type        = number
  description = "S3 output bucket CORS max age in seconds"
}

variable "s3_output_bucket_cors_allowed_headers" {
  default     = ["*"]
  type        = list(string)
  description = "S3 output bucket CORS allowed headers"
}

variable "s3_output_bucket_force_destroy" {
  default     = true
  type        = bool
  description = "Whether or not to force destroy bucket"
}

variable "env" {
    type = string
    description = "Environment to deploy resources to"
}
