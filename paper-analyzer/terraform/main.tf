# Terraform Configuration for AWS Bedrock Setup
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS Region for Bedrock"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for tagging"
  type        = string
  default     = "paper-analyzer"
}

# Data source to get current AWS account
data "aws_caller_identity" "current" {}

# IAM Role for Bedrock access
resource "aws_iam_role" "bedrock_role" {
  name = "${var.project_name}-bedrock-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name    = "${var.project_name}-bedrock-role"
    Project = var.project_name
  }
}

# IAM Policy for Bedrock model access
resource "aws_iam_policy" "bedrock_policy" {
  name        = "${var.project_name}-bedrock-policy"
  description = "Policy for Bedrock model invocation"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:ListFoundationModels",
          "bedrock:GetFoundationModel"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Name    = "${var.project_name}-bedrock-policy"
    Project = var.project_name
  }
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "bedrock_policy_attachment" {
  role       = aws_iam_role.bedrock_role.name
  policy_arn = aws_iam_policy.bedrock_policy.arn
}

# IAM User for programmatic access
resource "aws_iam_user" "bedrock_user" {
  name = "${var.project_name}-bedrock-user"

  tags = {
    Name    = "${var.project_name}-bedrock-user"
    Project = var.project_name
  }
}

# Attach Bedrock policy to user
resource "aws_iam_user_policy_attachment" "bedrock_user_policy" {
  user       = aws_iam_user.bedrock_user.name
  policy_arn = aws_iam_policy.bedrock_policy.arn
}

# Create access key for the user
resource "aws_iam_access_key" "bedrock_user_key" {
  user = aws_iam_user.bedrock_user.name
}

# Outputs
output "aws_account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "bedrock_user_name" {
  description = "IAM User name for Bedrock access"
  value       = aws_iam_user.bedrock_user.name
}

output "bedrock_access_key_id" {
  description = "Access Key ID (save this to .env)"
  value       = aws_iam_access_key.bedrock_user_key.id
  sensitive   = false
}

output "bedrock_secret_access_key" {
  description = "Secret Access Key (save this to .env)"
  value       = aws_iam_access_key.bedrock_user_key.secret
  sensitive   = true
}

output "bedrock_role_arn" {
  description = "Bedrock IAM Role ARN"
  value       = aws_iam_role.bedrock_role.arn
}

output "instructions" {
  description = "Next steps"
  value = <<-EOT
  
  ✅ Terraform applied successfully!
  
  Next steps:
  1. Copy the credentials to backend/.env:
     AWS_ACCESS_KEY_ID=${aws_iam_access_key.bedrock_user_key.id}
     AWS_SECRET_ACCESS_KEY=<run: terraform output -raw bedrock_secret_access_key>
  
  2. Enable Bedrock in AWS Console:
     - Go to: https://console.aws.amazon.com/bedrock
     - Click "Model Access" in left sidebar
     - Request access to DeepSeek models
     - Wait for approval (usually instant)
  
  3. Restart the backend server
  
  EOT
}
