from truemark_terraform.model.resource import Resource
from truemark_terraform.model.provider import Provider
from truemark_terraform.model.module import Module
from truemark_terraform.model.terraform import Terraform

terraform=Terraform()
Provider("aws", "hashicorp/aws", "~> 3.0", region = "us-east-1")

locals = {}
locals['name'] = f"website-${terraform.workspace}"
locals['account_id'] = "123456"
locals['s3_bucket'] = f"{locals['account_id']}-{locals['name']}"
locals['zone_name'] = "truemark.io" if terraform.workspace == "prod" else f"{terraform.workspace}.truemark.io"

mod_crt = Module("crt", "truemark/certificate-route53/aws", "1.0.1", 
    domain_names = [{'record_name': "www", 'zone_name': locals['zone_name']},
                    {'record_name': "", 'zone_name': locals['zone_name']}])

mod_s3 = Module("s3", "truemark/s3-iam/aws", "1.0.0", name = locals['s3_bucket'])

mod_web = Module("website", "truemark/website/aws", "1.0.0",
    s3_bucket = locals['s3_bucket'],
    name = locals['name'],
    domain_names = [{'record_name': "www", 'zone_name': locals['zone_name']},
                    {'record_name': "", 'zone_name': locals['zone_name']}],
    certificate_domain = "cert-domain", 
    depends_on = [mod_s3, mod_crt])

Resource("aws_iam_user_policy_attachment", "spa", 
    user = "myValue", 
    policy_arn = "iam_policy_arn")
