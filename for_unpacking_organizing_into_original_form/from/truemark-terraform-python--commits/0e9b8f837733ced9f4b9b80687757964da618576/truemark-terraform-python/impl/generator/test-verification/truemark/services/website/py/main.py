from truemark_terraform.model.resource import Resource
from truemark_terraform.model.provider import Provider
from truemark_terraform.model.data import Data
from truemark_terraform.model.module import Module
from truemark_terraform.model.terraform import Terraform

terraform=Terraform()
Provider("aws", "hashicorp/aws", "~> 3.0", region = "us-east-1")

data_aws_ci=Data("aws_caller_identity" "current")

locals = {
  'name': f"website-${terraform.workspace}",
  's3_bucket': f"{data_aws_ci.current.account_id}-{locals['name']}",
  'zone_name': "truemark.io" if terraform.workspace == "prod" else f"{terraform.workspace}.truemark.io"
}

mod_crt = Module("crt", "truemark/certificate-route53/aws", "1.0.1", 
    domain_names = [{'record_name': "www", 'zone_name': locals['zone_name']},
                    {'record_name': "", 'zone_name': locals['zone_name']}])

mod_s3 = Module("s3", "truemark/s3-iam/aws", "1.0.0", name = locals['s3_bucket'])

mod_web = Module("website", "truemark/website/aws", "1.0.0",
    s3_bucket = mod_s3.s3_bucket_name,
    name = locals['name'],
    domain_names = [{'record_name': "www", 'zone_name': locals['zone_name']},
                    {'record_name': "", 'zone_name': locals['zone_name']}],
    certificate_domain = mod_crt.certificate_domain,
    depends_on = [mod_s3, mod_crt])

Resource("aws_iam_user_policy_attachment" "spa", 
    user = mod_s3.iam_user_rw_name, 
    policy_arn = mod_web.iam_policy_arn)
