from truemark_terraform.model.resource import Resource
from truemark_terraform.model.provider import Provider
from truemark_terraform.model.data import Data
from truemark_terraform.model.module import Module
from truemark_terraform.model.terraform import Terraform

terraform=Terraform()

Provider("aws", "hashicorp/aws", "~> 3.0", region = "us-east-1")

data_awsci=Data("aws_caller_identity" "current")

locals = {
  'name': f"alerts-api-${terraform.workspace}",
  'provisioner_name': f"${locals['name']}-provisioner",
  'sam_s3_bucket': f"${data_awsci.current.account_id}-${locals['name']}-sam",
  'zone_name': "truemark.io" if terraform.workspace == "prod" else f"${terraform.workspace}.truemark.io"
}

Module("crt", "truemark/certificate-route53/aws", "1.0.1", 
    domain_names = {
        'record_name': "alerts",
        'zone_name': locals['zone_name']
    })

mod_s3=Module("s3", "truemark/s3-iam/aws", "1.0.4", 
    name = locals['sam_s3_bucket'], 
    create_ro_user = False, 
    create_rw_user = False)

data_awsiam = Data("aws_iam_user", "sam", user_name="sam-provisioner")

Resource("aws_iam_user_policy_attachment", "s3", policy_arn = mod_s3.iam_policy_rw_arn, user = data_awsiam.sam.user_name)