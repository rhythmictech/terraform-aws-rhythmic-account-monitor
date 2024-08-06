terraform {
  required_version = ">= 1.5"

  required_providers {
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.5.0"
    }

    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.40"
    }

    datadog = {
      source  = "datadog/datadog"
      version = ">= 3.42"
    }
  }
}

provider "aws" {
}

module "example" {
  source = "../.."

  name_prefix                = "test"
  datadog_api_key_secret_arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:datadog-api-key"
}

output "example" {
  value = module.example
}
