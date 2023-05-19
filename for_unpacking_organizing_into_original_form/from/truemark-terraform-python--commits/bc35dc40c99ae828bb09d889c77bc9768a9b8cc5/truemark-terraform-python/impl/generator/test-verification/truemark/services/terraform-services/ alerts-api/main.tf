terraform {
  backend "s3" {}
  required_providers {
    aws = {
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region      = "us-east-1"
}


data "aws_caller_identity" "current" {}

locals {
  name = "alerts-api-${terraform.workspace}"
  provisioner_name = "${local.name}-provisioner"
  sam_s3_bucket = "${data.aws_caller_identity.current.account_id}-${local.name}-sam"
  zone_name = terraform.workspace == "prod" ? "truemark.io" : "${terraform.workspace}.truemark.io"
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
  user_name = "sam-provisioner"
}

resource "aws_iam_user_policy_attachment" "s3" {
  policy_arn = module.s3.iam_policy_rw_arn
  user = data.aws_iam_user.sam.user_name
}
