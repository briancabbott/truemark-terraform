from truemark_terraform.model.resource import Resource
from truemark_terraform.model.provider import Provider

Provider("aws", "hashicorp/aws", "~> 3.27", profile="default", region="us-west-1")

Resource("aws_instance", "app_server", ami="ami-0577b787189839998", instance_type="t2.micro", 
    tags={'Name': "2ndDemo_Third_ExampleAppServerInstance"})

Resource("aws_instance", "app_server_third", ami="ami-0577b787189839998", instance_type="t2.micro", 
    tags={'Name': "2ndDemo_Fourth_ExampleAppServerInstance"})
