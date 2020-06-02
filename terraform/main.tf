provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

terraform {
  required_version = "~> 0.12"

  backend "s3" {
    encrypt = true
  }
}

resource "aws_dynamodb_table" "image_object_detection_table" {
  name         = var.dynamodb_table_name
  billing_mode = var.dynamodb_table_billing_mode
  hash_key     = "input_md5_checksum"

  attribute {
    name = "input_md5_checksum"
    type = "S"
  }
}

resource "aws_s3_bucket" "input_bucket" {
  bucket = var.s3_input_bucket_name

  cors_rule {
    allowed_origins = var.s3_input_bucket_cors_allowed_origins
    allowed_methods = var.s3_input_bucket_cors_allowed_methods
    max_age_seconds = var.s3_input_bucket_cors_max_age_seconds
    allowed_headers = var.s3_input_bucket_cors_allowed_headers
  }

  force_destroy = var.s3_input_bucket_force_destroy
}

resource "aws_s3_bucket" "output_bucket" {
  bucket = var.s3_output_bucket_name

  cors_rule {
    allowed_origins = var.s3_output_bucket_cors_allowed_origins
    allowed_methods = var.s3_output_bucket_cors_allowed_methods
    max_age_seconds = var.s3_output_bucket_cors_max_age_seconds
    allowed_headers = var.s3_output_bucket_cors_allowed_headers
  }

  force_destroy = var.s3_output_bucket_force_destroy
}

resource "local_file" "website_js" {
  filename = "../ui/script.js"
  content = format(
    file("../ui/base-script.js"),
    "${data.external.api_gw_url.result["api_gw_url"]}"
  )
}

data "external" "api_gw_url" {
  program = ["sh", "bin/get_api_gw_url.sh"]

  query = {
    env = var.env
  }

  depends_on = [
    null_resource.chalice
  ]
}

resource "aws_s3_bucket" "website" {
  bucket = var.website_bucket_name
  acl    = "public-read"

  tags = {
    Name        = "website"
    Environment = var.env
  }

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadForGetBucketObjects",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${var.website_bucket_name}/*"
    }
  ]
}
EOF

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  force_destroy = true

  provisioner "local-exec" {
    command = "aws s3 cp --recursive ../ui s3://${var.website_bucket_name}"
  }

  depends_on = [
    local_file.website_js
  ]
}

resource "local_file" "chalice_config" {
  filename = "../.chalice/config.json"
  content = format(
    file("../.chalice/base-config.json"),
    var.s3_input_bucket_name,
    var.s3_output_bucket_name,
    var.dynamodb_table_name,
    var.s3_input_bucket_name,
    var.s3_output_bucket_name,
    var.dynamodb_table_name
  )
}

resource "local_file" "chalice_iam_policy" {
  filename = "../.chalice/policy-${var.env}.json"
  content = format(
    file("../.chalice/base-policy.json"),
    var.s3_input_bucket_name,
    var.s3_input_bucket_name,
    var.s3_output_bucket_name,
    var.s3_output_bucket_name,
    var.dynamodb_table_name
  )
}

resource "null_resource" "chalice" {
  # Deploy via chalice
  provisioner "local-exec" {
    command = "rm -rf ../.chalice/deployed && chalice --project-dir .. deploy --stage ${var.env}"
    environment = {
      AWS_REGION = var.aws_region
    }
  }

  provisioner "local-exec" {
    when    = destroy
    command = "chalice --project-dir .. delete --stage ${var.env}"
    environment = {
      AWS_REGION = var.aws_region
    }
  }

  depends_on = [
    local_file.chalice_config,
    local_file.chalice_iam_policy
  ]
}
