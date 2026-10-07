terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

variable "username" {
  type    = string
  default = "demo4-labskraft-com"
}

variable "exam_code" {
  type    = string
  default = "1123"
}

# 1. S3 Bucket for Centralized Terraform State
resource "aws_s3_bucket" "terraform_state" {
  bucket        = "${var.username}-${var.exam_code}"
  force_destroy = true

  tags = {
    Name = "${var.username}-${var.exam_code}"
  }
}

# 2. S3 Bucket Versioning Enabled
resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

# 3. S3 Bucket Server-Side Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_encryption" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 4. DynamoDB Table for State Locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "${var.username}-${var.exam_code}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "${var.username}-${var.exam_code}"
  }
}
