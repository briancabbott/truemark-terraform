terraform {
  backend "s3" {}
  required_providers {
    aws = {
      version = "~> 3.0"
    }
    google = {
      source = "hashicorp/google"
      version = "3.66.1"
    }
  }
}

provider "aws" {
  region      = "us-east-1"
}

data "aws_caller_identity" "current" {}

locals {
  name = "alerts-api-dev"
  provisioner_name = "alerts-api-dev-provisioner"
  sam_s3_bucket = "briancabbott-terraform-in-python-bucket"
  zone_name = "brianabbott.io" # terraform.workspace == "prod" ? "truemark.io" : "${terraform.workspace}.truemark.io"
}

module "crt" {
  source = "truemark/certificate-route53/aws"
  version = "1.0.1"
  domain_names = [
    {
      record_name = "alerts"
      zone_name = local.zone_name
    }
  ]
}

module "s3" {
  source = "truemark/s3-iam/aws"
  version = "1.0.4"
  name = local.sam_s3_bucket
  create_ro_user = false
  create_rw_user = false
}

data "aws_iam_user" "sam" {
  user_name = "briancabbott"
}

resource "aws_iam_user_policy_attachment" "s3" {
  policy_arn = module.s3.iam_policy_rw_arn
  user = data.aws_iam_user.sam.user_name
}
