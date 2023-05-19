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
  name = "website-${terraform.workspace}"
  s3_bucket = "${data.aws_caller_identity.current.account_id}-${local.name}"
  zone_name = terraform.workspace == "prod" ? "truemark.io" : "${terraform.workspace}.truemark.io"
}

module "crt" {
  source = "truemark/certificate-route53/aws"
  version = "1.0.1"
  domain_names = [
    {
      record_name = "www"
      zone_name = local.zone_name
    },
    {
      record_name = ""
      zone_name = local.zone_name
    }
  ]
}

module "s3" {
  source = "truemark/s3-iam/aws"
  version = "1.0.0"
  name = local.s3_bucket
}

module "website" {
  source = "truemark/website/aws"
  version = "1.0.0"
  s3_bucket = module.s3.s3_bucket_name
  name = local.name
  domain_names = [
    {
      record_name = "www"
      zone_name = local.zone_name
    },
    {
      record_name = ""
      zone_name = local.zone_name
    }
  ]
  certificate_domain = module.crt.certificate_domain
  depends_on = [module.s3, module.crt]
}

# Allow the rw user to perform invalidations
resource "aws_iam_user_policy_attachment" "spa" {
  user = module.s3.iam_user_rw_name
  policy_arn = module.website.iam_policy_arn
}